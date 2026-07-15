import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from bot.utils.database import get_all_subscribers, get_random_quran_verse, get_random_hadith

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def send_daily_reminders(bot):
    logger.info("Starting daily reminders job...")
    try:
        subscribers = get_all_subscribers()
        if not subscribers:
            logger.info("No subscribers to send daily reminders to.")
            return

        verse = get_random_quran_verse()
        hadith = get_random_hadith()

        from bot.commands.quran import format_quran_message
        from bot.commands.hadith import format_hadith_message

        message_parts = ["🌅 *Daily Islamic Reminder* 🌅\n"]
        if verse:
            message_parts.append(format_quran_message(verse))
            message_parts.append("\n" + "─" * 20 + "\n")
        if hadith:
            message_parts.append(format_hadith_message(hadith))
        
        full_message = "\n".join(message_parts)

        success_count = 0
        for user_id in subscribers:
            try:
                await bot.send_message(
                    chat_id=user_id,
                    text=full_message,
                    parse_mode="Markdown"
                )
                success_count += 1
            except Exception as e:
                logger.error(f"Failed to send daily reminder to {user_id}: {e}")

        logger.info(f"Daily reminders sent successfully to {success_count}/{len(subscribers)} subscribers.")
    except Exception as e:
        logger.error(f"Error executing send_daily_reminders: {e}")


def start_scheduler(bot=None):
    if not scheduler.running:
        scheduler.start()
        logger.info("APScheduler started.")
        
        # Schedule daily reminders at 9:00 AM every day
        if bot:
            scheduler.add_job(
                send_daily_reminders,
                trigger=CronTrigger(hour=9, minute=0),
                id="daily_reminders",
                replace_existing=True,
                kwargs={"bot": bot},
            )
            logger.info("Scheduled daily reminders job at 09:00 AM.")


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        logger.info("APScheduler stopped.")


def add_daily_job(func, hour: int, minute: int, job_id: str, **kwargs):
    scheduler.add_job(
        func,
        trigger=CronTrigger(hour=hour, minute=minute),
        id=job_id,
        replace_existing=True,
        kwargs=kwargs,
    )
    logger.info(f"Scheduled daily job '{job_id}' at {hour:02d}:{minute:02d}.")

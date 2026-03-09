import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


def start_scheduler():
    if not scheduler.running:
        scheduler.start()
        logger.info("APScheduler started.")


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

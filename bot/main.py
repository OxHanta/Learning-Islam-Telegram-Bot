import logging
import sys
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from bot.config import TELEGRAM_BOT_TOKEN
from bot.utils.database import init_db
from bot.utils.scheduler import start_scheduler, stop_scheduler
from bot.commands.start import start_command, help_command
from bot.commands.islamic_history import islamic_history_command, islamic_history_callback
from bot.commands.prayer_times import prayer_times_command, prayer_times_callback, city_selection_callback
from bot.commands.hadith import hadith_command, hadith_callback
from bot.commands.quran import quran_command, quran_callback
from bot.commands.random_fact import random_fact_callback, handle_message

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


async def error_handler(update: object, context):
    logger.error(f"Exception while handling an update: {context.error}", exc_info=context.error)
    if isinstance(update, Update) and update.effective_message:
        from bot.keyboards.inline_keyboard import retry_keyboard
        try:
            await update.effective_message.reply_text(
                "❌ Sorry, an error occurred. Please try again.",
                reply_markup=retry_keyboard(),
            )
        except Exception:
            pass


def main():
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN environment variable is not set!")
        sys.exit(1)

    init_db()
    logger.info("Database initialized.")

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("islamic_history", islamic_history_command))
    app.add_handler(CommandHandler("prayer_times", prayer_times_command))
    app.add_handler(CommandHandler("hadith", hadith_command))
    app.add_handler(CommandHandler("quran", quran_command))

    app.add_handler(CallbackQueryHandler(islamic_history_callback, pattern="^islamic_history$"))
    app.add_handler(CallbackQueryHandler(prayer_times_callback, pattern="^prayer_times$"))
    app.add_handler(CallbackQueryHandler(hadith_callback, pattern="^hadith$"))
    app.add_handler(CallbackQueryHandler(quran_callback, pattern="^quran$"))
    app.add_handler(CallbackQueryHandler(random_fact_callback, pattern="^random_fact$"))
    app.add_handler(CallbackQueryHandler(city_selection_callback, pattern="^city_"))
    app.add_handler(CallbackQueryHandler(start_command, pattern="^main_menu$"))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.add_error_handler(error_handler)

    start_scheduler()
    logger.info("Islamic Learning Bot started. Polling for updates...")

    app.run_polling(allowed_updates=Update.ALL_TYPES)

    stop_scheduler()


if __name__ == "__main__":
    main()

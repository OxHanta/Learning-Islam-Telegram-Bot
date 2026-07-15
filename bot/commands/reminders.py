import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.utils.database import add_subscriber, remove_subscriber, is_subscribed
from bot.keyboards.inline_keyboard import retry_keyboard

logger = logging.getLogger(__name__)


def reminders_keyboard(subscribed: bool) -> InlineKeyboardMarkup:
    if subscribed:
        button = InlineKeyboardButton("🔕 Unsubscribe", callback_data="reminders_unsub")
    else:
        button = InlineKeyboardButton("🔔 Subscribe", callback_data="reminders_sub")
    
    keyboard = [
        [button],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)


async def subscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        add_subscriber(user_id)
        await update.message.reply_text(
            "🔔 *Subscribed to Daily Reminders!*\n\n"
            "You will now receive a beautiful daily Quran verse and Hadith every morning. "
            "May Allah make it a source of guidance and barakah for you! 🤲",
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Error in subscribe_command: {e}")
        await update.message.reply_text("❌ Sorry, an error occurred while subscribing. Please try again.")


async def unsubscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        remove_subscriber(user_id)
        await update.message.reply_text(
            "🔕 *Unsubscribed from Daily Reminders.*\n\n"
            "You have been unsubscribed. You can subscribe again at any time using /subscribe or the main menu.",
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Error in unsubscribe_command: {e}")
        await update.message.reply_text("❌ Sorry, an error occurred while unsubscribing. Please try again.")


async def reminders_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        subbed = is_subscribed(user_id)
        if subbed:
            text = (
                "🔔 *Daily Reminders Status*\n\n"
                "You are currently *subscribed* to daily reminders!\n\n"
                "Every morning, you will receive an inspiring Quran verse and a selected Hadith with interpretation "
                "to start your day with knowledge.\n\n"
                "Would you like to turn off reminders?"
            )
        else:
            text = (
                "🔕 *Daily Reminders Status*\n\n"
                "You are currently *not subscribed* to daily reminders.\n\n"
                "Subscribe to receive a handpicked Quran verse and authenticated Hadith every morning (at 9:00 AM) "
                "directly in this chat. It's a wonderful way to learn consistently!\n\n"
                "Would you like to subscribe?"
            )
        
        await update.message.reply_text(
            text,
            parse_mode="Markdown",
            reply_markup=reminders_keyboard(subbed)
        )
    except Exception as e:
        logger.error(f"Error in reminders_command: {e}")
        await update.message.reply_text("❌ Sorry, an error occurred while checking reminders status.")


async def reminders_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    try:
        subbed = is_subscribed(user_id)
        if subbed:
            text = (
                "🔔 *Daily Reminders Status*\n\n"
                "You are currently *subscribed* to daily reminders!\n\n"
                "Every morning, you will receive an inspiring Quran verse and a selected Hadith with interpretation "
                "to start your day with knowledge.\n\n"
                "Would you like to turn off reminders?"
            )
        else:
            text = (
                "🔕 *Daily Reminders Status*\n\n"
                "You are currently *not subscribed* to daily reminders.\n\n"
                "Subscribe to receive a handpicked Quran verse and authenticated Hadith every morning (at 9:00 AM) "
                "directly in this chat. It's a wonderful way to learn consistently!\n\n"
                "Would you like to subscribe?"
            )
        
        await query.message.edit_text(
            text,
            parse_mode="Markdown",
            reply_markup=reminders_keyboard(subbed)
        )
    except Exception as e:
        logger.error(f"Error in reminders_menu_callback: {e}")
        await query.message.reply_text("❌ Sorry, an error occurred. Please try again.", reply_markup=retry_keyboard())


async def reminders_subscribe_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    try:
        add_subscriber(user_id)
        text = (
            "🔔 *Daily Reminders Status*\n\n"
            "✨ *Successfully Subscribed!*\n\n"
            "You are now subscribed to daily reminders! You will receive a Quran verse and Hadith every morning "
            "at 9:00 AM. May Allah bless your journey of seeking knowledge. Ameen 🤲"
        )
        await query.message.edit_text(
            text,
            parse_mode="Markdown",
            reply_markup=reminders_keyboard(subscribed=True)
        )
    except Exception as e:
        logger.error(f"Error in reminders_subscribe_callback: {e}")
        await query.message.reply_text("❌ Sorry, an error occurred.", reply_markup=retry_keyboard())


async def reminders_unsubscribe_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    try:
        remove_subscriber(user_id)
        text = (
            "🔕 *Daily Reminders Status*\n\n"
            "✨ *Successfully Unsubscribed*\n\n"
            "You have been unsubscribed from daily reminders. You can re-subscribe at any time."
        )
        await query.message.edit_text(
            text,
            parse_mode="Markdown",
            reply_markup=reminders_keyboard(subscribed=False)
        )
    except Exception as e:
        logger.error(f"Error in reminders_unsubscribe_callback: {e}")
        await query.message.reply_text("❌ Sorry, an error occurred.", reply_markup=retry_keyboard())

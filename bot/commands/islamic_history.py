from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.database import get_random_history
from bot.keyboards.inline_keyboard import make_action_keyboard


def format_history_message(history: dict) -> str:
    category_icons = {
        "events": "⚡",
        "battles": "⚔️",
        "personalities": "👤",
        "civilization": "🏛️",
        "scholars": "📚",
        "expansion": "🌍",
        "general": "📜",
    }
    icon = category_icons.get(history.get("category", "general"), "📜")

    return (
        f"{icon} *Islamic History*\n\n"
        f"*{history['title']}*\n\n"
        f"{history['content']}\n\n"
        f"_Category: {history.get('category', 'General').title()}_"
    )


async def islamic_history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _send_history(update, context, is_callback=False)


async def islamic_history_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _send_history(update, context, is_callback=True)


async def _send_history(update: Update, context: ContextTypes.DEFAULT_TYPE, is_callback: bool):
    loading_msg = None
    try:
        if is_callback:
            query = update.callback_query
            await query.answer()
            loading_msg = await query.message.reply_text("⏳ Loading Islamic history...")
        else:
            loading_msg = await update.message.reply_text("⏳ Loading Islamic history...")

        history = get_random_history()
        if not history:
            text = "❌ No history records found. Please try again later."
            keyboard = make_action_keyboard("islamic_history")
        else:
            text = format_history_message(history)
            keyboard = make_action_keyboard("islamic_history")

        await loading_msg.edit_text(
            text,
            parse_mode="Markdown",
            reply_markup=keyboard,
        )
    except Exception:
        if loading_msg:
            from bot.keyboards.inline_keyboard import retry_keyboard
            await loading_msg.edit_text(
                "❌ Sorry, an error occurred while fetching Islamic history. Please try again.",
                reply_markup=retry_keyboard(),
            )

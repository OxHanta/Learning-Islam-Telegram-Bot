from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.database import get_random_fact
from bot.keyboards.inline_keyboard import make_action_keyboard, retry_keyboard


async def random_fact_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    loading_msg = await query.message.reply_text("⏳ Loading Islamic fact...")
    try:
        fact = get_random_fact()
        await loading_msg.edit_text(
            f"💡 *Did You Know?*\n\n{fact}",
            parse_mode="Markdown",
            reply_markup=make_action_keyboard("random_fact"),
        )
    except Exception:
        await loading_msg.edit_text(
            "❌ Sorry, an error occurred. Please try again.",
            reply_markup=retry_keyboard(),
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        fact = get_random_fact()
        from bot.keyboards.inline_keyboard import main_menu_keyboard
        await update.message.reply_text(
            f"💡 *Did You Know?*\n\n{fact}\n\n_Send another message for a new fact, or explore the menu below!_",
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard(),
        )
    except Exception:
        await update.message.reply_text(
            "❌ Sorry, an error occurred. Please try again.",
            reply_markup=retry_keyboard(),
        )

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.database import get_random_hadith
from bot.keyboards.inline_keyboard import make_action_keyboard, retry_keyboard


def format_hadith_message(hadith: dict) -> str:
    return (
        f"📖 *Hadith*\n\n"
        f"_{hadith['text']}_\n\n"
        f"*Narrated by:* {hadith['narrator']}\n"
        f"*Collection:* {hadith['collection']}\n\n"
        f"💡 *Interpretation:*\n{hadith['interpretation']}"
    )


async def hadith_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _send_hadith(update, context, is_callback=False)


async def hadith_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _send_hadith(update, context, is_callback=True)


async def _send_hadith(update: Update, context: ContextTypes.DEFAULT_TYPE, is_callback: bool):
    loading_msg = None
    try:
        if is_callback:
            query = update.callback_query
            await query.answer()
            loading_msg = await query.message.reply_text("⏳ Loading Hadith...")
        else:
            loading_msg = await update.message.reply_text("⏳ Loading Hadith...")

        hadith = get_random_hadith()
        if not hadith:
            text = "❌ No hadith found. Please try again later."
            keyboard = make_action_keyboard("hadith")
        else:
            text = format_hadith_message(hadith)
            keyboard = make_action_keyboard("hadith")

        await loading_msg.edit_text(
            text,
            parse_mode="Markdown",
            reply_markup=keyboard,
        )
    except Exception:
        if loading_msg:
            await loading_msg.edit_text(
                "❌ Sorry, an error occurred while fetching the Hadith. Please try again.",
                reply_markup=retry_keyboard(),
            )

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.database import get_random_quran_verse
from bot.keyboards.inline_keyboard import make_action_keyboard, retry_keyboard


def format_quran_message(verse: dict) -> str:
    return (
        f"🌙 *Quran Verse*\n\n"
        f"*Surah {verse['surah_name']}* ({verse['surah_number']}:{verse['ayah_number']})\n\n"
        f"*Arabic:*\n{verse['arabic']}\n\n"
        f"*Translation:*\n_{verse['translation']}_\n\n"
        f"💡 *Explanation:*\n{verse['explanation']}"
    )


async def quran_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _send_verse(update, context, is_callback=False)


async def quran_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _send_verse(update, context, is_callback=True)


async def _send_verse(update: Update, context: ContextTypes.DEFAULT_TYPE, is_callback: bool):
    loading_msg = None
    try:
        if is_callback:
            query = update.callback_query
            await query.answer()
            loading_msg = await query.message.reply_text("⏳ Loading Quran verse...")
        else:
            loading_msg = await update.message.reply_text("⏳ Loading Quran verse...")

        verse = get_random_quran_verse()
        if not verse:
            text = "❌ No Quran verses found. Please try again later."
            keyboard = make_action_keyboard("quran")
        else:
            text = format_quran_message(verse)
            keyboard = make_action_keyboard("quran")

        await loading_msg.edit_text(
            text,
            parse_mode="Markdown",
            reply_markup=keyboard,
        )
    except Exception:
        if loading_msg:
            await loading_msg.edit_text(
                "❌ Sorry, an error occurred while fetching the Quran verse. Please try again.",
                reply_markup=retry_keyboard(),
            )

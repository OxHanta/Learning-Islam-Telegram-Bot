import asyncio
import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.ai import ask_ai, clear_history
from bot.keyboards.inline_keyboard import main_menu_keyboard, retry_keyboard

logger = logging.getLogger(__name__)

THINKING_MESSAGES = [
    "🤔 Thinking...",
    "📚 Searching for an answer...",
    "✨ Preparing a response...",
]


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text.strip()

    thinking_msg = await update.message.reply_text("🤔 Thinking...")

    try:
        loop = asyncio.get_event_loop()
        reply = await loop.run_in_executor(None, ask_ai, user_id, user_text)

        if len(reply) > 4000:
            parts = [reply[i:i+4000] for i in range(0, len(reply), 4000)]
            await thinking_msg.edit_text(parts[0])
            for part in parts[1:]:
                await update.message.reply_text(part)
            await update.message.reply_text(
                "Use the menu for more topics or keep asking me anything about Islam!",
                reply_markup=main_menu_keyboard(),
            )
        else:
            await thinking_msg.edit_text(
                reply + "\n\n_Ask me another question or use the menu below._",
                reply_markup=main_menu_keyboard(),
            )

    except Exception as e:
        logger.error(f"AI error for user {user_id}: {e}")
        error_msg = str(e)
        if "FREE_CLOUD_BUDGET_EXCEEDED" in error_msg:
            await thinking_msg.edit_text(
                "Your cloud AI budget has been exceeded. Please check your Replit account.",
                reply_markup=retry_keyboard(),
            )
        else:
            await thinking_msg.edit_text(
                "Sorry, I had trouble answering that. Please try again or rephrase your question.",
                reply_markup=retry_keyboard(),
            )


async def random_fact_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    thinking_msg = await query.message.reply_text("🤔 Thinking of an interesting Islamic fact...")

    try:
        loop = asyncio.get_event_loop()
        reply = await loop.run_in_executor(
            None, ask_ai, user_id,
            "Share one interesting and educational Islamic fact or piece of trivia with me. Make it informative and engaging."
        )
        await thinking_msg.edit_text(
            reply + "\n\n_Ask me anything about Islam or use the menu below._",
            reply_markup=main_menu_keyboard(),
        )
    except Exception as e:
        logger.error(f"AI fact error for user {user_id}: {e}")
        await thinking_msg.edit_text(
            "Sorry, I had trouble fetching a fact right now. Please try again.",
            reply_markup=retry_keyboard(),
        )


async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    clear_history(user_id)
    await update.message.reply_text(
        "Your conversation history has been cleared. Feel free to start a fresh conversation!\n\nAsk me anything about Islam.",
        reply_markup=main_menu_keyboard(),
    )

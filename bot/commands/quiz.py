import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.utils.database import get_random_quiz, get_quiz_by_id
from bot.keyboards.inline_keyboard import retry_keyboard

logger = logging.getLogger(__name__)


def format_quiz_message(quiz: dict) -> str:
    return (
        f"🧠 *Islamic Quiz*\n\n"
        f"*Question:*\n{quiz['question']}\n\n"
        f"🇦 {quiz['option_a']}\n"
        f"🇧 {quiz['option_b']}\n"
        f"🇨 {quiz['option_c']}\n"
        f"🇩 {quiz['option_d']}\n\n"
        f"_Select an option below to test your knowledge!_"
    )


def quiz_keyboard(quiz: dict) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("🇦", callback_data=f"quiz_opt_{quiz['id']}_A"),
            InlineKeyboardButton("🇧", callback_data=f"quiz_opt_{quiz['id']}_B"),
        ],
        [
            InlineKeyboardButton("🇨", callback_data=f"quiz_opt_{quiz['id']}_C"),
            InlineKeyboardButton("🇩", callback_data=f"quiz_opt_{quiz['id']}_D"),
        ],
        [
            InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def quiz_next_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("🔄 Next Question", callback_data="quiz_next"),
            InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


async def quiz_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        quiz = get_random_quiz()
        if not quiz:
            await update.message.reply_text("❌ No quiz questions available right now.")
            return

        text = format_quiz_message(quiz)
        await update.message.reply_text(
            text,
            parse_mode="Markdown",
            reply_markup=quiz_keyboard(quiz)
        )
    except Exception as e:
        logger.error(f"Error in quiz_command: {e}")
        await update.message.reply_text(
            "❌ Sorry, an error occurred while starting the quiz.",
            reply_markup=retry_keyboard()
        )


async def quiz_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        quiz = get_random_quiz()
        if not quiz:
            await query.message.reply_text("❌ No quiz questions available right now.")
            return

        text = format_quiz_message(quiz)
        await query.message.edit_text(
            text,
            parse_mode="Markdown",
            reply_markup=quiz_keyboard(quiz)
        )
    except Exception as e:
        logger.error(f"Error in quiz_callback: {e}")
        await query.message.reply_text(
            "❌ Sorry, an error occurred while loading the quiz.",
            reply_markup=retry_keyboard()
        )


async def quiz_option_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Callback pattern: quiz_opt_{quiz_id}_{option}
    parts = query.data.split("_")
    quiz_id = int(parts[2])
    selected_option = parts[3]

    try:
        quiz = get_quiz_by_id(quiz_id)
        if not quiz:
            await query.message.edit_text("❌ Question not found.", reply_markup=retry_keyboard())
            return

        correct = quiz["correct_option"].strip().upper()
        is_correct = selected_option == correct

        # Get option text
        option_map = {
            "A": quiz["option_a"],
            "B": quiz["option_b"],
            "C": quiz["option_c"],
            "D": quiz["option_d"],
        }
        selected_text = option_map.get(selected_option, "")
        correct_text = option_map.get(correct, "")

        if is_correct:
            result_header = "✅ *Correct Answer! SubhanAllah!*\n\n"
            answer_details = f"You selected: *{selected_option}. {selected_text}*\n\n"
        else:
            result_header = "❌ *Incorrect Answer!*\n\n"
            answer_details = (
                f"You selected: *{selected_option}. {selected_text}*\n"
                f"Correct answer: *{correct}. {correct_text}*\n\n"
            )

        explanation_block = f"💡 *Explanation:*\n{quiz['explanation']}"
        full_text = (
            f"🧠 *Islamic Quiz Results*\n\n"
            f"*Question:*\n{quiz['question']}\n\n"
            f"{result_header}"
            f"{answer_details}"
            f"{explanation_block}"
        )

        await query.message.edit_text(
            full_text,
            parse_mode="Markdown",
            reply_markup=quiz_next_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in quiz_option_callback: {e}")
        await query.message.reply_text(
            "❌ Sorry, an error occurred while checking your answer.",
            reply_markup=retry_keyboard()
        )


async def quiz_next_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        quiz = get_random_quiz()
        if not quiz:
            await query.message.reply_text("❌ No more quiz questions available.")
            return

        text = format_quiz_message(quiz)
        await query.message.edit_text(
            text,
            parse_mode="Markdown",
            reply_markup=quiz_keyboard(quiz)
        )
    except Exception as e:
        logger.error(f"Error in quiz_next_callback: {e}")
        await query.message.reply_text(
            "❌ Sorry, an error occurred while loading the next question.",
            reply_markup=retry_keyboard()
        )

from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboards.inline_keyboard import main_menu_keyboard


WELCOME_MESSAGE = """🌙 As-salamu alaykum! Welcome to Islamic Learning Bot 🌙

I am your companion for Islamic knowledge and learning.

You can talk to me naturally — ask me any question about Islam and I will do my best to give you a thorough, accurate answer. Here are some things you can ask:

• "What are the Five Pillars of Islam?"
• "Tell me about the life of Prophet Ibrahim (AS)"
• "What does the Quran say about patience?"
• "How do I perform Wudu?"
• "Explain the concept of Tawakkul"

You can also use the menu buttons below or commands to explore specific topics:

📜 Islamic History — Key events, battles and personalities
🕌 Prayer Times — Accurate prayer times for major cities
📖 Hadith — Authenticated hadith with interpretations
🌙 Quran — Verses with Arabic, translation and explanation
🧠 Islamic Quiz — Interactive multiple-choice quizzes to test your knowledge!
❓ Random Fact — An interesting Islamic fact from the AI
🔔 Daily Reminders — Subscribe to get a daily verse and Hadith in the morning

🔍 Search the database at any time using `/search <keyword>`!
Type /reset at any time to start a fresh conversation.

May Allah bless your learning journey. Ameen 🤲"""


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(
            WELCOME_MESSAGE,
            reply_markup=main_menu_keyboard(),
        )
    else:
        await update.message.reply_text(
            WELCOME_MESSAGE,
            reply_markup=main_menu_keyboard(),
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """📚 Islamic Learning Bot — Help Guide

Available Commands:
/start — Show the main menu and welcome message
/help — Show this help guide
/search <keyword> — Search the database (Quran, Hadith, History) or ask AI if not found
/quiz — Start an interactive multiple-choice Islamic quiz
/reminders — View daily reminder subscription status
/subscribe — Subscribe to daily Quran & Hadith reminders
/unsubscribe — Unsubscribe from daily reminders
/islamic_history — Get a random Islamic history entry
/prayer_times — Get prayer times for a city
/hadith — Get a random authenticated Hadith
/quran — Get a random Quran verse with explanation
/reset — Clear your conversation history and start fresh

How to Chat:
Just type any question in plain text and I will answer it! I am an AI assistant specialised in Islamic knowledge. For example:
  • "What is the significance of Laylat al-Qadr?"
  • "Who was Umar ibn al-Khattab?"
  • "What are the conditions for Hajj?"

How to Use the Menu:
• Tap any button to explore topics
• Use "Show Another" to get fresh content
• Use "Main Menu" to return to the menu

Seeking knowledge is an obligation upon every Muslim.
— Prophet Muhammad (PBUH)"""

    await update.message.reply_text(
        help_text,
        reply_markup=main_menu_keyboard(),
    )

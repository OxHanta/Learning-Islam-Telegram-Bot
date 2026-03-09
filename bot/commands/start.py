from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboards.inline_keyboard import main_menu_keyboard


WELCOME_MESSAGE = """
🌙 *As-salamu alaykum! Welcome to Islamic Learning Bot* 🌙

I am your companion for Islamic knowledge and learning. Here is what I can help you with:

📜 *Islamic History* — Learn about significant events, battles, and personalities that shaped Islamic civilization.

🕌 *Prayer Times* — Get prayer times for major cities around the world.

📖 *Hadith* — Explore authentic hadith with interpretations to guide your daily life.

🌙 *Quran* — Reflect on Quran verses with translations and explanations.

❓ *Random Facts* — Discover interesting facts about Islam anytime you send a message.

_Choose a topic below to get started, or simply send me a message and I will share an Islamic fact with you!_

*May Allah bless your learning journey. Ameen.* 🤲
"""


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        WELCOME_MESSAGE,
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📚 *Islamic Learning Bot — Help Guide*

*Available Commands:*
/start — Show the main menu and welcome message
/help — Show this help guide
/islamic\_history — Get a random Islamic history fact
/prayer\_times — Get prayer times for a city
/hadith — Get a random authenticated Hadith
/quran — Get a random Quran verse with explanation

*How to Use:*
• Tap any button in the menu to explore topics
• Send any text message to receive a random Islamic fact
• Use the "Show Another" button to get more content
• Use the "Main Menu" button to return to the main menu

*About This Bot:*
This bot provides Islamic educational content including history, hadith, Quran verses, and prayer times. All content is carefully curated from authentic Islamic sources.

_Seeking knowledge is an obligation upon every Muslim._ — Prophet Muhammad (PBUH)
"""
    await update.message.reply_text(
        help_text,
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )

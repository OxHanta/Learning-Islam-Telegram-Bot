# Islamic Learning Telegram Bot

## Overview
A modular Islamic Learning Telegram Bot built with Python and python-telegram-bot 20.x. The bot provides Islamic educational content including history, hadith, Quran verses, and prayer times.

## Architecture

### File Structure
```
bot/
  __init__.py
  main.py              — Entry point, registers all handlers
  config.py            — Configuration and constants
  commands/
    __init__.py
    start.py           — /start and /help commands
    islamic_history.py — /islamic_history command & callback
    prayer_times.py    — /prayer_times command & callback + prayer calculation
    hadith.py          — /hadith command & callback
    quran.py           — /quran command & callback
    random_fact.py     — random_fact callback & message handler
  utils/
    __init__.py
    database.py        — SQLite database setup, seeding, and queries
    scheduler.py       — APScheduler wrapper for scheduled tasks
  keyboards/
    __init__.py
    inline_keyboard.py — All InlineKeyboardMarkup builders
requirements.txt
```

### Tech Stack
- **Python 3.10**
- **python-telegram-bot 20.7** — Async Telegram bot framework
- **SQLite3** — Embedded database for storing Islamic content
- **APScheduler 3.10.4** — Task scheduling
- **pytz** — Timezone handling for prayer times

### Data Storage
- SQLite database (`islamic_bot.db`) auto-created on first run
- Tables: `islamic_history`, `hadiths`, `quran_verses`, `user_locations`, `islamic_facts`
- All tables seeded with curated content on first run

### Commands
- `/start` — Welcome message with inline menu
- `/help` — Help guide with command list
- `/islamic_history` — Random Islamic history entry
- `/prayer_times` — Prayer times by city selection
- `/hadith` — Random authenticated hadith with interpretation
- `/quran` — Random Quran verse with explanation
- Any text message → Random Islamic fact

## Environment Variables
- `TELEGRAM_BOT_TOKEN` — Required. Telegram Bot API token from @BotFather

## Running the Bot
```bash
python -m bot.main
```

## Workflow
Configured as a console workflow: `python -m bot.main`

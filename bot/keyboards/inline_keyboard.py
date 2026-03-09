from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("📜 Islamic History", callback_data="islamic_history"),
            InlineKeyboardButton("🕌 Prayer Times", callback_data="prayer_times"),
        ],
        [
            InlineKeyboardButton("📖 Hadith", callback_data="hadith"),
            InlineKeyboardButton("🌙 Quran", callback_data="quran"),
        ],
        [
            InlineKeyboardButton("❓ Random Fact", callback_data="random_fact"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def city_selection_keyboard() -> InlineKeyboardMarkup:
    cities = [
        "Mecca", "Medina", "Cairo", "Istanbul",
        "Kuala Lumpur", "Jakarta", "Dubai", "Karachi",
        "Lagos", "London"
    ]
    keyboard = []
    for i in range(0, len(cities), 2):
        row = [InlineKeyboardButton(cities[i], callback_data=f"city_{cities[i]}")]
        if i + 1 < len(cities):
            row.append(InlineKeyboardButton(cities[i + 1], callback_data=f"city_{cities[i + 1]}"))
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)


def back_to_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🔄 Show Another", callback_data="{{action}}")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


def retry_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🔄 Try Again", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


def make_action_keyboard(action: str) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🔄 Show Another", callback_data=action)],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

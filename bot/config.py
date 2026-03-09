import os

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

BOT_NAME = "Islamic Learning Bot"
BOT_USERNAME = "@IslamicLearningBot"

DATABASE_PATH = "islamic_bot.db"

PRAYER_CITIES = {
    "Mecca": {"lat": 21.3891, "lon": 39.8579, "timezone": "Asia/Riyadh"},
    "Medina": {"lat": 24.5247, "lon": 39.5692, "timezone": "Asia/Riyadh"},
    "Cairo": {"lat": 30.0444, "lon": 31.2357, "timezone": "Africa/Cairo"},
    "Istanbul": {"lat": 41.0082, "lon": 28.9784, "timezone": "Europe/Istanbul"},
    "Kuala Lumpur": {"lat": 3.1390, "lon": 101.6869, "timezone": "Asia/Kuala_Lumpur"},
    "Jakarta": {"lat": -6.2088, "lon": 106.8456, "timezone": "Asia/Jakarta"},
    "Dubai": {"lat": 25.2048, "lon": 55.2708, "timezone": "Asia/Dubai"},
    "Karachi": {"lat": 24.8607, "lon": 67.0011, "timezone": "Asia/Karachi"},
    "Lagos": {"lat": 6.5244, "lon": 3.3792, "timezone": "Africa/Lagos"},
    "London": {"lat": 51.5074, "lon": -0.1278, "timezone": "Europe/London"},
}

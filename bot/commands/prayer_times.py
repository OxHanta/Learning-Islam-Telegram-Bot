import math
import datetime
import pytz
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.database import save_user_location, get_user_location
from bot.keyboards.inline_keyboard import city_selection_keyboard, make_action_keyboard, retry_keyboard
from bot.config import PRAYER_CITIES


def calculate_prayer_times(lat: float, lon: float, timezone_str: str) -> dict:
    tz = pytz.timezone(timezone_str)
    now_utc = datetime.datetime.now(pytz.utc)
    now_local = now_utc.astimezone(tz)
    date = now_local.date()

    year = date.year
    month = date.month
    day = date.day

    jd = _julian_date(year, month, day)
    d = jd - 2451545.0

    lat_r = math.radians(lat)
    lon_deg = lon

    ecl_long = math.radians(280.460 + 0.9856474 * d)
    mean_anom = math.radians(357.528 + 0.9856003 * d)
    ecl_long2 = ecl_long + math.radians(1.915) * math.sin(mean_anom) + math.radians(0.020) * math.sin(2 * mean_anom)

    obliq = math.radians(23.439 - 0.0000004 * d)
    sin_dec = math.sin(obliq) * math.sin(ecl_long2)
    dec = math.asin(sin_dec)

    RA = math.atan2(math.cos(obliq) * math.sin(ecl_long2), math.cos(ecl_long2))
    RA = math.degrees(RA) / 15

    EOT = (280.460 + 0.9856474 * d) / 15 - RA
    EOT = EOT % 24

    transit = 12 + (15 - lon_deg) / 15 - EOT

    def hour_angle(angle):
        cos_h = (math.sin(math.radians(angle)) - math.sin(lat_r) * math.sin(dec)) / (math.cos(lat_r) * math.cos(dec))
        cos_h = max(-1, min(1, cos_h))
        return math.degrees(math.acos(cos_h)) / 15

    fajr_ha = hour_angle(-18)
    sunrise_ha = hour_angle(-0.8333)
    asr_factor = 1 + math.tan(abs(lat_r - dec))
    asr_angle = math.degrees(math.atan(1 / asr_factor))
    asr_ha = hour_angle(-asr_angle)
    maghrib_ha = hour_angle(-0.8333)
    isha_ha = hour_angle(-17)

    fajr = transit - fajr_ha
    sunrise = transit - sunrise_ha
    dhuhr = transit
    asr = transit + asr_ha
    maghrib = transit + maghrib_ha
    isha = transit + isha_ha

    def to_time_str(hours):
        h = int(hours) % 24
        m = int((hours - int(hours)) * 60)
        dt = now_local.replace(hour=h, minute=m, second=0, microsecond=0)
        return dt.strftime("%I:%M %p")

    return {
        "Fajr": to_time_str(fajr),
        "Sunrise": to_time_str(sunrise),
        "Dhuhr": to_time_str(dhuhr),
        "Asr": to_time_str(asr),
        "Maghrib": to_time_str(maghrib),
        "Isha": to_time_str(isha),
        "date": now_local.strftime("%A, %d %B %Y"),
        "timezone": timezone_str,
    }


def _julian_date(year, month, day):
    if month <= 2:
        year -= 1
        month += 12
    A = int(year / 100)
    B = 2 - A + int(A / 4)
    return int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5


def format_prayer_times_message(city: str, times: dict) -> str:
    prayer_icons = {
        "Fajr": "🌄",
        "Sunrise": "☀️",
        "Dhuhr": "🕛",
        "Asr": "🌤️",
        "Maghrib": "🌅",
        "Isha": "🌙",
    }
    lines = [f"🕌 *Prayer Times — {city}*\n", f"📅 {times['date']}\n"]
    for prayer, icon in prayer_icons.items():
        lines.append(f"{icon} *{prayer}:* {times[prayer]}")
    lines.append(f"\n_Timezone: {times['timezone']}_")
    return "\n".join(lines)


async def prayer_times_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _ask_for_city(update, context, is_callback=False)


async def prayer_times_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _ask_for_city(update, context, is_callback=True)


async def _ask_for_city(update: Update, context: ContextTypes.DEFAULT_TYPE, is_callback: bool):
    try:
        if is_callback:
            query = update.callback_query
            await query.answer()
            user_id = query.from_user.id
            saved_city = get_user_location(user_id)
            if saved_city and saved_city in PRAYER_CITIES:
                await _show_prayer_times(query.message, saved_city)
                return
            await query.message.reply_text(
                "🕌 *Prayer Times*\n\nPlease select your city to get prayer times:",
                parse_mode="Markdown",
                reply_markup=city_selection_keyboard(),
            )
        else:
            user_id = update.effective_user.id
            saved_city = get_user_location(user_id)
            if saved_city and saved_city in PRAYER_CITIES:
                await _show_prayer_times(update.message, saved_city)
                return
            await update.message.reply_text(
                "🕌 *Prayer Times*\n\nPlease select your city to get prayer times:",
                parse_mode="Markdown",
                reply_markup=city_selection_keyboard(),
            )
    except Exception:
        msg = update.message if not is_callback else update.callback_query.message
        await msg.reply_text(
            "❌ Sorry, an error occurred. Please try again.",
            reply_markup=retry_keyboard(),
        )


async def city_selection_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    city = query.data.replace("city_", "")
    user_id = query.from_user.id

    if city not in PRAYER_CITIES:
        await query.message.reply_text("❌ Unknown city. Please select a valid city.")
        return

    save_user_location(user_id, city)
    loading_msg = await query.message.reply_text(f"⏳ Getting prayer times for {city}...")
    await _show_prayer_times(loading_msg, city, edit=True)


async def _show_prayer_times(message, city: str, edit: bool = False):
    try:
        city_data = PRAYER_CITIES[city]
        times = calculate_prayer_times(city_data["lat"], city_data["lon"], city_data["timezone"])
        text = format_prayer_times_message(city, times)
        keyboard = make_action_keyboard("prayer_times")

        if edit:
            await message.edit_text(text, parse_mode="Markdown", reply_markup=keyboard)
        else:
            await message.reply_text(text, parse_mode="Markdown", reply_markup=keyboard)
    except Exception:
        await message.reply_text(
            "❌ Sorry, an error occurred while fetching prayer times. Please try again.",
            reply_markup=retry_keyboard(),
        )

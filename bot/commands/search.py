import logging
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.database import search_database
from bot.utils.ai import ask_ai
from bot.keyboards.inline_keyboard import main_menu_keyboard, retry_keyboard

logger = logging.getLogger(__name__)


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Check if a search term was provided
    if not context.args:
        usage_text = (
            "🔍 *Islamic Knowledge Search*\n\n"
            "Use this command to search our authentic database for any keyword!\n\n"
            "*Usage:*\n"
            "`/search <keyword>`\n\n"
            "*Examples:*\n"
            "• `/search patience`\n"
            "• `/search charity`\n"
            "• `/search Badr`\n"
            "• `/search prayer`\n\n"
            "If no matches are found locally, I will search using my AI Islamic Learning Assistant! ✨"
        )
        await update.message.reply_text(usage_text, parse_mode="Markdown")
        return

    keyword = " ".join(context.args).strip()
    loading_msg = await update.message.reply_text(f"🔍 Searching database for *'{keyword}'*...", parse_mode="Markdown")

    try:
        # Perform local database search
        results = search_database(keyword)
        q_matches = results.get("quran", [])
        h_matches = results.get("hadith", [])
        hist_matches = results.get("history", [])

        has_results = len(q_matches) > 0 or len(h_matches) > 0 or len(hist_matches) > 0

        if has_results:
            response_parts = [f"🔍 *Search Results for '{keyword}'*\n"]

            if q_matches:
                response_parts.append("🌙 *Quran Verses:*")
                for q in q_matches:
                    response_parts.append(
                        f"• *Surah {q['surah_name']}* ({q['surah_number']}:{q['ayah_number']})\n"
                        f"  _Arabic:_ {q['arabic']}\n"
                        f"  _Translation:_ {q['translation']}\n"
                    )
                response_parts.append("")

            if h_matches:
                response_parts.append("📖 *Hadiths:*")
                for h in h_matches:
                    # Clip long text if needed
                    text_snippet = h['text'] if len(h['text']) < 300 else h['text'][:297] + "..."
                    response_parts.append(
                        f"• *{h['collection']}* (Narrated by {h['narrator']})\n"
                        f"  _{text_snippet}_\n"
                    )
                response_parts.append("")

            if hist_matches:
                response_parts.append("📜 *Islamic History:*")
                for hist in hist_matches:
                    content_snippet = hist['content'] if len(hist['content']) < 200 else hist['content'][:197] + "..."
                    response_parts.append(
                        f"• *{hist['title']}* (Category: {hist['category'].title()})\n"
                        f"  {content_snippet}\n"
                    )
                response_parts.append("")

            response_parts.append("_Type /search <another keyword> or use the menu below._")
            full_response = "\n".join(response_parts)
            
            # Send results
            if len(full_response) > 4000:
                parts = [full_response[i:i+4000] for i in range(0, len(full_response), 4000)]
                await loading_msg.edit_text(parts[0], parse_mode="Markdown")
                for part in parts[1:]:
                    await update.message.reply_text(part, parse_mode="Markdown")
                await update.message.reply_text("Use the menu below to explore other topics:", reply_markup=main_menu_keyboard())
            else:
                await loading_msg.edit_text(full_response, parse_mode="Markdown", reply_markup=main_menu_keyboard())

        else:
            # Fallback to AI!
            await loading_msg.edit_text(
                f"🔍 No exact matches found in our local database for *'{keyword}'*.\n\n"
                f"⏳ Consulting our AI Islamic Learning Assistant for a comprehensive response...",
                parse_mode="Markdown"
            )
            
            loop = asyncio.get_event_loop()
            ai_query = f"Provide a comprehensive overview on the topic: '{keyword}' in Islam, quoting relevant Quran verses or Hadiths if applicable."
            reply = await loop.run_in_executor(None, ask_ai, user_id, ai_query)
            
            full_reply = (
                f"✨ *AI Scholar Response for '{keyword}':*\n\n"
                f"{reply}\n\n"
                f"_Ask me another question or use the menu below._"
            )
            
            if len(full_reply) > 4000:
                parts = [full_reply[i:i+4000] for i in range(0, len(full_reply), 4000)]
                await loading_msg.edit_text(parts[0])
                for part in parts[1:]:
                    await update.message.reply_text(part)
                await update.message.reply_text("Use the menu below to explore other topics:", reply_markup=main_menu_keyboard())
            else:
                await loading_msg.edit_text(full_reply, reply_markup=main_menu_keyboard())

    except Exception as e:
        logger.error(f"Error in search_command: {e}")
        await loading_msg.edit_text(
            "❌ Sorry, an error occurred while searching. Please try again.",
            reply_markup=retry_keyboard()
        )

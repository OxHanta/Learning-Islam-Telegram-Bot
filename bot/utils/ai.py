import os
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

# the newest OpenAI model is "gpt-5" which was released August 7, 2025.
# do not change this unless explicitly requested by the user
MODEL = "gpt-5"

SYSTEM_PROMPT = """You are an Islamic Learning Assistant — a knowledgeable, friendly, and respectful guide to Islamic knowledge.

Your role:
- Answer questions about Islam with accuracy, depth, and clarity
- Cover topics such as: Quran and tafsir, Hadith, Islamic history, fiqh (jurisprudence), aqeedah (belief), seerah (Prophet's biography), Islamic ethics, worship, and daily Islamic practice
- Always cite sources where relevant (e.g., Quran chapter/verse, hadith collection)
- Present different scholarly opinions fairly when topics have legitimate scholarly disagreement
- Be warm, encouraging, and non-judgmental in tone
- Use relevant Arabic terms with their translations (e.g., Salah (prayer), Zakat (charity))

Boundaries:
- Politely decline to answer questions that are completely unrelated to Islam or Islamic knowledge
- Do not issue personal fatwas (religious rulings) — instead, explain general scholarly positions and recommend consulting a qualified scholar for personal matters
- Never produce content that is disrespectful to Islam, other religions, or people
- Keep responses concise but complete — aim for 2–4 paragraphs unless more depth is needed

Format:
- Use plain text (no markdown bold/italic — Telegram will display it as literal asterisks in some contexts)
- Break longer answers into short paragraphs for readability
- When quoting Quran, use the format: (Surah Name, Chapter:Verse)
- When referencing hadith, mention the collection (e.g., Sahih Bukhari)

Begin each conversation warmly and remind users they can ask you anything about Islam."""

_conversation_histories: dict[int, list[dict]] = {}
MAX_HISTORY = 20


def get_history(user_id: int) -> list[dict]:
    return _conversation_histories.get(user_id, [])


def add_to_history(user_id: int, role: str, content: str):
    if user_id not in _conversation_histories:
        _conversation_histories[user_id] = []
    _conversation_histories[user_id].append({"role": role, "content": content})
    if len(_conversation_histories[user_id]) > MAX_HISTORY:
        _conversation_histories[user_id] = _conversation_histories[user_id][-MAX_HISTORY:]


def clear_history(user_id: int):
    _conversation_histories.pop(user_id, None)


def ask_ai(user_id: int, user_message: str) -> str:
    add_to_history(user_id, "user", user_message)

    client = OpenAI(
        api_key=os.environ.get("AI_INTEGRATIONS_OPENAI_API_KEY"),
        base_url=os.environ.get("AI_INTEGRATIONS_OPENAI_BASE_URL"),
    )

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + get_history(user_id)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_completion_tokens=8192,
        )
        reply = response.choices[0].message.content or "I'm sorry, I could not generate a response. Please try again."
        add_to_history(user_id, "assistant", reply)
        return reply
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        _conversation_histories[user_id].pop()
        raise

import sqlite3
from bot.config import DATABASE_PATH


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS islamic_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT DEFAULT 'general'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hadiths (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            narrator TEXT NOT NULL,
            collection TEXT NOT NULL,
            text TEXT NOT NULL,
            interpretation TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quran_verses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            surah_name TEXT NOT NULL,
            surah_number INTEGER NOT NULL,
            ayah_number INTEGER NOT NULL,
            arabic TEXT NOT NULL,
            translation TEXT NOT NULL,
            explanation TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_locations (
            user_id INTEGER PRIMARY KEY,
            city TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS islamic_facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fact TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_option TEXT NOT NULL,
            explanation TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            user_id INTEGER PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    _seed_data(cursor)
    conn.commit()
    conn.close()


def _seed_data(cursor):
    cursor.execute("SELECT COUNT(*) FROM islamic_history")
    if cursor.fetchone()[0] == 0:
        history_data = [
            ("The Hijra - The Migration to Medina", "In 622 CE, Prophet Muhammad (PBUH) and his companions migrated from Mecca to Medina. This event, known as the Hijra, marks the beginning of the Islamic calendar. The journey was made under difficult conditions, with the Prophet and Abu Bakr hiding in a cave for three days to evade their pursuers.", "events"),
            ("The Battle of Badr", "The Battle of Badr in 624 CE was the first major military victory for the early Muslim community. A force of 313 Muslims defeated a Meccan army of around 1,000. This decisive victory is considered a turning point in Islamic history and is mentioned in the Quran.", "battles"),
            ("The Conquest of Mecca", "In 630 CE, Prophet Muhammad (PBUH) led an army of 10,000 Muslims into Mecca without significant bloodshed. The Prophet showed great mercy, granting general amnesty to the Meccans who had previously persecuted Muslims. The Kaaba was cleansed of idols and rededicated to the worship of Allah.", "events"),
            ("Saladin and the Crusades", "Salah ad-Din Yusuf ibn Ayyub, known as Saladin in the West, was a Muslim military leader who recaptured Jerusalem from the Crusaders in 1187 CE. Known for his chivalry and mercy, he allowed Christians to leave Jerusalem safely, in stark contrast to the Crusader siege decades before.", "personalities"),
            ("The Golden Age of Islam", "From the 8th to the 14th century, the Islamic world experienced a Golden Age of science, culture, and philosophy. Muslim scholars made groundbreaking contributions in mathematics, astronomy, medicine, and philosophy. Scholars like Ibn Sina (Avicenna), Al-Khawarizmi, and Ibn Rushd (Averroes) laid foundations for modern science.", "civilization"),
            ("The Life of Khadijah (RA)", "Khadijah bint Khuwaylid was the first wife of Prophet Muhammad (PBUH) and the first person to embrace Islam. She was a successful businesswoman who supported the Prophet through the early years of his mission. She remained a pillar of strength until her death, and the Prophet deeply mourned her loss.", "personalities"),
            ("The Abbasid Caliphate", "The Abbasid Caliphate (750-1258 CE) was one of the most prosperous periods in Islamic history. Based in Baghdad, the caliphate was a center of learning and culture. The House of Wisdom (Bayt al-Hikmah) in Baghdad became the world's greatest repository of knowledge.", "civilization"),
            ("Imam Malik and the Muwatta", "Imam Malik ibn Anas (711-795 CE) was one of the most influential Islamic scholars. His work, the Muwatta, is one of the earliest and most important collections of hadith and jurisprudence. He spent his entire life in Medina and his school of thought, the Maliki madhab, remains one of the four major schools of Islamic law.", "scholars"),
            ("The Spread of Islam in Africa", "Islam began spreading in Africa during the lifetime of Prophet Muhammad (PBUH) when early Muslims fled persecution to Abyssinia (modern Ethiopia). Over the centuries, Islam spread through trade, scholarship, and peaceful missionary work across the entire African continent.", "expansion"),
            ("Ibn Battuta - The Greatest Traveler", "Abu Abdullah Muhammad Ibn Battuta (1304-1368 CE) was a Moroccan Muslim scholar and explorer. He traveled over 75,000 miles across Africa, the Middle East, India, Central Asia, Southeast Asia, and China. His book, the Rihla, remains an invaluable historical document.", "personalities"),
        ]
        cursor.executemany("INSERT INTO islamic_history (title, content, category) VALUES (?, ?, ?)", history_data)

    cursor.execute("SELECT COUNT(*) FROM hadiths")
    if cursor.fetchone()[0] == 0:
        hadith_data = [
            ("Abdullah ibn Umar", "Sahih Bukhari", "The Prophet (PBUH) said: 'None of you will have faith until you love for your brother what you love for yourself.'", "This hadith emphasizes the importance of brotherhood, empathy, and selflessness in Islam. True faith requires that we genuinely desire good for others as we desire it for ourselves."),
            ("Abu Hurairah", "Sahih Muslim", "The Prophet (PBUH) said: 'A strong believer is better and more beloved to Allah than a weak believer, while there is good in both.'", "This hadith encourages Muslims to seek strength - both physical and spiritual - while reminding us that all believers are valued. Strength here encompasses physical health, mental resilience, and strength of faith."),
            ("Anas ibn Malik", "Sahih Bukhari", "The Prophet (PBUH) said: 'Make things easy and do not make them difficult. Give glad tidings and do not repel people.'", "This hadith establishes a foundational principle in Islamic teaching: ease and mercy over hardship. Islam is a religion of moderation and the Prophet (PBUH) consistently chose the easier path when given options."),
            ("Abu Hurairah", "Sahih Bukhari", "The Prophet (PBUH) said: 'The best of you are those who learn the Quran and teach it to others.'", "This hadith highlights the immense virtue of Quran education. Learning and teaching the Quran is considered one of the most noble acts in Islam, creating a chain of spiritual benefit that continues across generations."),
            ("Abdullah ibn Masud", "Sahih Bukhari", "The Prophet (PBUH) said: 'Truthfulness leads to righteousness and righteousness leads to Paradise. A man keeps telling the truth until he is recorded before Allah as truthful.'", "Truth is one of the most valued virtues in Islam. This hadith shows how truthfulness builds character over time, ultimately leading to righteousness and Paradise."),
            ("Abu Hurairah", "Sahih Muslim", "The Prophet (PBUH) said: 'Removing a harmful object from the road is charity (sadaqah).'", "Islam teaches that charity encompasses far more than monetary giving. Even the smallest act of benefit to others - like clearing an obstacle from the road - is considered an act of worship and charity."),
            ("Aisha (RA)", "Sahih Bukhari", "The Prophet (PBUH) said: 'The most beloved deeds to Allah are those done regularly, even if they are small.'", "Consistency in worship is more beloved to Allah than sporadic grand acts. This hadith encourages Muslims to establish regular habits of worship, no matter how small, rather than occasional bursts of intense devotion."),
            ("Abu Hurairah", "Sahih Muslim", "The Prophet (PBUH) said: 'Allah is gentle and loves gentleness in all matters.'", "This profound hadith reveals an essential attribute of Allah and sets the standard for how Muslims should interact with the world. Gentleness, kindness, and mercy are to be practiced in every aspect of life."),
            ("Muadh ibn Jabal", "Tirmidhi", "The Prophet (PBUH) said: 'Fear Allah wherever you are. Follow a bad deed with a good deed and it will blot it out. And interact with people with good character.'", "This concise hadith contains three comprehensive principles of Islamic ethics: God-consciousness, repentance through good deeds, and excellent character in social interactions."),
            ("Abu Hurairah", "Sahih Bukhari", "The Prophet (PBUH) said: 'Whoever believes in Allah and the Last Day, let him speak good or remain silent.'", "This hadith teaches Muslims the power of speech. Words have consequences in this life and the hereafter. If one cannot say something beneficial, silence is better than harmful speech."),
        ]
        cursor.executemany("INSERT INTO hadiths (narrator, collection, text, interpretation) VALUES (?, ?, ?, ?)", hadith_data)

    cursor.execute("SELECT COUNT(*) FROM quran_verses")
    if cursor.fetchone()[0] == 0:
        quran_data = [
            ("Al-Fatiha", 1, 1, "بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ", "In the name of Allah, the Most Gracious, the Most Merciful.", "This verse, known as the Basmalah, begins almost every chapter of the Quran. It reminds us that all actions should begin in the name of Allah. The names Ar-Rahman (Most Gracious) and Ar-Raheem (Most Merciful) emphasize Allah's boundless mercy."),
            ("Al-Baqarah", 2, 255, "ٱللَّهُ لَآ إِلَٰهَ إِلَّا هُوَ ٱلۡحَيُّ ٱلۡقَيُّومُ", "Allah! There is no god but He, the Living, the Self-Subsisting, Eternal.", "Ayat al-Kursi (The Throne Verse) is considered the greatest verse in the Quran. It affirms Allah's absolute uniqueness, eternal existence, and complete sovereignty over all creation. The Prophet (PBUH) said that reciting it after prayers grants Allah's protection until the next prayer."),
            ("Al-Imran", 3, 185, "كُلُّ نَفۡسٍ ذَآئِقَةُ ٱلۡمَوۡتِۗ", "Every soul shall have a taste of death.", "This verse is a profound reminder of the temporary nature of worldly life. It encourages believers to focus on preparing for the eternal hereafter rather than becoming overly attached to this fleeting world."),
            ("An-Nisa", 4, 36, "وَٱعۡبُدُواْ ٱللَّهَ وَلَا تُشۡرِكُواْ بِهِۦ شَيۡـًٔا", "Worship Allah and join none with Him in worship.", "This verse establishes the fundamental principle of Islamic monotheism (Tawhid) - the absolute oneness of Allah. It then goes on to command kindness to parents, relatives, orphans, the poor, neighbors, and travelers, showing that worship of Allah must be paired with service to humanity."),
            ("Al-Anam", 6, 162, "قُلۡ إِنَّ صَلَاتِي وَنُسُكِي وَمَحۡيَايَ وَمَمَاتِي لِلَّهِ رَبِّ ٱلۡعَٰلَمِينَ", "Say: Truly, my prayer, my sacrifice, my living, and my dying are for Allah, the Lord of the worlds.", "This verse captures the essence of complete submission to Allah. A true Muslim dedicates every aspect of life - prayers, acts of worship, daily living, and even death - entirely to Allah. This is the meaning of Islam as a complete way of life."),
            ("Al-Kahf", 18, 10, "رَبَّنَآ ءَاتِنَا مِن لَّدُنكَ رَحۡمَةً وَهَيِّئۡ لَنَا مِنۡ أَمۡرِنَا رَشَدًا", "Our Lord! Bestow on us mercy from Yourself, and facilitate for us our affairs in the right way.", "This is the prayer of the People of the Cave (Ashab al-Kahf), young believers who fled persecution to preserve their faith. This dua teaches us to seek Allah's mercy and guidance when facing trials and tribulations in life."),
            ("Al-Anfal", 8, 2, "إِنَّمَا ٱلۡمُؤۡمِنُونَ ٱلَّذِينَ إِذَا ذُكِرَ ٱللَّهُ وَجِلَتۡ قُلُوبُهُمۡ", "The believers are only those who, when Allah is mentioned, their hearts tremble with fear.", "This verse describes the qualities of true believers - their hearts are moved when Allah is mentioned, their faith increases when His verses are recited, and they put their trust in Allah. It sets a high standard for genuine faith."),
            ("Az-Zumar", 39, 53, "قُلۡ يَٰعِبَادِيَ ٱلَّذِينَ أَسۡرَفُواْ عَلَىٰٓ أَنفُسِهِمۡ لَا تَقۡنَطُواْ مِن رَّحۡمَةِ ٱللَّهِ", "Say: O My servants who have transgressed against themselves! Despair not of the Mercy of Allah.", "This is one of the most hopeful verses in the Quran. No matter how many sins a person has committed, Allah's mercy is greater. The door of repentance (tawbah) is always open. This verse gives hope to all who feel overwhelmed by their mistakes."),
            ("Al-Inshirah", 94, 5, "فَإِنَّ مَعَ ٱلۡعُسۡرِ يُسۡرًا", "Verily, with hardship comes ease.", "This short but powerful verse is repeated twice in the same chapter, emphasizing its importance. It assures believers that no matter how difficult the circumstances, relief and ease will come. This is one of the most comforting promises in the Quran."),
            ("Al-Baqarah", 2, 286, "لَا يُكَلِّفُ ٱللَّهُ نَفۡسًا إِلَّا وُسۡعَهَا", "Allah does not burden a soul beyond that it can bear.", "This verse is a source of immense comfort for believers. Allah, in His infinite wisdom and mercy, never places a burden on any person beyond their capacity. Every trial and difficulty we face is within our ability to handle with patience and trust in Allah."),
        ]
        cursor.executemany("INSERT INTO quran_verses (surah_name, surah_number, ayah_number, arabic, translation, explanation) VALUES (?, ?, ?, ?, ?, ?)", quran_data)

    cursor.execute("SELECT COUNT(*) FROM islamic_facts")
    if cursor.fetchone()[0] == 0:
        facts = [
            ("Islam is the second largest religion in the world, with over 1.8 billion followers globally.",),
            ("The word 'Islam' in Arabic means 'submission' or 'peace through submission to God'.",),
            ("The Quran was revealed to Prophet Muhammad (PBUH) over a period of approximately 23 years.",),
            ("The Five Pillars of Islam are: Shahada (faith), Salah (prayer), Zakat (charity), Sawm (fasting), and Hajj (pilgrimage).",),
            ("Muslims pray five times a day: Fajr (dawn), Dhuhr (midday), Asr (afternoon), Maghrib (sunset), and Isha (night).",),
            ("The Kaaba in Mecca is considered the House of Allah and is the direction toward which Muslims pray worldwide.",),
            ("Zakat, the Islamic obligation of charity, requires eligible Muslims to give 2.5% of their accumulated wealth annually.",),
            ("The month of Ramadan commemorates the first revelation of the Quran to Prophet Muhammad (PBUH).",),
            ("The Islamic calendar is lunar, meaning it is based on the cycles of the moon and has 354 or 355 days per year.",),
            ("Arabic is the language of the Quran, and Muslims around the world learn Arabic to read and understand it.",),
            ("The Prophet Muhammad (PBUH) was born in Mecca in 570 CE and received his first revelation at age 40.",),
            ("Islam teaches that all humans are equal before Allah regardless of race, nationality, or social status.",),
            ("Wudu (ablution) is a ritual purification that Muslims perform before prayers using water.",),
            ("The Eid al-Fitr celebration marks the end of Ramadan and is one of the two major Islamic holidays.",),
            ("Eid al-Adha commemorates Prophet Ibrahim's willingness to sacrifice his son as an act of obedience to Allah.",),
        ]
        cursor.executemany("INSERT INTO islamic_facts (fact) VALUES (?)", facts)

    cursor.execute("SELECT COUNT(*) FROM quizzes")
    if cursor.fetchone()[0] == 0:
        quiz_data = [
            ("Which Prophet is mentioned the most times by name in the Holy Quran?", "Prophet Muhammad (PBUH)", "Prophet Ibrahim (AS)", "Prophet Musa (AS)", "Prophet Isa (AS)", "C", "Prophet Musa (AS) is mentioned by name 136 times in the Holy Quran, making him the most mentioned Prophet in the text."),
            ("What was the first Surah of the Holy Quran to be revealed?", "Al-Fatiha", "Al-Alaq", "Al-Ikhlas", "Al-Baqarah", "B", "The first five verses of Surah Al-Alaq (Chapter 96) were the first verses revealed to Prophet Muhammad (PBUH) in the Cave of Hira by Angel Jibreel."),
            ("How many chapters (Surahs) are there in the Holy Quran?", "114", "120", "99", "30", "A", "The Holy Quran consists of 114 Surahs, starting with Surah Al-Fatiha and ending with Surah An-Nas. It is also divided into 30 equal parts called Juz'."),
            ("Who was the first Caliph of Islam after the passing of Prophet Muhammad (PBUH)?", "Umar ibn al-Khattab (RA)", "Uthman ibn Affan (RA)", "Ali ibn Abi Talib (RA)", "Abu Bakr al-Siddiq (RA)", "D", "Abu Bakr al-Siddiq (RA) was chosen as the first Righteously Guided Caliph (Rashidun) of Islam. He ruled for about two years, unifying the Muslim community."),
            ("What is the primary meaning of the word 'Tawhid' in Islamic theology?", "The belief in Angels", "The Oneness and Unity of Allah", "The obligation of daily prayer", "The history of Islamic civilization", "B", "Tawhid is the defining doctrine of Islam. It declares the absolute oneness and uniqueness of Allah as the sole Creator, Sustainer, and Lord of the universe."),
            ("In which Islamic month is fasting (Sawm) obligatory upon every healthy, adult Muslim?", "Muharram", "Rajab", "Ramadan", "Dhul-Hijjah", "C", "Ramadan is the ninth month of the Islamic lunar calendar. Fasting during Ramadan is one of the Five Pillars of Islam, commemorating the first revelation of the Quran."),
            ("Which battle was the first major military confrontation between Muslims of Medina and the Quraish of Mecca?", "The Battle of Uhud", "The Battle of Badr", "The Battle of the Trench", "The Battle of Hunayn", "B", "The Battle of Badr took place in 2 AH (624 CE). Despite being outnumbered 3 to 1, the Muslims achieved a miraculous and decisive victory, which is celebrated in the Quran."),
            ("What is the name of the Prophet's night journey from Mecca to Jerusalem and ascension to the heavens?", "The Hijra", "The Hajj", "Isra' and Mi'raj", "The Fath", "C", "Isra' and Mi'raj are the two parts of a miraculous journey that Prophet Muhammad (PBUH) took in one night. During this journey, the five daily prayers (Salah) were made obligatory."),
            ("Which companion is known as the 'Sword of Allah' (Saifullah)?", "Khalid ibn al-Walid (RA)", "Hamza ibn Abdul-Muttalib (RA)", "Sa'd ibn Abi Waqqas (RA)", "Ali ibn Abi Talib (RA)", "A", "Khalid ibn al-Walid (RA) was given the title 'Saifullah' (Sword of Allah) by Prophet Muhammad (PBUH) because of his extraordinary military genius and bravery in battle."),
            ("Which female scholar and wife of the Prophet (PBUH) narrated over 2,200 Hadiths?", "Khadijah bint Khuwaylid (RA)", "Aisha bint Abu Bakr (RA)", "Hafsa bint Umar (RA)", "Umm Salama (RA)", "B", "Aisha bint Abu Bakr (RA) was a brilliant scholar, jurist, and teacher. She narrated 2,210 Hadiths, making her one of the most prolific sources of early Islamic knowledge.")
        ]
        cursor.executemany("INSERT INTO quizzes (question, option_a, option_b, option_c, option_d, correct_option, explanation) VALUES (?, ?, ?, ?, ?, ?, ?)", quiz_data)


def get_random_history():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM islamic_history ORDER BY RANDOM() LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_random_hadith():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hadiths ORDER BY RANDOM() LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_random_quran_verse():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quran_verses ORDER BY RANDOM() LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_random_fact():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM islamic_facts ORDER BY RANDOM() LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return row["fact"] if row else "SubhanAllah! (Glory be to Allah)"


def save_user_location(user_id: int, city: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_locations (user_id, city)
        VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET city=excluded.city, updated_at=CURRENT_TIMESTAMP
    """, (user_id, city))
    conn.commit()
    conn.close()


def get_user_location(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT city FROM user_locations WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row["city"] if row else None


def get_random_quiz():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quizzes ORDER BY RANDOM() LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_quiz_by_id(quiz_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quizzes WHERE id = ?", (quiz_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def add_subscriber(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO subscribers (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()


def remove_subscriber(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subscribers WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


def is_subscribed(user_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM subscribers WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row is not None


def get_all_subscribers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM subscribers")
    rows = cursor.fetchall()
    conn.close()
    return [row["user_id"] for row in rows]


def search_database(keyword: str) -> dict:
    """
    Search the database for a keyword in Quran verses, Hadiths, or Islamic history.
    Returns a dict with matches from each table.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Quran Search
    cursor.execute(
        "SELECT * FROM quran_verses WHERE translation LIKE ? OR explanation LIKE ? OR surah_name LIKE ? LIMIT 3",
        (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
    )
    quran_matches = [dict(r) for r in cursor.fetchall()]
    
    # Hadith Search
    cursor.execute(
        "SELECT * FROM hadiths WHERE text LIKE ? OR interpretation LIKE ? OR narrator LIKE ? LIMIT 3",
        (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
    )
    hadith_matches = [dict(r) for r in cursor.fetchall()]
    
    # History Search
    cursor.execute(
        "SELECT * FROM islamic_history WHERE title LIKE ? OR content LIKE ? LIMIT 3",
        (f"%{keyword}%", f"%{keyword}%")
    )
    history_matches = [dict(r) for r in cursor.fetchall()]
    
    conn.close()
    
    return {
        "quran": quran_matches,
        "hadith": hadith_matches,
        "history": history_matches,
    }

"""
Configuration settings for the Telegram bot
"""

import os
from dotenv import load_dotenv

# تحميل القيم من .env
load_dotenv()

# Telegram configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

# OpenAI configuration  
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Bot configuration
MESSAGES_PER_DAY = 8
HOURS_BETWEEN_MESSAGES = 2
MAX_RETRIES = 3

# Content subjects for Saudi high school curriculum
SUBJECTS = {
    "biology": "الأحياء",
    "environment": "البيئة", 
    "earth_science": "علم الأرض"
}

# Content types
CONTENT_TYPES = [
    "multiple_choice_question",
    "educational_tip",
    "motivational_message",
    "study_advice"
]

# Saudi educational guidelines keywords
EDUCATIONAL_KEYWORDS = [
    "الجد والاجتهاد",
    "الانضباط المدرسي",
    "السلوك الإيجابي",
    "المواظبة",
    "التفوق الأكاديمي",
    "احترام القوانين المدرسية",
    "التعلم النشط",
    "التحصيل العلمي"
]

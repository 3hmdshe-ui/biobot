"""
Configuration settings for the Telegram bot
"""

import os
# لتحميل ملف .env فقط في البيئة المحلية، لا حاجة لذلك في Render
# من الأفضل تعطيل load_dotenv عند النشر
# من الممكن إزالة التعليق لو كنت تحتاج للتطوير المحلي فقط:
# from dotenv import load_dotenv
# load_dotenv()

# قراءة المتغيرات من البيئة
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# إعدادات إضافية للبوت
MESSAGES_PER_DAY = 8
HOURS_BETWEEN_MESSAGES = 2
MAX_RETRIES = 3

# موضوعات المحتوى الخاصة بالمناهج السعودية
SUBJECTS = {
    "biology": "الأحياء",
    "environment": "البيئة",
    "earth_science": "علم الأرض"
}

CONTENT_TYPES = [
    "multiple_choice_question",
    "educational_tip",
    "motivational_message",
    "study_advice"
]

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

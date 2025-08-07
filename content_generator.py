"""
Content generator using OpenAI API for Saudi high school science subjects
"""

import json
import logging
import random
from openai import OpenAI
from config import OPENAI_API_KEY, SUBJECTS, EDUCATIONAL_KEYWORDS

logger = logging.getLogger(__name__)

class ContentGenerator:
    """Generates educational content using OpenAI API"""
    
    def __init__(self):
        """Initialize the content generator"""
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.model = "gpt-4o"
    
    def generate_multiple_choice_question(self, subject):
        """Generate a multiple choice question with poll for a specific subject"""
        subject_arabic = SUBJECTS.get(subject, subject)
        
        prompt = f"""
        أنشئ سؤال اختيار من متعدد في مادة {subject_arabic} للمرحلة الثانوية وفق المناهج السعودية.
        
        المطلوب:
        1. سؤال تعليمي مفيد ومناسب للمستوى
        2. أربعة خيارات (أ، ب، ج، د)
        3. الإجابة الصحيحة
        4. شرح مختصر للإجابة
        
        أجب بتنسيق JSON مع الحقول التالية:
        - question: نص السؤال
        - options: قائمة بأربعة خيارات
        - correct_answer: رقم الإجابة الصحيحة (0-3)
        - explanation: شرح الإجابة الصحيحة
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "أنت مدرس خبير في المناهج السعودية للمرحلة الثانوية. اجعل المحتوى تعليمي ومفيد."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            
            response_content = response.choices[0].message.content
            if response_content:
                content = json.loads(response_content)
                logger.info(f"Generated multiple choice question for {subject}")
                return content
            else:
                logger.error("Empty response from OpenAI")
                return None
            
        except Exception as e:
            logger.error(f"Error generating multiple choice question: {e}")
            return None
    
    def generate_educational_tip(self, subject):
        """Generate an educational tip for a specific subject"""
        subject_arabic = SUBJECTS.get(subject, subject)
        
        prompt = f"""
        أنشئ نصيحة تعليمية قصيرة ومفيدة في مادة {subject_arabic} للطلاب في المرحلة الثانوية.
        
        المطلوب:
        1. نصيحة عملية وتطبيقية
        2. مرتبطة بالمنهج السعودي
        3. تساعد في الفهم والحفظ
        4. لا تزيد عن 200 كلمة
        
        أجب بتنسيق JSON مع الحقول التالية:
        - tip: النصيحة التعليمية
        - subject: المادة
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "أنت مدرس خبير في إعطاء النصائح التعليمية الفعالة."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.8
            )
            
            response_content = response.choices[0].message.content
            if response_content:
                content = json.loads(response_content)
                logger.info(f"Generated educational tip for {subject}")
                return content
            else:
                logger.error("Empty response from OpenAI")
                return None
            
        except Exception as e:
            logger.error(f"Error generating educational tip: {e}")
            return None
    
    def generate_motivational_message(self):
        """Generate a motivational message about academic discipline"""
        keyword = random.choice(EDUCATIONAL_KEYWORDS)
        
        prompt = f"""
        أنشئ رسالة تحفيزية للطلاب في المرحلة الثانوية تركز على {keyword}.
        
        المطلوب:
        1. رسالة إيجابية ومحفزة
        2. تشجع على الجد والاجتهاد
        3. تؤكد على أهمية الانضباط المدرسي
        4. تتماشى مع القيم التعليمية السعودية
        5. لا تزيد عن 150 كلمة
        
        أجب بتنسيق JSON مع الحقول التالية:
        - message: الرسالة التحفيزية
        - keyword: الكلمة المفتاحية المستخدمة
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "أنت مرشد طلابي يهدف لتحفيز الطلاب وتوجيههم نحو التفوق الأكاديمي."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.9
            )
            
            response_content = response.choices[0].message.content
            if response_content:
                content = json.loads(response_content)
                logger.info("Generated motivational message")
                return content
            else:
                logger.error("Empty response from OpenAI")
                return None
            
        except Exception as e:
            logger.error(f"Error generating motivational message: {e}")
            return None
    
    def generate_study_advice(self):
        """Generate study advice and academic discipline tips"""
        
        prompt = """
        أنشئ نصيحة دراسية عملية للطلاب في المرحلة الثانوية.
        
        المطلوب:
        1. نصيحة عملية للمذاكرة الفعالة
        2. تؤكد على أهمية تنظيم الوقت
        3. تشجع على السلوك الإيجابي في المدرسة
        4. تتضمن إرشادات للمواظبة والانضباط
        5. لا تزيد عن 180 كلمة
        
        أجب بتنسيق JSON مع الحقول التالية:
        - advice: النصيحة الدراسية
        - focus_area: المجال الذي تركز عليه النصيحة
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "أنت مرشد أكاديمي متخصص في إرشاد الطلاب لتحقيق التفوق الدراسي."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            
            response_content = response.choices[0].message.content
            if response_content:
                content = json.loads(response_content)
                logger.info("Generated study advice")
                return content
            else:
                logger.error("Empty response from OpenAI")
                return None
            
        except Exception as e:
            logger.error(f"Error generating study advice: {e}")
            return None
    
    def generate_content(self, content_type):
        """Generate content based on the specified type"""
        try:
            if content_type == "multiple_choice_question":
                subject = random.choice(list(SUBJECTS.keys()))
                return self.generate_multiple_choice_question(subject)
            elif content_type == "educational_tip":
                subject = random.choice(list(SUBJECTS.keys()))
                return self.generate_educational_tip(subject)
            elif content_type == "motivational_message":
                return self.generate_motivational_message()
            elif content_type == "study_advice":
                return self.generate_study_advice()
            else:
                logger.error(f"Unknown content type: {content_type}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            return None

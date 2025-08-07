"""
Telegram bot for posting educational content to Saudi high school science channel
"""

import logging
import asyncio
import requests
from content_generator import ContentGenerator
from config import TELEGRAM_TOKEN, CHANNEL_ID, MAX_RETRIES

logger = logging.getLogger(__name__)

class SaudiScienceBot:
    """Telegram bot for educational content posting"""
    
    def __init__(self):
        """Initialize the bot"""
        self.token = TELEGRAM_TOKEN
        self.channel_id = CHANNEL_ID
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        self.content_generator = ContentGenerator()
        
    async def post_multiple_choice_question(self, content):
        """Post a multiple choice question with poll"""
        try:
            question = content.get('question', '')
            options = content.get('options', [])
            correct_answer = content.get('correct_answer', 0)
            explanation = content.get('explanation', '')
            
            if not question or len(options) != 4:
                logger.error("Invalid multiple choice question content")
                return False
            
            # Send the poll using direct API call
            url = f"{self.base_url}/sendPoll"
            payload = {
                'chat_id': self.channel_id,
                'question': question,
                'options': options,
                'type': 'quiz',
                'correct_option_id': correct_answer,
                'explanation': explanation,
                'is_anonymous': True,
                'allows_multiple_answers': False
            }
            
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    logger.info(f"Posted multiple choice question poll: {result['result']['message_id']}")
                    return True
                else:
                    logger.error(f"Telegram API error: {result.get('description', 'Unknown error')}")
                    return False
            else:
                logger.error(f"HTTP error: {response.status_code}")
                return False
            
        except Exception as e:
            logger.error(f"Error posting multiple choice question: {e}")
            return False
    
    async def post_text_message(self, content, message_type):
        """Post a text message"""
        try:
            if message_type == "educational_tip":
                tip = content.get('tip', '')
                subject = content.get('subject', '')
                message = f"💡 *نصيحة تعليمية - {subject}*\n\n{tip}"
                
            elif message_type == "motivational_message":
                message_text = content.get('message', '')
                keyword = content.get('keyword', '')
                message = f"🌟 *رسالة تحفيزية*\n\n{message_text}\n\n#{keyword.replace(' ', '_')}"
                
            elif message_type == "study_advice":
                advice = content.get('advice', '')
                focus_area = content.get('focus_area', '')
                message = f"📚 *نصيحة دراسية - {focus_area}*\n\n{advice}"
                
            else:
                logger.error(f"Unknown message type: {message_type}")
                return False
            
            # Send the message using direct API call
            url = f"{self.base_url}/sendMessage"
            payload = {
                'chat_id': self.channel_id,
                'text': message,
                'parse_mode': 'Markdown'
            }
            
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    logger.info(f"Posted {message_type} message: {result['result']['message_id']}")
                    return True
                else:
                    logger.error(f"Telegram API error: {result.get('description', 'Unknown error')}")
                    return False
            else:
                logger.error(f"HTTP error: {response.status_code}")
                return False
            
        except Exception as e:
            logger.error(f"Error posting text message: {e}")
            return False
    
    async def post_content(self, content_type):
        """Generate and post content of specified type"""
        for attempt in range(MAX_RETRIES):
            try:
                # Generate content
                content = self.content_generator.generate_content(content_type)
                
                if not content:
                    logger.error(f"Failed to generate content for type: {content_type}")
                    continue
                
                # Post content based on type
                if content_type == "multiple_choice_question":
                    success = await self.post_multiple_choice_question(content)
                else:
                    success = await self.post_text_message(content, content_type)
                
                if success:
                    logger.info(f"Successfully posted {content_type} content")
                    return True
                else:
                    logger.warning(f"Failed to post {content_type} content, attempt {attempt + 1}")
                    
            except Exception as e:
                logger.error(f"Error in post_content attempt {attempt + 1}: {e}")
            
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(5)  # Wait before retry
        
        logger.error(f"Failed to post {content_type} content after {MAX_RETRIES} attempts")
        return False
    
    async def test_bot_connection(self):
        """Test bot connection and channel access"""
        try:
            # Test bot connection
            url = f"{self.base_url}/getMe"
            response = requests.get(url)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    bot_info = result['result']
                    logger.info(f"Bot connected successfully: {bot_info['username']}")
                else:
                    logger.error(f"Bot connection failed: {result.get('description', 'Unknown error')}")
                    return False
            else:
                logger.error(f"HTTP error testing bot: {response.status_code}")
                return False
            
            # Test channel access
            url = f"{self.base_url}/getChat"
            response = requests.get(url, params={'chat_id': self.channel_id})
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    chat_info = result['result']
                    logger.info(f"Channel access confirmed: {chat_info.get('title', 'Unknown')}")
                    return True
                else:
                    logger.error(f"Channel access failed: {result.get('description', 'Unknown error')}")
                    return False
            else:
                logger.error(f"HTTP error testing channel: {response.status_code}")
                return False
            
        except Exception as e:
            logger.error(f"Bot connection test failed: {e}")
            return False
    
    def run(self):
        """Run the bot (for testing purposes)"""
        try:
            # Test connection
            asyncio.run(self.test_bot_connection())
            logger.info("Bot is ready and running...")
            
            # Keep the bot running
            while True:
                import time
                time.sleep(60)
                
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Bot run error: {e}")

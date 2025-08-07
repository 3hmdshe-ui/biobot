"""
Content scheduler for automated posting every 2 hours
"""

import time
import threading
import logging
import random
import asyncio
from datetime import datetime, timedelta
from content_generator import ContentGenerator
from bot import SaudiScienceBot
from config import HOURS_BETWEEN_MESSAGES, CONTENT_TYPES

logger = logging.getLogger(__name__)

class ContentScheduler:
    """Scheduler for automated content posting"""
    
    def __init__(self, bot):
        """Initialize the scheduler"""
        self.bot = bot
        self.running = False
        self.thread = None
        self.last_post_time = None
        
    def start(self):
        """Start the scheduler"""
        if self.running:
            logger.warning("Scheduler is already running")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        logger.info("Content scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.thread:
            self.thread.join()
        logger.info("Content scheduler stopped")
    
    def _should_post_now(self):
        """Check if it's time to post new content"""
        if not self.last_post_time:
            return True
        
        time_since_last_post = datetime.now() - self.last_post_time
        return time_since_last_post >= timedelta(hours=HOURS_BETWEEN_MESSAGES)
    
    def _get_next_content_type(self):
        """Get the next content type to post"""
        # Weighted distribution for content types
        weights = {
            "multiple_choice_question": 40,  # 40% - main educational content
            "educational_tip": 30,           # 30% - subject-specific tips
            "motivational_message": 20,      # 20% - motivational content
            "study_advice": 10               # 10% - general study advice
        }
        
        content_types = list(weights.keys())
        content_weights = list(weights.values())
        
        return random.choices(content_types, weights=content_weights, k=1)[0]
    
    async def _post_scheduled_content(self):
        """Post scheduled content"""
        try:
            content_type = self._get_next_content_type()
            logger.info(f"Attempting to post {content_type} content")
            
            success = await self.bot.post_content(content_type)
            
            if success:
                self.last_post_time = datetime.now()
                logger.info(f"Successfully posted {content_type} at {self.last_post_time}")
            else:
                logger.error(f"Failed to post {content_type} content")
            
            return success
            
        except Exception as e:
            logger.error(f"Error in scheduled content posting: {e}")
            return False
    
    def _run_scheduler(self):
        """Main scheduler loop"""
        logger.info("Scheduler thread started")
        
        # Post initial content immediately
        try:
            asyncio.run(self._post_scheduled_content())
        except Exception as e:
            logger.error(f"Error posting initial content: {e}")
        
        while self.running:
            try:
                if self._should_post_now():
                    asyncio.run(self._post_scheduled_content())
                
                # Check every 5 minutes
                time.sleep(300)
                
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
        
        logger.info("Scheduler thread stopped")
    
    def get_status(self):
        """Get scheduler status"""
        status = {
            "running": self.running,
            "last_post_time": self.last_post_time,
            "next_post_time": None
        }
        
        if self.last_post_time:
            status["next_post_time"] = self.last_post_time + timedelta(hours=HOURS_BETWEEN_MESSAGES)
        
        return status
    
    def force_post(self, content_type=None):
        """Force post content immediately"""
        if not content_type:
            content_type = self._get_next_content_type()
        
        try:
            success = asyncio.run(self._post_scheduled_content())
            return success
        except Exception as e:
            logger.error(f"Error in force post: {e}")
            return False

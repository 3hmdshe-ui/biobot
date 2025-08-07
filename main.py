#!/usr/bin/env python3
"""
Main entry point for the Saudi High School Science Telegram Bot
"""

import asyncio
import logging
from threading import Thread
from flask import Flask

from bot import SaudiScienceBot
from scheduler import ContentScheduler
from logger import setup_logging

# إعداد Flask لإبقاء Replit نشطًا
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

def main():
    """Main function to start the bot and scheduler"""
    # إبقاء Replit نشطًا
    keep_alive()

    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Starting Saudi High School Science Telegram Bot...")

    try:
        # Initialize the bot
        bot = SaudiScienceBot()

        # Initialize the scheduler
        scheduler = ContentScheduler(bot)

        # Start the scheduler in a separate thread
        scheduler.start()

        # Start the bot
        bot.run()

    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise

if __name__ == "__main__":
    main()
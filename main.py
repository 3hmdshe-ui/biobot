#!/usr/bin/env python3
"""
Main entry point for the Saudi High School Science Telegram Bot
"""

import os
from dotenv import load_dotenv
load_dotenv()  # ← هذا السطر مهم لتحميل ملف .env

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
    keep_alive()
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting Saudi High School Science Telegram Bot...")

    try:
        # Print environment variables (للتأكد فقط - احذفها لاحقًا)
        print("TELEGRAM_TOKEN:", os.getenv("TELEGRAM_TOKEN"))
        print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))

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

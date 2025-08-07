# Overview

This is a Telegram bot designed to automatically post educational content to a Saudi high school science channel. The bot generates and schedules multiple choice questions, educational tips, motivational messages, and study advice in Arabic, focusing on biology, earth science, and environmental science subjects aligned with Saudi educational curriculum standards.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Core Components

**Bot Architecture**: The system follows a modular Python architecture with clear separation of concerns:
- `SaudiScienceBot` class handles Telegram API interactions and message posting
- `ContentGenerator` manages OpenAI API integration for content creation
- `ContentScheduler` runs automated posting on a 2-hour interval schedule
- Configuration management through environment variables and centralized settings

**Content Generation Strategy**: Uses OpenAI's GPT-4o model to generate educational content in Arabic, specifically tailored for Saudi high school curriculum. Content types include multiple choice questions with polls, educational tips, motivational messages, and study advice.

**Scheduling System**: Implements a threaded scheduler that posts content every 2 hours, with 8 messages per day maximum. The scheduler runs as a daemon thread to avoid blocking the main application.

**Subject Focus**: Targets three core subjects from Saudi high school curriculum:
- Biology (الأحياء)
- Environmental Science (البيئة)  
- Earth Science (علم الأرض)

**Localization**: All content is generated in Arabic and incorporates Saudi educational guidelines and cultural values through predefined educational keywords.

**Error Handling**: Includes retry mechanisms with configurable maximum retry attempts and comprehensive logging for debugging and monitoring.

## Design Patterns

**Singleton-like Bot Instance**: The bot maintains a single instance per application run to manage Telegram connections efficiently.

**Factory Pattern for Content**: Content generation uses a factory-like approach where different content types are created based on subject and type parameters.

**Observer Pattern for Scheduling**: The scheduler observes time intervals and triggers content generation and posting events.

# External Dependencies

**Telegram Bot API**: Primary integration for sending messages, polls, and managing the Telegram channel. Uses the python-telegram-bot library for API interactions.

**OpenAI API**: Content generation powered by GPT-4o model for creating educational content in Arabic. Requires API key authentication and handles structured JSON responses for multiple choice questions.

**Python Standard Libraries**: 
- `asyncio` for asynchronous operations with Telegram API
- `threading` for background scheduling
- `logging` for application monitoring and debugging
- `json` for parsing OpenAI responses
- `datetime` for scheduling calculations

**Environment Configuration**: Relies on environment variables for sensitive configuration like API tokens, channel IDs, and API keys, with fallback default values for development.
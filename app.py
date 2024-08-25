#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 22:08:48 2024

@author: Maksim Blekhshtein
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.executor import start_webhook
from pyrogram import Client
from config import load_bot_config, load_user_config, BotConfig, UserConfig
from handlers import register_handlers
from middlewares import RateLimitMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='bot.log',
    filemode='a'
)
logger = logging.getLogger(__name__)

async def login_user(app: Client, phone_number: str, password: str):
    try:
        await app.start()
        await app.sign_in(phone_number=phone_number, password=password)
        logger.info("Successfully logged in to Telegram as user.")
    except Exception as e:
        logger.error(f"Failed to log in: {str(e)}")
        raise

async def on_startup(dp: Dispatcher, webhook_url: str, app: Client, user_config: UserConfig):
    await dp.bot.set_webhook(webhook_url)
    logger.info(f"Bot started with webhook at {webhook_url}")
    await login_user(app, user_config.PHONE_NUMBER, user_config.PASSWORD)

async def on_shutdown(dp: Dispatcher, app: Client):
    logger.info("Shutting down...")
    await dp.bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    await app.stop()

async def main():
    bot_config = load_bot_config()
    user_config = load_user_config()

    bot = Bot(token=bot_config.BOT_TOKEN)
    dp = Dispatcher(bot)
    
    # Add middlewares
    dp.middleware.setup(LoggingMiddleware())
    dp.middleware.setup(RateLimitMiddleware())

    app = Client(
        "user_session", 
        api_id=bot_config.API_ID, 
        api_hash=bot_config.API_HASH
    )

    register_handlers(dp, app, bot_config, user_config)

    webhook_url = f"{bot_config.WEBHOOK_URL}/webhook/{bot_config.BOT_TOKEN}"

    try:
        await start_webhook(
            dispatcher=dp,
            webhook_path=f"/webhook/{bot_config.BOT_TOKEN}",
            on_startup=lambda dp: on_startup(dp, webhook_url, app, user_config),
            on_shutdown=lambda dp: on_shutdown(dp, app),
            skip_updates=True,
            host=bot_config.WEBAPP_HOST,
            port=bot_config.WEBAPP_PORT,
        )
    except Exception as e:
        logger.error(f"Failed to start bot: {str(e)}")
        raise

if __name__ == '__main__':
    asyncio.run(main())

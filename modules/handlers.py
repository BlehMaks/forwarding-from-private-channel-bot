#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 22:55:19 2024

@author: Maksim Blekhshtein
"""
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command
from pyrogram import Client, filters
import logging
from config import BotConfig, UserConfig, save_bot_config

logger = logging.getLogger(__name__)

async def is_user_allowed(user_id: int, allowed_user_ids: list) -> bool:
    return user_id in allowed_user_ids

async def register_user(message: types.Message, bot_config: BotConfig):
    user_id = message.from_user.id
    if user_id not in bot_config.ALLOWED_USER_IDS:
        bot_config.ALLOWED_USER_IDS.append(user_id)
        save_bot_config(bot_config)
        logger.info(f"Registered user {user_id}")
        await message.reply("You have been registered successfully and can now use the bot.")
    else:
        await message.reply("You are already registered.")

async def start_command(message: types.Message, bot_config: BotConfig):
    await register_user(message, bot_config)
    await message.reply("Welcome! I'm a channel forwarding bot.")

async def help_command(message: types.Message, bot_config: BotConfig):
    if await is_user_allowed(message.from_user.id, bot_config.ALLOWED_USER_IDS):
        await message.reply("I'm forwarding messages from specified channels to a target channel.")
    else:
        await message.reply("You do not have permission to use this bot.")

async def forward_message(client: Client, message, user_config: UserConfig):
    try:
        await client.forward_messages(
            chat_id=user_config.TARGET_CHANNEL_ID,
            from_chat_id=message.chat.id,
            message_ids=message.message_id
        )
        logger.info(f"Forwarded message {message.message_id} from {message.chat.title} to target channel")
    except Exception as e:
        logger.error(f"Failed to forward message: {str(e)}")

def register_handlers(dp: Dispatcher, app: Client, bot_config: BotConfig, user_config: UserConfig):
    dp.register_message_handler(lambda message: start_command(message, bot_config), Command("start"))
    dp.register_message_handler(lambda message: help_command(message, bot_config), Command("help"))

    @app.on_message(filters.chat(user_config.SOURCE_CHANNEL_IDS))
    async def handle_new_message(client, message):
        if await is_user_allowed(message.from_user.id, bot_config.ALLOWED_USER_IDS):
            await forward_message(client, message, user_config)
        else:
            logger.warning(f"Unauthorized user {message.from_user.id} tried to forward a message.")

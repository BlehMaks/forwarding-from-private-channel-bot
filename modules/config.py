#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 22:16:32 2024

@author: Maksim Blekhshtein
"""

import json
from cryptography.fernet import Fernet
from dataclasses import dataclass
import os

# Generate a key and save it to a file
def generate_key():
    return Fernet.generate_key()

# Load the key from a file
def load_key():
    return open('secret.key', 'rb').read()

# Encrypt data
def encrypt_data(data: dict, key: bytes) -> bytes:
    f = Fernet(key)
    data_json = json.dumps(data)
    encrypted_data = f.encrypt(data_json.encode())
    return encrypted_data

# Decrypt data
def decrypt_data(encrypted_data: bytes, key: bytes) -> dict:
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data).decode()
    return json.loads(decrypted_data)

# Define the configuration dataclasses
@dataclass
class BotConfig:
    BOT_TOKEN: str
    API_ID: int
    API_HASH: str
    WEBHOOK_URL: str
    WEBAPP_HOST: str
    WEBAPP_PORT: int
    ALLOWED_USER_IDS: list

@dataclass
class UserConfig:
    PHONE_NUMBER: str
    PASSWORD: str
    TARGET_CHANNEL_ID: int
    SOURCE_CHANNEL_IDS: list

# Load bot configuration
def load_bot_config() -> BotConfig:
    key = load_key()
    with open('bot_config.enc', 'rb') as file:
        encrypted_data = file.read()
    bot_data = decrypt_data(encrypted_data, key)
    
    return BotConfig(
        BOT_TOKEN=bot_data['BOT_TOKEN'],
        API_ID=bot_data['API_ID'],
        API_HASH=bot_data['API_HASH'],
        WEBHOOK_URL=bot_data['WEBHOOK_URL'],
        WEBAPP_HOST=bot_data['WEBAPP_HOST'],
        WEBAPP_PORT=bot_data['WEBAPP_PORT'],
        ALLOWED_USER_IDS=bot_data['ALLOWED_USER_IDS']
    )

# Load user configuration
def load_user_config() -> UserConfig:
    key = load_key()
    with open('user_config.enc', 'rb') as file:
        encrypted_data = file.read()
    user_data = decrypt_data(encrypted_data, key)
    
    return UserConfig(
        PHONE_NUMBER=user_data['PHONE_NUMBER'],
        PASSWORD=user_data['PASSWORD'],
        TARGET_CHANNEL_ID=user_data['TARGET_CHANNEL_ID'],
        SOURCE_CHANNEL_IDS=user_data['SOURCE_CHANNEL_IDS']
    )

# Save bot configuration
def save_bot_config(bot_config: BotConfig):
    key = load_key()
    bot_data = {
        'BOT_TOKEN': bot_config.BOT_TOKEN,
        'API_ID': bot_config.API_ID,
        'API_HASH': bot_config.API_HASH,
        'WEBHOOK_URL': bot_config.WEBHOOK_URL,
        'WEBAPP_HOST': bot_config.WEBAPP_HOST,
        'WEBAPP_PORT': bot_config.WEBAPP_PORT,
        'ALLOWED_USER_IDS': bot_config.ALLOWED_USER_IDS
    }
    encrypted_data = encrypt_data(bot_data, key)
    with open('bot_config.enc', 'wb') as file:
        file.write(encrypted_data)

# Save user configuration
def save_user_config(user_config: UserConfig):
    key = load_key()
    user_data = {
        'PHONE_NUMBER': user_config.PHONE_NUMBER,
        'PASSWORD': user_config.PASSWORD,
        'TARGET_CHANNEL_ID': user_config.TARGET_CHANNEL_ID,
        'SOURCE_CHANNEL_IDS': user_config.SOURCE_CHANNEL_IDS
    }
    encrypted_data = encrypt_data(user_data, key)
    with open('user_config.enc', 'wb') as file:
        file.write(encrypted_data)

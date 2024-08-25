#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 22:57:18 2024

@author: Maksim Blekhshtein
"""
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
import asyncio

class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, limit=1, interval=1):
        self.limit = limit
        self.interval = interval
        self.timestamps = {}
        super().__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        user_id = message.from_user.id
        now = asyncio.get_event_loop().time()
        if user_id not in self.timestamps:
            self.timestamps[user_id] = []
        self.timestamps[user_id] = [ts for ts in self.timestamps[user_id] if now - ts < self.interval]
        if len(self.timestamps[user_id]) >= self.limit:
            raise CancelHandler()
        self.timestamps[user_id].append(now)

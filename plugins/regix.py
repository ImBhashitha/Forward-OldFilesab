#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Dark Angel

import os
import sys
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from pyrogram.errors import FloodWait
from config import Config
from translation import Translation

FILTER = Config.FILTER_TYPE
files_count = 0
IS_CANCELLED = False

@Client.on_callback_query(filters.regex(r'^start_public$'))
async def pub_(bot, message):
    global files_count, IS_CANCELLED
    await message.answer()
    await message.message.delete()
    from plugins.public import FROM, TO, SKIP, LIMIT
    buttons = [[
        InlineKeyboardButton('Cancel🚫', 'terminate_frwd')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    m = await bot.send_message(
        text="<i>File Forwording Started😉</i>",
        reply_markup=reply_markup,
        chat_id=message.message.chat.id
    )
    #files_count = 0
    async for message in bot.USER.search_messages(chat_id=FROM,offset=int(SKIP),limit=int(LIMIT),filter=FILTER):
        if IS_CANCELLED:
            IS_CANCELLED = False
            break
        try:
            if message.video:
                file_name = message.video.file_name
            elif message.document:
                file_name = message.document.file_name
            elif message.audio:
                file_name = message.audio.file_name
            else:
                file_name = None
            await bot.copy_message(
                chat_id=TO,
                from_chat_id=FROM,
                parse_mode="md",       
                caption=Translation.CAPTION.format(file_name),
                message_id=message.message_id
            )
            files_count += 1
            await asyncio.sleep(1)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await bot.copy_message(
                chat_id=TO,
                from_chat_id=FROM,
                parse_mode="md",       
                caption=Translation.CAPTION.format(file_name),
                message_id=message.message_id
            )
            files_count += 1
            await asyncio.sleep(1)
        except Exception as e:
            print(e)
            pass
   # await m.delete()
    buttons = [[
        InlineKeyboardButton('📜 Support Group', url='https://t.me/DxHelpDesk')
    ]] 
    reply_markup = InlineKeyboardMarkup(buttons)
    await m.edit_text(
        text=f"<u><i>Successfully Forwarded</i></u>\n\n<b>Total Forwarded Files:-</b> <code>{files_count}</code> <b>Files</b>\n<b>Thanks For Using Me❤️</b>",
        reply_markup=reply_markup
    )

@Client.on_callback_query(filters.regex(r'^start_private$'))
async def pri_(bot, message):
    global files_count
    await message.answer()
    await message.message.delete()
    from plugins.private import FROM, TO, SKIP, LIMIT
    buttons = [[
        InlineKeyboardButton('Cancel🚫', 'terminate_frwd')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    m = await bot.send_message(
        text="<i>File Forwording Started😉</i>",
        reply_markup=reply_markup,
        chat_id=message.message.chat.id
    )
   # files_count = 0
    async for message in bot.USER.search_messages(chat_id=FROM,offset=int(SKIP),limit=int(LIMIT),filter=Config.FILTER_TYPE):
        try:
            if message.video:
                file_name = message.video.file_name
            elif message.document:
                file_name = message.document.file_name
            elif message.audio:
                file_name = message.audio.file_name
            else:
                file_name = None
            caption = message.caption.markdown if message.caption else ''
            await bot.copy_message(
                chat_id=TO,
                from_chat_id=FROM,
                parse_mode="md",       
                caption=Translation.CAPTION.format(file_name),
                message_id=message.message_id
            )
            files_count += 1
            await asyncio.sleep(1)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await bot.copy_message(
                chat_id=TO,
                from_chat_id=FROM,
                parse_mode="md",       
                caption=Translation.CAPTION.format(file_name),
                message_id=message.message_id
            )
            files_count += 1
            await asyncio.sleep(1)
        except Exception as e:
            print(e)
            pass
   # await m.delete()
    buttons = [[
        InlineKeyboardButton('📜 Support Group', url='https://t.me/DxHelpDesk')
    ]] 
    reply_markup = InlineKeyboardMarkup(buttons)
    await m.edit_text(
        text=f"<u><i>Successfully Forwarded</i></u>\n\n<b>Total Forwarded Files:-</b> <code>{files_count}</code> <b>Files</b>\n<b>Thanks For Using Me❤️</b>",
        reply_markup=reply_markup
    )
      
@Client.on_callback_query(filters.regex(r'^terminate_frwd$'))
async def terminate_frwding(bot, update):
    global IS_CANCELLED
    IS_CANCELLED = True
    
@Client.on_callback_query(filters.regex(r'^close_btn$'))
async def close(bot, update):
    await update.answer()
    await update.message.delete()

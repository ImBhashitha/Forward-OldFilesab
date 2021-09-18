import asyncio, re
from bot import Bot
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from pyrogram.errors import FloodWait
from config import Config
from translation import Translation

#FROM = "-1001274403248"
#TO = "-1001584048226"
#SKIP = 0

#if re.match('-100\d+', FROM):
    #FROM = int(FROM)
#if re.match('-100\d+', TO):
    #TO = int(TO)

FILTER = Config.FILTER_TYPE
files_count = 0

@Client.on_message(filters.private & filters.command(["private"]))
async def private(bot, message):
    global SKIP
    global FROM
    global TO
    global LIMIT
    if str(message.from_user.id) not in Config.OWNER_ID:
        return
    fromid = await bot.ask(message.chat.id, Translation.PFROM_MSG)
    if fromid.text.startswith('/'):
        await message.reply(Translation.PCANCEL)
        return
    toid = await bot.ask(message.chat.id, Translation.TO_MSG)
    if toid.text.startswith('/'):
        await message.reply(Translation.PCANCEL)
        return
    skipno = await bot.ask(message.chat.id, Translation.SKIP_MSG)
    if skipno.text.startswith('/'):
        await message.reply(Translation.PCANCEL)
        return
    limitno = await bot.ask(message.chat.id, Translation.LIMIT_MSG)
    if limitno.text.startswith('/'):
        await message.reply(Translation.CANCEL)
        return
    buttons = [[
        InlineKeyboardButton('Yes', callback_data='start_private'),
        InlineKeyboardButton('No', callback_data='close_btn')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await bot.send_message(
        text=Translation.PDOUBLE_CHECK,
        reply_markup=reply_markup,
        chat_id=message.chat.id
    )
    SKIP = skipno.text
    FROM = fromid.text
    TO = toid.text
    LIMIT = limitno.text
    if re.match('-100\d+', FROM):
        FROM = int(FROM)
    if re.match('-100\d+', TO):
        TO = int(TO)

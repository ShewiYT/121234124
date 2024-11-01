from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config
import menu
import sqlite3
import statess
import random
import requests
from datetime import datetime, timedelta, date
import datetime
from PIL import Image, ImageDraw, ImageFont
import time
import asyncio
import logging
import aiohttp
import json
import string

bot = Bot(config.API_Nark, parse_mode='HTML')
workerbot = Bot(config.API_Worker, parse_mode='HTML')
dp = Dispatcher(bot,storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)
bd = 'data/database.db'#
now = datetime.datetime.today()

print('Нарк бот успешно запущен [+]')

canal = -1001780350691
TC_group = -1001888818346



def generate_word():
    W, H = (1920, 1080)
    place = Image.new("RGB", (1920, 1080), "white")
    font = ImageFont.truetype("NarkoShop/font.ttf", size=300)
    letters = string.ascii_lowercase
    rand_string = "".join(random.choice(letters) for i in range(8))
    imgdraw = ImageDraw.Draw(place)
    w, h = font.getsize(rand_string)
    imgdraw.text(((W-w)/2, (H-h)/2), rand_string, font=font, fill="black")
    place.save("NarkoShop/verification_img.jpg")
    return rand_string


@dp.message_handler(commands="start", state='*')
async def start(message: types.Message):
    text = generate_word()
    photo = open("NarkoShop/verification_img.jpg", "rb")
    with sqlite3.connect(bd) as c:
        c.execute("UPDATE mamonts_nark SET verifs = ? WHERE id = ?", (text,message.from_user.id,))
    await bot.send_photo(message.from_user.id, photo, 'Введи код с капчи', parse_mode='HTML')
    await statess.get_word.q1.set()
    
    
    
    

@dp.message_handler(state=statess.code.q1)
async def spammers(message: types.Message,state:FSMContext):
    with sqlite3.connect(bd) as c:
        ref = c.execute("SELECT id FROM workers WHERE ref_code = ?", (message.text,)).fetchone()
        info = c.execute('SELECT * FROM mamonts_nark WHERE id = ?',(message.chat.id,)).fetchone()
    if ref != None:
        with sqlite3.connect(bd) as c:
            c.execute('INSERT INTO mamonts_nark VALUES(?,?,?,?,?,?,?,?,?,?,?)',(message.from_user.id, '0', message.text, '0', '0', message.from_user.first_name, message.from_user.username, '0', '0', '0', '0'))
        #await workerbot.send_message(ref[0], f"<b><i>🎉У вас новый 🦣 подопытный! @{message.from_user.username}</i></b>")
        await state.finish()
        if info[8] == 0:
            text = generate_word()
            photo = open("NarkoShop/verification_img.jpg", "rb")
            await bot.send_photo(message.from_user.id, photo, 'Введи код с капчи', parse_mode='HTML')
            await statess.get_word.q1.set()
    else:
        await message.answer(f'Код не 6 значный! Введите 6 значный код:')

@dp.message_handler(state=statess.get_word.q1)
async def spammers(message: types.Message,state:FSMContext):
    async with state.proxy() as data:
        data["word"] = message.text
        with sqlite3.connect(bd) as c:
            get_verification_data = c.execute('SELECT * FROM mamonts_nark WHERE id = ?',(message.chat.id,)).fetchone()[8]
        print(get_verification_data)
        if data["word"] == get_verification_data:
            with open('NarkoShop/photo/olivander.jpg', 'rb') as photo:
                texst = f'''
Привет, {message.from_user.first_name}

С момента покупки до съема клада у вас есть 12 часов для того, чтобы открыть диспут при наличии проблемы/уточнения.Предоставьте 3-4 фотографии с ракурса курьера, сделанных в светлое время суток.
Будьте вежливы и спокойны, мы на вашей стороне и поможем вам разобраться с возникшими трудностями по заказу.

Наши операторы на связи с Вами 24/7

Если у вас есть какие-то вопросы по товару или пред заказам, то пишите администратору/оператору магазина
{config.TP_NICK}



Правила магазина:
1. С момента покупки до съема клада у вас есть 12 часов для того, чтобы открыть диспут при наличии проблемы/уточнения.
2. Предоставьте 3-4 фотографии с ракурса курьера, сделанных в светлое время суток.
3. Будьте спокойны, мы поможем вам разобраться с возникшими трудностями.
4. В случае НЕАДЕКВАТНОГО ПОВЕДЕНИЯ (мат, спам), магазин вправе оставить за собой выбор в пользу ОТКАЗА для рассмотрения вашей заявки.
            '''
                await bot.send_photo(message.from_user.id, photo, texst, reply_markup=menu.mainkb)
                with sqlite3.connect(bd) as c:
                    c.execute("UPDATE mamonts_nark SET verifs = 1 WHERE id = ?", (message.from_user.id,))
                await state.finish()
        else:
            await message.answer(f'Капча введена неверно!')

@dp.message_handler(content_types=['text'], text='Товар')
async def buy(message: types.Message):
    with sqlite3.connect(bd) as c:
        info = c.execute('SELECT * FROM mamonts_nark WHERE id = ?',(message.chat.id,)).fetchone()
    if info[4] == 0:
        spisok_towns = []
        for item in town_and_rajon.select():
            spisok_towns.append(item.town)
        
        await bot.send_message(message.from_user.id, text='Выберите город:',reply_markup=menu.kb_towns(spisok_towns=spisok_towns))
    else:
        await message.answer('Ты заблокирован.')
executor.start_polling(dp, skip_updates=False)
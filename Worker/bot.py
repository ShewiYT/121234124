# -*- coding: utf-8 -*-
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext 
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import Throttled
from aiogram.types import CallbackQuery
import config
import menu
from requests import get
import sqlite3
from statess import *
import random 
import aiohttp
import functions
import asyncio
import json
import math
from filters import IsAdminFilter
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler, current_handler
import logging, configparser
from aiogram.utils.exceptions import BotBlocked
from aiogram.dispatcher import filters
import datetime
import db
from db import Database
import time
from datetime import timedelta ,datetime , date
from aiogram.types import ChatType
config_name = "config.ini"

bot = Bot(config.API_Worker, parse_mode='HTML', disable_web_page_preview=True) 
arbitrbot = Bot(config.API_Arbitrage, parse_mode='HTML') 
casinobot = Bot(config.API_Casino, parse_mode='HTML') 
tradebot = Bot(config.API_Trade, parse_mode='HTML') 
dp = Dispatcher(bot,storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)
bd = 'data/database.db'

reported_users = {}
GROUP_ID = -1001802147747
REPORT_ID = -1001802147747
REPORT_TIME = 15 * 60

print('Воркер бот успешно запущен [+]')

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit=0.5, key_prefix="antiflood_"):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            limit = getattr(handler, "throttling_rate_limit", self.rate_limit)
            key = getattr(handler, "throttling_key", f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.message_throttled(message, t)
            raise CancelHandler()

    async def message_throttled(self, message: types.Message, throttled: Throttled):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            key = getattr(handler, "throttling_key", f"{self.prefix}_{handler.__name__}")
        else:
            key = f"{self.prefix}_message"
        delta = throttled.rate - throttled.delta
        if throttled.exceeded_count <= 2:
            await message.reply("<b>❗ Пожалуйста, не спамьте.</b>")
        await asyncio.sleep(delta)
        thr = await dispatcher.check_key(key)

def get_config(value):
	config = configparser.ConfigParser()
	config.read(config_name)
	r = config['Settings'][value]
	return r

async def config_set_value(value, value_set):
	config = configparser.ConfigParser()
	config.read(config_name)
	config.set('Settings', value, value_set)

	with open(config_name, 'w') as configfile:
		config.write(configfile)

def rate_limit(limit: int, key=None):
    def decorator(func):
        setattr(func, "throttling_rate_limit", limit)
        if key:
            setattr(func, "throttling_key", key)
        return func
    return decorator

dp.filters_factory.bind(IsAdminFilter)

async def started(dp):
	await bot.send_message(config.ADMIN, text='✅ Бот запущен!')

@dp.message_handler(commands="start", state="*")
@rate_limit(2, 'start')
async def cmd_start(message: types.Message, state: FSMContext):
    #try:
        await functions.update_data(message)
        if message.chat.type == 'private':
            with sqlite3.connect(bd) as c:
                check = c.execute("SELECT id FROM workers WHERE id = ?", (message.from_user.id,)).fetchone()
            if check is None:
                await message.answer(f"💬 Правила MONEY RAIN TEAM 💬\n\n"
                                     f"<b>Запрещено:</b>\n\n"
                                     f"<code>🔸 Распространение запрещённых материалов, 18+ GIF/Стикеров/Видео/Фото</code>\n"
                                     f"<code>🔸 Попрошайничество</code>\n"
                                     f"<code>🔸 Реклама сторонних проектов или же услуг</code>\n"
                                     f"<code>🔸 Принимать платежи на свои реквизиты</code>\n"
                                     f"<code>🔸 Спамить или тегать стафф, потому что вам не отвечают в лс</code>\n"
                                     f"<code>🔸 Оскорблять национальность/высказывать свои полит взгляды</code>\n"
                                     f"<code>🔸 Использовать любые ТП кроме ботов тимы</code>\n"
                                     f"<code>🔸 Оскорблять любого из представителей администрации</code>\n\n"
                                     f"<b>Вы подтверждаете, что ознакомились и согласны с условиями и правилами нашего проекта?</b>", reply_markup=menu.prinsogl, parse_mode='HTML')
            else:
                price = await convert_to_dollars()
                with sqlite3.connect(bd) as c:
                    result = c.execute(f"SELECT warn_count FROM workers WHERE id = {message.from_user.id}").fetchone()[0]
                    info = c.execute(f'SELECT * FROM workers WHERE id = {message.from_user.id}').fetchone()
                    get_s_profits = c.execute(f'SELECT * FROM profits WHERE user_id = {message.from_user.id}').fetchall()
                    refs = c.execute(f'SELECT * FROM workers WHERE ref = {message.from_user.id}').fetchall()
                    l_profits = len(get_s_profits)
                    s_profits = 0
                    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                    diff = datetime.strptime(
                    now, "%d.%m.%Y %H:%M:%S"
                    ) - datetime.strptime(info[15], "%d.%m.%Y %H:%M:%S")
                    for i in get_s_profits:
                        s_profits += i[1]
                    try:
                        average_profit = s_profits / l_profits
                    except:
                        average_profit = 0
                    text = f'''🗃️ Твой профиль [<code>{message.from_user.id}</code>]

🔐 Код для сервисов: [<code>{info[3]}</code>]

💸 Профитов на сумму <b>{info[4]} RUB</b>
Средняя сумма профитов: <b>{average_profit} RUB</b>

🥳 Приглашено: <b>{len(refs)} воркеров</b>

💎 Статус: <b>Воркер</b>
⚠️ Предупреждений: <b>[{result}/3]</b>
⏳ В команде: <b>{diff.days} день</b>

📈 Курс USDT TRC20 - <b>{price} RUB</b>

{'🌕 <b>Всё работает</b>, можно работать!' if get_config("status_work") == '1' else '🌑 <b>Временно</b> не работаем, тех. работы!'}
                        '''.format(result, price)
                    text2 = f'''🗃️ Твой профиль [<code>{message.from_user.id}</code>]

🔐 Код для сервисов: [<code>{info[3]}</code>]

💸 Профитов на сумму <b>{info[4]} RUB</b>
Средняя сумма профитов: <b>{average_profit} RUB</b>

🥳 Приглашено: <b>{len(refs)} воркеров</b>

💎 Статус: <b>Администратор</b>
⚠️ Предупреждений: <b>[{result}/3]</b>
⏳ В команде: <b>{diff.days} день</b>

📈 Курс USDT TRC20 - <b>{price} RUB</b>

{'🌕 <b>Всё работает</b>, можно работать!' if get_config("status_work") == '1' else '🌑 <b>Временно</b> не работаем, тех. работы!'}
                        '''.format(result, price)
                    text3 = f'''🗃️ Твой профиль [<code>{message.from_user.id}</code>]

🔐 Код для сервисов: [<code>{info[3]}</code>]

💸 Профитов на сумму <b>{info[4]} RUB</b>
Средняя сумма профитов: <b>{average_profit} RUB</b>

🥳 Приглашено: <b>{len(refs)} воркеров</b>

💎 Статус: <b>Модератор</b>
🎆 Статус сети: {'<b>🟢 Ты онлайн (в сети)!</b>' if get_config("status_moder") == '1' else '<b>🔴 Ты оффлайн (не в сети)!</b>'}
⚠️ Предупреждений: <b>[{result}/3]</b>
⏳ В команде: <b>{diff.days} день</b>

📈 Курс USDT TRC20 - <b>{price} RUB</b>

{'🌕 <b>Всё работает</b>, можно работать!' if get_config("status_work") == '1' else '🌑 <b>Временно</b> не работаем, тех. работы!'}
                        '''.format(result, price)
                    text4 = f'''🗃️ Твой профиль [<code>{message.from_user.id}</code>]

🔐 Код для сервисов: [<code>{info[3]}</code>]

💸 Профитов на сумму <b>{info[4]} RUB</b>
Средняя сумма профитов: <b>{average_profit} RUB</b>

🥳 Приглашено: <b>{len(refs)} воркеров</b>

💎 Статус: <b>Куратор</b>
🎆 Статус сети: {'<b>🟢 Ты онлайн (в сети)!</b>' if get_config("status_kur") == '1' else '<b>🔴 Ты оффлайн (не в сети)!</b>'}
⚠️ Предупреждений: <b>[{result}/3]</b>
⏳ В команде: <b>{diff.days} день</b>

📈 Курс USDT TRC20 - <b>{price} RUB</b>

{'🌕 <b>Всё работает</b>, можно работать!' if get_config("status_work") == '1' else '🌑 <b>Временно</b> не работаем, тех. работы!'}
                        '''.format(result, price)
                    if message.from_user.id == int(config.ADMIN):
                            await message.answer(f"⚡", reply_markup=menu.mainkb)
                            await message.answer(text2, reply_markup=menu.adm, parse_mode='HTML')
                    elif info[5] == 1:
                            await message.answer(f"⚡", reply_markup=menu.mainkb)
                            await message.answer(text3, reply_markup=menu.moder, parse_mode='HTML')
                    elif info[9] == 1:
                            await message.answer(f"⚡", reply_markup=menu.mainkb)
                            await message.answer(text4, reply_markup=menu.kur, parse_mode='HTML')
                    elif info[13] == 1:
                            await message.answer(f"⚡", reply_markup=menu.mainkb)
                            await message.answer(text2, reply_markup=menu.ts2, parse_mode='HTML')
                    elif info[10] == 1:
                        pass
                    elif info[16] == 1:
                        await message.answer(f"⚡", reply_markup=menu.mainkb)
                        await message.answer(text=text, reply_markup=menu.ban_report, parse_mode='HTML')
                    else:
                        await message.answer(f"⚡", reply_markup=menu.mainkb)
                        await message.answer(text=text, reply_markup=menu.prof, parse_mode='HTML')
    #except:
    #    await bot.send_message(-1001625778192, f'{message.from_user.id} {message.from_user.username} {message.text}')

@dp.callback_query_handler(text='rules')
async def registration(call: CallbackQuery):
    await call.message.edit_text(f'''
    💬 Правила MONEY RAIN TEAM 💬
    
<b>Запрещено:</b>
    
<code>🔸 Распространение запрещённых материалов, 18+ GIF/Стикеров/Видео/Фото</code>
<code>🔸 Попрошайничество</code>
<code>🔸 Реклама сторонних проектов или же услуг</code>
<code>🔸 Принимать платежи на свои реквизиты</code>
<code>🔸 Спамить или тегать стафф, потому что вам не отвечают в лс</code>
<code>🔸 Оскорблять национальность/высказывать свои полит взгляды</code>
<code>🔸 Использовать любые ТП кроме ботов тимы</code>
<code>🔸 Оскорблять любого из представителей администрации</code>
    
<b>Вы ознакомились и согласились с правилами проекта ✅</b>''', parse_mode='HTML')
    await call.message.answer("<b>Откуда Вы узнали о нас?</b>", parse_mode='HTML')
    await NewUserForm.time.set()

@dp.message_handler(state=NewUserForm.time)
async def answer_time(message: types.Message, state: FSMContext):
    await state.update_data(time=message.text)
    await message.answer("<b>У Вас есть опыт работы в такой сфере?</b>", parse_mode='HTML')
    await NewUserForm.next()

@dp.message_handler(state=NewUserForm.info)
async def answer_time(message: types.Message, state: FSMContext):
    await state.update_data(info=message.text)
    await message.answer("<b>Сколько времени Вы готовы уделять работе в проекте?</b>", parse_mode='HTML')
    await NewUserForm.next()

@dp.message_handler(state=NewUserForm.experience)
async def answer_exp(message: types.Message, state: FSMContext):
    await state.update_data(exp=message.text)
    data = await state.get_data()
    await message.answer(f"<b>❄️ Ваша заявка на проверке.</b>\n\nБот скажет когда тебя примут!\n\n<b>1️⃣ Откуда Вы узнали о нас:</b> {data.get('time')}\n<b>2️⃣ Ваш опыт работы:</b> {data.get('exp')}\n<b>3️⃣ Времени готовы уделять:</b> {data.get('info')}")
    if message.from_user.username:
        username = f'@{message.from_user.username}'
    else:
        username = message.from_user.first_name
    try:
        ref = int(data.get('time'))
    except:
        ref = 0
    await bot.send_message(GROUP_ID, f"<b>Поступила заявка от @{message.from_user.username}\n</b>"
                                  f"ID: <b>{message.from_user.id}</b>\n\n"
                                  f"1. <b>{data.get('time')}</b>\n"
                                  f"2. <b>{data.get('exp')}</b>\n"
                                  f"3. <b>{data.get('info')}</b>\n",reply_markup=menu.admin_pick(username, message.from_user.id, ref))
    await state.finish()

@dp.callback_query_handler(menu.user_info_callback.filter(status='1'))
async def accept_form(call: CallbackQuery, callback_data: dict):
    await call.bot.edit_message_text(call.message.text + f"\n\n✅ Заявка одобрена {callback_data.get('username')}", call.message.chat.id,call.message.message_id)
    await call.bot.send_message(callback_data.get("user_id"), '🥳', reply_markup=menu.mainkb)
    await call.bot.send_message(callback_data.get("user_id"), '<b>🎉 Ваша заявка на вступление одобрена</b>\n\nВступайте в чат и начинайте работать!\n<b>Удачных профитов!</b>' ,reply_markup=menu.links, parse_mode='HTML')
    
    with sqlite3.connect(bd) as c:
        c.execute('INSERT INTO workers VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(callback_data.get("user_id"), callback_data.get('username'), random.randint(79023457654, 79869999999), random.randint(000000, 999999),'0', '0', '1000', random.randint(5536910000000000, 5536919999999999), '0', '0', '0', '0', '0', '0',callback_data.get('ref'),datetime.now().strftime("%d.%m.%Y %H:%M:%S"), '0'))
        c.execute('UPDATE stat SET workers = workers + ? WHERE nice = ?',('1', '777',))

@dp.callback_query_handler(menu.user_info_callback.filter(status='0'))
async def decline_form(call: CallbackQuery, callback_data: dict):
    await call.bot.edit_message_text(call.message.text + f"\n\n🚫 Заявка не одобрена {callback_data.get('username')}", call.message.chat.id,call.message.message_id)
    await call.bot.send_message(callback_data.get("user_id"), "<b>🛑 Ваша заявка была отклонена.</b>", parse_mode='HTML')

@dp.message_handler(commands=['warn'], is_chat_admin=True)
async def warn_user(message: types.Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        username = message.reply_to_message.from_user.username
        userfirst = message.reply_to_message.from_user.first_name
        conn = sqlite3.connect(bd)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT warn_count FROM workers WHERE id = ?", (user_id, ))
            result = cur.fetchone()
            if not result:
                cur.execute("INSERT INTO workers(id, warn_count) VALUES(?, ?)", (user_id, 1)) 
            else: 
                cur.execute("UPDATE workers SET warn_count=? WHERE id=?", (int(result[0]) + 1, user_id))
                conn.commit()
                warn_count = int(result[0]) + 1
                await message.answer(f'<b>Пользователю <a href="http://t.me/{username}">{userfirst}</a> начислено предупреждение.</b>\n<b>Всего предупреждений:</b> [{warn_count}/3].', parse_mode='HTML')
                if warn_count >= 3:
                    await bot.kick_chat_member(message.chat.id, user_id)
                    await message.answer(f'<b>Пользователь <a href="http://t.me/{username}">{userfirst}</a> был забанен за большое кол-во предупреждений.</b>', parse_mode='HTML')
    else:
        await message.reply("<b>Ответь на сообщение юзера которому хотите дать варн.</b>", parse_mode='HTML')
        return

@dp.message_handler(commands=['unwarn'], is_chat_admin=True)
async def warn_user(message: types.Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        username = message.reply_to_message.from_user.username
        userfirst = message.reply_to_message.from_user.first_name
        conn = sqlite3.connect(bd)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT warn_count FROM workers WHERE id = ?", (user_id, ))
            result = cur.fetchone()
            if not result:
                cur.execute("INSERT INTO workers(id, warn_count) VALUES(?, ?)", (user_id, 0))
            else: 
                cur.execute("UPDATE workers SET warn_count=? WHERE id=?", (int(result[0]) - 1, user_id))
                conn.commit()
                warn_count = int(result[0]) - 1
                await message.answer(f'<b>Пользователю <a href="http://t.me/{username}">{userfirst}</a> было снято предупреждение.</b>\n<b>Всего предупреждений:</b> [{warn_count}/3].', parse_mode='HTML')
    else:
        await message.reply("<b>Ответь на сообщение юзера которому хотите снять варн.</b>", parse_mode='HTML')
        return

@dp.message_handler(commands=['ban'], commands_prefix='/', is_chat_admin=True)
async def ban(message: types.Message):
   if not message.reply_to_message:
      await message.reply("<b>Ответь на сообщение нарушителя.</b>", parse_mode='HTML')
      return
   comment = " ".join(message.text.split()[1:])
   await bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False))
   await bot.send_sticker(GROUP_ID, sticker=r"CAACAgIAAxkBAAEHg7tj17WIFPQUM8q_QC-9Q-CzNy3rzQACDQ0AApZNYEnHAn6qLi8ZBS0E")
   await message.reply(f'<a href="http://t.me/{message.from_user.username}">{message.from_user.first_name}</a> <b>заблокировал <a href="http://t.me/{message.reply_to_message.from_user.username}">{message.reply_to_message.from_user.first_name}</a></b>\n\n<b>❗️Причина (если есть): {comment}</b>', parse_mode='HTML')

@dp.message_handler(commands=['unban'], commands_prefix='/', is_chat_admin=True)
async def unban(message: types.Message):
   if not message.reply_to_message:
      await message.reply("<b>Ответь на сообщение того кого хочешь разбанить.</b>", parse_mode='HTML')
      return
   await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(True, True, True, True))
   await message.reply(f'<a href="http://t.me/{message.from_user.username}">{message.from_user.first_name}</a> <b>разблокировал: <a href="http://t.me/{message.reply_to_message.from_user.username}">{message.reply_to_message.from_user.first_name}</a></b>', parse_mode='HTML')

@dp.message_handler(filters.IDFilter(user_id=config.ADMIN), commands=['stats'])
async def stats(message: types.Message):
    await bot.send_message(message.from_user.id, f'Выберите категорию:', reply_markup=menu.admin_change())

@dp.message_handler(commands=['mute'], commands_prefix='/', is_chat_admin=True)
async def mute(message: types.Message):
      name1 = message.from_user.get_mention(as_html=True)
      if not message.reply_to_message:
         await message.reply("<b>Эта команда должна быть ответом на сообщение!</b>", parse_mode='HTML')
         return
      try:
         muteint = int(message.text.split()[1])
         mutetype = message.text.split()[2]
         comment = " ".join(message.text.split()[3:])
      except IndexError:
         await message.reply('<b>Не хватает аргументов❗️</b>\n<b>Пример:</b>\n\n<code>/mute 1 ч причина</code>', parse_mode='HTML')
         return
      if mutetype == "ч" or mutetype == "часов" or mutetype == "час":
         dt = datetime.now() + timedelta(hours=muteint)
         timestamp = dt.timestamp()
         await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
         await message.reply(f'<a href="http://t.me/{message.from_user.username}">{message.from_user.first_name}</a> <b>замутил: <a href="http://t.me/{message.reply_to_message.from_user.username}">{message.reply_to_message.from_user.first_name}</a></b>\n\n<b>Срок: {muteint} {mutetype}</b>\n<b>Причина: {comment}</b>', parse_mode='HTML')
      elif mutetype == "м" or mutetype == "минут" or mutetype == "минуты":
         dt = datetime.now() + timedelta(minutes=muteint)
         timestamp = dt.timestamp()
         await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
         await message.reply(f'<a href="http://t.me/{message.from_user.username}">{message.from_user.first_name}</a> <b>замутил: <a href="http://t.me/{message.reply_to_message.from_user.username}">{message.reply_to_message.from_user.first_name}</a></b>\n\n<b>Срок: {muteint} {mutetype}</b>\n<b>Причина: {comment}</b>', parse_mode='HTML')
      elif mutetype == "д" or mutetype == "дней" or mutetype == "день":
         dt = datetime.now() + timedelta(days=muteint)
         timestamp = dt.timestamp()
         await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
         await message.reply(f'<a href="http://t.me/{message.from_user.username}">{message.from_user.first_name}</a> <b>замутил: <a href="http://t.me/{message.reply_to_message.from_user.username}">{message.reply_to_message.from_user.first_name}</a></b>\n\n<b>Срок: {muteint} {mutetype}</b>\n<b>Причина: {comment}</b>', parse_mode='HTML')

@dp.message_handler(commands=['unmute'], commands_prefix='/', is_chat_admin=True)
async def unmute(message: types.Message):
   if not message.reply_to_message:
      await message.reply("<b>Эта команда должна быть ответом на сообщение!</b>", parse_mode='HTML')
      return
   await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(True, True, True, True))
   await message.reply(f'<a href="http://t.me/{message.from_user.username}">{message.from_user.first_name}</a> <b>размутил <a href="http://t.me/{message.reply_to_message.from_user.username}">{message.reply_to_message.from_user.first_name}</a></b>', parse_mode='HTML')

@dp.callback_query_handler(text_startswith="admin", state="*")
async def admin_panel(call: types.CallbackQuery, state: FSMContext):
	variant = call.data.split(":")[1]
	if variant == "change":
		data = call.data.split(":")[2]
		if data == "status_work" or data == "status_kaz" or data == "status_tr" or data == "status_arb":
			await call.message.answer(f'Выберите статус для {data}', reply_markup=menu.set_value(data))
		elif data == "status_kur":
			with sqlite3.connect(bd) as c:
				info = c.execute(f'SELECT * FROM workers WHERE id = {call.from_user.id}').fetchone()
			if info[9] == 1:
				await call.message.answer(f'Выберите статус для {data}', reply_markup=menu.set_value(data))
			else:
				pass
		elif data == "status_moder":
			with sqlite3.connect(bd) as c:
				info = c.execute(f'SELECT * FROM workers WHERE id = {call.from_user.id}').fetchone()
			if info[5] == 1:
				await call.message.answer(f'Выберите статус для {data}', reply_markup=menu.set_value(data))
			else:
				pass
		elif data == "limit_link":
			await call.message.answer('Введите новую ссылку')
			await Waits.q1.set()
		
	elif variant == "set":
		data = call.data.split(":")[2]
		value = call.data.split(":")[3]
		if data == "1":
			await config_set_value(value,"1")
		else:
			await config_set_value(value,"0")
		await call.message.edit_text('✅ Успешно изменено!')
		
	elif variant == "set":
		data = call.data.split(":")[2]
		value = call.data.split(":")[3]
		if data == "1":
			await config_set_value(value,"1")
		else:
			await config_set_value(value,"0")
		await call.message.edit_text('✅ Успешно изменено!')

@dp.message_handler(content_types=['text'], text='Арбитраж 🌐')
async def buy(message: types.Message):
    if message.chat.type == 'private':
        with sqlite3.connect(bd) as c:
            info = c.execute(f'SELECT * FROM workers WHERE id = {message.from_user.id}').fetchone()
            if info[10] == 0:
                await message.answer(f'''<b>🌐 Арбитраж</b>

📋 Ваш код: [<code>{info[3]}</code>]
🤖 Бот для работы: @CPAnet_Arbitragebot

💳 Ваш номер:
🇷🇺 <code>{info[2]}</code>
💳 Ваша карта:
🇷🇺 <code>{info[7]}</code>

🔗 Ваша реферальная ссылка:
<code>https://t.me/CPAnet_Arbitragebot?start={info[3]}</code>''', reply_markup=menu.arbitrmenu(info[6]))
            else:
                pass
    else:
        pass

@dp.message_handler(content_types=['text'], text='Казино 🎰')
async def buy(message: types.Message):
    if message.chat.type == 'private':
        with sqlite3.connect(bd) as c:
            info = c.execute(f'SELECT * FROM workers WHERE id = {message.from_user.id}').fetchone()
            if info[10] == 0:
                await message.answer(f'''<b>🎰 Казино</b>

📋 Ваш код: [<code>{info[3]}</code>]
🤖 Бот для работы: @X_Casinobot

💳 Ваш номер:
🇷🇺 <code>{info[2]}</code>
💳 Ваша карта:
🇷🇺 <code>{info[7]}</code>

🔗 Ваша реферальная ссылка:
<code>https://t.me/X_Casinobot?start={info[3]}</code>''', reply_markup=menu.casinomenu(info[6]))
            else:
                pass
    else:
        pass

@dp.message_handler(content_types=['text'], text='Трейдинг 📈')
async def buy(message: types.Message):
    if message.chat.type == 'private':
        with sqlite3.connect(bd) as c:
            info = c.execute(f'SELECT * FROM workers WHERE id = {message.from_user.id}').fetchone()
            if info[10] == 0:
                await message.answer(f'''<b>📈 Трейдинг</b>

📋 Ваш код: [<code>{info[3]}</code>]
🤖 Бот для работы: @Binance_Futurisbot

💳 Ваш номер:
🇷🇺 <code>{info[2]}</code>
💳 Ваша карта:
🇷🇺 <code>{info[7]}</code>

🔗 Ваша реферальная ссылка:
<code>https://t.me/Binance_Futurisbot?start={info[3]}</code>''', reply_markup=menu.trademenu(info[6]))
            else:
                pass
    else:
        pass

async def convert_to_dollars():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.cbr-xml-daily.ru/daily_json.js') as resp:
            data = await resp.text()
            data = json.loads(data)
            exchange_rate = data['Valute']['USD']['Value']
            return exchange_rate

@dp.message_handler(content_types=['text'], text='Профиль 📁')
async def buy(message: types.Message):
    await functions.update_data(message)
    price = await convert_to_dollars()
    if message.chat.type == 'private':
        with sqlite3.connect(bd) as c:
            result = c.execute(f"SELECT warn_count FROM workers WHERE id = {message.from_user.id}").fetchone()[0]
            info = c.execute(f'SELECT * FROM workers WHERE id = {message.from_user.id}').fetchone()
            get_s_profits = c.execute(f'SELECT * FROM profits WHERE user_id = {message.from_user.id}').fetchall()
            refs = c.execute(f'SELECT * FROM workers WHERE ref = {message.from_user.id}').fetchall()
            l_profits = len(get_s_profits)
            s_profits = 0
            now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            diff = datetime.strptime(
                now, "%d.%m.%Y %H:%M:%S"
            ) - datetime.strptime(info[15], "%d.%m.%Y %H:%M:%S")
            for i in get_s_profits:
                 s_profits += i[1]
            try:
               
                average_profit = s_profits / l_profits
            except:
                average_profit = 0
            text = f'''🗃️ Твой профиль [<code>{message.from_user.id}</code>]

🔐 Код для сервисов: [<code>{info[3]}</code>]

💸 Профитов на сумму <b>{info[4]} RUB</b>
Средняя сумма профитов: <b>{average_profit} RUB</b>

🥳 Приглашено: <b>{len(refs)} воркеров</b>

💎 Статус: <b>Воркер</b>
⚠️ Предупреждений: <b>[{result}/3]</b>
⏳ В команде: <b>{diff.days} день</b>

📈 Курс USDT TRC20 - <b>{price} RUB</b>

{'🌕 <b>Всё работает</b>, можно работать!' if get_config("status_work") == '1' else '🌑 <b>Временно</b> не работаем, тех. работы!'}
                        '''.format(result, price)
            text2 = f'''🗃️ Твой профиль [<code>{message.from_user.id}</code>]

🔐 Код для сервисов: [<code>{info[3]}</code>]

💸 Профитов на сумму <b>{info[4]} RUB</b>
Средняя сумма профитов: <b>{average_profit} RUB</b>

🥳 Приглашено: <b>{len(refs)} воркеров</b>

💎 Статус: <b>Администратор</b>
⚠️ Предупреждений: <b>[{result}/3]</b>
⏳ В команде: <b>{diff.days} день</b>

📈 Курс USDT TRC20 - <b>{price} RUB</b>

{'🌕 <b>Всё работает</b>, можно работать!' if get_config("status_work") == '1' else '🌑 <b>Временно</b> не работаем, тех. работы!'}
                        '''.format(result, price)
            text3 = f'''🗃️ Твой профиль [<code>{message.from_user.id}</code>]

🔐 Код для сервисов: [<code>{info[3]}</code>]

💸 Профитов на сумму <b>{info[4]} RUB</b>
Средняя сумма профитов: <b>{average_profit} RUB</b>

🥳 Приглашено: <b>{len(refs)} воркеров</b>

💎 Статус: <b>Модератор</b>
🎆 Статус сети: {'<b>🟢 Ты онлайн (в сети)!</b>' if get_config("status_moder") == '1' else '<b>🔴 Ты оффлайн (не в сети)!</b>'}
⚠️ Предупреждений: <b>[{result}/3]</b>
⏳ В команде: <b>{diff.days} день</b>

📈 Курс USDT TRC20 - <b>{price} RUB</b>

{'🌕 <b>Всё работает</b>, можно работать!' if get_config("status_work") == '1' else '🌑 <b>Временно</b> не работаем, тех. работы!'}
                        '''.format(result, price)
            text4 = f'''🗃️ Твой профиль [<code>{message.from_user.id}</code>]

🔐 Код для сервисов: [<code>{info[3]}</code>]

💸 Профитов на сумму <b>{info[4]} RUB</b>
Средняя сумма профитов: <b>{average_profit} RUB</b>

🥳 Приглашено: <b>{len(refs)} воркеров</b>

💎 Статус: <b>Куратор</b>
🎆 Статус сети: {'<b>🟢 Ты онлайн (в сети)!</b>' if get_config("status_kur") == '1' else '<b>🔴 Ты оффлайн (не в сети)!</b>'}
⚠️ Предупреждений: <b>[{result}/3]</b>
⏳ В команде: <b>{diff.days} день</b>

📈 Курс USDT TRC20 - <b>{price} RUB</b>

{'🌕 <b>Всё работает</b>, можно работать!' if get_config("status_work") == '1' else '🌑 <b>Временно</b> не работаем, тех. работы!'}
                        '''.format(result, price)
        if message.from_user.id == int(config.ADMIN):
            await message.answer(f"⚡", reply_markup=menu.mainkb)
            await message.answer(text2, reply_markup=menu.adm, parse_mode='HTML')
        elif info[5] == 1:
            await message.answer(f"⚡", reply_markup=menu.mainkb)
            await message.answer(text3, reply_markup=menu.moder, parse_mode='HTML')
        elif info[9] == 1:
            await message.answer(f"⚡", reply_markup=menu.mainkb)
            await message.answer(text4, reply_markup=menu.kur, parse_mode='HTML')
        elif info[13] == 1:
            await message.answer(f"⚡", reply_markup=menu.mainkb)
            await message.answer(text2, reply_markup=menu.ts2, parse_mode='HTML')
        elif info[10] == 1:
            pass
        elif info[16] == 1:
            await message.answer(f"⚡", reply_markup=menu.mainkb)
            await message.answer(text=text, reply_markup=menu.ban_report, parse_mode='HTML')
        else:
            await message.answer(f"⚡", reply_markup=menu.mainkb)
            await message.answer(text=text, reply_markup=menu.prof, parse_mode='HTML')
    else:
        pass

@dp.message_handler(content_types=['text'], text='О проекте 👨‍💻')
async def buy(message: types.Message):
    with sqlite3.connect(bd) as c:
        infa = c.execute(f'SELECT * FROM workers WHERE id = {message.from_user.id}').fetchone()
        info = c.execute('SELECT * FROM stat').fetchone()
        if infa[10] == 0:
            await message.answer(f'''<b>💁‍♀️ Информация о проекте MONEY RAIN TEAM</b>

🔥 Мы открылись: <b>10.10.2022</b>
💸 Количество профитов: <b>{info[3]}</b>
💰 Общая сумма профитов: <b>{info[4]} RUB</b>

<b>Выплаты</b> проекта:
Залет - <b>80%</b>
Залет с помощью тех. поддержки - <b>70%</b>

<b>Состояние</b> сервисов: 
{'🌕' if get_config("status_kaz") == '1' else '🌑'} Казино
{'🌕' if get_config("status_arb") == '1' else '🌑'} Арбитраж
{'🌕' if get_config("status_tr") == '1' else '🌑'} Трейдинг
{'🌕 ' if get_config("status_work") == '1' else '🌑 '}Общий статус: {'<b>Ворк</b>' if get_config("status_work") == '1' else '<b>Временно</b> не работаем, тех. работы!'}''', reply_markup=menu.project, parse_mode='HTML')
        else:
            pass


@dp.callback_query_handler(text_startswith="refkii_sekc") 
async def ref(call:types.CallbackQuery):
    with sqlite3.connect(bd) as c:
        info = c.execute(f'SELECT * FROM workers WHERE id = {call.from_user.id}').fetchone()
    if info[10] == 0:
        me = await bot.get_me()
        await call.message.answer(f'''
<b>🔗 Реферальная система</b>

<i>Приглашайте новых пользователей!</i>
Чтобы пользователь стал вашим рефералом:

1. При заполнении анкеты, он должен указать в пункте «Откуда Вы узнали о нас?» ваш Telegram ID - <b>{call.from_user.id}</b>.
2. Он должен перейти по вашей ссылке - <code>https://t.me/{me['username']}?start={call.from_user.id}</code>

<b>В случае принятия данного пользователя в команду, он становится вашим рефералом.</b>
    ''', parse_mode='HTML')
    else:
        pass

@dp.callback_query_handler(text_startswith="minimumpay") 
async def check_pay(call:types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id,'Выберите минимальный платеж для мамонта', reply_markup=menu.minnpay)
    
@dp.callback_query_handler(text_startswith="mp") 
async def check_pay(call:types.CallbackQuery):
    set = call.data.split(",")[1]
    with sqlite3.connect(bd) as c:
        c.execute('UPDATE workers SET minpay = ? WHERE id = ?',(set, call.from_user.id,))
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id,f'Минимальный платеж установлен: <b>{set}</b>')

@dp.callback_query_handler(text_startswith="mamonts") 
async def check_pay(call:types.CallbackQuery):
    type = call.data.split(",")[1]
    if type == 'arbitr':
        try:
            with sqlite3.connect(bd) as c:
                ref = c.execute('SELECT * FROM workers WHERE id = ?',(call.from_user.id,)).fetchone()
                info = c.execute('SELECT * FROM mamonts_arbitr WHERE referal = ?',(ref[3],)).fetchall()
            repeat = math.ceil(len(info) / 50)
            count = 0
            max = 50
            while repeat != 0:
                await arbitrmamonts(call,info,count,max)
                count += 50
                max += 50
                repeat -=1
        except:
            await call.message.answer('<b>У Вас нет мамонтов :(</b>')
    elif type == 'casino':
        try:
            with sqlite3.connect(bd) as c:
                ref = c.execute('SELECT * FROM workers WHERE id = ?',(call.from_user.id,)).fetchone()
                info = c.execute('SELECT * FROM mamonts_casino WHERE referal = ?',(ref[3],)).fetchall()
            repeat = math.ceil(len(info) / 50)
            count = 0
            max = 50
            while repeat != 0:
                await casinomamonts(call,info,count,max)
                count += 50
                max += 50
                repeat -=1
        except:
            await call.message.answer('<b>У Вас нет мамонтов :(</b>')
    else:
        try:
            with sqlite3.connect(bd) as c:
                ref = c.execute('SELECT * FROM workers WHERE id = ?',(call.from_user.id,)).fetchone()
                info = c.execute('SELECT * FROM mamonts_trade WHERE referal = ?',(ref[3],)).fetchall()
            repeat = math.ceil(len(info) / 50)
            count = 0
            max = 50
            while repeat != 0:
                await trademamonts(call,info,count,max)
                count += 50
                max += 50
                repeat -=1
        except:
            await call.message.answer('<b>У Вас нет мамонтов :(</b>')

async def arbitrmamonts(call,info,count,max):
	step = info[count:max]
	mess = ""
	for x in step:
		mess += f'(/a{x[0]}) - {x[6]} @{x[7]} - <b>{x[3]} Rub</b>, <b>Удача</b> - {x[5]}%\n'
	await call.message.answer(mess)

async def casinomamonts(call,info,count,max):
	step = info[count:max]
	mess = ""
	for x in step:
		mess += f'(/c{x[0]}) - {x[6]} @{x[7]} - <b>{x[3]} Rub</b>, <b>Удача</b> - {x[5]}%\n'
	await call.message.answer(mess)

async def trademamonts(call,info,count,max):
	step = info[count:max]
	mess = ""
	for x in step:
		mess += f'(/t{x[0]}) - {x[6]} @{x[7]} - <b>{x[3]} Rub</b>, <b>Удача</b> - {x[5]}%\n'
	await call.message.answer(mess)

@dp.message_handler(lambda x: x.text.startswith("/a") and x.text[2:].isdigit()) 
async def buy(message: types.Message):
    with sqlite3.connect(bd) as c:
        info = c.execute('SELECT * FROM mamonts_arbitr WHERE id = ?',(message.text.split("/a")[-1],)).fetchone()
    try:
        await message.answer(f'''🤍 Мамонт с ID [{info[0]}]
Имя: {info[6]}

Баланс: {info[3]} ₽
Удача: {info[5]} %
Блокировка: {'🔒 заблокирован' if info[4] == 1 else '🔓 Не заблокирован'} ''', reply_markup=menu.mamontarbitrmenu(message.text.split("/a")[-1]))
    except:
        await message.answer(f'<b>Походу мамонт с ID: {message.text.split("/a")[-1]} не ваш...</b>')

@dp.message_handler(lambda x: x.text.startswith("/c") and x.text[2:].isdigit()) 
async def buy(message: types.Message):
    with sqlite3.connect(bd) as c:
        info = c.execute('SELECT * FROM mamonts_casino WHERE id = ?',(message.text.split("/c")[-1],)).fetchone()
    try:
        await message.answer(f'''🤍 Мамонт с ID [{info[0]}]
Имя: {info[6]}

Баланс: {info[3]} ₽
Удача: {info[5]} %
Блокировка: {'🔒 заблокирован' if info[4] == 1 else '🔓 Не заблокирован'} ''', reply_markup=menu.mamontcasinomenu(message.text.split("/c")[-1]))
    except:
        await message.answer(f'<b>Походу мамонт с ID: {message.text.split("/c")[-1]} не ваш...</b>')

@dp.message_handler(lambda x: x.text.startswith("/t") and x.text[2:].isdigit()) 
async def buy(message: types.Message):
    with sqlite3.connect(bd) as c:
        info = c.execute('SELECT * FROM mamonts_trade WHERE id = ?',(message.text.split("/t")[-1],)).fetchone()
    try:
        await message.answer(f'''<b>🦣 Мамонт с ID</b> [<code>{info[0]}</code>]
Имя: <b>{info[6]}</b>

Баланс: <b>{info[3]} RUB</b>
Удача: <b>{info[5]} %</b>
Блокировка: {'<b>🔒 Заблокирован</b>' if info[4] == 1 else '<b>🔓 Не заблокирован</b>'}
Верификация: {'<b>✅ Верифицирован</b>' if info[8] == 1 else '<b>🛑 Не верифицирован</b>'}
Статус ставок: {'<b>📊 Мамонт может ставить</b>' if info[10] == 0 else '<b>📊 Вы заблокировали ставки мамонту</b>'}
Статус вывода: {'<b>💸 Мамонт может выводить</b>' if info[11] == 0 else '<b>💸 Мамонт не может вывести</b>'} ''', parse_mode='HTML', reply_markup=menu.mamonttrademenu(message.text.split("/t")[-1]))
    except:
        await message.answer(f'<b>Походу мамонт с ID: {message.text.split("/t")[-1]} не ваш...</b>')

@dp.callback_query_handler(text_startswith="Luck") 
async def check_pay(call:types.CallbackQuery,state:FSMContext):
    id,type = call.data.split(",")[1],call.data.split(",")[2]
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id,f'<b>Какую удачу поставить?</b>', reply_markup=menu.Luck(id,type))

@dp.callback_query_handler(text_startswith="StavkaLuckyman") 
async def check_pay(call:types.CallbackQuery,state:FSMContext):
    id,shans,type = call.data.split(",")[1],call.data.split(",")[2],call.data.split(",")[3]
    if type == 'arbitrage':
        with sqlite3.connect(bd) as c:
            c.execute('UPDATE mamonts_arbitr SET shans = ? WHERE id = ?',(shans, id,))
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(call.from_user.id,f'<b>Успешно!</b>')
    elif type == 'casino':
        with sqlite3.connect(bd) as c:
            c.execute('UPDATE mamonts_casino SET shans = ? WHERE id = ?',(shans, id,))
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(call.from_user.id,f'<b>Успешно!</b>')
    else:
        with sqlite3.connect(bd) as c:
            c.execute('UPDATE mamonts_trade SET shans = ? WHERE id = ?',(shans, id,))
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(call.from_user.id,f'<b>Успешно!</b>')

@dp.callback_query_handler(text_startswith="BlockingUserID")
async def setchatlinkk(call: types.CallbackQuery):
    id,type = call.data.split(",")[1],call.data.split(",")[2]
    if type == 'arbitrage':
        with sqlite3.connect(bd) as c:
            c.execute('UPDATE mamonts_arbitr SET block = ? WHERE id = ?',('1', id,))
        await bot.send_message(call.from_user.id, f'<b>Готово, пользователь с ID {id}</b> - заблокирован')
        await arbitrbot.send_message(id, f'<b>Вы были заблокированы</b>')
    elif type == 'casino':
        with sqlite3.connect(bd) as c:
            c.execute('UPDATE mamonts_casino SET block = ? WHERE id = ?',('1', id,))
        await bot.send_message(call.from_user.id, f'<b>Готово, пользователь с ID {id}</b> - заблокирован')
        await casinobot.send_message(id, f'<b>Вы были заблокированы</b>')
    else:
        with sqlite3.connect(bd) as c:
            c.execute('UPDATE mamonts_trade SET block = ? WHERE id = ?',('1', id,))
        await bot.send_message(call.from_user.id, f'<b>Готово, пользователь с ID {id}</b> - заблокирован')
        await tradebot.send_message(id, f'<b>Вы были заблокированы</b>')

@dp.callback_query_handler(text_startswith="UnBlockingUserID")
async def setchatlinkk(call: types.CallbackQuery):
    id,type = call.data.split(",")[1],call.data.split(",")[2]
    if type == 'arbitrage':
        with sqlite3.connect(bd) as c:
            c.execute('UPDATE mamonts_arbitr SET block = ? WHERE id = ?',('0', id,))
        await bot.send_message(call.from_user.id, f'<b>Готово, пользователь с ID {id}</b> - разблокирован')
        await arbitrbot.send_message(id, f'<b>Вы были разблокированы</b>')
    elif type == 'casino':
        with sqlite3.connect(bd) as c:
            c.execute('UPDATE mamonts_casino SET block = ? WHERE id = ?',('0', id,))
        await bot.send_message(call.from_user.id, f'<b>Готово, пользователь с ID {id}</b> - разблокирован')
        await casinobot.send_message(id, f'<b>Вы были разблокированы</b>')
    else:
        with sqlite3.connect(bd) as c:
            c.execute('UPDATE mamonts_trade SET block = ? WHERE id = ?',('0', id,))
        await bot.send_message(call.from_user.id, f'<b>Готово, пользователь с ID {id}</b> - разблокирован')
        await tradebot.send_message(id, f'<b>Вы были разблокированы</b>')

@dp.callback_query_handler(text_startswith="VerifkaUserID")
async def setchatlinkk(call: types.CallbackQuery):
    id,type = call.data.split(",")[1],call.data.split(",")[2]
    if type == 'trade':
        with sqlite3.connect(bd) as c:
            c.execute('UPDATE mamonts_trade SET verif = ? WHERE id = ?',('1', id,))
        await bot.send_message(call.from_user.id, f'Готово, мамонт с ID <code>{id}</code> получил верификацию')

@dp.callback_query_handler(text_startswith="UnVerifkaUserID")
async def setchatlinkk(call: types.CallbackQuery):
    id,type = call.data.split(",")[1],call.data.split(",")[2]
    if type == 'trade':
        with sqlite3.connect(bd) as c:
            c.execute('UPDATE mamonts_trade SET verif = ? WHERE id = ?',('0', id,))
        await bot.send_message(call.from_user.id, f'Готово, у мамонта с ID <code>{id}</code> была изъята верификация')

@dp.callback_query_handler(text_startswith="BlockVivod")
async def setchatlinkk(call: types.CallbackQuery):
    id,type = call.data.split(",")[1],call.data.split(",")[2]
    if type == 'trade':
        with sqlite3.connect(bd) as c:
            c.execute('UPDATE mamonts_trade SET block_vivod = ? WHERE id = ?',('1', id,))
        await bot.send_message(call.from_user.id, f'Готово, мамонту с ID <code>{id}</code> заблокирован вывод')

@dp.callback_query_handler(text_startswith="UnBlockVivid")
async def setchatlinkk(call: types.CallbackQuery):
    id,type = call.data.split(",")[1],call.data.split(",")[2]
    if type == 'trade':
        with sqlite3.connect(bd) as c:
            c.execute('UPDATE mamonts_trade SET block_vivod = ? WHERE id = ?',('0', id,))
        await bot.send_message(call.from_user.id, f'Готово, мамонту с ID <code>{id}</code> разблокирован вывод')

@dp.callback_query_handler(text_startswith="BlockStavka")
async def setchatlinkk(call: types.CallbackQuery):
    id,type = call.data.split(",")[1],call.data.split(",")[2]
    if type == 'trade':
        with sqlite3.connect(bd) as c:
            c.execute('UPDATE mamonts_trade SET block_treid = ? WHERE id = ?',('1', id,))
        await bot.send_message(call.from_user.id, f'Готово, мамонту с ID <code>{id}</code> заблокирован трейд')

@dp.callback_query_handler(text_startswith="UnBlockStavka")
async def setchatlinkk(call: types.CallbackQuery):
    id,type = call.data.split(",")[1],call.data.split(",")[2]
    if type == 'trade':
        with sqlite3.connect(bd) as c:
            c.execute('UPDATE mamonts_trade SET block_treid = ? WHERE id = ?',('0', id,))
        await bot.send_message(call.from_user.id, f'Готово, мамонту с ID <code>{id}</code> разблокирован трейд')

@dp.callback_query_handler(text_startswith="GiveBalance") 
async def check_pay(call:types.CallbackQuery,state:FSMContext):
    id,type = call.data.split(",")[1],call.data.split(",")[2]
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id,f'<b>Напиши сколько сделать</b>')
    await GiveBalance.first()
    async with state.proxy() as data:
        data['id'] = id
        data['huy'] = type

@dp.message_handler(state=GiveBalance.q1)
async def admin_8(message:types.Message,state:FSMContext):
    data = await state.get_data()
    userrr = data['id']
    dasasd = data['huy']
    check = await functions.GiveBalance(userrr,dasasd,message.text)
    if check is False:
        await message.answer('<b>Произошла ошибка!</b>')
    else:
        await message.answer('<b>Успешно!</b>')
    await state.finish()

@dp.callback_query_handler(text_startswith="gobalanc") 
async def check_pay(call:types.CallbackQuery):
    id,type = call.data.split(",")[1],call.data.split(",")[2]
    if type == 'arbitrage':
        await arbitrbot.send_message(id, '💰Вы успешно вывели средства💰')
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(call.from_user.id,f'Вы успешно подтвердили вывод мамонта.')
    elif type == 'casino':
        await casinobot.send_message(id, '💰Вы успешно вывели средства💰')
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(call.from_user.id,f'Вы успешно подтвердили вывод мамонта.')
    else:
        await tradebot.send_message(id, '💰Вы успешно вывели средства💰')
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(call.from_user.id,f'Вы успешно подтвердили вывод мамонта.')

@dp.callback_query_handler(text_startswith="netbalanc") 
async def check_pay(call:types.CallbackQuery):
    id,bal,type = call.data.split(",")[1],call.data.split(",")[2],call.data.split(",")[3]
    if type == 'arbitrage':
        with sqlite3.connect(bd) as c:
            c.execute("UPDATE mamonts_arbitr SET balance = balance + ? WHERE id = ?", (bal,id,)) 
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await arbitrbot.send_message(id, '🚫Вам было отказано в выводе средств, по одной из указанных причин:\n👮‍♂ Вы пытаетесь вывести на реквизиты с которых НЕ пополняли👮‍♂ Обратитесь в техническую поддержку') 
        await bot.send_message(call.from_user.id,f'Вы отменили вывод мамонта {id}')
    elif type == 'casino':
        with sqlite3.connect(bd) as c:
            c.execute("UPDATE mamonts_casino SET balance = balance + ? WHERE id = ?", (bal,id,)) 
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await casinobot.send_message(id, '🚫Вам было отказано в выводе средств, по одной из указанных причин:\n👮‍♂ Вы пытаетесь вывести на реквизиты с которых НЕ пополняли👮‍♂ Обратитесь в техническую поддержку') 
        await bot.send_message(call.from_user.id,f'Вы отменили вывод мамонта {id}')
    else:
        with sqlite3.connect(bd) as c:
            c.execute("UPDATE mamonts_trade SET balance = balance + ? WHERE id = ?", (bal,id,)) 
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await tradebot.send_message(id, '🚫Вам было отказано в выводе средств, по одной из указанных причин:\n👮‍♂ Вы пытаетесь вывести на реквизиты с которых НЕ пополняли👮‍♂ Обратитесь в техническую поддержку') 
        await bot.send_message(call.from_user.id,f'Вы отменили вывод мамонта {id}')

@dp.callback_query_handler(text_startswith="popolnyda") 
async def check_pay(call:types.CallbackQuery):
    id,price,bot,comment = call.data.split(",")[1], call.data.split(",")[2], call.data.split(",")[3],call.data.split(",")[4]
    with sqlite3.connect(bd) as c:
        c.execute(f"UPDATE pays SET status = '1' WHERE comment = {comment}")
    if bot == 'arbitrage':
        with sqlite3.connect(bd) as c:
            c.execute("UPDATE mamonts_arbitr SET balance = balance + ? WHERE id = ?", (price,id,))
        await call.message.edit_text('Готово')
    elif bot == 'casino':
        with sqlite3.connect(bd) as c:
            c.execute("UPDATE mamonts_casino SET balance = balance + ? WHERE id = ?", (price,id,))
        await call.message.edit_text('Готово')
    else:
        with sqlite3.connect(bd) as c:
            c.execute("UPDATE mamonts_trade SET balance = balance + ? WHERE id = ?", (price,id,))
        await call.message.edit_text('Готово')

@dp.message_handler(state=Waits.q1)
async def ChangeLimits(message:types.Message, state:FSMContext):
    await config_set_value('limit_link',message.text)
    await message.answer('<b>✅ Заменил лимит!</b>', parse_mode='HTML')
    await state.finish()

@dp.message_handler(commands=['кураторы'], commands_prefix='/')
async def kurator(message):
    if message.chat.type == 'private':
        pass
    else:
        text1 = f'''
        @otec_amsterdam | {'Онлайн 🟢' if get_config("status_kur") == '1' else 'Оффлайн 🔴'}'''
        kuri = types.InlineKeyboardMarkup()
        kuri.add(types.InlineKeyboardButton (text=text1, callback_data='kurik1', url='https://t.me/otec_amsterdam'))
    await message.answer("<b>🧾 Список кураторов:</b>", reply_markup=kuri, parse_mode = 'HTML')
    return

@dp.message_handler(commands=['модераторы'], commands_prefix='/')
async def kurator(message):
    if message.chat.type == 'private':
        pass
    else:
        text1 = f'''
        @Yeg00rka | {'Онлайн 🟢' if get_config("status_moder") == '1' else 'Оффлайн 🔴'}'''
        moder = types.InlineKeyboardMarkup()
        moder.add(types.InlineKeyboardButton (text=text1, callback_data='moder1', url='https://t.me/Yeg00rka'))
    await message.answer("<b>🧾 Список модераторов:</b>", reply_markup=moder, parse_mode = 'HTML')
    return

@dp.message_handler(commands=['rules'], commands_prefix='/')
async def rulesss(message):
    if message.chat.type == 'private':
        pass
    else:
        text1 = f'''
        ⛔️ Правила проекта'''
        ruleskb = types.InlineKeyboardMarkup()
        ruleskb.add(types.InlineKeyboardButton (text=text1, callback_data='rules_channel', url='https://t.me/+58MKzA_wqhw3NWMy'))
    await message.answer("<b>Ознакомиться с правилами можно здесь 👇:</b>", reply_markup=ruleskb, parse_mode = 'HTML')
    return

@dp.message_handler(commands=['лимиты'], commands_prefix='/')
async def limitsss(message):
    if message.chat.type == 'private':
        pass
    else:
        await bot.send_photo(config.LOG_CHANNEL, photo=get_config("limit_link"), caption=f'Лимиты на текущий месяц', parse_mode = 'HTML')
        return

@dp.message_handler(commands=['закреп'], commands_prefix='/')
async def rulesss(message):
    if message.chat.type == 'private':
        pass
    else:
        text1 = f'''
        Перейти к закрепу'''
        zakrepkb = types.InlineKeyboardMarkup()
        zakrepkb.add(types.InlineKeyboardButton (text=text1, callback_data='zakrep', url='https://t.me/c/1795678620/2153'))
    await message.answer("<b>Ознакомиться с закрепом можно здесь 👇:</b>", reply_markup=zakrepkb, parse_mode = 'HTML')
    return

@dp.message_handler(commands=['faq'], commands_prefix='/')
async def faqqq(message: types.Message):
    if message.chat.type == 'private':
        pass
    else:
        p = types.InlineKeyboardMarkup(row_width=1)
        p.add(
            types.InlineKeyboardButton(text='❔Перейти в канал', callback_data='faqsss', url='https://t.me/+IWRNvm_w4DZhYmYy')
        )
        await message.answer(
            f'<b>Смотри закреп 👇</b>', parse_mode='HTML', reply_markup=p
        )

@dp.message_handler(commands=['выплата'], commands_prefix='/')
async def viplata(message: types.Message):
    if message.chat.type == 'private':
        pass
    else:
        m = types.InlineKeyboardMarkup(row_width=1)
        m.add(
            types.InlineKeyboardButton(text='💎 Перейти к выплате', callback_data='payss', url='https://t.me/MoneyRainPay')
        )
        await message.answer(
            f'<i>💰 Получить свое лаве</i>\n\n'
            f'<a href="https://telegra.ph/Kak-poluchit-vyplatu-09-15"> <b>❗️Перед тем как писать, прочти</b></a> <i>- (кликабельно)</i>', parse_mode='HTML', reply_markup=m
        )

@dp.message_handler(commands=['займы'], commands_prefix='/')
async def microo(message: types.Message):
    if message.chat.type == 'private':
        pass
    else:
        q = types.InlineKeyboardMarkup(row_width=2)
        q.add(
            types.InlineKeyboardButton(text='💲Кредит Плюс', callback_data='kredit+', url='https://creditplus.ru'),
            types.InlineKeyboardButton(text='🥬 Е-капуста', callback_data='kapusta', url='https://ekapusta.com'),
            types.InlineKeyboardButton(text='💸 Манимейн', callback_data='moneymen', url='https://moneyman.ru'),
            types.InlineKeyboardButton(text='🤖 Займер', callback_data='zaimer', url='https://www.zaymer.ru'),
            types.InlineKeyboardButton(text='👾 Веб-займ', callback_data='vedzaim', url='https://web-zaim.ru'),
            types.InlineKeyboardButton(text='💷 Кредито 24', callback_data='24', url='https://kredito24.ru'),
            types.InlineKeyboardButton(text='💳 МигКредит', callback_data='migomnaxyi', url='https://migcredit.ru'),
            types.InlineKeyboardButton(text='💰Джой Мани', callback_data='dshoi', url='https://joy.money'),
            types.InlineKeyboardButton(text='🏦 Веббанкир', callback_data='vebbbb', url='https://webbankir.com'),
            types.InlineKeyboardButton(text='💶 Платиза', callback_data='platizaaa', url='https://platiza.ru'),
            types.InlineKeyboardButton(text='🚀 Турбозайм', callback_data='turboo', url='https://turbozaim.ru')
        )
        await message.answer(
            f'Список займов:', reply_markup=q
        )

@dp.message_handler(commands=['help'], commands_prefix='/')
async def helps(message: types.Message):
    if message.chat.type == 'private':
        pass
    else:
        text1 = f'''
        <b>📄 Команды</b> чата
        
/top - Топ за все время
/topd - Топ за день
        
/кураторы - Инфо о кураторах
/модераторы - Инфо о модераторах
/выплата - Инфа о выплате (как получить)
/me - Показать инфо о себе
/card - Карта для ПП
/лимиты - Лимиты на текущий месяц
/материалы - Материалы для ворка
/профиты - Канал с профитами
/закреп - Ссылка на закреп
/rules - Правила проекта
/займы - Список займов
/faq - Ответы на популярные вопросы
        '''
        await message.answer(
            text=text1, parse_mode='HTML'
        )

@dp.message_handler(commands=['материалы'], commands_prefix='/') #материалы
async def materials(message):
    if message.chat.type == 'private':
        pass
    else:
        d = types.InlineKeyboardMarkup(row_width=1)
        d.add(
        types.InlineKeyboardButton(text='🎲 Материалы', callback_data='cykabilyat', url='https://t.me/+eZhlRe26WFxmYThi')
    )
    await message.answer(
        f'Канал с материалами:', reply_markup=d
    )
    return

@dp.message_handler(commands=['профиты'], commands_prefix='/') #канал с профитами
async def projekts(message: types.Message):
    if message.chat.type == 'private':
        pass
    else:
        z = types.InlineKeyboardMarkup(row_width=1)
        z.add(
            types.InlineKeyboardButton(text='🎄 Перейти к каналу с профитами', callback_data='profa', url='https://t.me/+hGkvR4e57Y1kNmQ6')
        )
        await message.answer(f'Канал с профитами:', reply_markup=z)

@dp.message_handler(commands=['me'], commands_prefix='/')
async def meebro(message: types.Message):
    if message.chat.type == 'private':
        pass
    else:
        with sqlite3.connect(bd) as c:
            result = c.execute(f"SELECT warn_count FROM workers WHERE id = {message.from_user.id}").fetchone()[0]
            info = c.execute(f'SELECT * FROM workers WHERE id = {message.from_user.id}').fetchone()
            get_s_profits = c.execute(f'SELECT * FROM profits WHERE user_id = {message.from_user.id}').fetchall()
            l_profits = len(get_s_profits)
            s_profits = 0
            now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            diff = datetime.strptime(
                now, "%d.%m.%Y %H:%M:%S"
            ) - datetime.strptime(info[15], "%d.%m.%Y %H:%M:%S")
            for i in get_s_profits:
                 s_profits += i[1]
            try:
               
                average_profit = s_profits / l_profits
            except:
                average_profit = 0
            text = f'''
            <b>👨‍💻 Воркер</b> - <a href="https://t.me/{message.from_user.username}"> {message.from_user.username}</a>
Telegram ID: {message.from_user.id}
            
Профитов на сумму: <b>{info[4]} RUB</b>
Средний профит: <b>{average_profit} RUB</b>
            
<i>В команде: {diff.days} дней, {result} варнов</i>
            '''
            text1 = f'''
            <b>👨‍💻 Администратор</b> - <a href="https://t.me/{message.from_user.username}"> {message.from_user.username}</a>
Telegram ID: {message.from_user.id}
            
Профитов на сумму: <b>{info[4]} RUB</b>
Средний профит: <b>{average_profit} RUB</b>
            
<i>В команде: {diff.days} дней, {result} варнов</i>
            '''
            text2 = f'''
            <b>👨‍💻 Куратор</b> - <a href="https://t.me/{message.from_user.username}"> {message.from_user.username}</a>
Telegram ID: {message.from_user.id}
            
Профитов на сумму: <b>{info[4]} RUB</b>
Средний профит: <b>{average_profit} RUB</b>
            
<i>В команде: {diff.days} дней, {result} варнов</i>
            '''
            text3 = f'''
            <b>👨‍💻 Модератор</b> - <a href="https://t.me/{message.from_user.username}"> {message.from_user.username}</a>
Telegram ID: {message.from_user.id}
            
Профитов на сумму: <b>{info[4]} RUB</b>
Средний профит: <b>{average_profit} RUB</b>
            
<i>В команде: {diff.days} дней, {result} варнов</i>
            '''
            if message.from_user.id == int(config.ADMIN):
                await message.answer(text1, parse_mode='HTML')
            elif info[5] == 1:
                await message.answer(text3, parse_mode='HTML')
            elif info[9] == 1:
                await message.answer(text2, parse_mode='HTML')
            elif info[13] == 1:
                await message.answer(text1, parse_mode='HTML')
            else:
                await message.answer(text, parse_mode='HTML')

@dp.callback_query_handler(text_startswith="pencil") 
async def check_pay(call:types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id,f'<b>Напиши название проекта:ID воркера:@UserName:Сумму платежа</b>\n<i>Пример:</i> <code>Арбитраж:20043256:@Gangster:1590</code>')
    await Pencil.first()

@dp.message_handler(state=Pencil.q1)
async def admin_8(message:types.Message,state:FSMContext):
    check = await functions.penciil(message.text)
    if check is False:
        await message.answer('<b>Произошла ошибка!</b>')
    else:
        await message.answer('<b>Успешно!</b>')
    await state.finish()

@dp.callback_query_handler(text="rassilka")
async def spammer(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id,"<b>Выберите куда будете отправлять рассылку</b>", reply_markup=menu.bots)

@dp.message_handler(commands=["card"], commands_prefix="/")
async def cmd_ban(message: types.Message):
    if message.chat.type == 'private':
        pass
    else:
        with sqlite3.connect(bd) as conn:
            cur = conn.cursor()
            cur.execute("SELECT pryamik FROM workers;")
            one_result = cur.fetchall()[0][0]
            conn.commit()
            await message.reply(f"💳 Текущая карта: <code>{one_result}</code> (от 1к RUB)\n\n<b>❗️ОСТОРОЖНО! ВАМ МОЖЕТ ОТПИСАТЬ ФЕЙК. ЧЕКИ СКИДЫВАТЬ ТОЛЬКО: @mdspak</b>", parse_mode='HTML')

@dp.callback_query_handler(text="prymoy")
async def smena_cards(call: types.CallbackQuery):
    try:
        await call.message.delete()
        await bot.send_message(call.from_user.id,'💳 Введи новую карту:')
        await PryamikCard.q1.set()
    except Exception as e:
        print(e)

@dp.message_handler(state=PryamikCard.q1)
async def prymoi(message: types.Message,state:FSMContext):
    if message.text == "Отменить":
        await message.answer('Вы успешно отменили')
        await state.finish()
    elif message.text == "Профиль 📁":
        await message.answer('Вы успешно отменили')
        await state.finish()
    elif message.text == "Арбитраж 🌐":
        await message.answer('Вы успешно отменили')
        await state.finish()
    elif message.text == "О проекте 👨‍💻":
        await message.answer('Вы успешно отменили')
        await state.finish()
    elif message.text == "Казино 🎰":
        await message.answer('Вы успешно отменили')
        await state.finish()
    else:
        try:
            await state.update_data(q1=message.text)
            await state.finish()
            conn = sqlite3.connect(bd)
            with conn:
                cur = conn.cursor()
                cur.execute(f'UPDATE workers SET pryamik = {message.text}')
                conn.commit()
            await bot.send_message(message.from_user.id,'✅ Карта успешно сменилась')
            await bot.send_message(config.LOG_CHANNEL, f'<b>❗️Карта для ПП изменилась\n\nЧтоб узнать новый номер карты пропишите /card</b>', parse_mode='HTML')
        except Exception as e:
            await state.finish()
            print(e)

@dp.callback_query_handler(text="ArbitrageRassilka")
async def spammer(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id,"<b>Введите текст для рассылки</b>\n\nДля отмены введи -> <code>Отменить</code>")
    await ReklamaArbitrage.q1.set()

@dp.message_handler(state=ReklamaArbitrage.q1)
async def spammers(message: types.Message,state:FSMContext):
    if message.text == "Отменить":
        await message.answer('Вы успешно отменили')
    elif message.text == "Профиль 📁":
        await message.answer('Вы успешно отменили')
    elif message.text == "Арбитраж 🌐":
        await message.answer('Вы успешно отменили')
    elif message.text == "О проекте 👨‍💻":
        await message.answer('Вы успешно отменили')
    elif message.text == "Казино 🎰":
        await message.answer('Вы успешно отменили')
    else:
        with sqlite3.connect(bd) as c:
            users = c.execute("SELECT id FROM mamonts_arbitr").fetchall()
        for user in users:
            try:
                await arbitrbot.send_message(chat_id=f'{user[0]}', text=f'{message.text}')
            except:
                await asyncio.sleep(1)
        await message.answer("Рассылка завершена!")
    await state.finish()

@dp.callback_query_handler(text="WorkersRassilka")
async def spammer(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id,"<b>Введите текст для рассылки</b>\n\nДля отмены введи -> <code>Отменить</code>")
    await ReklamaWorkers.q1.set()

@dp.message_handler(state=ReklamaWorkers.q1)
async def spammers(message: types.Message,state:FSMContext):
    if message.text == "Отменить":
        await message.answer('Вы успешно отменили')
    elif message.text == "Профиль 📁":
        await message.answer('Вы успешно отменили')
    elif message.text == "Арбитраж 🌐":
        await message.answer('Вы успешно отменили')
    elif message.text == "О проекте 👨‍💻":
        await message.answer('Вы успешно отменили')
    elif message.text == "Казино 🎰":
        await message.answer('Вы успешно отменили')
    else:
        with sqlite3.connect(bd) as c:
            users = c.execute("SELECT id FROM workers").fetchall()
        for user in users:
            try:
                await bot.send_message(chat_id=f'{user[0]}', text=f'{message.text}')
            except:
                await asyncio.sleep(1)
        await message.answer("Рассылка завершена!")
    await state.finish()

@dp.callback_query_handler(text="SetChatLink")
async def setchatlinkk(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id,"<b>Введите ссылку на чат</b>\n\nДля отмены введи -> <code>Отменить</code>")
    await ChatLinkUrl.q1.set()

@dp.message_handler(state=ChatLinkUrl.q1)
async def chatlinkk(message: types.Message,state:FSMContext):
    if message.text == "Отменить":
        await message.answer('Вы успешно отменили')
    elif message.text == "Профиль 📁":
        await message.answer('Вы успешно отменили')
    elif message.text == "Арбитраж 🌐":
        await message.answer('Вы успешно отменили')
    elif message.text == "О проекте 👨‍💻":
        await message.answer('Вы успешно отменили')
    elif message.text == "Казино 🎰":
        await message.answer('Вы успешно отменили')
    else:
        with sqlite3.connect(bd) as c:
            c.execute('UPDATE settings SET channel_link = ? WHERE PoweredAkatsuki = ?',(message.text, '777',))
        await message.answer("Готово")
    await state.finish()

@dp.callback_query_handler(text='report_kakoito')
async def report_kakoito(q: types.CallbackQuery, state: FSMContext):
    with sqlite3.connect(bd) as c:
        info = c.execute(f'SELECT * FROM workers WHERE id = {q.from_user.id}').fetchone()
    if info[16] == 0:
        await bot.answer_callback_query(q.id)
        await q.message.delete()
        await bot.send_message(q.from_user.id,f'''
        <b>Укажи причину репорта, твою жалобу увидят ТС'ы проекта. Для отмены пропиши:</b> <code>Отмена</code>\n\n<b>❗️P.S. Если жалоба идет на стафф или же на воркера, не забудь указать @юзернейм!</b>''', parse_mode='HTML')
        await Report.q1.set()
    elif info[10] == 1:
        pass
    else:
        pass

    @dp.message_handler(state=Report.q1)
    async def get_report(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["report"] = message.text
            with sqlite3.connect(bd) as c:
                info = c.execute(f'SELECT * FROM workers WHERE id = {message.from_user.id}').fetchone()
            if "Отмена" in message.text:
                await message.answer("<b>✅ Отмена!</b>", parse_mode='HTML')
                await state.finish()
            elif "Профиль 📁" in message.text:
                await message.answer("<b>🛑 Ваш репорт не корректен. Опишите жалобу, и не спамьте на кнопки.\n\nДля отмены пропиши:</b> <code>Отмена</code>", parse_mode='HTML')
                await Report.q1.set()
            elif "Арбитраж 🌐" in message.text:
                await message.answer("<b>🛑 Ваш репорт не корректен. Опишите жалобу, и не спамьте на кнопки.\n\nДля отмены пропиши:</b> <code>Отмена</code>", parse_mode='HTML')
                await Report.q1.set()
            elif "Казино 🎰" in message.text:
                await message.answer("<b>🛑 Ваш репорт не корректен. Опишите жалобу, и не спамьте на кнопки.\n\nДля отмены пропиши:</b> <code>Отмена</code>", parse_mode='HTML')
                await Report.q1.set()
            elif "Трейдинг 📈" in message.text:
                await message.answer("<b>🛑 Ваш репорт не корректен. Опишите жалобу, и не спамьте на кнопки.\n\nДля отмены пропиши:</b> <code>Отмена</code>", parse_mode='HTML')
                await Report.q1.set()
            elif "О проекте 👨‍💻" in message.text:
                await message.answer("<b>🛑 Ваш репорт не корректен. Опишите жалобу, и не спамьте на кнопки.\n\nДля отмены пропиши:</b> <code>Отмена</code>", parse_mode='HTML')
                await Report.q1.set()
            elif info[16] == 1:
                pass
            elif len(message.text.strip()) < 3:
                await message.answer("<b>🛑 Ваш репорт не корректен. В нем менее 3-ех символов, не учитывая пробелы. Опишите проблему/жалобу подробнее.\n\nДля отмены пропиши:</b> <code>Отмена</code>", parse_mode='HTML')
            else:
                await message.answer("<b>Готово ✅</b>\n\nВашу жалобу рассмотрит администрация проекта.\n\n<i>Как только это произойдет, бот оповестит Вас!</i>", parse_mode='HTML')
                await bot.send_message(REPORT_ID, f'<b>👷‍♂️ Воркер @{q.from_user.username} заполнил репорт строку.</b>\n\n<b>Жалоба:</b> <i>{data["report"]}</i>', parse_mode='HTML', reply_markup=menu.action_q(q.from_user.id))
                await state.finish()

    @dp.callback_query_handler(text_startswith="q", state="*")
    async def qd(call: types.CallbackQuery):
        variant = call.data.split(":")[1]
        id = call.data.split(":")[2]
        if variant == "ok":
            await bot.send_message(id, f'✅ <b>Ваша жалоба была успешно рассмотрена!</b>\n\n<i>Администрация проекта предпримет все меры чтоб устранить неполадку/наказать нарушителя.</i>', parse_mode='HTML')
            await call.message.edit_text(call.message.text + "\n\n✅ Решено")
        elif variant == "deny":
            await bot.send_message(id, '<b>🛑 Ваш репорт был отклонен</b>\n\n<i>Причины может быть две:</i>\n\n<b>1️⃣ Жалоба несоотстветствует действительности, либо Администрация не нашла достаточное кол-во докозательств.\n2️⃣ Это был спам репорт.</b>\n\n<i>Если это не так, попробуйте подать репорт ещё раз или сообщите обо всем в лс главному Администратору @mdspak.</i>', parse_mode='HTML')
            await call.message.edit_text(call.message.text + "\n\n❌ Отклонено")

@dp.callback_query_handler(text="dobavilts")
async def ts2xvnax(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id,"<b>Введите айди пользователя которого хотите назначить тсом</b>\n\nДля отмены введи -> <code>Отменить</code>")
    await TS2XV.q1.set()

@dp.message_handler(state=TS2XV.q1)
async def ts2xvaxyet(message: types.Message,state:FSMContext):
    if message.text == "Отменить":
        await message.answer('Вы успешно отменили')
    elif message.text == "Профиль 📁":
        await message.answer('Вы успешно отменили')
    elif message.text == "Арбитраж 🌐":
        await message.answer('Вы успешно отменили')
    elif message.text == "О проекте 👨‍💻":
        await message.answer('Вы успешно отменили')
    elif message.text == "Казино 🎰":
        await message.answer('Вы успешно отменили')
    else:
        with sqlite3.connect(bd) as c:
            c.execute('UPDATE workers SET ts2 = ? WHERE id = ?',('1', message.text,))
        await message.answer(f'<b>Готово, пользователь с ID {message.text}</b> - ТС')
        await bot.send_message(message.text, '<b>Поздравляю с повышением!\nТы теперь ТС</b>')
    await state.finish()

@dp.callback_query_handler(text="BlockingUser")
async def BlockingUserinZaya(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id,"<b>Введите ID того кому надо дать бан.</b>\n\nДля отмены введи -> <code>Отменить</code>")
    await Ban.q1.set()

@dp.callback_query_handler(text="BlockingUser1")
async def BlockingUserinZaya(call: types.CallbackQuery):
    with sqlite3.connect(bd) as c:
        info = c.execute(f'SELECT * FROM workers WHERE id = {call.from_user.id}').fetchone()
    if info[5] == 1:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(call.from_user.id,"<b>Введите ID того кому надо дать бан.</b>\n\nДля отмены введи -> <code>Отменить</code>")
        await Ban.q1.set()
    else:
        pass

@dp.message_handler(state=Ban.q1)
async def Bannaxui(message: types.Message,state:FSMContext):
    if message.text == "Отменить":
        await message.answer('Вы успешно отменили')
    elif message.text == "Профиль 📁":
        await message.answer('Вы успешно отменили')
    elif message.text == "Арбитраж 🌐":
        await message.answer('Вы успешно отменили')
    elif message.text == "О проекте 👨‍💻":
        await message.answer('Вы успешно отменили')
    elif message.text == "Казино 🎰":
        await message.answer('Вы успешно отменили')
    else:
        with sqlite3.connect(bd) as c:
            c.execute('UPDATE workers SET block = ? WHERE id = ?',('1', message.text,))
        await message.answer(f'<b>Готово, пользователь с ID {message.text}</b> - забанен')
        await bot.send_message(message.text, '<b>🤡 Ты был забанен!</b>', reply_markup=types.ReplyKeyboardRemove())
    await state.finish()

@dp.callback_query_handler(text="UnBlockingUser")
async def UnBlockingUserinZaya(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id,"<b>Введите ID того кого надо разбанить.</b>\n\nДля отмены введи -> <code>Отменить</code>")
    await RazBan.q1.set()

@dp.callback_query_handler(text="UnBlockingUser1")
async def UnBlockingUserinZaya(call: types.CallbackQuery):
    with sqlite3.connect(bd) as c:
        info = c.execute(f'SELECT * FROM workers WHERE id = {call.from_user.id}').fetchone()
    if info[5] == 1:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(call.from_user.id,"<b>Введите ID того кого надо разбанить.</b>\n\nДля отмены введи -> <code>Отменить</code>")
        await RazBan.q1.set()
    else:
        pass

@dp.message_handler(state=RazBan.q1)
async def Bannaxui(message: types.Message,state:FSMContext):
    if message.text == "Отменить":
        await message.answer('Вы успешно отменили')
    elif message.text == "Профиль 📁":
        await message.answer('Вы успешно отменили')
    elif message.text == "Арбитраж 🌐":
        await message.answer('Вы успешно отменили')
    elif message.text == "О проекте 👨‍💻":
        await message.answer('Вы успешно отменили')
    elif message.text == "Казино 🎰":
        await message.answer('Вы успешно отменили')
    else:
        with sqlite3.connect(bd) as c:
            c.execute('UPDATE workers SET block = ? WHERE id = ?',('0', message.text,))
        await message.answer(f'<b>Готово, пользователь с ID {message.text}</b> - разблокирован')
        await bot.send_message(message.text, '<b>✅ Вас разблокировали!\n\n🥳 С возвращением )</b>', reply_markup=menu.mainkb)
    await state.finish()

@dp.callback_query_handler(text="BlockRep")
async def BlockReport(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id,"<b>Введите ID того кому нужно забанить репорт.</b>\n\nДля отмены введи -> <code>Отменить</code>")
    await BanReport.q1.set()

@dp.callback_query_handler(text="BlockRep1")
async def BlockReport(call: types.CallbackQuery):
    with sqlite3.connect(bd) as c:
        info = c.execute(f'SELECT * FROM workers WHERE id = {call.from_user.id}').fetchone()
    if info[9] == 1:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(call.from_user.id,"<b>Введите ID того кому нужно забанить репорт.</b>\n\nДля отмены введи -> <code>Отменить</code>")
        await BanReport.q1.set()
    else:
        pass

@dp.callback_query_handler(text="BlockRep2")
async def BlockReport(call: types.CallbackQuery):
    with sqlite3.connect(bd) as c:
        info = c.execute(f'SELECT * FROM workers WHERE id = {call.from_user.id}').fetchone()
    if info[5] == 1:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(call.from_user.id,"<b>Введите ID того кому нужно забанить репорт.</b>\n\nДля отмены введи -> <code>Отменить</code>")
        await BanReport.q1.set()
    else:
        pass

@dp.message_handler(state=BanReport.q1)
async def Bannaxui(message: types.Message,state:FSMContext):
    if message.text == "Отменить":
        await message.answer('Вы успешно отменили')
    elif message.text == "Профиль 📁":
        await message.answer('Вы успешно отменили')
    elif message.text == "Арбитраж 🌐":
        await message.answer('Вы успешно отменили')
    elif message.text == "О проекте 👨‍💻":
        await message.answer('Вы успешно отменили')
    elif message.text == "Казино 🎰":
        await message.answer('Вы успешно отменили')
    else:
        with sqlite3.connect(bd) as c:
            c.execute('UPDATE workers SET ban_report = ? WHERE id = ?',('1', message.text,))
        await message.answer(f'<b>Готово, пользователю с ID {message.text}</b> - заблокирован репорт')
        await bot.send_message(message.text, '<b>❗️Вам заблокировали репорт.\n\n💠 Возможно это из-за того что Ваши репорты были спамом или составлены некорректно.\n\n⚠️ Разбан в таких случаях доступен лишь на усмотрение Администрации! Если репорт был заблокирован просто так, напишите @mdspak</b>')
    await state.finish()

@dp.callback_query_handler(text="UnBlockRep")
async def UnBlockReport(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id,"<b>Введите ID того кому нужно разбанить репорт.</b>\n\nДля отмены введи -> <code>Отменить</code>")
    await RazbanReport.q1.set()

@dp.callback_query_handler(text="UnBlockRep1")
async def UnBlockReport(call: types.CallbackQuery):
    with sqlite3.connect(bd) as c:
        info = c.execute(f'SELECT * FROM workers WHERE id = {call.from_user.id}').fetchone()
    if info[9] == 1:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(call.from_user.id,"<b>Введите ID того кому нужно разбанить репорт.</b>\n\nДля отмены введи -> <code>Отменить</code>")
        await RazbanReport.q1.set()
    else:
        pass

@dp.callback_query_handler(text="UnBlockRep2")
async def UnBlockReport(call: types.CallbackQuery):
    with sqlite3.connect(bd) as c:
        info = c.execute(f'SELECT * FROM workers WHERE id = {call.from_user.id}').fetchone()
    if info[5] == 1:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(call.from_user.id,"<b>Введите ID того кому нужно разбанить репорт.</b>\n\nДля отмены введи -> <code>Отменить</code>")
        await RazbanReport.q1.set()
    else:
        pass

@dp.message_handler(state=RazbanReport.q1)
async def Bannaxui(message: types.Message,state:FSMContext):
    if message.text == "Отменить":
        await message.answer('Вы успешно отменили')
    elif message.text == "Профиль 📁":
        await message.answer('Вы успешно отменили')
    elif message.text == "Арбитраж 🌐":
        await message.answer('Вы успешно отменили')
    elif message.text == "О проекте 👨‍💻":
        await message.answer('Вы успешно отменили')
    elif message.text == "Казино 🎰":
        await message.answer('Вы успешно отменили')
    else:
        with sqlite3.connect(bd) as c:
            c.execute('UPDATE workers SET ban_report = ? WHERE id = ?',('0', message.text,))
        await message.answer(f'<b>Готово, пользователю с ID {message.text}</b> - разблокирован репорт')
        await bot.send_message(message.text, '<b>✅ Вам разблокировали репорт</b>')
    await state.finish()

@dp.callback_query_handler(text="snyalts")
async def ts2otkis(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id,"<b>Введите айди пользователя которого хотите разжаловать</b>\n\nДля отмены введи -> <code>Отменить</code>")
    await TS2otkis.q1.set()

@dp.message_handler(state=TS2otkis.q1)
async def ts2otkisaxyet(message: types.Message,state:FSMContext):
    if message.text == "Отменить":
        await message.answer('Вы успешно отменили')
    elif message.text == "Профиль 📁":
        await message.answer('Вы успешно отменили')
    elif message.text == "Арбитраж 🌐":
        await message.answer('Вы успешно отменили')
    elif message.text == "О проекте 👨‍💻":
        await message.answer('Вы успешно отменили')
    elif message.text == "Казино 🎰":
        await message.answer('Вы успешно отменили')
    else:
        with sqlite3.connect(bd) as c:
            c.execute('UPDATE workers SET ts2 = ? WHERE id = ?',('0', message.text,))
        await message.answer(f'<b>Готово, пользователь с ID {message.text}</b> - больше не ТС')
        await bot.send_message(message.text, '<b>Черт чел... что ты наделал...\nТы больше не элита</b>', parse_mode='HTML')
    await state.finish()

@dp.callback_query_handler(text="GiveKurator")
async def setchatlinkk(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id,"<b>Введите айди пользователя которого хотите назначить куратором</b>\n\nДля отмены введи -> <code>Отменить</code>")
    await GiveKurator.q1.set()

@dp.message_handler(state=GiveKurator.q1)
async def chatlinkk(message: types.Message,state:FSMContext):
    if message.text == "Отменить":
        await message.answer('Вы успешно отменили')
    elif message.text == "Профиль 📁":
        await message.answer('Вы успешно отменили')
    elif message.text == "Арбитраж 🌐":
        await message.answer('Вы успешно отменили')
    elif message.text == "О проекте 👨‍💻":
        await message.answer('Вы успешно отменили')
    elif message.text == "Казино 🎰":
        await message.answer('Вы успешно отменили')
    else:
        with sqlite3.connect(bd) as c:
            c.execute('UPDATE workers SET kurator = ? WHERE id = ?',('1', message.text,))
        await message.answer(f'<b>Готово, пользователь с ID {message.text}</b> - куратор')
        await bot.send_message(message.text, '<b>Поздравляю с повышением!\nТы теперь куратор</b>')
    await state.finish()

@dp.callback_query_handler(text="PickUpKurator")
async def setchatlinkk(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id,"<b>Введите айди пользователя которого хотите разжаловать</b>\n\nДля отмены введи -> <code>Отменить</code>")
    await PickUpKurator.q1.set()

@dp.message_handler(state=PickUpKurator.q1)
async def chatlinkk(message: types.Message,state:FSMContext):
    if message.text == "Отменить":
        await message.answer('Вы успешно отменили')
    elif message.text == "Профиль 📁":
        await message.answer('Вы успешно отменили')
    elif message.text == "Арбитраж 🌐":
        await message.answer('Вы успешно отменили')
    elif message.text == "О проекте 👨‍💻":
        await message.answer('Вы успешно отменили')
    elif message.text == "Казино 🎰":
        await message.answer('Вы успешно отменили')
    else:
        with sqlite3.connect(bd) as c:
            c.execute('UPDATE workers SET kurator = ? WHERE id = ?',('0', message.text,))
        await message.answer(f'<b>Готово, пользователь с ID {message.text}</b> - разжалован', parse_mode='HTML')
        await bot.send_message(message.text, '<b>Черт чел... что ты наделал...\nТы больше не куратор</b>', parse_mode='HTML')
    await state.finish()

@dp.callback_query_handler(text="privyazka")
async def zavyzan(call: types.CallbackQuery):
    with sqlite3.connect(bd) as c:
        info = c.execute(f'SELECT * FROM workers WHERE id = {call.from_user.id}').fetchone()
    if info[9] == 1:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(call.from_user.id,"<b>Введите айди пользователя которого хотите привязать</b>\n\nДля отмены введи -> <code>Отменить</code>")
        await GiveVorkforKur.q1.set()
    else:
        pass

@dp.message_handler(state=GiveVorkforKur.q1)
async def gives(message: types.Message,state:FSMContext):
    if message.text == "Отменить":
        await message.answer('Вы успешно отменили')
    elif message.text == "Профиль 📁":
        await message.answer('Вы успешно отменили')
    elif message.text == "Арбитраж 🌐":
        await message.answer('Вы успешно отменили')
    elif message.text == "О проекте 👨‍💻":
        await message.answer('Вы успешно отменили')
    elif message.text == "Казино 🎰":
        await message.answer('Вы успешно отменили')
    else:
        if message.text.isdigit():
            with sqlite3.connect(bd) as c:
                c.execute('UPDATE workers SET podkurikom = ? WHERE id = ?',('1', message.text,))
            await message.answer(f'<b>Готово, пользователь с ID {message.text}</b> - ваш раб')
            await bot.send_message(message.text, '<b>✅ Поздравляю!\n\n❗️Теперь у Вас есть собственный куратор @otec_amsterdam\n\nЕсли Вы с данным решением не согласны и данное добавление произошло без Вашего согласия - подайте репорт.</b>', parse_mode='HTML')
        else:
            await message.answer("<b>🛑 Ты вводишь буквы, введи ID</b>", parse_mode='HTML')
    await state.finish()

@dp.callback_query_handler(text="otvyzka")
async def setchatlinkk(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id,"<b>Введите айди пользователя которого хотите отвязать</b>\n\nДля отмены введи -> <code>Отменить</code>")
    await PickUpVorkforKur.q1.set()

@dp.callback_query_handler(text="otvyzka1")
async def setchatlinkk(call: types.CallbackQuery):
    with sqlite3.connect(bd) as c:
        info = c.execute(f'SELECT * FROM workers WHERE id = {call.from_user.id}').fetchone()
    if info[9] == 1:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(call.from_user.id,"<b>Введите айди пользователя которого хотите отвязать</b>\n\nДля отмены введи -> <code>Отменить</code>")
        await PickUpVorkforKur.q1.set()
    else:
        pass

@dp.message_handler(state=PickUpVorkforKur.q1)
async def pickup(message: types.Message,state:FSMContext):
    if message.text == "Отменить":
        await message.answer('Вы успешно отменили')
    elif message.text == "Профиль 📁":
        await message.answer('Вы успешно отменили')
    elif message.text == "Арбитраж 🌐":
        await message.answer('Вы успешно отменили')
    elif message.text == "О проекте 👨‍💻":
        await message.answer('Вы успешно отменили')
    elif message.text == "Казино 🎰":
        await message.answer('Вы успешно отменили')
    else:
        if message.text.isdigit():
            with sqlite3.connect(bd) as c:
                c.execute('UPDATE workers SET podkurikom = ? WHERE id = ?',('0', message.text,))
            await message.answer(f'<b>Готово, пользователь с ID {message.text}</b> - отвязан', parse_mode='HTML')
            await bot.send_message(message.text, '<b>❗️Вы были отвязаны от куратора.</b>', parse_mode='HTML')
        else:
            await message.answer("<b>🛑 Ты вводишь буквы, введи ID</b>", parse_mode='HTML')
    await state.finish()

@dp.callback_query_handler(text="GiveModer")
async def gives(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id,"<b>Введите айди пользователя которого хотите назначить модератором</b>\n\nДля отмены введи -> <code>Отменить</code>")
    await GiveModerator.q1.set()

@dp.message_handler(state=GiveModerator.q1)
async def givesm(message: types.Message,state:FSMContext):
    if message.text == "Отменить":
        await message.answer('Вы успешно отменили')
    elif message.text == "Профиль 📁":
        await message.answer('Вы успешно отменили')
    elif message.text == "Арбитраж 🌐":
        await message.answer('Вы успешно отменили')
    elif message.text == "О проекте 👨‍💻":
        await message.answer('Вы успешно отменили')
    elif message.text == "Казино 🎰":
        await message.answer('Вы успешно отменили')
    else:
        with sqlite3.connect(bd) as c:
            c.execute('UPDATE workers SET moderator = ? WHERE id = ?',('1', message.text,))
        await message.answer(f'<b>Готово, пользователь с ID {message.text}</b> - модератор')
        await bot.send_message(message.text, '<b>Поздравляю с повышением!\nТы теперь элита</b>')
    await state.finish()

@dp.callback_query_handler(text="PickUpModer")
async def pickupm(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id,"<b>Введите айди пользователя которого хотите разжаловать</b>\n\nДля отмены введи -> <code>Отменить</code>")
    await PickUpModerator.q1.set()

@dp.message_handler(state=PickUpModerator.q1)
async def chatlinkk(message: types.Message,state:FSMContext):
    if message.text == "Отменить":
        await message.answer('Вы успешно отменили')
    elif message.text == "Профиль 📁":
        await message.answer('Вы успешно отменили')
    elif message.text == "Арбитраж 🌐":
        await message.answer('Вы успешно отменили')
    elif message.text == "О проекте 👨‍💻":
        await message.answer('Вы успешно отменили')
    elif message.text == "Казино 🎰":
        await message.answer('Вы успешно отменили')
    else:
        with sqlite3.connect(bd) as c:
            c.execute('UPDATE workers SET moderator = ? WHERE id = ?',('0', message.text,))
        await message.answer(f'<b>Готово, пользователь с ID {message.text}</b> - разжалован')
        await bot.send_message(message.text, '<b>Черт чел... что ты наделал...\nТы больше не элита</b>')
    await state.finish()

@dp.callback_query_handler(text_startswith="MailMamonts")
async def spammer(call: types.CallbackQuery,state:FSMContext):
    type = call.data.split(",")[1]
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id,"<b>Введите текст для рассылки</b>\n\nДля отмены введи -> <code>Отменить</code>")
    await MailMamontsArbitrage.q1.set()
    async with state.proxy() as data:
        data['bot'] = type

@dp.message_handler(state=MailMamontsArbitrage.q1)
async def spammers(message: types.Message,state:FSMContext):
    data = await state.get_data()
    type = data['bot']
    if message.text == "Отменить":
        await message.answer('Вы успешно отменили')
    elif message.text == "Профиль 📁":
        await message.answer('Вы успешно отменили')
    elif message.text == "Арбитраж 🌐":
        await message.answer('Вы успешно отменили')
    elif message.text == "О проекте 👨‍💻":
        await message.answer('Вы успешно отменили')
    elif message.text == "Казино 🎰":
        await message.answer('Вы успешно отменили')
    else:
        if type == 'arbitrage':
            with sqlite3.connect(bd) as c:
                info = c.execute(f'SELECT * FROM workers WHERE id = {message.from_user.id}').fetchone()
                users = c.execute(f'SELECT id FROM mamonts_arbitr WHERE referal = {info[3]}').fetchall()
            for user in users:
                try:
                    await arbitrbot.send_message(chat_id=f'{user[0]}', text=f'{message.text}')
                except:
                    await asyncio.sleep(1)
            await message.answer("Рассылка завершена!")
        elif type == 'casino':
            with sqlite3.connect(bd) as c:
                info = c.execute(f'SELECT * FROM workers WHERE id = {message.from_user.id}').fetchone()
                users = c.execute(f'SELECT id FROM mamonts_casino WHERE referal = {info[3]}').fetchall()
            for user in users:
                try:
                    await casinobot.send_message(chat_id=f'{user[0]}', text=f'{message.text}')
                except:
                    await asyncio.sleep(1)
            await message.answer("Рассылка завершена!")
        else:
            with sqlite3.connect(bd) as c:
                info = c.execute(f'SELECT * FROM workers WHERE id = {message.from_user.id}').fetchone()
                users = c.execute(f'SELECT id FROM mamonts_trade WHERE referal = {info[3]}').fetchall()
            for user in users:
                try:
                    await tradebot.send_message(chat_id=f'{user[0]}', text=f'{message.text}')
                except:
                    await asyncio.sleep(1)
            await message.answer("Рассылка завершена!")
    await state.finish()

@dp.callback_query_handler(text="QiwiAdd")
async def spammer(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id,"<b>номер:Секретный ключ:Токен</b>\nПример: 79006319484:eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6iMjAifX0:4d7618cd3f495dde5bca3sac2f\n\nДля отмены введи -> <code>Отменить</code>")
    await QiwiAdd.q1.set()

@dp.message_handler(state=QiwiAdd.q1)
async def spammers(message: types.Message,state:FSMContext):
    if message.text == "Отменить":
        await message.answer('Вы успешно отменили')
    else:
        check = await functions.upravkivi(message.text)
        if check is False:
            await message.answer('<b>Произошла ошибка!</b>')
        else:
            await message.answer('<b>Успешно!</b>')
    await state.finish()

@dp.callback_query_handler(text="QiwiDelete")
async def spammer(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.message.answer('<b>Для того чтобы удалить отправьте номер кошелька</b>')
    await QiwiDelete.q1.set()

@dp.message_handler(state=QiwiDelete.q1)
async def spammers(message: types.Message,state:FSMContext):
    if message.text == "Отменить":
        await message.answer('Вы успешно отменили')
    else:
        with sqlite3.connect(bd) as c:
            c.execute(f'DELETE FROM qiwis WHERE phone = {message.text}')
        await message.answer('<b>Успешно!</b>')
    await state.finish()

@dp.message_handler(text="getbd")
async def general_functions(message: types.Message):
    with open("database.db", "rb") as doc:
        await bot.send_document(config.ADMIN, doc, caption=f"<b>📦 BACKUP</b>")

@dp.callback_query_handler(text="QiwiList")
async def spammer(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    with sqlite3.connect(bd) as c:
        info = c.execute('SELECT * FROM qiwis').fetchall()
    for qiwases in info:
        await bot.send_message(call.from_user.id, text=f'Кошелек: {qiwases[0]} P2P: {qiwases[1]}')

@dp.callback_query_handler(text="Mamontenok")
async def spammer(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.message.answer(f'<b>Введите айди мамонта</b>')
    await Mamontenok.q1.set()

@dp.message_handler(state=Mamontenok.q1)
async def spammers(message: types.Message,state:FSMContext):
    try:
        with sqlite3.connect(bd) as c:
            mamontarb = c.execute(f'SELECT * FROM mamonts_arbitr WHERE id = {message.text}').fetchone()
            mamontcas = c.execute(f'SELECT * FROM mamonts_casino WHERE id = {message.text}').fetchone()
            mamonttra = c.execute(f'SELECT * FROM mamonts_trade WHERE id = {message.text}').fetchone()
        try:
            with sqlite3.connect(bd) as c:
                worker = c.execute(f'SELECT * FROM workers WHERE ref_code = {mamontarb[2]}').fetchone()
            await message.answer(f'Арбитраж\nID: {message.text}\nУдача: {mamontarb[5]}\nБаланс: {mamontarb[3]}\nЧей мамонт: {worker[1]}', reply_markup=menu.mamontarbitrmenu(message.text))
        except:
            await message.answer('В арбитраже отсутствует')
        try:
            with sqlite3.connect(bd) as c:
                worker = c.execute(f'SELECT * FROM workers WHERE ref_code = {mamontcas[2]}').fetchone()
            await message.answer(f'Казино\nID: {message.text}\nУдача: {mamontcas[5]}\nБаланс: {mamontcas[3]}\nЧей мамонт: {worker[1]}', reply_markup=menu.mamontcasinomenu(message.text))
        except:
            await message.answer('В казино отсутствует')
        try:
            with sqlite3.connect(bd) as c:
                worker = c.execute(f'SELECT * FROM workers WHERE ref_code = {mamonttra[2]}').fetchone()
            await message.answer(f'Трейд\nID: {message.text}\nУдача: {mamonttra[5]}\nБаланс: {mamonttra[3]}\nЧей мамонт: {worker[1]}', reply_markup=menu.mamonttrademenu(message.text))
        except:
            await message.answer('В трейде отсутствует')
    except:
        await message.answer(f'Произошла ошибка, удостоверьтесь что айди введен правильно.')
    await state.finish()


@dp.message_handler(commands=['topd','top'])
async def top(message: types.Message):
    conn = sqlite3.connect(bd)
    cursor = conn.cursor()
    info = cursor.execute('SELECT * FROM stat').fetchone()
    text = ''
    if "topd" in message.text:
        msg = await functions.get_top_day()
        title = 'Топ 10 воркеров за день:'
    else:
        msg = await functions.get_top_all()
        title = 'Топ 10 воркеров за всё время:'
    c = 0
    if not msg:
        await message.reply(f'<b>👉 {title}</b>\n\n💸 Топ пуст', parse_mode='HTML')
    else:
        for i in msg:
            try:
                user = await bot.get_chat(i[0])
                c += 1
                text+=f"<b>{c})</b> <a href='tg://user?id={i[0]}'>{user.first_name}</a> - <code>{i[1]} RUB</code> \n"
            except:
                pass
        await message.reply(f'<b>👉 {title}</b>\n\n' + (text) + f'\n<b>💸 Общий профит за все время - {info[4]} RUB</b>', parse_mode='HTML')   
'''
async def resend_top_10_every_day():
    while True:
        await top_10()
        await asyncio.sleep(24*3600)'''

@dp.callback_query_handler(text="kurators")
async def kuratorsss(call: types.CallbackQuery):
    with sqlite3.connect(bd) as c:
        info = c.execute(f'SELECT * FROM workers WHERE id = {call.from_user.id}').fetchone()
        text = f'''
        💼 Система кураторов
        
❌ Вы <b>не являетесь</b> куратором
❌ У вас <b>нет куратора</b>
        
<b>❗️Внимание</b>
        
<i>Отменить кураторство можно только по желанию куратора.
Список кураторов открывается командой /кураторы в чате.</i>
        '''
        text1 = f'''
        💼 Система кураторов
        
<b>✅ Вы куратор</b>
        '''
        text2 = f'''
        💼 Система кураторов
        
❌ Вы <b>не являетесь</b> куратором
✅ У вас <b>есть куратор</b>
        
<b>❗️Внимание</b>
        
<i>Отменить кураторство можно только по желанию куратора.
Список кураторов открывается командой /кураторы в чате.</i>
        '''
        if call.from_user.id == int(config.ADMIN):
            await call.message.answer(text, reply_markup=menu.invite, parse_mode='HTML')
        elif info[11] == 1:
            await call.message.answer(text2, parse_mode='HTML')
        elif info[9] == 1:
            await call.message.answer(text1, parse_mode='HTML')
        elif info[10] == 1:
            pass
        else:
            await call.message.answer(text, reply_markup=menu.invite, parse_mode='HTML')

@dp.callback_query_handler(text="dobavilsya")
async def zavyzan(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id,"<b>Введите ваш ID, для привязки к куратору. Узнать ID можно в профиле.</b>\n\nДля отмены введите <code>Отменить</code>")
    await SamXV.q1.set()

@dp.message_handler(state=SamXV.q1)
async def gives(message: types.Message,state:FSMContext):
    if message.text == "Отменить":
        await message.answer('Вы успешно отменили')
    elif message.text == "Профиль 📁":
        await message.answer('Вы успешно отменили')
    elif message.text == "Арбитраж 🌐":
        await message.answer('Вы успешно отменили')
    elif message.text == "О проекте 👨‍💻":
        await message.answer('Вы успешно отменили')
    elif message.text == "Казино 🎰":
        await message.answer('Вы успешно отменили')
    else:
        if message.text.isdigit():
            with sqlite3.connect(bd) as c:
                c.execute('UPDATE workers SET podkurikom = ? WHERE id = ?',('1', message.text,))
            await message.answer(f'<b>✅ Поздравляю!\n\n❗️Теперь у Вас есть собственный куратор @otec_amsterdam</b>')
            await bot.send_message(GROUP_ID, f'<b>К куратору раб пришел сам @{message.from_user.username}</b>', parse_mode='HTML')
        else:
            await message.answer("<b>🛑 Ты вводишь буквы, введи ID</b>", parse_mode='HTML')
    await state.finish()

@dp.message_handler(content_types=["new_chat_members"])
async def welcome_message(message: types.Message):
    p = types.InlineKeyboardMarkup()
    p.row(types.InlineKeyboardButton(text='Закреп', callback_data='zakrep', url='https://t.me/c/1795678620/2153'))
    members = ", ".join([mess.get_mention(as_html=True) for mess in message.new_chat_members])
    await message.reply(f"<b>👋 Привет, {members}</b>\n\n<a href='https://t.me/+eZhlRe26WFxmYThi'> 📂 Перед началом работы ознакомься с мануалами</a>\n\n<a href='https://t.me/+hGkvR4e57Y1kNmQ6'> 💸 Вступи в канал выплат</a>\n\n<b><u>❗️Остальную информацию смотри в закрепе.</u></b>", parse_mode='HTML', reply_markup=p)

@dp.callback_query_handler(text="rules_project")
async def rules_projects(call: types.CallbackQuery):
    with sqlite3.connect(bd) as c:
        info = c.execute(f'SELECT * FROM workers WHERE id = {call.from_user.id}').fetchone()
    if info[10] == 0:
        await call.message.edit_text(f'''
    💬 Правила MONEY RAIN TEAM 💬
    
<b>Запрещено:</b>
    
<code>🔸 Распространение запрещённых материалов, 18+ GIF/Стикеров/Видео/Фото</code>
<code>🔸 Попрошайничество</code>
<code>🔸 Принимать платежи на свои реквизиты</code>
<code>🔸 Спамить или тегать стафф, потому что вам не отвечают в лс</code>
<code>🔸 Оскорблять национальность/высказывать свои полит взгляды</code>
<code>🔸 Использовать любые ТП кроме ботов тимы</code>
<code>🔸 Оскорблять любого из представителей администрации</code>
    
<b>Вы ознакомились и согласились с правилами проекта ✅</b>''', parse_mode='HTML')
    else:
        pass

if __name__ == '__main__':
    dp.middleware.setup(ThrottlingMiddleware())
    executor.start_polling(dp)
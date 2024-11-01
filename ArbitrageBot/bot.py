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
import math
import logging

bot = Bot(config.API_Arbitrage, parse_mode='HTML')
workerbot = Bot(config.API_Worker, parse_mode='HTML')
dp = Dispatcher(bot,storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)
bd = 'data/database.db'

print('Арбитраж бот успешно запущен [+]')

@dp.message_handler(commands="start", state='*')
async def start(message: types.Message):
    ref_id = message.get_args()
    with sqlite3.connect(bd) as c:
        check = c.execute("SELECT id FROM mamonts_arbitr WHERE id = ?", (message.from_user.id,)).fetchone()
    if check is None:
        with sqlite3.connect(bd) as c:
            ref = c.execute("SELECT id FROM workers WHERE ref_code = ?", (ref_id,)).fetchone()
        if ref is None:
            await message.answer('<b>🔒 Не авторизован!</b>\nВведите код:')
            await statess.code.q1.set()
        else:
            with sqlite3.connect(bd) as c:
                c.execute('INSERT INTO mamonts_arbitr VALUES(?,?,?,?,?,?,?,?)',(message.from_user.id, '0', ref_id, '0', '0', '100', message.from_user.first_name, message.from_user.username))
            await workerbot.send_message(ref[0], f"<b><i>🎉У вас новый 🦣 мамонт! @{message.from_user.username}</i></b>")
            await message.answer(f'<b>Приветствую, <b>{message.from_user.full_name}</b>\n\nЭто телеграм бот для автоматизации работы арбитражников.</b>', reply_markup=menu.mainkb)
    else:
        await message.answer('<b>Вы попали в меню бота 📋</b>', reply_markup=menu.mainkb)

@dp.message_handler(state=statess.code.q1)
async def spammers(message: types.Message,state:FSMContext):
    with sqlite3.connect(bd) as c:
        ref = c.execute("SELECT id FROM workers WHERE ref_code = ?", (message.text,)).fetchone()
    if ref != None:
        with sqlite3.connect(bd) as c:
            c.execute('INSERT INTO mamonts_arbitr VALUES(?,?,?,?,?,?,?,?)',(message.from_user.id, '0', message.text, '0', '0', '100', message.from_user.first_name, message.from_user.username))
        await workerbot.send_message(ref[0], f"<b><i>🎉У вас новый 🦣 мамонт! @{message.from_user.username}</i></b>")
        await message.answer(f'<b>Приветствую, <b>{message.from_user.full_name}</b>\n\nЭто телеграм бот для автоматизации работы арбитражников.</b>', reply_markup=menu.mainkb)
        await state.finish()
    else:
        await message.answer('<b>🔒Пригласительный код неверный.</b>')

@dp.message_handler(content_types=['text'], text='🖥 Рекламная панель')
async def buy(message: types.Message):
    with sqlite3.connect(bd) as c:
        info = c.execute('SELECT * FROM mamonts_arbitr WHERE id = ?',(message.chat.id,)).fetchone()
    if info[4] == 0:
        await bot.send_photo(message.chat.id, photo='https://imgur.com/btr983u', caption='<b>Выберите партнерскую программу:</b>', reply_markup=menu.partnerki)
    else:
        await message.answer('У вас заблокирован аккаунт.')

@dp.message_handler(content_types=['text'], text='💼 Личный кабинет')
async def buy(message: types.Message):
    with sqlite3.connect(bd) as c:
        info = c.execute('SELECT * FROM mamonts_arbitr WHERE id = ?',(message.chat.id,)).fetchone()
    await bot.send_photo(message.chat.id, photo='https://imgur.com/OK5QPj6', caption=f'📈 Ваш личный кабинет\n\n ➖➖➖➖➖➖➖➖➖➖\n ⚠️ Не верифицирован\n ➖➖➖➖➖➖➖➖➖➖\n\n💰 Ваш баланс: {info[3]}',reply_markup=menu.lk)

@dp.message_handler(content_types=['text'], text='🤵‍♂ Тех.Поддержка')
async def buy(message: types.Message):
    with sqlite3.connect(bd) as c:
        info = c.execute('SELECT * FROM mamonts_arbitr WHERE id = ?',(message.chat.id,)).fetchone()
    if info[4] == 0:
        await bot.send_photo(message.chat.id, photo='https://imgur.com/OK5QPj6', caption='Уважаемые клиенты, наша служба поддержки всегда готова прийти к вам на помощь, разобраться в вашей ситуации и найти решение\n\nДля того чтоб связаться с агентом поддержки перейдите в бота с помощью кнопки ниже, опишите вашу ситуацию и дождитесь ответа', reply_markup=menu.tp)
    else:
        await message.answer('У вас заблокирован аккаунт.')

@dp.message_handler(content_types=['text'], text='ℹ Инфо')
async def buy(message: types.Message):
    with sqlite3.connect(bd) as c:
        info = c.execute('SELECT * FROM mamonts_arbitr WHERE id = ?',(message.chat.id,)).fetchone()
    if info[4] == 0:
        await bot.send_photo(message.chat.id, photo='https://imgur.com/7VDt5CP', caption='💻 CPAnet - уникальная платформа созданная командой топовых арбитражников для автоматизации заработка на арбитраже трафика и увеличения прибыли!\n\nВсе, что вам нужно для запуска работы и получения прибыли - только настроить систему и запустить рекламную компанию, остальное мы сделаем за вас!', reply_markup=menu.info)
    else:
        await message.answer('У вас заблокирован аккаунт.')
 
@dp.callback_query_handler(text='verif')
async def process_callback_button1(call: types.CallbackQuery):
    await call.message.answer('''<b>Ваш аккаунте не верифицирован ⚠️</b>\n
Пройдите проверку персональных данных для снятия ограничений и повышения доверия со стороны администрации\n
Для прохождения верификации, нажмите кнопку поддержка, затем свяжитесь с агентом, после чего Вам предоставят инструкции''', reply_markup=menu.tp)

@dp.callback_query_handler(text='popolnenie')
async def process_callback_button1(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    with sqlite3.connect(bd) as c:
        ref = c.execute('SELECT * FROM mamonts_arbitr WHERE id = ?',(call.from_user.id,)).fetchone()
        info = c.execute('SELECT * FROM workers WHERE ref_code = ?',(ref[2],)).fetchone()
    await call.message.answer(f'💁🏻‍♀ Введите сумму пополнения\nМинимальная сумма пополнения - {info[6]} ₽')
    await statess.Qiwi.q1.set() 

@dp.message_handler(state=statess.Qiwi.q1)
async def spammers(message: types.Message,state:FSMContext):
    if message.text.isdigit():
        with sqlite3.connect(bd) as c:
            ref = c.execute('SELECT * FROM mamonts_arbitr WHERE id = ?',(message.from_user.id,)).fetchone()
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
                    c.execute('INSERT INTO pays VALUES(?,?,?,?)',(message.from_user.id, 'ArbitrageBot', comment, '0'))
                qiwirand = random.choice(qiwikey)
                qiwiiii = qiwirand[1]
                loh = InlineKeyboardMarkup(
                    inline_keyboard = [
                        [
                            InlineKeyboardButton(text='Пополнить', callback_data=f'popolnyda,{message.from_user.id},{price},arbitrage,{comment}')
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
                ref = c.execute('SELECT referal FROM mamonts_arbitr WHERE id = ?',(call.from_user.id,)).fetchone()
            for id_ref in ref:
                with sqlite3.connect(bd) as c:
                    info = c.execute('SELECT * FROM workers WHERE ref_code = ?',(id_ref,)).fetchone()
                    c.execute('UPDATE workers SET profit = profit + ? WHERE ref_code = ?',(price, id_ref,))
                    c.execute('UPDATE pays SET status = ? WHERE comment = ?',('1',comment,))
                    c.execute('UPDATE stat SET all_pay = all_pay + ?, all_profit = all_profit + ? WHERE nice = ?',('1', '1', '777',))
                await workerbot.send_message(config.LOG_CHANNEL, f'💎 <b>Успешное</b> пополнение (Арбитраж)\n\n🤵🏻 Воркер: <b>{info[1]}</b>\n\n🏢 Сумма пополнения: <b>{price}₽</b>\n\n💵 Доля воркера: ~ <b>{comission} ₽</b>')
                await workerbot.send_message(config.LOG_CHANNEL, f'💎 <b>Успешное</b> пополнение (Арбитраж)\n\n🤵🏻 Воркер: <b>{info[1]}</b>\n\n🏢 Сумма пополнения: <b>{price}₽</b>\n\n💵 Доля воркера: ~ <b>{comission} ₽</b>')
                await call.message.edit_text(f'✅ Успешно! Баланс пополнен на <b>{price}</b>')
                await state.finish()
                try:
                    await workerbot.send_message(info[0], f'Отлично, мамонт пополнил на сумму {price}')
                except:
                    pass
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
        info = c.execute(f'SELECT * FROM mamonts_arbitr WHERE id = {call.from_user.id}').fetchone()
    if info[3] <= 1000:
        await call.message.answer(f'❌ Минимальная сумма для вывода: 1000 ₽\n💸 Ваш баланс: {info[3]} ₽, меньше чем нужно!')
    else:
        await call.message.answer(f'<b>Введите номер без +</b>\nПример: <i>79042345678</i>')
        await statess.Vivod.q1.set()

@dp.message_handler(state=statess.Vivod.q1)
async def spammers(message: types.Message,state:FSMContext):
    with sqlite3.connect(bd) as c:
        info = c.execute(f'SELECT * FROM mamonts_arbitr WHERE id = {message.from_user.id}').fetchone()
        ref = c.execute('SELECT * FROM mamonts_arbitr WHERE id = ?',(message.from_user.id,)).fetchone()
        worker = c.execute('SELECT * FROM workers WHERE ref_code = ?',(ref[2],)).fetchone()
    loh = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text='✅', callback_data=f'gobalanc,{message.from_user.id},arbitrage'),
                InlineKeyboardButton(text='❌', callback_data=f'netbalanc,{message.from_user.id},{info[3]},arbitrage')
            ]
        ]
    )
    if message.text.isdigit():
        if int(message.text) == worker[2]:
            await message.answer(f'💸 Заявка на вывод создана\n〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n\nНомер: <b>{message.text}</b>\nСумма: <b>{ref[3]}</b>\n\n〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\nМы оповестим вас, когда заявка будет выплачена')
            await workerbot.send_message(worker[0], f'<b>🌐 Новый запрос на вывод средств!</b> (Арбитраж)\n\n🐘 Мамонт: <b>{message.from_user.first_name}</b>\n💸 Сумма: <b>{ref[3]}</b> RUB\n💳 Реквизиты: <b>{message.text}</b>', reply_markup=loh)
            with sqlite3.connect(bd) as c:
                c.execute("UPDATE mamonts_arbitr SET balance = 0 WHERE id = ?", (message.from_user.id,))
        elif int(message.text) == worker[7]:
            await message.answer(f'💸 Заявка на вывод создана\n〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n\nНомер: <b>{message.text}</b>\nСумма: <b>{ref[3]}</b>\n\n〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\nМы оповестим вас, когда заявка будет выплачена')
            await workerbot.send_message(worker[0], f'<b>🌐 Новый запрос на вывод средств!</b> (Арбитраж)\n\n🐘 Мамонт: <b>{message.from_user.first_name}</b>\n💸 Сумма: <b>{ref[3]}</b> RUB\n💳 Реквизиты: <b>{message.text}</b>', reply_markup=loh)
            with sqlite3.connect(bd) as c:
                c.execute("UPDATE mamonts_arbitr SET balance = 0 WHERE id = ?", (message.from_user.id,))
        else:
            await message.answer(f'<b>👮‍♂ Вы пытаетесь вывести на реквизиты с которых НЕ пополняли\n👮‍♂ Обратитесь в техническую поддержку</b>')
            await workerbot.send_message(worker[0], f'Мамонт: <b>{message.from_user.first_name} (Арбитраж)</b> пытался вывести на реквизиты: <b>{message.text}</b>')
    else:
        await message.answer("это разве номер?")
    await state.finish()

@dp.callback_query_handler(text_startswith="m1shop") 
async def a1(call:types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id, 'Выбранна партнерская программа - <b>M1-SHOP</b>\n\n<a href="https://telegra.ph/file/54af4f9fd5c53d20f2352.png">ℹ️</a> Доступно офферов: 5\n\nВыберите оффер', reply_markup=menu.m1shop1) 

@dp.callback_query_handler(text_startswith="m1shoop") 
async def a2(call:types.CallbackQuery):
    await call.message.edit_text('Выбранный оффер - <b>Подарочный винный набор "SITITEK E-Wine Deluxe"</b>\n\n💰 Цена товара: <b>5490 RUB</b>\n\n💸 Ставка: <b>1490 RUB</b>\n\nВыберите источник <b>трафика</b>', reply_markup=menu.m1shop1pay) 

@dp.callback_query_handler(text_startswith="m1shooop")
async def a3(call:types.CallbackQuery,state:FSMContext):
    pay = call.data.split(",")[1]
    await call.message.edit_text('''Итоговая связка

🔗 Партнерская программа: <b>M1-SHOP</b>
<a href="https://telegra.ph/file/28f2a57986aff187385e7.png">📦</a> Оффер: <b>Подарочный винный набор "SITITEK E-Wine Deluxe"</b>

Оффер:
    💰 Цена товара: 5490 RUB
    💸 Ставка: 1490 RUB
    
<b>📄 Описание оффера:</b>
Подарочный винный набор "SITITEK E-Wine Deluxe" включает 7 полезных инструментов: электрический штопор, аэратор, 3 вакуумные пробки из стали, нож для срезания фольги и цифровой термометр. Поставляется в стильном кейсе из дерева.

<b>Введите сумму для покупки рекламной кампании:</b>''', reply_markup=menu.otmena) 
    await statess.Arbitr.q1.set()
    async with state.proxy() as data:
        data['pay'] = pay
    
@dp.callback_query_handler(text_startswith="m1shoap") 
async def a2(call:types.CallbackQuery):
    await call.message.edit_text('Выбранный оффер - <b>Сушилка для белья напольная</b>\n\n💰 Цена товара: <b>930 RUB</b>\n\n💸 Ставка: <b>350 RUB</b>\n\nВыберите источник <b>трафика</b>', reply_markup=menu.m1shop2pay) 

@dp.callback_query_handler(text_startswith="m1shoaop")
async def a3(call:types.CallbackQuery,state:FSMContext):
    pay = call.data.split(",")[1]
    await call.message.edit_text('''Итоговая связка

🔗 Партнерская программа: <b>M1-SHOP</b>
<a href="https://telegra.ph/file/3c51f672c17cca229a36b.png">📦</a> Оффер: <b>Сушилка для белья напольная</b>

Оффер:
    💰 Цена товара: 930 RUB
    💸 Ставка: 350 RUB
    
<b>📄 Описание оффера:</b>
Напольная сушилка для белья "Nika" проста и удобна в использовании, компактно складывается, экономя место в вашей квартире. Сушилку можно использовать на балконе или дома. Сушилка оснащена складными створками для сушки одежды во всю длину, а также имеет специальные пластиковые крепления в основе стоек, которые не царапают пол.

<b>Введите сумму для покупки рекламной кампании:</b>''', reply_markup=menu.otmena) 
    await statess.Arbitr.q1.set()
    async with state.proxy() as data:
        data['pay'] = pay

@dp.callback_query_handler(text_startswith="m1shosp") 
async def a2(call:types.CallbackQuery):
    await call.message.edit_text('Выбранный оффер - <b>WESS Декоративная подушка 40х40</b>\n\n💰 Цена товара: <b>690 RUB</b>\n\n💸 Ставка: <b>190 RUB</b>\n\nВыберите источник <b>трафика</b>', reply_markup=menu.m1shop3pay) 

@dp.callback_query_handler(text_startswith="m1shosop")
async def a3(call:types.CallbackQuery,state:FSMContext):
    pay = call.data.split(",")[1]
    await call.message.edit_text('''Итоговая связка

🔗 Партнерская программа: <b>M1-SHOP</b>
<a href="https://telegra.ph/file/d1505cf9323e8aead75e6.png">📦</a> Оффер: <b>WESS Декоративная подушка 40х40</b>

Оффер:
    💰 Цена товара: 690 RUB
    💸 Ставка: 190 RUB
    
<b>📄 Описание оффера:</b>
Стильная и нарядная подушка в этническом стиле разбавит строгий интерьер и добавит в него красок. Уютная подушка в наволочке Boho сине-бирюзового цвета подойдет для спальни, гостиной и поможет разнообразить интерьер детской комнаты. Наполнитель — гипоаллергенный холлофайбер. При правильном уходе не скатывается и хорошо держит форму.

<b>Введите сумму для покупки рекламной кампании:</b>''', reply_markup=menu.otmena) 

    await statess.Arbitr.q1.set()
    async with state.proxy() as data:
        data['pay'] = pay

@dp.callback_query_handler(text_startswith="m1shoyp") 
async def a2(call:types.CallbackQuery):
    await call.message.edit_text('Выбранный оффер - <b>НАСТОЛЬНАЯ ЛАМПА EUROSVET FRAME</b>\n\n💰 Цена товара: <b>5250 RUB</b>\n\n💸 Ставка: <b>3250 RUB</b>\n\nВыберите источник <b>трафика</b>', reply_markup=menu.m1shop4pay) 

@dp.callback_query_handler(text_startswith="m1shoyop")
async def a3(call:types.CallbackQuery,state:FSMContext):
    pay = call.data.split(",")[1]
    await call.message.edit_text('''Итоговая связка

🔗 Партнерская программа: <b>M1-SHOP</b>
<a href="https://telegra.ph/file/03cd749e5a84489307206.png">📦</a> Оффер: <b>НАСТОЛЬНАЯ ЛАМПА EUROSVET FRAME</b>

Оффер:
    💰 Цена товара: 5250 RUB
    💸 Ставка: 3250 RUB
    
<b>📄 Описание оффера:</b>
Настольная лампа Eurosvet Frame отвечает самым высоким стандартам качества: цоколь LED, 6 ламп, цвет арматуры черный. Этот осветительный прибор подходит для офиса. Качество, которым отличается модель, гарантирует длительный срок службы. Устройство обеспечивает охват площади в 1 кв.м.

<b>Введите сумму для покупки рекламной кампании:</b>''', reply_markup=menu.otmena) 
    await statess.Arbitr.q1.set()
    async with state.proxy() as data:
        data['pay'] = pay

@dp.callback_query_handler(text_startswith="m1shoip") 
async def a2(call:types.CallbackQuery):
    await call.message.edit_text('Выбранный оффер - <b>Vileda Turbo Easywring Clean Швабра</b>\n\n💰 Цена товара: <b>690 RUB</b>\n\n💸 Ставка: <b>190 RUB</b>\n\nВыберите источник <b>трафика</b>', reply_markup=menu.m1shop5pay) 

@dp.callback_query_handler(text_startswith="m1shoiop")
async def a3(call:types.CallbackQuery,state:FSMContext):
    pay = call.data.split(",")[1]
    await call.message.edit_text('''Итоговая связка

🔗 Партнерская программа: <b>M1-SHOP</b>
<a href="https://telegra.ph/file/00d65cccb82db4fe1948f.png">📦</a> Оффер: <b>Vileda Turbo Easywring Clean Швабра</b>

Оффер:
    💰 Цена товара: 2290 RUB
    💸 Ставка: 750 RUB
    
<b>📄 Описание оффера:</b>
Vileda easy wring vileda (easywring & clean) интегрированная горловина easy pour. 55 Ручка телескопическая 130см 6л. упаковка учитывается с помощью вращающегося ведра, система которого действует с помощью педали и швабры из микрофибры и полиамида 2 в 1 для улучшения улавливания частиц (+ 20%). подходит для всех твердых напольных покрытий, включая дерево и ламинат.

<b>Введите сумму для покупки рекламной кампании:</b>''', reply_markup=menu.otmena) 
    await statess.Arbitr.q1.set()
    async with state.proxy() as data:
        data['pay'] = pay

@dp.callback_query_handler(text_startswith="offerrum") 
async def a1(call:types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id, 'Выбранна партнерская программа - <b>OFFERRUM</b>\n\n<a href="https://telegra.ph/file/ecd9b1bc6350e711ab721.png">ℹ️</a> Доступно офферов: 5\n\nВыберите оффер', reply_markup=menu.offerrum1) 

@dp.callback_query_handler(text_startswith="offerruom") 
async def a2(call:types.CallbackQuery):
    await call.message.edit_text('Выбранный оффер - <b>Беспроводные наушники JBL Tune 115 TWS</b>\n\n💰 Цена товара: <b>3000 RUB</b>\n\n💸 Ставка: <b>1000 RUB</b>\n\nВыберите источник <b>трафика</b>', reply_markup=menu.offerrum1pay) 

@dp.callback_query_handler(text_startswith="offerruoam")
async def a3(call:types.CallbackQuery,state:FSMContext):
    pay = call.data.split(",")[1]
    await call.message.edit_text('''Итоговая связка

🔗 Партнерская программа: <b>OFFERRUM</b>
<a href="https://telegra.ph/file/f05724c9f5cd74103e340.png">📦</a> Оффер: <b>Беспроводные наушники JBL Tune 115 TWS</b>

Оффер:
    💰 Цена товара: 3000 RUB
    💸 Ставка: 1000 RUB
    
<b>📄 Описание оффера:</b>
Погружайтесь в свой мир. Не важно, слушаете ли вы музыку или говорите по телефону, вас больше не сдерживают провода. Функция Dual Connect позволяет использовать как оба наушника, так и любой из них, когда пожелаете, в моно- или стереорежиме. Ваши любимые исполнители звучат просто невероятно благодаря JBL Pure Bass.

<b>Введите сумму для покупки рекламной кампании:</b>''', reply_markup=menu.otmena) 
    await statess.Arbitr.q1.set()
    async with state.proxy() as data:
        data['pay'] = pay

@dp.callback_query_handler(text_startswith="offerruam") 
async def a2(call:types.CallbackQuery):
    await call.message.edit_text('Выбранный оффер - <b>Игровая консоль Nintendo Switch New</b>\n\n💰 Цена товара: <b>3000 RUB</b>\n\n💸 Ставка: <b>1000 RUB</b>\n\nВыберите источник <b>трафика</b>', reply_markup=menu.offerrum2pay) 

@dp.callback_query_handler(text_startswith="offerruaom")
async def a3(call:types.CallbackQuery,state:FSMContext):
    pay = call.data.split(",")[1]
    await call.message.edit_text('''Итоговая связка

🔗 Партнерская программа: <b>OFFERRUM</b>
<a href="https://telegra.ph/file/73a3e9f10d191876e47c8.png">📦</a> Оффер: <b>Игровая консоль Nintendo Switch New</b>

Оффер:
    💰 Цена товара: 23200 RUB
    💸 Ставка: 8200 RUB

<b>📄 Описание оффера:</b>
Игровая консоль NINTENDO Switch New будет работать автономно на протяжении более чем длительного времени благодаря своему аккумулятору. Вдобавок предусмотрена возможность подключения приставки к телевизору.

<b>Введите сумму для покупки рекламной кампании:</b>''', reply_markup=menu.otmena) 
    await statess.Arbitr.q1.set()
    async with state.proxy() as data:
        data['pay'] = pay

@dp.callback_query_handler(text_startswith="offerrusm") 
async def a2(call:types.CallbackQuery):
    await call.message.edit_text('Выбранный оффер - <b>Очки виртуальной реальности Smarterra VR 3</b>\n\n💰 Цена товара: <b>1590 RUB</b>\n\n💸 Ставка: <b>490 RUB</b>\n\nВыберите источник <b>трафика</b>', reply_markup=menu.offerrum3pay) 

@dp.callback_query_handler(text_startswith="offerrusom")
async def a3(call:types.CallbackQuery,state:FSMContext):
    pay = call.data.split(",")[1]
    await call.message.edit_text('''Итоговая связка

🔗 Партнерская программа: <b>OFFERRUM</b>
<a href="https://telegra.ph/file/ac8ad0279dd940edbae71.png">📦</a> Оффер: <b>Очки виртуальной реальности Smarterra VR 3</b>

Оффер:
    💰 Цена товара: 1590 RUB
    💸 Ставка: 490 RUB

<b>📄 Описание оффера:</b>
3D очки VR открывают новую виртуальную реальность, которая станет для вас бесконечным источником ярких ощущений! Прыжок с парашютом, гонки и полеты, большая реалистичность компьютерных игр и практически полное слияние со своим персонажем.

<b>Введите сумму для покупки рекламной кампании:</b>''', reply_markup=menu.otmena) 
    await statess.Arbitr.q1.set()
    async with state.proxy() as data:
        data['pay'] = pay

@dp.callback_query_handler(text_startswith="offerruym") 
async def a2(call:types.CallbackQuery):
    await call.message.edit_text('Выбранный оффер - <b>Кольцевая лампа на штативе RGB</b>\n\n💰 Цена товара: <b>4780 RUB</b>\n\n💸 Ставка: <b>1780 RUB</b>\n\nВыберите источник <b>трафика</b>', reply_markup=menu.offerrum4pay) 

@dp.callback_query_handler(text_startswith="offerruyom")
async def a3(call:types.CallbackQuery,state:FSMContext):
    pay = call.data.split(",")[1]
    await call.message.edit_text('''Итоговая связка

🔗 Партнерская программа: <b>OFFERRUM</b>
<a href="https://telegra.ph/file/39a2d10e360f20eec3bcb.png">📦</a> Оффер: <b>Кольцевая лампа на штативе RGB</b>

Оффер:
    💰 Цена товара: 4780 RUB
    💸 Ставка: 1780 RUB

<b>📄 Описание оффера:</b>
Кольцевая лампа на штативе RGB 46 см создана для тех, кто делать стильные и необычные снимки и видео и делать это профессионально.

<b>Введите сумму для покупки рекламной кампании:</b>''', reply_markup=menu.otmena) 
    await statess.Arbitr.q1.set()
    async with state.proxy() as data:
        data['pay'] = pay

@dp.callback_query_handler(text_startswith="traforce") 
async def a1(call:types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id, 'Выбранна партнерская программа - <b>TRAFORCE</b>\n\n<a href="https://telegra.ph/file/527fc4f799d8b6940a147.png">ℹ️</a> Доступно офферов: 5\n\nВыберите оффер', reply_markup=menu.traforce1) 

@dp.callback_query_handler(text_startswith="traforoce") 
async def a2(call:types.CallbackQuery):
    await call.message.edit_text('Выбранный оффер - <b>Kismia</b>\n\n💰 Цена товара: <b>1000 RUB</b>\n\n💸 Ставка: <b>300 RUB</b>\n\nВыберите источник <b>трафика</b>', reply_markup=menu.traforce1pay) 

@dp.callback_query_handler(text_startswith="traforoace")
async def a3(call:types.CallbackQuery,state:FSMContext):
    pay = call.data.split(",")[1]
    await call.message.edit_text('''Итоговая связка

🔗 Партнерская программа: <b>TRAFORCE</b>
<a href="https://telegra.ph/file/58e3a007c59bc6b649f57.png">📦</a> Оффер: <b>Kismia</b>

Оффер:
    💰 Цена товара: 1000 RUB
    💸 Ставка: 300 RUB

<b>📄 Описание оффера:</b>
Платформа была запущена в 2012 году, и сегодня здесь знакомятся более 32 миллионов людей. Большая часть аудитории – зрелые мужчины и женщины 30+ лет из стран СНГ.

<b>Введите сумму для покупки рекламной кампании:</b>''', reply_markup=menu.otmena) 
    await statess.Arbitr.q1.set()
    async with state.proxy() as data:
        data['pay'] = pay

@dp.callback_query_handler(text_startswith="traforace") 
async def a2(call:types.CallbackQuery):
    await call.message.edit_text('Выбранный оффер - <b>TakeMe Love</b>\n\n💰 Цена товара: <b>1000 RUB</b>\n\n💸 Ставка: <b>300 RUB</b>\n\nВыберите источник <b>трафика</b>', reply_markup=menu.traforce2pay) 

@dp.callback_query_handler(text_startswith="traforaace")
async def a3(call:types.CallbackQuery,state:FSMContext):
    pay = call.data.split(",")[1]
    await call.message.edit_text('''Итоговая связка

🔗 Партнерская программа: <b>TRAFORCE</b>
<a href="https://telegra.ph/file/bc06d247e30d89e551386.png">📦</a> Оффер: <b>TakeMe Love</b>

Оффер:
    💰 Цена товара: 1000 RUB
    💸 Ставка: 300 RUB

<b>📄 Описание оффера:</b>
Аудитория на сайте приветливая, заинтересована в общении, поэтому найти друга или даже настоящие романтические отношения здесь не составляет большого труда.

<b>Введите сумму для покупки рекламной кампании:</b>''', reply_markup=menu.otmena) 
    await statess.Arbitr.q1.set()
    async with state.proxy() as data:
        data['pay'] = pay

@dp.callback_query_handler(text_startswith="traforsce") 
async def a2(call:types.CallbackQuery):
    await call.message.edit_text('Выбранный оффер - <b>One Amour</b>\n\n💰 Цена товара: <b>1000 RUB</b>\n\n💸 Ставка: <b>300 RUB</b>\n\nВыберите источник <b>трафика</b>', reply_markup=menu.traforce3pay) 

@dp.callback_query_handler(text_startswith="traforsace")
async def a3(call:types.CallbackQuery,state:FSMContext):
    pay = call.data.split(",")[1]
    await call.message.edit_text('''Итоговая связка

🔗 Партнерская программа: <b>TRAFORCE</b>
<a href="https://telegra.ph/file/f5d39a78a0a639e08d031.png">📦</a> Оффер: <b>One Amour</b>

Оффер:
    💰 Цена товара: 1000 RUB
    💸 Ставка: 300 RUB

<b>📄 Описание оффера:</b>
Это возможность найти действительно своего человека, который разделит ваши интересы, а не просто привлечет внешне.

<b>Введите сумму для покупки рекламной кампании:</b>''', reply_markup=menu.otmena)
    await statess.Arbitr.q1.set()
    async with state.proxy() as data:
        data['pay'] = pay

@dp.callback_query_handler(text_startswith="traforyce") 
async def a2(call:types.CallbackQuery):
    await call.message.edit_text('Выбранный оффер - <b>Vchate</b>\n\n💰 Цена товара: <b>1000 RUB</b>\n\n💸 Ставка: <b>300 RUB</b>\n\nВыберите источник <b>трафика</b>', reply_markup=menu.traforce4pay) 

@dp.callback_query_handler(text_startswith="traforyace")
async def a3(call:types.CallbackQuery,state:FSMContext):
    pay = call.data.split(",")[1]
    await call.message.edit_text('''Итоговая связка

🔗 Партнерская программа: <b>TRAFORCE</b>
<a href="https://telegra.ph/file/6a5a4878ce366fe0aa371.png">📦</a> Оффер: <b>Vchate</b>

Оффер:
    💰 Цена товара: 1000 RUB
    💸 Ставка: 300 RUB

<b>📄 Описание оффера:</b>
Современная интернет-площадка для людей, ищущих серьезные отношения, а также для дружбы и простого общения с интересными собеседниками.

<b>Введите сумму для покупки рекламной кампании:</b>''', reply_markup=menu.otmena)
    await statess.Arbitr.q1.set()
    async with state.proxy() as data:
        data['pay'] = pay

@dp.callback_query_handler(text_startswith="traforice") 
async def a2(call:types.CallbackQuery):
    await call.message.edit_text('Выбранный оффер - <b>Poblizosti</b>\n\n💰 Цена товара: <b>1000 RUB</b>\n\n💸 Ставка: <b>300 RUB</b>\n\nВыберите источник <b>трафика</b>', reply_markup=menu.traforce5pay) 

@dp.callback_query_handler(text_startswith="traforiace")
async def a3(call:types.CallbackQuery,state:FSMContext):
    pay = call.data.split(",")[1]
    await call.message.edit_text('''Итоговая связка

🔗 Партнерская программа: <b>TRAFORCE</b>
<a href="https://mir-s3-cdn-cf.behance.net/projects/max_808/e935ba119855921.Y3JvcCwxOTk5LDE1NjQsMCwyMTc.png">📦</a> Оффер: <b>Poblizosti</b>

Оффер:
    💰 Цена товара: 1000 RUB
    💸 Ставка: 300 RUB

<b>📄 Описание оффера:</b>
Удобный и простой в использовании ресурс для знакомств в интернете.

<b>Введите сумму для покупки рекламной кампании:</b>''', reply_markup=menu.otmena) 
    await statess.Arbitr.q1.set()
    async with state.proxy() as data:
        data['pay'] = pay

@dp.message_handler(state=statess.Arbitr.q1)
async def spammers(message: types.Message,state:FSMContext):
    if message.text.isdigit():
        data = await state.get_data()
        with sqlite3.connect(bd) as c:
            info = c.execute("SELECT * FROM mamonts_arbitr WHERE id = ?", (message.from_user.id,)).fetchone()
        if info[3] >= int(data['pay']):
            if int(message.text) >= int(data['pay']):
                with sqlite3.connect(bd) as c:
                    c.execute('UPDATE mamonts_arbitr SET balance = balance - ? WHERE id = ?',(int(message.text),message.from_user.id,))
                msg = await message.answer(f'<b>Рекламная комания была запущена, ожидайте.</b>\n\n💰 Сумма вложений: <b>{message.text}</b> RUB\n✅ Сделано конверсий: <b>0</b>\n⏱ Время: <b>0/210</b> Секунд')
                next_id = msg.message_id
                conv = 0
                proc = 0
                if info[5] == 100:
                    for i in range (1, 270, 3):
                        if i % 5 == 0:
                            conv += 1
                            proc += 4
                        await bot.edit_message_text(chat_id=message.chat.id, message_id=next_id, text=f'<b>Рекламная комания была запущена, ожидайте.</b>\n\n💰 Сумма вложений: <b>{message.text}</b> RUB\n✅ Сделано конверсий: <b>{conv}</b>\n⏱ Время: <b>{i}/270</b> Секунд')
                        await asyncio.sleep(3)
                elif info[5] == 50:
                    for i in range (1, 270, 3):
                        if i % 8 == 0:
                            conv += 1
                            proc += 4
                        await bot.edit_message_text(chat_id=message.chat.id, message_id=next_id, text=f'<b>Рекламная комания была запущена, ожидайте.</b>\n\n💰 Сумма вложений: <b>{message.text}</b> RUB\n✅ Сделано конверсий: <b>{conv}</b>\n⏱ Время: <b>{i}/270</b> Секунд')
                        await asyncio.sleep(3)
                else:
                    for i in range (1, 270, 3):
                        if i % 13 == 0:
                            conv += 1
                            proc += 4
                        await bot.edit_message_text(chat_id=message.chat.id, message_id=next_id, text=f'<b>Рекламная комания была запущена, ожидайте.</b>\n\n💰 Сумма вложений: <b>{message.text}</b> RUB\n✅ Сделано конверсий: <b>{conv}</b>\n⏱ Время: <b>{i}/270</b> Секунд')
                        await asyncio.sleep(3)
                profit = (int(message.text) * (proc * 0.1)) - int(message.text)
                if profit <= 0:
                    with sqlite3.connect(bd) as c:
                        info = c.execute("SELECT * FROM mamonts_arbitr WHERE id = ?", (message.from_user.id,)).fetchone()
                    await bot.send_message(message.from_user.id, text=f'<b>✅ Кампания завершилась</b>\n\nДлительность компании:<b> 270 сек.</b>\nУдалось получить конверсий: <b>{conv}</b>\nПрибыль: <b>{math.ceil(profit)} RUB</b>\n\n💰 Ваш баланс: <b>{info[3]} Rub</b>')
                else:
                    with sqlite3.connect(bd) as c:
                        c.execute('UPDATE mamonts_arbitr SET balance = balance + ? WHERE id = ?',(math.ceil(profit),message.from_user.id,))
                        info = c.execute("SELECT * FROM mamonts_arbitr WHERE id = ?", (message.from_user.id,)).fetchone()
                    await bot.send_message(message.from_user.id, text=f'<b>✅ Кампания завершилась</b>\n\nДлительность компании:<b> 270 сек.</b>\nУдалось получить конверсий: <b>{conv}</b>\nПрибыль: <b>{math.ceil(profit)} RUB</b>\n\n💰 Ваш баланс: <b>{info[3]} Rub</b>')
            else:
                await message.answer(f'<b>❌ Сумма должна быть не меньше </b>' + data['pay'])
        else:
            await message.answer('🙅‍♂️ Ваш баланс меньше чем стоит товар.')
            await state.finish()
    else:
        await message.answer('<b>❌ Это не число</b>')
        await state.finish()

@dp.callback_query_handler(text_startswith="otmenilsuka",state="*") 
async def otmenaasuchka(call:types.CallbackQuery,state:FSMContext):
    await state.finish()
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id,'Отмененно') 

executor.start_polling(dp)
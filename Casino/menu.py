from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

mainkb = ReplyKeyboardMarkup(
    resize_keyboard=True,
	keyboard = [
        [
            KeyboardButton(text="☘️ Играть")
		],
		[
            KeyboardButton(text="Информация ℹ️"),
            KeyboardButton(text="Личный кабинет 🤳")
		]
	]
)

gamekb = ReplyKeyboardMarkup(
    resize_keyboard=True,
	keyboard = [
        [
            KeyboardButton(text="Кости 🎲")
		],
		[
            KeyboardButton(text="Числа 🔢"),
            KeyboardButton(text="Орёл & Решка")
		],
        [
            KeyboardButton(text="Назад")
		]
	]
)

pt1 = InlineKeyboardButton('Отменить', callback_data='otmenilsuka')
otmena = InlineKeyboardMarkup(row_width=1).add(pt1)

lk = InlineKeyboardMarkup(
	inline_keyboard = [
        [
            InlineKeyboardButton(text='⬆Пополнить', callback_data='popolnenie'),
            InlineKeyboardButton(text='⬇Вывести', callback_data='vivod')
        ]
	]
)

tp = InlineKeyboardMarkup(
	inline_keyboard = [
        [
            InlineKeyboardButton(text='Поддержка 👩‍💻', url='https://t.me/AlexTopMelbet')
		]
	]
)

pay = InlineKeyboardMarkup(
	inline_keyboard = [
        [
            InlineKeyboardButton(text='🥝 Киви', callback_data='qiwi_payments')
        ],
        [
            InlineKeyboardButton(text='💳 P2P перевод', callback_data='p2pcard')
		]
	]
)

def interval(amount) -> InlineKeyboardMarkup:
    biggest_50 = InlineKeyboardButton(text='> 50', callback_data=f'RandomNumberr,{amount},biggest')
    equals_50 = InlineKeyboardButton(text='= 50', callback_data=f'RandomNumberr,{amount},equals')
    smaller_50 = InlineKeyboardButton(text='< 50', callback_data=f'RandomNumberr,{amount},smaller')
    return InlineKeyboardMarkup(row_width=3).add(biggest_50, equals_50, smaller_50)

def coin(amount) -> InlineKeyboardMarkup:
    biggest_50 = InlineKeyboardButton(text='Орёл', callback_data=f'Coinflip,{amount},Orel')
    equals_50 = InlineKeyboardButton(text='Решка', callback_data=f'Coinflip,{amount},Reshka')
    return InlineKeyboardMarkup(row_width=3).add(biggest_50, equals_50)

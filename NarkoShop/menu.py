from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

mainkb = ReplyKeyboardMarkup(
    resize_keyboard=True,
	keyboard = [
		[
            KeyboardButton(text="Товары"),
            KeyboardButton(text="Отзывы"),
            KeyboardButton(text="Правила"),
            KeyboardButton(text="Мои заказы"),
		],
        [
            KeyboardButton(text="Найти город"),
            KeyboardButton(text="Работа"),
            KeyboardButton(text="Оператор"),
            KeyboardButton(text="Баланс")
		]
	]
)

town = InlineKeyboardMarkup(
    row_width = 2,
    inline_keyboard = [
        [
            InlineKeyboardButton(text="Москва", callback_data='town,1'),
            InlineKeyboardButton(text="Екатеринбург", callback_data='town,2'),
            InlineKeyboardButton(text="Симферополь", callback_data='town,3'),
            InlineKeyboardButton(text="Ярославль", callback_data='town,4'),
            InlineKeyboardButton(text="Пушкино", callback_data='town,5'),
            InlineKeyboardButton(text="Подольск", callback_data='town,6'),
            InlineKeyboardButton(text="Химки", callback_data='town,7'),
            InlineKeyboardButton(text="Мытищи", callback_data='town,8'),
            InlineKeyboardButton(text="Люберцы", callback_data='town,9'),
            InlineKeyboardButton(text="Казань", callback_data='town,10'),
            InlineKeyboardButton(text="Воронеж", callback_data='town,11'),
            InlineKeyboardButton(text="Омск", callback_data='town,12'),
            InlineKeyboardButton(text="Владивосток", callback_data='town,13'),
            InlineKeyboardButton(text="Новосибирск", callback_data='town,14'),
            InlineKeyboardButton(text="Нижний Новгород", callback_data='town,15'),
            InlineKeyboardButton(text="Севастополь", callback_data='town,16'),
            InlineKeyboardButton(text="Подольск", callback_data='town,17'),
            InlineKeyboardButton(text="Королёв", callback_data='town,18'),
            InlineKeyboardButton(text="Самара", callback_data='town,19'),
            InlineKeyboardButton(text="Орехово Зуево", callback_data='town,20'),
            InlineKeyboardButton(text="Саратов", callback_data='town,21'),
            InlineKeyboardButton(text="Ростов на Дону", callback_data='town,22'),
            InlineKeyboardButton(text="Хабаровск", callback_data='town,23'),
            InlineKeyboardButton(text="Санкт-Петербург", callback_data='town,24'),
            InlineKeyboardButton(text="Сыктывкар", callback_data='town,25'),
            InlineKeyboardButton(text="Тверь", callback_data='town,26'),
            InlineKeyboardButton(text="Уфа", callback_data='town,27'),
            InlineKeyboardButton(text="Краснодар", callback_data='town,28'),
            InlineKeyboardButton(text="Ульяновск", callback_data='town,29'),
            InlineKeyboardButton(text="Чебоксары", callback_data='town,30'),
            InlineKeyboardButton(text="Якутск", callback_data='town,31'),
            InlineKeyboardButton(text="Рязань", callback_data='town,32'),
            InlineKeyboardButton(text="Калуга", callback_data='town,33'),
            InlineKeyboardButton(text="Ташкент", callback_data='town,34'),
            InlineKeyboardButton(text="Сочи", callback_data='town,35'),
            InlineKeyboardButton(text="Пермь", callback_data='town,36'),
            InlineKeyboardButton(text="Ставрополь", callback_data='town,37'),
            InlineKeyboardButton(text="Челябинск", callback_data='town,38'),
            InlineKeyboardButton(text="Барнаул", callback_data='town,39'),
            InlineKeyboardButton(text="Красноярск", callback_data='town,40'),
            InlineKeyboardButton(text="Волгоград", callback_data='town,41'),
            InlineKeyboardButton(text="Иркутск", callback_data='town,42')
        ]
    ]
)
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

mainkb = ReplyKeyboardMarkup(
    resize_keyboard=True,
	keyboard = [
		[
            KeyboardButton(text="💼 Личный кабинет")
		],
        [
            KeyboardButton(text="ℹ Инфо"),
            KeyboardButton(text="🤵‍♂ Тех.Поддержка")
		],
        [
            KeyboardButton(text="🖥 Рекламная панель")
		]
	]
)

pt1 = InlineKeyboardButton('Отменить', callback_data='otmenilsuka')
otmena = InlineKeyboardMarkup(row_width=1).add(pt1)

pt1 = InlineKeyboardButton('✅ Принять правила', callback_data='SoglDa')
prinsogl = InlineKeyboardMarkup(row_width=1).add(pt1)

pt1 = InlineKeyboardButton('📄 Соглашение', url='https://telegra.ph/Polzovatelskoe-soglashenie-CPAnet-Arbitrage-05-26')
pt2 = InlineKeyboardButton('Личный кабинет', callback_data='lk')
goodsogl = InlineKeyboardMarkup(row_width=1).add(pt1,pt2)

lk = InlineKeyboardMarkup(
	inline_keyboard = [
        [
            InlineKeyboardButton(text='⬆Пополнить', callback_data='popolnenie'),
            InlineKeyboardButton(text='⬇Вывести', callback_data='vivod')
        ],
        [
            InlineKeyboardButton(text='✅Верификация', callback_data='verif')
		]
	]
)

tp = InlineKeyboardMarkup(
	inline_keyboard = [
        [
            InlineKeyboardButton(text='Поддержка 👩‍💻', url='https://t.me/CPAnet_Support_bot')
		]
	]
)


info = InlineKeyboardMarkup(
	inline_keyboard = [
        [
            InlineKeyboardButton(text='👩‍💻 Поддержка', url='https://t.me/CPAnet_Support_bot'),
            InlineKeyboardButton(text='📄 Соглашение', url='https://telegra.ph/Polzovatelskoe-soglashenie-CPAnet-Arbitrage-05-26')
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

pt1 = InlineKeyboardButton('M1-SHOP', callback_data='m1shop')
pt2 = InlineKeyboardButton('OFFERRUM',callback_data='offerrum')
pt3 = InlineKeyboardButton('TRAFORCE',callback_data='traforce')
partnerki = InlineKeyboardMarkup(row_width=1).add(pt1, pt2, pt3)


pt1 = InlineKeyboardButton('Подарочный винный набор SITITEK E-Wine Deluxe', callback_data='m1shoop')
pt2 = InlineKeyboardButton('Сушилка для белья напольная',callback_data='m1shoap')
pt3 = InlineKeyboardButton('WESS Декоративная подушка 40x40',callback_data='m1shosp')
pt4 = InlineKeyboardButton('Настольная лампа EUROSVET FRAME',callback_data='m1shoyp')
pt5 = InlineKeyboardButton('Vileda Turbo Easywring Clean Швабра',callback_data='m1shoip')
m1shop1 = InlineKeyboardMarkup(row_width=1).add(pt1, pt2, pt3, pt4, pt5)

pt1 = InlineKeyboardButton('Яндекс.Директ', callback_data='m1shooop,5490')
pt2 = InlineKeyboardButton('Google AdWords',callback_data='m1shooop,5490')
pt3 = InlineKeyboardButton('Социальные сети',callback_data='m1shooop,5490')
m1shop1pay = InlineKeyboardMarkup(row_width=1).add(pt1, pt2, pt3)

pt1 = InlineKeyboardButton('Яндекс.Директ', callback_data='m1shoaop,930')
pt2 = InlineKeyboardButton('Google AdWords',callback_data='m1shoaop,930')
pt3 = InlineKeyboardButton('Социальные сети',callback_data='m1shoaop,930')
m1shop2pay = InlineKeyboardMarkup(row_width=1).add(pt1, pt2, pt3)

pt1 = InlineKeyboardButton('Яндекс.Директ', callback_data='m1shosop,690')
pt2 = InlineKeyboardButton('Google AdWords',callback_data='m1shosop,690')
pt3 = InlineKeyboardButton('Социальные сети',callback_data='m1shosop,690')
m1shop3pay = InlineKeyboardMarkup(row_width=1).add(pt1, pt2, pt3)

pt1 = InlineKeyboardButton('Яндекс.Директ', callback_data='m1shoyop,5250')
pt2 = InlineKeyboardButton('Google AdWords',callback_data='m1shoyop,5250')
pt3 = InlineKeyboardButton('Социальные сети',callback_data='m1shoyop,5250')
m1shop4pay = InlineKeyboardMarkup(row_width=1).add(pt1, pt2, pt3)

pt1 = InlineKeyboardButton('Яндекс.Директ', callback_data='m1shoiop,2290')
pt2 = InlineKeyboardButton('Google AdWords',callback_data='m1shoiop,2290')
pt3 = InlineKeyboardButton('Социальные сети',callback_data='m1shoiop,2290')
m1shop5pay = InlineKeyboardMarkup(row_width=1).add(pt1, pt2, pt3)

pt1 = InlineKeyboardButton('Беспроводные наушники JBL Tune 115 TWS', callback_data='offerruom')
pt2 = InlineKeyboardButton('Игровая консоль Nintendo Switch New',callback_data='offerruam')
pt3 = InlineKeyboardButton('Очки виртуальной реальности Smarterra VR 3',callback_data='offerrusm')
pt4 = InlineKeyboardButton('Кольцевая лампа на штативе RGB',callback_data='offerruym')
pt5 = InlineKeyboardButton('Колонка портативная JBL Charge 4',callback_data='offerruim')
offerrum1 = InlineKeyboardMarkup(row_width=1).add(pt1, pt2, pt3, pt4, pt5)

pt1 = InlineKeyboardButton('Яндекс.Директ', callback_data='offerruoam,3000')
pt2 = InlineKeyboardButton('Google AdWords',callback_data='offerruoam,3000')
pt3 = InlineKeyboardButton('Социальные сети',callback_data='offerruoam,3000')
offerrum1pay = InlineKeyboardMarkup(row_width=1).add(pt1, pt2, pt3)

pt1 = InlineKeyboardButton('Яндекс.Директ', callback_data='offerruaom,23200')
pt2 = InlineKeyboardButton('Google AdWords',callback_data='offerruaom,23200')
pt3 = InlineKeyboardButton('Социальные сети',callback_data='offerruaom,23200')
offerrum2pay = InlineKeyboardMarkup(row_width=1).add(pt1, pt2, pt3)

pt1 = InlineKeyboardButton('Яндекс.Директ', callback_data='offerrusom,1590')
pt2 = InlineKeyboardButton('Google AdWords',callback_data='offerrusom,1590')
pt3 = InlineKeyboardButton('Социальные сети',callback_data='offerrusom,1590')
offerrum3pay = InlineKeyboardMarkup(row_width=1).add(pt1, pt2, pt3)

pt1 = InlineKeyboardButton('Яндекс.Директ', callback_data='offerruyom,4780')
pt2 = InlineKeyboardButton('Google AdWords',callback_data='offerruyom,4780')
pt3 = InlineKeyboardButton('Социальные сети',callback_data='offerruyom,4780')
offerrum4pay = InlineKeyboardMarkup(row_width=1).add(pt1, pt2, pt3)

pt1 = InlineKeyboardButton('Яндекс.Директ', callback_data='offerruiom,8990')
pt2 = InlineKeyboardButton('Google AdWords',callback_data='offerruiom,8990')
pt3 = InlineKeyboardButton('Социальные сети',callback_data='offerruiom,8990')
offerrum5pay = InlineKeyboardMarkup(row_width=1).add(pt1, pt2, pt3)

pt1 = InlineKeyboardButton('Kismia', callback_data='traforoce')
pt2 = InlineKeyboardButton('TakeMe Love',callback_data='traforace')
pt3 = InlineKeyboardButton('One Amour',callback_data='traforsce')
pt4 = InlineKeyboardButton('Vchate',callback_data='traforyce')
pt5 = InlineKeyboardButton('Poblizosti',callback_data='traforice')
traforce1 = InlineKeyboardMarkup(row_width=1).add(pt1, pt2, pt3, pt4, pt5)

pt1 = InlineKeyboardButton('Яндекс.Директ', callback_data='traforoace,1000')
pt2 = InlineKeyboardButton('Google AdWords',callback_data='traforoace,1000')
pt3 = InlineKeyboardButton('Социальные сети',callback_data='traforoace,1000')
traforce1pay = InlineKeyboardMarkup(row_width=1).add(pt1, pt2, pt3)

pt1 = InlineKeyboardButton('Яндекс.Директ', callback_data='traforaace,1000')
pt2 = InlineKeyboardButton('Google AdWords',callback_data='traforaace,1000')
pt3 = InlineKeyboardButton('Социальные сети',callback_data='traforaace,1000')
traforce2pay = InlineKeyboardMarkup(row_width=1).add(pt1, pt2, pt3)

pt1 = InlineKeyboardButton('Яндекс.Директ', callback_data='traforsace,1000')
pt2 = InlineKeyboardButton('Google AdWords',callback_data='traforsace,1000')
pt3 = InlineKeyboardButton('Социальные сети',callback_data='traforsace,1000')
traforce3pay = InlineKeyboardMarkup(row_width=1).add(pt1, pt2, pt3)

pt1 = InlineKeyboardButton('Яндекс.Директ', callback_data='traforyace,1000')
pt2 = InlineKeyboardButton('Google AdWords',callback_data='traforyace,1000')
pt3 = InlineKeyboardButton('Социальные сети',callback_data='traforyace,1000')
traforce4pay = InlineKeyboardMarkup(row_width=1).add(pt1, pt2, pt3)

pt1 = InlineKeyboardButton('Яндекс.Директ', callback_data='traforiace,1000')
pt2 = InlineKeyboardButton('Google AdWords',callback_data='traforiace,1000')
pt3 = InlineKeyboardButton('Социальные сети',callback_data='traforiace,1000')
traforce5pay = InlineKeyboardMarkup(row_width=1).add(pt1, pt2, pt3)

























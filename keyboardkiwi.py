from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton



topup=InlineKeyboardMarkup(row_width=1)
pop=InlineKeyboardButton(text="пополнить", callback_data="popolnit")
subscribechapters=InlineKeyboardButton(text="купить подписку на все манхвы", callback_data="subscribeALL")
topup.insert(pop)
topup.insert(subscribechapters)
btnreturnmenu=InlineKeyboardButton(text='вернуться в меню', callback_data='returnMenu')


def buy_menu(isUrl=True, url="", bill=""):
    qiwiMenu=InlineKeyboardMarkup(row_width=1)
    if isUrl:
        btnurlqiwi=InlineKeyboardButton(text="ссылка на оплату", url=url)
        qiwiMenu.insert(btnurlqiwi)
    btncheckqiwi = InlineKeyboardButton(text="проверить оплату", callback_data="check_"+bill)
    qiwiMenu.insert(btncheckqiwi)
    qiwiMenu.insert(btnreturnmenu)
    return qiwiMenu



confirmkb=InlineKeyboardMarkup(row_width=1)
confirmbtn=InlineKeyboardButton(text="ДА", callback_data="confirmpay")
confirmkb.insert(confirmbtn)
confirmkb.insert(btnreturnmenu)
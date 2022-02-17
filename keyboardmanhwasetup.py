from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
btnreturnmenu=InlineKeyboardButton(text='вернуться в меню', callback_data='returnMenu')




clava18=InlineKeyboardMarkup(row_width=5)
buy_pear2 = InlineKeyboardButton(text="убийца героев", callback_data="HeroKiller")
hent1 = InlineKeyboardButton(text="я забыл название но оно работает", callback_data="хент1")
clava18.insert(hent1)

clavaTOP = InlineKeyboardMarkup(row_width=1)

GreenLight=InlineKeyboardButton(text="Под зеленым светом", callback_data="GreenLight")
clavaTOP.insert(GreenLight)
clavaTOP.insert(btnreturnmenu)
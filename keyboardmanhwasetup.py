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
BjAlex=InlineKeyboardButton(text="Bj Alex", callback_data="BjAlex")
##########

VosHoz=InlineKeyboardButton(text="Воспитание хозяина", callback_data="VosHoz")
VrataAda=InlineKeyboardButton(text="Врата Ада", callback_data="VrataAda")
TigerLun=InlineKeyboardButton(text="Тигр, проглотивший луну", callback_data="TigerLun")
Killstalker=InlineKeyboardButton(text="Убить сталкера", callback_data="Killstalker")


clavaTOP.insert(GreenLight)
clavaTOP.insert(BjAlex)
clavaTOP.insert(VrataAda)
clavaTOP.insert(TigerLun)
clavaTOP.insert(Killstalker)
clavaTOP.insert(btnreturnmenu)

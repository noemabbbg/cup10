from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton






clava = InlineKeyboardMarkup(row_width=1)
btnreturnmenu=InlineKeyboardButton(text='вернуться в меню', callback_data='returnMenu')
buy_pear1 = InlineKeyboardButton(text="доступные манхвы", callback_data="топ")
buy_pear13=InlineKeyboardButton(text="манхвы 18+", callback_data="18+")
buy_pear15=InlineKeyboardButton(text="управление подпиской", callback_data="subscribemanagment")
clava.insert(buy_pear1)
#clava.insert(buy_pear13)
#clava.insert(buy_pear15)






clavaChangeState=InlineKeyboardMarkup(row_width=1)
buy_pear5 = InlineKeyboardButton(text="начать читать с начала", callback_data="начать с начала")
buy_pear6 = InlineKeyboardButton(text="я знаю с какой главы хочу читать", callback_data="поиск главы")
subscribe = InlineKeyboardButton(text="подписаться на выход новой главы", callback_data="subscribeNew")
download=InlineKeyboardButton(text="прислать все главы сразу", callback_data="download")
clavaChangeState.insert(buy_pear5)
clavaChangeState.insert(buy_pear6)
clavaChangeState.insert(subscribe)
#clavaChangeState.insert(download)
clavaChangeState.insert(btnreturnmenu)



nextchapter=InlineKeyboardMarkup(row_width=1)
buy_pear7 = InlineKeyboardButton(text="next", callback_data="next")
buy_pear8 = InlineKeyboardButton(text="найти другую главу", callback_data="поиск главы")
nextchapter.insert(buy_pear7)
nextchapter.insert(buy_pear8)
nextchapter.insert(btnreturnmenu)



checkSubm=InlineKeyboardMarkup(row_width=1)
btnurlchannel= InlineKeyboardButton(text='подписаться', url='https://t.me/manhwastorage')
btndonesub=InlineKeyboardButton(text='я подписался', callback_data='саб')
checkSubm.insert(btnurlchannel)
checkSubm.insert(btndonesub)


cancelsub=InlineKeyboardMarkup(row_width=1)
btncancel=InlineKeyboardButton(text="отменить?", callback_data="cancelmanhwasub")
cancelsub.insert(btncancel)
cancelsub.insert(btnreturnmenu)



returN=InlineKeyboardMarkup(row_width=1)
returN.insert(btnreturnmenu)

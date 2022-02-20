import asyncio
import logging
import unittest
import random
from collections import defaultdict
import manhwaclass
import aiogram_broadcaster
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.utils.emoji import emojize
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions
from aiogram.types import Message, CallbackQuery
from config import TOKEN, MY_ID, channel_id, QIWI_TOKEN
import keyboardkiwi
import keyboardmainmenu
import keyboardmanhwasetup
from keyboardmainmenu import clava, clavaChangeState, nextchapter, checkSubm, cancelsub, returN
from keyboardkiwi import topup, buy_menu, confirmkb
from keyboardmanhwasetup import clava18,clavaTOP
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from manhwaclass import stateManhwa, is_number
import dictant
from dictant import Maindict
import os
from mysql.connector import MySQLConnection
from aiogram_broadcaster import TextBroadcaster
from aiogram_broadcaster import MessageBroadcaster
from aiogram.dispatcher import FSMContext
from db import Database, get
from pyqiwip2p import QiwiP2P
from pathlib import Path

db=Database('yaoibase.db')
S=stateManhwa()
storage=MemoryStorage()
p2p=QiwiP2P(auth_key=QIWI_TOKEN)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)
def check_sub_channel(chat_member):
    if chat_member['status']!='left':
        return True
    else:
        return False
#####блок рассылки#####
async def subchanneldone(message: types.Message):
    await bot.send_message('133886300', text="broadcast1337 sheesh")
@dp.message_handler(commands=['sheesh'])
async def subchanneldone(message: types.Message):
    await bot.send_message('133886300', text=get.get_user(1))

@dp.message_handler(commands=['norqo'])
async def subchanneldone(message: types.Message):
    await bot.send_message('133886300', text='/broadcastboxer /broadcastsuicideboy /broadcastsuicideboy /broadcastbastard /broadcastantifanatka /broadcastqueenwithscalpel /broadcastodnazhprinc /broadcastchertovka /broadcast1337 /sheesh /start')
@dp.message_handler(commands=['broadcast1337'])
async def broadcast_command_handler(msg: Message, state: FSMContext):
    await msg.answer('Введите текст для начала рассылки:')
    await state.set_state('broadcast_text1')
async def start_broadcast(msg: Message, state: FSMContext):
   
    await state.finish()
    storage = state.storage 
    #users=get.get_user(k)
    await MessageBroadcaster((get.get_user(1)), msg).run()
dp.register_message_handler(broadcast_command_handler, commands='broadcast1337')
dp.register_message_handler(start_broadcast, state='broadcast_text1', content_types=types.ContentTypes.ANY)



#####блок рассылки#####

#####блок баланса, пополнения#####
@dp.message_handler(commands=['balance'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id, f"СЧЕТ: {db.user_money(message.from_user.id)} руб.", reply_markup=topup)
@dp.callback_query_handler(text_contains="popolnit")
async def process_video_command(call: CallbackQuery): 
    
    message_money=100
    comment=str(call.message.from_user.id) +"_"+ str(random.randint(1000,9999))
    bill=p2p.bill(amount=message_money, lifetime=15, comment=comment)
    db.add_check(call.message.from_user.id, message_money,bill.bill_id)
    await bot.send_message(call.from_user.id, "пополнение на месячную подписку будет 100 рублей",  reply_markup=buy_menu(url=bill.pay_url, bill=bill.bill_id))
       
@dp.callback_query_handler(text="subscribemanagment")
async def chet(call: CallbackQuery):
    if db.state_subscribe(call.from_user.id)==1:
        await bot.send_message(call.from_user.id, text="у вас уже есть подписка и она дейсвтует до:")
    else:
        await bot.send_message(call.from_user.id, f"сейчас на твоем балансе: {db.user_money(call.from_user.id)} руб.")
        await bot.send_message(call.from_user.id, "подписка дает доступ к самым последним главам таких манхв как:  чтобы ее купить нужно пополнить счет на 100рублей и купить по кнопке :)", reply_markup=topup)
@dp.callback_query_handler(text_contains="check_")
async def process_video_command(call: CallbackQuery):
    bill=str(call.data[6:])
    info=db.get_check(bill)
    print(info)
    if info!=False:
        if str(p2p.check(bill_id=bill).status)== "PAID":
            user_money=db.user_money(call.from_user.id)
            money=int(info[2])
            print(money)
            db.set_money(call.from_user.id, user_money+money)
            await bot.send_message(call.from_user.id, f"ваш счет пополнен на: {money} и теперь он составляет: {user_money}")
        else:
            await bot.send_message(call.from_user.id,text="счет не оплачен чел ало", reply_markup=buy_menu(False,bill=bill))
    else:
        await bot.send_message(call.from_user.id,text="счет не найден")


@dp.callback_query_handler(text="subscribeALL")
async def process_video_command(call: CallbackQuery):
    await bot.send_message(call.from_user.id,text="подписка стоит 100рублей, с баланса спишется 100. Подтверждаем?",reply_markup=confirmkb)

@dp.callback_query_handler(text="confirmpay")   
async def da(message:types.Message):
        if (db.user_money(message.from_user.id)==100 or db.user_money(message.from_user.id)>100):
            newmoney=db.user_money(message.from_user.id)-100
            db.pay_subcribe(message.from_user.id, newmoney)
            subscribe=1
            await bot.send_message(message.from_user.id, text="поздравляю, вы приобрели подписку на месяц")
            print(db.state_subscribe(message.from_user.id))
            db.add_subscribe(message.from_user.id, subscribe)
            print(db.add_subscribe(message.from_user.id, subscribe))
        else:
            await bot.send_message(message.from_user.id, text="мало денег чел", reply_markup=topup)

#####блок баланса, пополнения#####

#####блок старта и основного функционала#####
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    #await bot.send_message('133886300', Herokiller)
    if check_sub_channel(await bot.get_chat_member(chat_id=channel_id, user_id=message.from_user.id)):
        if not (db.user_exists(message.from_user.id)):
            db.add_user(message.from_user.id)
            await bot.send_message(message.from_user.id, text="привет! сейчас бот работает в тестовом режиме и я буду очень рад, если ты напишешь мне обратную свзяь по работе бота, спасибо! @bububucheel",reply_markup=clava)
        
        else:
            await bot.send_message(message.from_user.id, text="привет! сейчас бот работает в тестовом режиме и я буду очень рад, если ты напишешь мне обратную свзяь по работе бота, спасибо! @bububucheel ",reply_markup=clava)
            if not (db.user_exists(message.from_user.id)):
                db.add_user(message.from_user.id)
    else:
         await bot.send_message(message.from_user.id, 'подписка чек', reply_markup=checkSubm)
         if not (db.user_exists(message.from_user.id)):
            db.add_user(message.from_user.id)

@dp.callback_query_handler(text_contains="returnMenu")
async def process_video_command(call: CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer(text="буду рад обратной связи :) @bububucheel",reply_markup=clava)
    buffer=0
    db.addbuffer(call.from_user.id, buffer)
    db.addsearch(call.from_user.id, buffer)

@dp.callback_query_handler(text_contains="subscribeNew")    # подписка на выход новых глав чего-либо (реализовать в одном модуле)
async def broad(call:CallbackQuery):
    if db.statebuffer(call.from_user.id)==6:
        if db.state_broadcast_boxer(call.from_user.id)==0:
            boxerbroadcast=call.from_user.id
            db.add_user_broadcast_boxer(call.from_user.id, boxerbroadcast)
        else: 
            await call.message.answer("кажется ты уже подписан на выход этой манхвы, хочешь отменить?",reply_markup=cancelsub) #в этом блоке нужно дописаь и реализовать функционал отмены рассылки
        await call.message.answer("Мы пришлем тебе новую главу как только она выйдет! :)",reply_markup=cancelsub)
    elif db.statebuffer(call.from_user.id)==5:
        if db.state_broadcast_suicideboy(call.from_user.id)==0:
            suicideBoy=call.from_user.id
            db.add_user_broadcast_suicideboy(call.from_user.id, suicideBoy)
        else: 
            await call.message.answer("кажется ты уже подписан на выход этой манхвы, хочешь отменить?",reply_markup=cancelsub) #в этом блоке нужно дописаь и реализовать функционал отмены рассылки
        await call.message.answer("Мы пришлем тебе новую главу как только она выйдет! :)",reply_markup=cancelsub)
    elif db.statebuffer(call.from_user.id)==7:
        if db.state_broadcast_suicideboy(call.from_user.id)==0:
            bastard=call.from_user.id
            db.add_user_broadcast_suicideboy(call.from_user.id, bastard)
        else: 
            await call.message.answer("кажется ты уже подписан на выход этой манхвы, хочешь отменить?", reply_markup=cancelsub) #в этом блоке нужно дописаь и реализовать функционал отмены рассылки
        await call.message.answer("Мы пришлем тебе новую главу как только она выйдет! :)",reply_markup=cancelsub)
    elif db.statebuffer(call.from_user.id)==8:
        if db.state_broadcast_antifanatka(call.from_user.id)==0:
            bastard=call.from_user.id
            db.add_user_broadcast_antifanatka(call.from_user.id, bastard)
        else: 
            await call.message.answer("кажется ты уже подписан на выход этой манхвы, хочешь отменить?", reply_markup=cancelsub) #в этом блоке нужно дописаь и реализовать функционал отмены рассылки
        await call.message.answer("Мы пришлем тебе новую главу как только она выйдет! :)",reply_markup=cancelsub)
    elif db.statebuffer(call.from_user.id)==9:
        if db.state_broadcast_queenwithscalpel(call.from_user.id)==0:
            bastard=call.from_user.id
            db.add_user_broadcast_queenwithscalpel(call.from_user.id, bastard)
        else: 
            await call.message.answer("кажется ты уже подписан на выход этой манхвы, хочешь отменить?", reply_markup=cancelsub) #в этом блоке нужно дописаь и реализовать функционал отмены рассылки
        await call.message.answer("Мы пришлем тебе новую главу как только она выйдет! :)",reply_markup=cancelsub)
    elif db.statebuffer(call.from_user.id)==10:
        if db.state_broadcast_odnazhprinc(call.from_user.id)==0:
            bastard=call.from_user.id
            db.add_user_broadcast_odnazhprinc(call.from_user.id, bastard)
        else: 
            await call.message.answer("кажется ты уже подписан на выход этой манхвы, хочешь отменить?", reply_markup=cancelsub) #в этом блоке нужно дописаь и реализовать функционал отмены рассылки
        await call.message.answer("Мы пришлем тебе новую главу как только она выйдет! :)",reply_markup=cancelsub)
    elif db.statebuffer(call.from_user.id)==11:
        if db.state_broadcast_chertovka(call.from_user.id)==0:
            bastard=call.from_user.id
            db.add_user_broadcast_chertovka(call.from_user.id, bastard)
        else: 
            await call.message.answer("кажется ты уже подписан на выход этой манхвы, хочешь отменить?", reply_markup=cancelsub) #в этом блоке нужно дописаь и реализовать функционал отмены рассылки
        await call.message.answer("Мы пришлем тебе новую главу как только она выйдет! :)",reply_markup=cancelsub)






@dp.callback_query_handler(text_contains="cancelmanhwasub")
async def cancelsubfunc(call:CallbackQuery):
    if db.statebuffer(call.from_user.id)==6:
        if db.state_broadcast_boxer(call.from_user.id)==call.from_user.id:
            boxerbroadcast=0
            db.add_user_broadcast_boxer(call.from_user.id, boxerbroadcast)
        else: 
            await call.message.answer("отменили твою подписку!",reply_markup=returN) #в этом блоке нужно дописаь и реализовать функционал отмены рассылки
        await call.message.answer("твоя подписка  отменена")
    elif db.statebuffer(call.from_user.id)==5:
        if db.state_broadcast_suicideboy(call.from_user.id)==call.from_user.id:
            suicideBoy=0
            db.add_user_broadcast_suicideboy(call.from_user.id, suicideBoy)
        else: 
            await call.message.answer("отменили твою подписку!",reply_markup=returN) #в этом блоке нужно дописаь и реализовать функционал отмены рассылки
        await call.message.answer("твоя подписка отменена")
    elif db.statebuffer(call.from_user.id)==7:
        if db.state_broadcast_suicideboy(call.from_user.id)==call.from_user.id:
            bastard=0
            db.add_user_broadcast_suicideboy(call.from_user.id, bastard)
        else: 
            await call.message.answer("отменили твою подписку!", reply_markup=returN) #в этом блоке нужно дописаь и реализовать функционал отмены рассылки
        await call.message.answer("твоя подписка отменена")



@dp.callback_query_handler(text_contains="саб")
async def subfunc(call:CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"callback_data='{callback_data}'")
    if check_sub_channel(await bot.get_chat_member(chat_id=channel_id, user_id=call.from_user.id)):
        await call.message.answer(text="start", reply_markup=clava)
    else:
        await call.bot.send_message(call.from_user.id, 'Для просмотра сначала подпишись на канал', reply_markup=checkSubm)

@dp.callback_query_handler(text_contains="топ")
async def process_video_command(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"callback_data='{callback_data}'")
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer('🤔 что же выбрать', reply_markup=clavaTOP)

@dp.callback_query_handler(text_contains="18+")
async def process_video_command(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"callback_data='{callback_data}'")
    await call.message.answer('рейтинг популярных', reply_markup=clava18)


@dp.callback_query_handler(text_contains="поиск главы")
async def process_video_command(call: CallbackQuery):
    buffer=db.statebuffer(call.from_user.id) 
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"callback_data='{callback_data}'")
    await call.message.answer('доступные главы:')
    
    list_keys = list(Maindict[buffer].keys())
    list_keys.sort()
    await bot.send_message(call.from_user.id, text=(list_keys))
   
    await call.message.answer('введи номер главы с которой ты хочешь продолжить читать')
    @dp.message_handler()
    async def buffer(message: types.Message):
            buff=int(message.text)
            db.addsearch(message.from_user.id, buff)
            search=db.statesearch(message.from_user.id)
            buffer=db.statebuffer(message.from_user.id)
            user_id = message.from_user.id
            
            if buff==S.payfullChapters[buffer]:
                   if db.state_subscribe(message.from_user.id)==1:
                        try:
                            await bot.send_message(message.from_user.id, text='глава по подписке')
                            await bot.send_document(message.from_user.id, document=Maindict[buffer][search], reply_markup=nextchapter)
                        except:
                            await bot.send_message(message.from_user.id, text='кажется этой главы еще нет :(', reply_markup=clavaTOP)
                   else:
                        await bot.send_message(message.from_user.id, text='эта глава доступна по подписке')
            else:
                try:
                    await bot.send_document(message.from_user.id, document=Maindict[buffer][search], reply_markup=nextchapter)
                except:
                    await bot.send_message(message.from_user.id, text='кажется этой главы еще нет :(', reply_markup=clavaTOP)






@dp.callback_query_handler(text_contains="начать с начала")
async def process_video_command(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"callback_data='{callback_data}'")
    buffer=db.statebuffer(call.from_user.id)
    await call.message.answer('чтение с нулевой главы')
    await call.bot.send_document(call.from_user.id, document=Maindict[buffer][1], reply_markup=nextchapter)


@dp.callback_query_handler(text_contains="next")
async def nextSERIA(message:types.Message): 
    buffer=db.statebuffer(message.from_user.id)
    search1=db.statesearch(message.from_user.id)+1
    db.addsearch(message.from_user.id, search1)
    search=db.statesearch(message.from_user.id)
    try:
        await bot.send_document(message.from_user.id, Maindict[buffer][search], reply_markup=nextchapter) 
    except:
         await bot.send_message(message.from_user.id, text="кажется эта глава еще не добавлена :(,\n попробуй что нибудь другое", reply_markup=clavaTOP)

'''
@dp.callback_query_handler(text_contains="download")
async def process_video_command(call: CallbackQuery):
    buffer=db.statebuffer(call.from_user.id)
    for i in range(0,)
    await bot.send_document(call.from_user.id, Maindict[buffer][i]
'''
#####блок старта и основного функционала#####




#####блок callbackov манхв#####

@dp.callback_query_handler(text_contains="GreenLight")
async def process_video_command(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"callback_data='{callback_data}'")
    if check_sub_channel(await bot.get_chat_member(chat_id=channel_id, user_id=call.from_user.id)):
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.send_photo(call.from_user.id, caption='*Описание:* \n«…Я хочу воплотить ваш образ в скульптуре. В форме, что навеки останется неизменной". В городе, полном высотных зданий, Мэттью Рейнор, студент-скульптор, живет жизнью одиночки, изолировавшись от остального мира. Неожиданно он встречает на своем пути прекрасного мужчину по имени Цзинь Цинь-Ю и чувствует, что эта встреча была дарована ему самой судьбой. Мэттью делает мужчине предложение: стать моделью для его скульптуры. \n*Оценка на мангалибе: 4.94*\n яой', photo="AgACAgIAAxkDAAMCYg4cc4ayb2aB_wQeo2TOEg81aDMAAjy5MRtH43BIfZ4d3dVfkyEBAAMCAAN4AAMjBA", reply_markup=clavaChangeState, parse_mode="Markdown")
        #await call.message.answer(text='*Описание:* \nЯ стала злодейкой любовного романа. Думаете, меня что-то не устраивает? Нет, всё просто прекрасно. Статус дочери герцога даёт возможность жить в роскоши и комфорте, и я собираюсь извлечь всю выгоду из своего нынешнего положения. Но, хотя я не хочу идти по пути антагонистки, белой и пушистой тоже не буду. Мой жених изменил мне с главной героиней, поэтому я перепишу оригинальную историю и поставлю всех на колени. Эти ублюдки не стоят моих слёз. \n*оценка на мангалибе: 4.83*', reply_markup=clavaChangeState, parse_mode="Markdown")
        
    else:
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await call.bot.send_message(call.from_user.id, 'Для просмотра сначала подпишись на канал', reply_markup=checkSubm)
    buffer=1
    db.addbuffer(call.from_user.id, buffer)

@dp.callback_query_handler(text_contains="BjAlex")
async def process_video_command(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"callback_data='{callback_data}'")
    if check_sub_channel(await bot.get_chat_member(chat_id=channel_id, user_id=call.from_user.id)):
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.send_photo(call.from_user.id, caption='*Описание:* \nНам Дон Гюн является истинным фанатом. Он безвозвратно влюбился в BJ Алекса, который транслирует порно для геев. Каждый раз смотря, как он мастурбирует во время своей трансляции, Нам Дон Гюн фантазирует о сексе с ним… Однажды он замечает у популярного президента студсовета Ан Джи Вона такое же, как у Алекса, пятно на животе в форме бабочки. Воплотятся ли его фантазии в реальность?\n*Оценка на мангалибе: 4.86*\n ', photo="AgACAgIAAxkDAAPPYg6ndFTDu2wk_mnbJqEX5u6xSBkAAhC5MRtH43hIzVBGcRRKxXEBAAMCAAN4AAMjBA", reply_markup=clavaChangeState, parse_mode="Markdown")
        #await call.message.answer(text='*Описание:* \nЯ стала злодейкой любовного романа. Думаете, меня что-то не устраивает? Нет, всё просто прекрасно. Статус дочери герцога даёт возможность жить в роскоши и комфорте, и я собираюсь извлечь всю выгоду из своего нынешнего положения. Но, хотя я не хочу идти по пути антагонистки, белой и пушистой тоже не буду. Мой жених изменил мне с главной героиней, поэтому я перепишу оригинальную историю и поставлю всех на колени. Эти ублюдки не стоят моих слёз. \n*оценка на мангалибе: 4.83*', reply_markup=clavaChangeState, parse_mode="Markdown")
        
    else:
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await call.bot.send_message(call.from_user.id, 'Для просмотра сначала подпишись на канал', reply_markup=checkSubm)
    buffer=2
    db.addbuffer(call.from_user.id, buffer)

@dp.callback_query_handler(text_contains="VrataAda")
async def process_video_command(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"callback_data='{callback_data}'")
    if check_sub_channel(await bot.get_chat_member(chat_id=channel_id, user_id=call.from_user.id)):
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.send_photo(call.from_user.id, caption='*Описание:* Шокирующий способ открыть врата в Ад! Когда всё получится, вам понравится, но войдя туда, вас это не порадует.\n\n*Оценка на мангалибе: 4.92*\n ', photo="AgACAgIAAxkDAAID-2ISp4Zc2kNJfJpnAWOAkX5b2lg5AALsuTEb8qiRSCiSuHcktCW3AQADAgADeAADIwQ", reply_markup=clavaChangeState, parse_mode="Markdown")
        #await call.message.answer(text='*Описание:* \nЯ стала злодейкой любовного романа. Думаете, меня что-то не устраивает? Нет, всё просто прекрасно. Статус дочери герцога даёт возможность жить в роскоши и комфорте, и я собираюсь извлечь всю выгоду из своего нынешнего положения. Но, хотя я не хочу идти по пути антагонистки, белой и пушистой тоже не буду. Мой жених изменил мне с главной героиней, поэтому я перепишу оригинальную историю и поставлю всех на колени. Эти ублюдки не стоят моих слёз. \n*оценка на мангалибе: 4.83*', reply_markup=clavaChangeState, parse_mode="Markdown")
        
    else:
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await call.bot.send_message(call.from_user.id, 'Для просмотра сначала подпишись на канал', reply_markup=checkSubm)
    buffer=3
    db.addbuffer(call.from_user.id, buffer)

@dp.callback_query_handler(text_contains="TigerLun")
async def process_video_command(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"callback_data='{callback_data}'")
    if check_sub_channel(await bot.get_chat_member(chat_id=channel_id, user_id=call.from_user.id)):
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.send_photo(call.from_user.id, caption='*Описание:* Квак Тхебом — член национальной сборной по стрельбе из оружия, золотой медалист олимпийских игр. Но несмотря на идеальную жизнь, Тхебома сбивает машина, а виновник скрывается с места преступления. Первое, что видит наш бедняга после того, как приходит в чувства — «высокого дядю» Ру Нейтана, который скрывает свою личность. Но на самом деле «дядя»…вампир?!\n\n*Оценка на мангалибе: 4.6*\n ', photo="AgACAgIAAxkDAAID-GISp4W5QaWC4iXOLwh8TMGbp6oYAALpuTEb8qiRSNCoHusj7kJqAQADAgADeAADIwQ", reply_markup=clavaChangeState, parse_mode="Markdown")
        #await call.message.answer(text='*Описание:* \nЯ стала злодейкой любовного романа. Думаете, меня что-то не устраивает? Нет, всё просто прекрасно. Статус дочери герцога даёт возможность жить в роскоши и комфорте, и я собираюсь извлечь всю выгоду из своего нынешнего положения. Но, хотя я не хочу идти по пути антагонистки, белой и пушистой тоже не буду. Мой жених изменил мне с главной героиней, поэтому я перепишу оригинальную историю и поставлю всех на колени. Эти ублюдки не стоят моих слёз. \n*оценка на мангалибе: 4.83*', reply_markup=clavaChangeState, parse_mode="Markdown")
        
    else:
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await call.bot.send_message(call.from_user.id, 'Для просмотра сначала подпишись на канал', reply_markup=checkSubm)
    buffer=4
    db.addbuffer(call.from_user.id, buffer)


@dp.callback_query_handler(text_contains="Killstalker")
async def process_video_command(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"callback_data='{callback_data}'")
    if check_sub_channel(await bot.get_chat_member(chat_id=channel_id, user_id=call.from_user.id)):
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.send_photo(call.from_user.id, caption='*Описание:*Юн Бум одержим своим однокурсником О Сану и везде тайно за ним следует. Однако у Сану есть маленький секрет, и когда Юн Бум случайно его раскрывает... его жизнь подвергается настоящей опасности! \n\n*Оценка на мангалибе: 4.49*\n ', photo="AgACAgIAAxkDAAID-WISp4VhenAk13_ZLnl2UF2Ihh_3AALquTEb8qiRSIN7gpJ69mTIAQADAgADeAADIwQ", reply_markup=clavaChangeState, parse_mode="Markdown")
        #await call.message.answer(text='*Описание:* \nЯ стала злодейкой любовного романа. Думаете, меня что-то не устраивает? Нет, всё просто прекрасно. Статус дочери герцога даёт возможность жить в роскоши и комфорте, и я собираюсь извлечь всю выгоду из своего нынешнего положения. Но, хотя я не хочу идти по пути антагонистки, белой и пушистой тоже не буду. Мой жених изменил мне с главной героиней, поэтому я перепишу оригинальную историю и поставлю всех на колени. Эти ублюдки не стоят моих слёз. \n*оценка на мангалибе: 4.83*', reply_markup=clavaChangeState, parse_mode="Markdown")
        
    else:
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await call.bot.send_message(call.from_user.id, 'Для просмотра сначала подпишись на канал', reply_markup=checkSubm)
    buffer=5
    db.addbuffer(call.from_user.id, buffer)

#####блок callbackov манхв конец#####





























































if __name__ == '__main__':
    executor.start_polling(dp)







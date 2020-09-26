#!/bin/python3
import telebot
import requests
import json
import urllib.parse


class isheet:
    """
    rc_mark: a marks that we will sent
    tid: sheets'es id
    sid: sheet's name
    surl: sheet's api url
    google_token: a token that can used in refresh token
    tgbot_token: a bot's token, nothing interesting
    """
    rc_mark = {'П', 'Н', 'Б', 'О'}
    tid = '1m9z7XD6eIDdGeKSyOtzVDdsLpUdkbn4wEN9Krt5aP0g'
    sid = 'БНГ-001'
    surl = f"https://sheets.googleapis.com/v4/spreadsheets/{tid}/values/{sid}"
    google_token = '1//0ckdqe3fJ4-LRCgYIARAAGAwSNwF-L9IrmPKSdeA2eL0DzmYocxM9J5oENiVZZzcfSix2f9DtcdmC89OJbimZdoWiSuCfu5ikeVc'
    tgbot_token = "1277500164:AAEkU8DbjZX0E6wRa3JDKUKumIjlOuSLsRM"
    url_token = "https://oauth2.googleapis.com/token"
    gclient_id = "173493138930-85ifhekbvi7iak312hvbcok3f8466hn6.apps.googleusercontent.com"
    gclient_secret = "wVPZmRRZquXcrcZ53Ygryj7C"

    def __init__(self, access_token):
        self.acc_token = access_token


class get_new_token:
    payload = f"client_id={isheet.gclient_id}&client_secret={isheet.gclient_secret}&grant_type=refresh_token&refresh_token={isheet.google_token}"
    headers = {
        'charset': 'UTF-8',
        'Content-Type': 'application/x-www-form-urlencoded'
    }


tg = telebot.TeleBot(isheet.tgbot_token)
keyboard_main_menu = telebot.types.ReplyKeyboardMarkup()
keyboard_main_menu.row('Выгрузить таблицу', 'Закрыть')
remove_main_menu = telebot.types.ReplyKeyboardRemove()
keyboard_students_menu = telebot.types.ReplyKeyboardMarkup()
keyboard_students_menu.row('Присутствует', 'Отсутствует')
keyboard_students_menu.add('Болеет', 'Отчислен')
keyboard_students_menu.add('Главное меню')
remove_students_menu = telebot.types.ReplyKeyboardRemove()
keyboard_rollCall = telebot.types.ReplyKeyboardMarkup()
keyboard_rollCall.row('Начать перекличку', 'Открыть Таблицу')
keyboard_rollCall.add('Главное меню')
keyboard_link_sheet_menu = telebot.types.ReplyKeyboardMarkup()
keyboard_link_sheet_menu.row("гиперссылка", "Отмена")
tableupload = "Делаются запросы, делается структурка, вместо такого сообщения можно вывести список студентов и " \
              "подсчёт их пропусков "
turl = "https://docs.google.com/spreadsheets/d/1m9z7XD6eIDdGeKSyOtzVDdsLpUdkbn4wEN9Krt5aP0g/edit#gid=0"


@tg.message_handler(commands=['get_token'])
def gtoken(message):
    tg.send_message(message.chat.id, "Токен обновлён.")
    rtest = requests.request("POST", isheet.url_token, headers=get_new_token.headers, data=get_new_token.payload)
    prtest = json.loads(rtest.text)
    access_token = prtest['access_token']
    return access_token


@tg.message_handler(commands=['start'])
def sendFirstMessage(message):
    tg.send_message(message.chat.id, "Внимание!\nРаботать ТОЛЬКО последовательно по менюшкам, потому что пока что"
                                     " всё сделано сплошными условиями, т.е. хрень может получится,"
                                     " НЕ НАДО включать сейчас режим тестирование головного мозга"
                                     " (это шутка)\nUPD:Забыл добавить выбор дисциплины и выбор группы/направления,"
                                     "но это поправимо считтаю", reply_markup=keyboard_main_menu)


@tg.message_handler(content_types=['text'])
def sendText(tmessage):
    if tmessage.text.lower() == "выгрузить таблицу":
        global access_token
        access_token = gtoken(tmessage)
        gtest = requests.get(f"{isheet.surl}!A:A?access_token={access_token}")
        grtest = json.loads(gtest.text)
        print(grtest)
        FIO = list(grtest['values'])
        # print(FIO)
        for i in range(len(FIO)):
            FIO[i] = ''.join(map(str, FIO[i][0]))

        kList = '\n'.join(FIO[1:])
        print(kList)
        tg.send_message(tmessage.chat.id, kList,
                        reply_markup=keyboard_rollCall)
    elif tmessage.text == "Закрыть":
        tg.send_message(tmessage.chat.id, "Ну, видимо не сегодня", reply_markup=remove_main_menu)
    elif tmessage.text == 'Начать перекличку':
        # full_data = ' '.join(FIO)
        # print(full_data)
        tg.send_message(tmessage.chat.id, "Здесь каждый раз будет выводиться студент, его посещаемость и"
                                          " при нажатии на одну из кнопок, будет совершаться переход к"
                                          " следующему", reply_markup=keyboard_students_menu)
    elif tmessage.text == 'Присутствует':
        tg.send_message(tmessage.chat.id, "Ну тип присутствует и происходит переход к следующему по порядку студенту")
    elif tmessage.text == 'Отсутствует':
        tg.send_message(tmessage.chat.id, "Ну тип отсутствует и происходит переход к следующему по порядку студенту")
    elif tmessage.text == 'Болеет':
        tg.send_message(tmessage.chat.id, "Ну тип болеет и происходит переход к следующему по порядку студенту")
    elif tmessage.text == 'Отчислен/Переведён':
        tg.send_message(tmessage.chat.id, "Ну тип отчислен или переведён и происходит переход к следующему по порядку "
                                          "студенту")
    elif tmessage.text == 'Главное меню':
        sendFirstMessage(tmessage)
    elif tmessage.text == 'Открыть Таблицу':
        markup = telebot.types.InlineKeyboardMarkup()
        btn_my_site = telebot.types.InlineKeyboardButton(text='Наш сайт', url=turl)
        markup.add(btn_my_site)
        tg.send_message(tmessage.chat.id, "Ссылка на Таблицу с посещением", reply_markup=markup)
    else:
        tg.send_message(tmessage.chat.id, "Я тебя не понимаю")


tg.polling()

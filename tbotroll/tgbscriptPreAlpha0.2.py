#!/bin/python3
import telebot
import requests
import json
import os

global nInfo1
global nInfo2
groupFile = "Groups.txt"
subjectFile = "Subjects.txt"
sGroupFile = "sGroups.txt"
urlFile = "urls.txt"
dUpdate_text = "Удалить файлы - удаление существующих файлов\n\n"
dOpen_text = "Открыть файлы - которые возможно открыть и посмотреть их содержимое\n\n"
dCancel_text = "Главное меню - возврат на главное меню"
rGroup_text = "Группы - список групп, учащихся у тебя\n\n"
rSubject_text = "Дисциплины - список дисциплин, что ты ведёшь\n\n"
rLink_text = "Ссылки - список ссылок на доки с более подробной информацией о каждой группе\n\n"
rCancel_text = "Главное меню - возврат на главное меню"
unresolved_message = "На всякую хрень не отвечаю, якобы отсутствие чувств проявляю, оскорблять не стоит🗿🗿🗿"


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
    tid = ''
    sid1 = '1сем-Осень'
    sid2 = '2сем-Весна'
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


'''Межменюшные клавиатуры'''
tg = telebot.TeleBot(isheet.tgbot_token)
keyboard_main_menu = telebot.types.ReplyKeyboardMarkup()
keyboard_main_remove = telebot.types.ReplyKeyboardRemove()
keyboard_main_menu.row('Начать')
keyboard_main_menu.add('Настройки файлов', 'Закрыть')
keyboard_update_menu = telebot.types.ReplyKeyboardMarkup()
keyboard_update_remove = telebot.types.ReplyKeyboardRemove()
keyboard_update_menu.row("Удалить файлы", "Открыть файлы")
keyboard_update_menu.add("Главное меню", "")
keyboard_read_menu = telebot.types.ReplyKeyboardMarkup()
keyboard_read_remove = telebot.types.ReplyKeyboardRemove()
keyboard_read_menu.row("Группы", "Дисциплины")
keyboard_read_menu.add("Ссылки", "Главное меню")
keyboard_choose_group = telebot.types.ReplyKeyboardMarkup()

'''Клавы в текстовых сообщениях бота'''


def addFile(Groups, Subjests, sGroups, Urls):
    print('а это внутри функции...')
    _Groups = json.loads(Groups.text)
    _Subjests = json.loads(Subjests.text)
    _sGroups = json.loads(sGroups.text)
    _Urls = json.loads(Urls.text)
    ff1 = _Groups['values'][1:]
    with open(f"iFiles/{groupFile}", "w+") as file:
        print(ff1)
        for line in ff1:
            f = " ".join(line)
            file.write(f + '\n')
    file.close()
    ff2 = _Subjests['values'][1:]
    with open(f"iFiles/{subjectFile}", "w+") as file:
        print(ff2)
        for line in ff2:
            f = " ".join(line)
            file.write(f + '\n')
    file.close()
    ff3 = _sGroups['values'][1:]
    with open(f"iFiles/{sGroupFile}", "w+") as file:
        print(ff3)
        for line in ff3:
            f = " ".join(line)
            file.write(f + '\n')
    file.close()
    ff4 = _Urls['values'][1:]
    with open(f"iFiles/{urlFile}", "w+") as file:
        print(ff4)
        for line in ff4:
            f = " ".join(line)
            file.write(f + '\n')
    file.close()


@tg.message_handler(commands=['get_token'])
def gtoken(message):
    rtest = requests.request("POST", isheet.url_token, headers=get_new_token.headers, data=get_new_token.payload)
    prtest = json.loads(rtest.text)
    access_token = prtest['access_token']
    print(access_token)
    return access_token


@tg.message_handler(commands=['start'])
def sendFirstMessage(message):
    global access_token
    fStartText = "Привет, давай начнём работу\n"
    mid = message.chat.id
    dirList = list(os.listdir("iFiles"))
    if urlFile in dirList:
        gmsg = tg.send_message(mid, f"{fStartText}\nФайлы в порядке, можно работать", reply_markup=keyboard_main_menu)
        tg.register_next_step_handler(gmsg, main_choice_menu)
    else:
        bmsg = tg.send_message(mid, f"{fStartText}\nОтсутствуют файлы для работы, отправь мне"
                                    f"ссылку на Таблицу, введя ссылку в"
                                    f"поле ввода, она находится ниже, рекомендуется"
                                    f"перед отправкой убедиться, что доступ к Таблице у "
                                    f"бота имеется, ссылка корректна и имеет актуальный "
                                    f"айди Таблицы", reply_markup=keyboard_main_remove)
        access_token = gtoken(message)
        tg.register_next_step_handler(bmsg, getUrl)


def delete_files(umessage):
    uid = umessage.chat.id
    os.remove(f"iFiles/{groupFile}")
    os.remove(f"iFiles/{subjectFile}")
    os.remove(f"iFiles/{sGroupFile}")
    os.remove(f"iFiles/{urlFile}")
    checkpoint = tg.send_message(uid, "Удаление прошло успешно")
    tg.register_next_step_handler(checkpoint, main_setting_menu)


def main_setting_menu(smessage):
    sid = smessage.chat.id
    if smessage.text == "Удалить файлы":
        delete_files(smessage)
    elif smessage.text == "Открыть файлы":
        checkpoint = tg.send_message(sid, "Вывод содержимого файлов", reply_markup=keyboard_read_menu)
        tg.register_next_step_handler(checkpoint, read_files)
    elif smessage.text == "Главное меню":
        sendFirstMessage(smessage)

    else:
        checkpoint = tg.send_message(sid, unresolved_message)
        tg.register_next_step_handler(checkpoint, main_setting_menu)


def read_files(message):
    rid = message.chat.id
    if message.text == "Группы":
        if os.path.isfile(f'iFiles/{groupFile}'):
                rGroup = open(f'iFiles/{groupFile}', 'r')
                rgStr = ''.join(rGroup.readlines())
                rGroup.close()
                if rgStr:
                    checkpoint = tg.send_message(rid, rgStr)
                else:
                    checkpoint = tg.send_message(rid, "Файл пуст")

        else:
            checkpoint = tg.send_message(rid, "Файла нету")
        tg.register_next_step_handler(checkpoint, read_files)
    elif message.text == "Дисциплины":
        if os.path.isfile(f'iFiles/{subjectFile}'):
                rSubject = open(f'iFiles/{subjectFile}', 'r')
                rsStr = ''.join(rSubject.readlines())
                rSubject.close()
                if rsStr:
                    checkpoint = tg.send_message(rid, rsStr)
                else:
                    checkpoint = tg.send_message(rid, "Файл пуст")

        else:
            checkpoint = tg.send_message(rid, "Файла нету")
        tg.register_next_step_handler(checkpoint, read_files)
    elif message.text == "Главное меню":
        sendFirstMessage(message)
    elif message.text == "Ссылки":
        if os.path.isfile(f'iFiles/{subjectFile}'):
                rUrl = open(f'iFiles/{urlFile}', 'r')
                ruStr = ''.join(rUrl.readlines())
                rUrl.close()
                if ruStr:
                    checkpoint = tg.send_message(rid, ruStr)
                else:
                    checkpoint = tg.send_message(rid, "Файл пуст")

        else:
            checkpoint = tg.send_message(rid, "Файла нету")
        tg.register_next_step_handler(checkpoint, read_files)
    else:
        checkpoint = tg.send_message(rid, unresolved_message)
        tg.register_next_step_handler(checkpoint, read_files)
# rSubject = open(f'iFiles/{subjectFile}', 'r')
# rsGroup = open(f'iFiles/{sGroupFile}', 'r')


def choose_sheet(mid, includeData):
    try:
        idResult = requests.get(includeData)
        sheetsList = []
        idJSON = json.loads(idResult.text)
        for i in range(len(idJSON['sheets'])):
            sheetsList.append(idJSON['sheets'][i]['properties']['title'])
        print(sheetsList)
        inline_keyboard_choice_sheet = telebot.types.ReplyKeyboardMarkup()
        for i in range(len(sheetsList)):
            inline_keyboard_choice_sheet.add(f"{sheetsList[i]}")
        checkpoint = tg.send_message(mid, "Эта клавиатура создаётся динамически исходя из первого сделанного"
                                          " запроса, после него мы выбираем на какой лист отправлять запрос и на основе какого "
                                          "листа формировать файлы", reply_markup=inline_keyboard_choice_sheet)
        tg.register_next_step_handler(checkpoint, load_sheet)
    except:
        checkpoint = tg.send_message(mid, f"Ошибка {idResult.status_code}, попробуй ещё раз"
                                          f"через /start")


def load_sheet(message):
    lid = message.chat.id
    lsheet_name = message.text
    tg.send_message(lid, f"Ну {lsheet_name} так {lsheet_name}")
    try:
        surl1 = f"https://sheets.googleapis.com/v4/spreadsheets/{tid}/values/{lsheet_name}"
        tg.send_message(lid, "Попытка загрузки...")
        rGroup = requests.get(f"{surl1}!A:A?access_token={access_token}")
        rSubject = requests.get(f"{surl1}!B:B?access_token={access_token}")
        rLink = requests.get(f"{surl1}!C:C?access_token={access_token}")
        rShortGroup = requests.get(f"{surl1}!D:D?access_token={access_token}")
        if rLink.status_code == 200:
            addFile(rGroup, rSubject, rShortGroup, rLink)
            tg.send_message(lid, "Успешно")
            sendFirstMessage(message)
    except:
        checkpoint = tg.send_message(lid, f"Не успешно, {rLink.status_code}, попробуй ещё раз")
        tg.register_next_step_handler(checkpoint, load_sheet)


def main_choice_menu(call):
    cid = call.chat.id
    if call.text == "Настройки файлов":
        checkpoint = tg.send_message(cid, dUpdate_text + dOpen_text + dCancel_text, reply_markup=keyboard_update_menu)
        tg.register_next_step_handler(checkpoint, main_setting_menu)
    elif call.text == "Начать":
        # checkpoint = tg.send_message(cid, rGroup_text + rSubject_text + rLink_text + rCancel_text,
        #                              reply_markup=keyboard_read_menu)
        checkpoint = tg.send_message(cid, "Этот модуль не работает, нажми на /start")
        tg.register_next_step_handler(checkpoint, choose_subject)
    elif call.text == "Закрыть":
        tg.send_message(cid, "Чтобы снова получить доступ к боту, пропиши или нажми на /start",
                        reply_markup=keyboard_main_remove)
    else:
        checkpoint = tg.send_message(cid, unresolved_message)
        tg.register_next_step_handler(checkpoint, main_choice_menu)


def getUrl(gmessage):
    global irul
    mid = gmessage.chat.id
    global tid
    tid = '/'.join(gmessage.text.split('/')[5:][:-1])
    print(tid)
    includeData = f"https://sheets.googleapis.com/v4/spreadsheets/{tid}?includeGridData=True&access_token={access_token}"
    choose_sheet(mid, includeData)


def choose_subject(message):
    cid = message.chat.id
    if os.path.isfile(f'iFiles/{subjectFile}'):
        cGroup = open(f"iFiles/{groupFile}")
        cSubject = open(f"iFiles/{subjectFile}")
        csGroup = open(f"iFiles/{sGroupFile}")
        cUrl = open(f"iFiles/{urlFile}")
        clGroup = cGroup.readlines()
        clSubject = cSubject.readlines()
        clsGroup = csGroup.readlines()
        clUrl = cUrl.readlines()
        for i in range(len(clGroup)):
            if clGroup[i].strip() and clSubject[i].strip() and clsGroup[i].strip() and clUrl[i].strip():
                keyboard_choose_group.add(f"{clSubject[i]}")
        cGroup.close()
        cSubject.close()
        csGroup.close()
        cUrl.close()
        checkpoint = tg.send_message(cid, "Выбери дисциплины, здесь показаны только те, у которых в наличии ссылка на "
                                          "таблицу с ней", reply_markup=keyboard_choose_group)
        tg.register_next_step_handler(checkpoint, choose_subject)
    else:
        tg.send_message(cid, "Файлов нет:/")
        sendFirstMessage(message)


def test(message):
    tid = message.chat.id
    checkpoint = tg.send_message(tid, "asdf")
    tg.register_next_step_handler(checkpoint, test)


tg.polling()

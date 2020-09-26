def getUrl(gmessage):
    global irul
    mid = gmessage.chat.id
    tid = '/'.join(gmessage.text.split('/')[5:][:-1])
    print(tid)
    includeData = f"https://sheets.googleapis.com/v4/spreadsheets/1Nc3gkg-sGfrj84ludywF-eixv4oNoul38lsYq456t-Y?includeGridData=True&access_token={access_token}"
    surl1 = f"https://sheets.googleapis.com/v4/spreadsheets/{tid}/values/{isheet.sid1}"
    surl2 = f"https://sheets.googleapis.com/v4/spreadsheets/{tid}/values/{isheet.sid2}"
    try:
        tg.send_message(mid, "Попытка загрузки...")
        gtest_col1 = requests.get(f"{surl1}!A:A?access_token={access_token}&majorDimension=COLUMNS")
        print(gtest_col1)
        if gtest_col1.status_code != 200:
            tg.send_message(mid, f"{isheet.sid1} в виде столбцов - ?")
        else:
            tg.send_message(mid, f"{isheet.sid1} в виде столбцов - ??")
        gtest_rows1 = requests.get(f"{surl1}!A:O?access_token={access_token}&majorDimension=ROWS")
        tg.send_message(mid, "33%")
        if gtest_rows1.status_code != 200:
            tg.send_message(mid, f"{isheet.sid1} в виде строк - ?")
        else:
            tg.send_message(mid, f"{isheet.sid1} в виде строк - ??")
        gtest_urls1 = requests.get(f"{surl1}!C:C?access_token={access_token}&majorDimension=COLUMNS")
        tg.send_message(mid, "40%")
        if gtest_urls1.status_code != 200:
            tg.send_message(mid, f"{isheet.sid1} ссылки - ?")
        else:
            tg.send_message(mid, f"{isheet.sid1} ссылки - ??")
        gtest_col2 = requests.get(f"{surl1}!A:O?access_token={access_token}&majorDimension=COLUMNS")
        tg.send_message(mid, "56%")
        if gtest_col2.status_code != 200:
            tg.send_message(mid, f"{isheet.sid2} в виде столбцов - ?")
        else:
            tg.send_message(mid, f"{isheet.sid2} в виде столбцов - ??")
        gtest_rows2 = requests.get(f"{surl2}!A:O?access_token={access_token}&majorDimension=ROWS")
        tg.send_message(mid, "82%")
        if gtest_rows2.status_code != 200:
            tg.send_message(mid, f"{isheet.sid2} в виде строк - ?")
        else:
            tg.send_message(mid, f"{isheet.sid2} в виде строк - ??")
        gtest_urls2 = requests.get(f"{surl2}!C:C?access_token={access_token}&majorDimension=COLUMNS")
        if gtest_urls2.status_code != 200:
            tg.send_message(mid, f"{isheet.sid2} ссылки - ?")
        else:
            tg.send_message(mid, f"{isheet.sid2} ссылки - ??")
        tg.send_message(mid, "100%")
        if gtest_col1.status_code == 200:
            tg.send_message(mid, "Загрузил:)")
            '''Функция которая будет создавать файл и в него все все все загружать'''
            print('ну тип тут функция вроде бы...')
            addFile(gtest_col1, gtest_rows1, gtest_urls1, gtest_col2, gtest_rows2, gtest_urls2, True, mid)
            return sendFirstMessage(gmessage)
        else:
            checkpoint = tg.send_message((mid, f"Ошибка {gtest_col1.status_code}, попробуй вбить ещё раз"))
    except:
        if gtest_col1.status_code == 403:
            checkpoint = tg.send_message(mid, f"Ошибка {gtest_col1.status_code}, введённые значения не верны, "
                                         f"попробуй ещё раз")
            return sendFirstMessage(gmessage)
        if gtest_col1.status_code == 404:
            tg.send_message(mid, f"Такой Таблицы не существует ({gtest_col1.status_code}), попробуй вбить ещё раз")
            return sendFirstMessage(gmessage)
        if gtest_col1.status_code == 400:
            tg.send_message(mid,
                            f"Я ничего не загрузил, у меня {gtest_col1.status_code}, пересмотри введённые"
                            f"данные!")
            return sendFirstMessage(gmessage)

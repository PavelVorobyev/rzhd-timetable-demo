import datetime
import pprint
import time

import requests

# URL для отправки запроса на получение расписания
# Возвращает уникальный RID запроса на сервере РЖД
URL_REQUEST = 'https://pass.rzd.ru/timetable/public/ru?layer_id=5827&dir=0&tfl=3&checkSeats=1&code0={code_src}&dt0={dt:%d.%m.%Y}&code1={code_dst}&dt1={dt:%d.%m.%Y}'

# URL для получения результата запроса расписания по RID
URL_RESULT = 'https://pass.rzd.ru/timetable/public/ru?layer_id=5827&rid={rid}'

# Коды города отправления и прибытия
code_src = '2000000'  # Москва
code_dst = '2004000'  # Питер

# Открываем сессию для сохранения cookies между запросами
session = requests.Session()

# Дата нужно будет в циле менять, если нужно получить за год
tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)

print('{dt:%d.%m.%Y}{code_src} -> {code_dst}'.format(dt=tomorrow, code_src=code_src, code_dst=code_dst))
print('\tPlacing timetable request.')

# Отправляем запрос и получаем идентификатор запроса на сервере
rid = session.get(url=URL_REQUEST.format(code_src=code_src, code_dst=code_dst, dt=tomorrow)).json().get('RID')

if rid:
    print('\tGetting timetable result. RID: {}'.format(rid))
    # Пауза, чтобы запрос успел обработаться
    time.sleep(1)
    result = session.get(
        url=URL_RESULT.format(rid=rid)
    )
    pprint.pprint(result.json())

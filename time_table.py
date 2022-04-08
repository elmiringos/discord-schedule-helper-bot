from bs4 import BeautifulSoup
import requests
import json
import datetime   #импортирует все необходимые библиотеки

def get_schedule(name_of_group):   
    with open("data.json", "r") as file:
        schedule = json.load(file)  #загружаем json файл в переменную
    index_of_today = 0
    headers = {        #
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:97.0) Gecko/20100101 Firefox/97.0"
    }


    now = datetime.datetime.now() #узнаем сегодняшнюю дату
    month = str(now.month)
    if len(month) < 2:
        month = "0" + month
    day = str(now.day)
    if len(day) < 2:
        day = "0" + day

    today = day + "." + month #преобразуем в удобный формат
    print(today) #для проверки выводим в консоль


    group_schedule_href = schedule[name_of_group] #из json файла находим нужную ссылку на расписание
    req = requests.get(url = group_schedule_href, headers= headers) # создаем get запрос
    src = req.text #через метод text получаем html текст страницы
    soup = BeautifulSoup(src, "lxml") #"прогоняем" через парсер

    days = soup.find_all(class_='vt237')[1:] #создаем массив в days, который заполняем датами, т.е например 02.12 где 02 - день, 12 - месяц  


    for i in range(len(days)):
        days[i] = days[i].text.strip()[:5] #из всех элементов массивов удаляем все пробелы, также удаляем теги


    for i in range(len(days)): #находим из списка дней сегодняшний день
        if today == days[i]:
            index_of_today = i + 1 #находим индек и прибавляем 1
    
    if index_of_today == 0: #день с таким индексом - это воскресенье => сразу прерываем работу функции и выводим результат
        return "Выходной"

    lessons = soup.find_all(class_= f"vt239 rasp-day rasp-day{index_of_today}") #находим все занятия на сегодняшний день
    time = soup.select("div[class='vt239']") #находим все верменную промежутки для каждого занятия
    time_table = [] #массив для отформатированных строк (временные промежутки)

    for item in time: #форматируем строку для лучшего ввида
        cur = item.text
        if "ФЗ" in cur:
            time_table.append(item.text[:2] + ")" + item.text[2:7] + "-" + item.text[7:])
            continue
        time_table.append(item.text[0] + ")" + item.text[1:6] + "-" + item.text[6:])
    lessons_of_today = [] #массив отформатированных строк (занятия)
    for item in lessons:
        cur = " ".join(item.text.strip().split())
        lessons_of_today.append(cur)

    schedule_for_today = [] #результирующий массив
    for i in range(len(lessons_of_today)): #конкатенация строк и добавление их в результирующийй массив 
        if len(lessons_of_today[i]) > 1: 
            schedule_for_today.append(time_table[i] + ' -- ' + lessons_of_today[i])

    if len(schedule_for_today): #проверка на длину массива
        return "Выходной"

    return schedule_for_today

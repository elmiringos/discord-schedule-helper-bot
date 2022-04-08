from bs4 import BeautifulSoup
import requests
import json   #импортирование необходимых библиотек

url = "https://www.sut.ru/studentu/raspisanie/raspisanie-zanyatiy-studentov-ochnoy-i-vecherney-form-obucheniya"  #ссылка на сайт Бонча

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:97.0) Gecko/20100101 Firefox/97.0"
}

req = requests.get(url, headers = headers) #создаем get запрос


src = req.text #получаем html текст

with open("index.html", "w") as file: #записываем html страницу в отдельный файл 
    file.write(src)

soup = BeautifulSoup(src) #"прогоняем через парсер" 

all_groups_href = soup.find_all(class_ = "vt256") #находим ссылки на расписание каждой группы 

all_schedules = {} #создаем словарь

for item in all_groups_href: #заполняем словарь
    group_name = item.text.strip()
    group_schedule_href = "https://www.sut.ru/studentu/raspisanie/raspisanie-zanyatiy-studentov-ochnoy-i-vecherney-form-obucheniya" + item.get("href").strip()
    print(group_name, group_schedule_href)

    all_schedules[group_name] = group_schedule_href

with open("data.json", "w") as file:  #записываем словарь в json файл
    json.dump(all_schedules, file, indent=4, ensure_ascii = False)
 

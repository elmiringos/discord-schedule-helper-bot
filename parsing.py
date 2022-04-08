from bs4 import BeautifulSoup
import requests
import json

# url = "https://www.sut.ru/studentu/raspisanie/raspisanie-zanyatiy-studentov-ochnoy-i-vecherney-form-obucheniya"

# headers = {
#     "Accept": "*/*",
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:97.0) Gecko/20100101 Firefox/97.0"
# }

# req = requests.get(url, headers = headers)


# src = req.text

# with open("index.html", "w") as file:
#     file.write(src)


# with open("index.html", "r") as file:
#     src = file.read()



# soup = BeautifulSoup(src)

# all_groups_href = soup.find_all(class_ = "vt256")

# all_schedules = {}

# for item in all_groups_href:
#     group_name = item.text.strip()
#     group_schedule_href = "https://www.sut.ru/studentu/raspisanie/raspisanie-zanyatiy-studentov-ochnoy-i-vecherney-form-obucheniya" + item.get("href").strip()
#     print(group_name, group_schedule_href)

#     all_schedules[group_name] = group_schedule_href

# with open("data.json", "w") as file:
#     json.dump(all_schedules, file, indent=4, ensure_ascii = False)
 

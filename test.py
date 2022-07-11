from bs4 import BeautifulSoup
import requests

html = ""
years = ["2020","2021","2022","2023","2024"]
for year in years:
    response = requests.get(f"https://www.timeanddate.com/holidays/us/{year}?hol=33554809")
    html += response.text

soup = BeautifulSoup(html,"html.parser")
table = soup.find("table",attrs = {"id":"holidays-table"})

holidaylist = []
for row in table.find_all_next("tr",attrs = {"class":"showrow"}):
    holidays = row.find_all_next("td")
    holidaydict = {}
    holidaydict["name"] = holidays[1].string
    dates = row.find("th")
    holidaydict["date"] = dates.string
    holidaylist.append(holidaydict)
print(holidaylist)


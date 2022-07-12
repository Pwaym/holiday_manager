from bs4 import BeautifulSoup
import requests
from datetime import datetime
import json

file2 = open("holidays.json")
reading = json.loads(file2.read())
print(reading)

file = open("holidaystesting.json", "w")
json.dump(reading["holidays"],file)

# print(jsonfile)

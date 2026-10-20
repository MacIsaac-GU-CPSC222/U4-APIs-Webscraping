import requests
from bs4 import BeautifulSoup
# python -m pip install beautifulsoup4
import pandas as pd

url = "https://www.allmysportsteamssuck.com/ncaa-division-i-football-and-basketball-twitter-hashtags-and-handles/"

response = requests.get(url)
print(response)
# print(response.text)

soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table", attrs={"id":"rankingstable"})

print(type(table))

tbody = table.find("tbody")
# print(tbody)

trs = tbody.find_all("tr")
# print(trs)
print(len(trs))

rows = []
for tr in trs:
    # print(tr)
    tds = tr.find_all("td")
    row = []
    for td in tds:
        # print(td)
        text = td.get_text()
        # print(text)
        row.append(text)
    rows.append(row)
    # print(rows)

print(rows)
print(len(rows))

# TASK: Get the header data from the website. 
# convert it into a 1D list of column names
# use rows and header to create a new pandas dataframe
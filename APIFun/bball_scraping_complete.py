import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.allmysportsteamssuck.com/ncaa-division-i-football-and-basketball-twitter-hashtags-and-handles/"

response = requests.get(url)
# print(response.text)
soup = BeautifulSoup(response.text, "html.parser")
print(type(soup))
# # step 1: get the table element (AKA tag)
table = soup.find("table", attrs={"id": "rankingstable"})
# print(table)
print(type(table))
# # step 2: grab the tbody's table rows (trs)
tbody = table.find("tbody")
print(type(tbody))

trs = tbody.find_all("tr")

print(type(trs))
print(len(trs))
# # step 3: process each table row (tr) by getting its data (tds)
rows = []
for tr in trs:
    row = []
    tds = tr.find_all("td")
    # print(tds)
    for td in tds:
        # print(td.get_text())
        # print(td.get_text(), end="\t")
        row.append(td.get_text())
    # print()
    rows.append(row)

# print(rows)
# step 4 TASK: create a pandas dataframe for this table data
# then, parse the thead element to get the names of the columns
# and make these your dataframe column names
# then write the dataframe to a file

thead = table.find("thead")
ths = thead.find_all("th")
header = []
for th in ths:
    header.append(th.get_text())

# print(header, rows)
df = pd.DataFrame(rows, columns=header)
df = df.set_index("School")
print(df)
df.to_csv("bball_twitter_names.csv")
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.allmysportsteamssuck.com/ncaa-division-i-football-and-basketball-twitter-hashtags-and-handles/"


response = requests.get(url)
# print(response.text)

soup = BeautifulSoup(response.text,"html.parser")
print(type(soup))

table = soup.find("table", attrs={"id":"rankingstable"})

print(type(table))

# print(table)
tbody  = table.find("tbody")
# print(tbody)

trs = tbody.find_all("tr")
print(type(trs))
print(len(trs))

rows = []
for tr in trs:
    # print(tr)
    tds = tr.find_all("td")
    row = []
    # print(len(tds))
    for td in tds:
        # print(td)
        text = td.get_text()
        row.append(text)
    rows.append(row)

# print(len(rows))
# print(rows[:3])
# step 4 TASK: create a pandas dataframe for this table data
# then, parse the thead element to get the names of the columns
# and make these your dataframe column names
# then write the dataframe to a file

thead = table.find("thead")
ths = thead.find_all("th")
# print(ths)
header = []
for th in ths:
    header.append(th.get_text())
# print(header)

df = pd.DataFrame(rows, columns = header)

df = df.set_index("School")
print(df.head())
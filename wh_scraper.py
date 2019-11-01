import requests
import sqlite3

from time import sleep
from bs4 import BeautifulSoup


def get_urls(page=1):
    url = "https://www.whitehouse.gov/briefings-statements/page/{}/"
    briefings = requests.get(url.format(page))
    articles = []
    
    if briefings.status_code == 404:
        return articles
    
    soup = BeautifulSoup(briefings.content, "lxml")
    for article in soup.find_all("article"):
        articles.append({
            "title": article.h2.text,
            "link": article.h2.a.get("href")
        })

    return articles


def get_article(url):
    article = requests.get(url)
    soup = BeautifulSoup(article.content, "lxml")
    
    text = ""
    for para in soup.find_all("p"):
        text += para.text + "\n"
    
    return text


uris = []
page = 1
while True:
    result = get_urls(page)
    if len(result) == 0:
        break
    uris.extend(result)
    page += 1
    sleep(0.1)

print("Got urls")

fname = "{:04}.txt"
base_path = "data/wh_briefings/"
db = sqlite3.connect("data/gathered.db")
cur = db.cursor()
for i, article in enumerate(reversed(uris)):
    cur.execute("INSERT INTO wh_briefings VALUES (?,?)", (article["link"], base_path+fname.format(i)))
    text = get_article(article["link"])
    path = base_path + fname.format(i)
    with open(path, "w") as fl:
        fl.write(text)
    sleep(0.1)

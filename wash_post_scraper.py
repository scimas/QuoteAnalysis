import requests

from bs4 import BeautifulSoup


def get_article(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    article = soup.find("div", attrs={"class": "article-body"})
    
    text = ""
    for para in article.find_all(["p", "h3"]):
        text += para.text + "\n"
    
    return text

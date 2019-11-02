import requests

from bs4 import BeautifulSoup


def get_article(url):
    articles = []
    for ur in url:
        page = requests.get(ur)
        soup = BeautifulSoup(page.content, "lxml")
        article = soup.find("article").find("div", attrs={"class": "entry-content"})
        
        text = ""
        for para in article.find_all(["p", "h2", "blockquote"]):
            text += para.text + "\n"
        articles.append(text)

    return articles

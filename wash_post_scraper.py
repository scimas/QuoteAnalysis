import requests

from bs4 import BeautifulSoup


def get_article(url):
    articles = []
    for ur in url:
        page = requests.get(ur)
        soup = BeautifulSoup(page.content, "lxml")
        article = soup.find("div", attrs={"class": "article-body"})
        
        text = ""
        for para in article.find_all(["p", "h3"]):
            text += para.text + "\n"
        articles.append(text)
    
    return articles

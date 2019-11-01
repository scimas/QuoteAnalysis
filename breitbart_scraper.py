import requests

from bs4 import BeautifulSoup


def get_article(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    article = soup.find("article").find("div", attrs={"class": "entry-content"})
    
    text = ""
    for para in article.find_all(["p", "h2", "blockquote"]):
        text += para.text + "\n"
    
    return text

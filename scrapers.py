import requests

from bs4 import BeautifulSoup


def get_article_breitbart(url):
    """
    @author: Mihir Gadgil
    Breitbart News Web Scraper
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    content = soup.find("article").find("div", attrs={"class": "entry-content"})
    
    article = ""
    for para in content.find_all(["p", "h2", "blockquote"]):
        article += para.text + "\n"
    
    return article


def get_article_bbc(url):
    """
    @author: Charles Garrett Eason
    BBC News Web Scraper
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="lxml")
    content = soup.find("div", attrs={"class": "story-body__inner"})
    article = ''
    for i in content.findAll('p'):
        article = article + ' ' +  i.text
    
    return article


def get_article_fox(url):
    """
    @author: Charles Garrett Eason
    Fox News Web Scraper
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="lxml")
    content = soup.find("div", attrs={"class": "article-body"})
    article = ''
    for i in content.findAll('p'):
        article = article + ' ' + i.text
    
    return article


def get_article_wp(url):
    """
    @author: Mihir Gadgil
    Washington Post News Web Scraper
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    content = soup.find("div", attrs={"class": "article-body"})
    
    article = ""
    for para in content.find_all(["p", "h3"]):
        article += para.text + "\n"
    
    return article


def get_article_ap(url):
    """
    @author: Charles Garrett Eason
    Associated Press News Web Scraper
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="lxml")
    content = soup.find("div", attrs={"class": "Article"})
    article = ''

    for i in content.findAll('p'):
        article = article + ' ' +  i.text
    
    return article


def get_article_cnn(url):
    """
    @author: Binbin Wu
    CNN News Web Scraper
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")
    content = soup.find_all(class_="zn-body__paragraph")
    
    article = ""
    for para in article:
        article += para.text + "\n"
    
    return article

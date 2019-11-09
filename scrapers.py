import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

gecko_path = r'geckodriver'

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

def get_article_wsj(URL, U_P):
    """
    @author: Charles Garrett Eason
    Wall Street Journal News Web Scraper
    """
    #Login location:
    Login_URL = 'https://id.wsj.com/access/pages/wsj/us/signin.html'

    #Setting up browser:
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(
        options=options, 
        executable_path=gecko_path
    )
    
    #Logging in:
    driver.get(Login_URL)
    U_Field = driver.find_element_by_id([*U_P][0])
    P_Field = driver.find_element_by_id([*U_P][1])
    U_Field.send_keys(U_P[[*U_P][0]])
    P_Field.send_keys(U_P[[*U_P][1]])
    button = driver.find_element_by_tag_name('button')
    driver.execute_script("arguments[0].click();", button)
    
    #Obtaining content:
    driver.get(URL)
    element = driver.find_element_by_class_name('article-content ')
    html = element.get_attribute('innerHTML')
    driver.close()
    
    #Parsing content:
    content = BeautifulSoup(html, "lxml")
    article = ''
    for i in content.findAll('p'):
        article = article + ' ' +  i.text
    
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

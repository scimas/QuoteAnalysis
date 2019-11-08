"""
Created on Fri Nov  1 12:48:11 2019
@author: Charles Garrett Eason
Fox News Web Scraper
"""
# %% Packages:
import requests
from bs4 import BeautifulSoup
import time
start_time = time.time()

# %% Functions:
def Fox_Scraper(URLs):
    articles = []
    for u in URLs:
        response = requests.get(u)
        soup = BeautifulSoup(response.text, features="lxml")
        content = soup.find("div", attrs={"class": "article-body"})
        article = ''
        for i in content.findAll('p'):
            article = article + ' ' + i.text
        articles.append(article)

    return (articles)


# %% Execution:
URLs = ['https://www.foxnews.com/politics/officials-say-bolton-shut-down-ukraine-meeting-warned-of-hand-grenade-giuliani-transcript']
articles = Fox_Scraper(URLs)
print("--- %s seconds ---" % (time.time() - start_time))
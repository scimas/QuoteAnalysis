#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 12:48:11 2019

@author: Charles Garrett Eason
BBC News Web Scraper
"""
#%% Packages:
import requests
from bs4 import BeautifulSoup

#%% Functions:
def BBC_Scraper(URLs):
    
    articles = []
    for u in URLs:
        response = requests.get(u)
        soup = BeautifulSoup(response.text, features="html.parser")
        content = soup.find("div", attrs={"class": "story-body__inner"})
        article = ''
        for i in content.findAll('p'):
            article = article + ' ' +  i.text
        articles.append(article)
    
    return(article)

#%% Execution:
URLs = ['https://www.bbc.com/news/world-asia-india-50258947']
article = BBC_Scraper(URLs)

 

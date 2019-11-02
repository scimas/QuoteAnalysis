#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 12:48:11 2019

@author: Charles Garrett Eason
WSJ Web Scraper
"""
#%% Packages:
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options
start_time = time.time()

#%% Functions:
def WSJ_Scraper(URLs, U_P):
    
    #Login location:
    Login_URL = 'https://id.wsj.com/access/pages/wsj/us/signin.html'

    #Setting up browser:
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(
        options=options, 
        executable_path=r'/home/garrett/geckodriver/geckodriver'
    )
    
    #Logging in:
    driver.get(Login_URL)
    U_Field = driver.find_element_by_id([*U_P][0])
    P_Field = driver.find_element_by_id([*U_P][1])
    U_Field.send_keys(U_P[[*U_P][0]])
    P_Field.send_keys(U_P[[*U_P][1]])
    button = driver.find_element_by_tag_name('button')
    driver.execute_script("arguments[0].click();", button)
    time.sleep(1)
    
    #Obtaining content:
    htmls = []
    for u in URLs:
        driver.get(u)
        element = driver.find_element_by_class_name('article-content ')
        html = element.get_attribute('innerHTML')
        htmls.append(html)
    driver.close()
    
    #Parsing content:
    articles = []
    for h in htmls:
        content = BeautifulSoup(h, "lxml")
        article = ''
        for i in content.findAll('p'):
            article = article + ' ' +  i.text
        articles.append(article)
    
    return(articles)


#%% Execution:
URLs = ['https://www.wsj.com/articles/fitbit-to-be-acquired-by-google-llc-11572613473?mod=business_lead_pos1', 
        'https://www.wsj.com/articles/u-s-payrolls-grew-by-128-000-in-october-despite-the-gm-strike-11572611632?mod=hp_lead_pos1']
U_P = {'username': 'easoncharles9@gmail.com', 'password': 'greatpassword9'}
articles = WSJ_Scraper(URLs, U_P)
print("--- %s seconds ---" % (time.time() - start_time))





 

#!/usr/bin/env python
# coding: utf-8

#%% Packages
import requests
from bs4 import BeautifulSoup
import urllib
import numpy as np
from numpy.linalg import norm
from nltk.tokenize import TreebankWordTokenizer
from sklearn.preprocessing import OneHotEncoder
import re
from nltk.tokenize import sent_tokenize
from googlesearch import search
import spacy
import scrapers
import metrics
import quote_extraction


#%% Functions

###############################################################################
# Scrapers
###############################################################################
def news_api(source, qurry, from_,to_):
    url = ('https://newsapi.org/v2/everything?'
       'q={}&'
       'sources={}&'
       'from={}&to={}&'
       'apiKey=52654b37ed4a4570ad8cf1933879fe14')
    response = requests.get(url.format(qurry,source,from_,to_))
    return response.json()


def get_Stories(api_response_json):
    stories_urls = []
    for i in api_response_json['articles']:
        stories_urls.append(i['url'])
    return stories_urls

###############################################################################
# Other Functions
###############################################################################

def Google_quote(quote) :
    matching_quote_url=[]
    for url in search(quote, stop=20):
        matching_quote_url.append(url)
    return matching_quote_url


def text_from_Google_url(Google_urls):
    fox_url_regex = re.compile('.*www.foxnews.com.*')
    cnn_url_regex = re.compile('.*www.cnn.com.*')
    bbc_url_regex = re.compile('.*www.bbc.com.*')
    bb_url_regex = re.compile('.*www.breitbart.com.*')
    ap_url_regex = re.compile('.*www.apnews.com.*')
    wp_url_regex = re.compile('.*www.washingtonpost.com.*')
    
    fox_article=[]
    bb_article=[]
    cnn_article=[]
    bbc_article=[]
    wp_article=[]
    ap_article=[]
    
    for url in Google_urls:
        if fox_url_regex.fullmatch(url):
            fox_article.append(scrapers.get_article_fox(url))
        elif bb_url_regex.fullmatch(url):
            bb_article.append(scrapers.get_article_breitbart(url))
        elif cnn_url_regex.fullmatch(url):
            cnn_article.append(scrapers.get_article_cnn(url))
        elif bbc_url_regex.fullmatch(url):
            bbc_article.append(scrapers.get_article_bbc(url))
        elif wp_url_regex.fullmatch(url):
            wp_article.append(scrapers.get_article_wp(url))
        elif ap_url_regex.fullmatch(url):
            ap_article.append(scrapers.get_article_ap(url))
    
    return {
            'fox':fox_article,
            'bb':bb_article,
            'cnn':cnn_article,
            'bbc':bbc_article,
            'wp':wp_article,
            'ap':ap_article
            }


tokenizer = TreebankWordTokenizer()
# Didn't work on the below:






test=news_api('fox-news','trump AND impeach','2019-10-31','2019-11-02')




urls=get_Stories(test)




article_list=[]
for i in urls:
    article_list.append(scrapers.get_article_fox(i))



article_list[1]



quotes=[]
for article in article_list:
    quotes.append(quote_extraction.find_quotes_in_text(article))



quotes1 = [y for x in quotes for y in x]




len(quotes1)




for i in search(quotes1[0],stop=10):
    print (i)





dictionary = text_from_Google_url(google_urls)



quote="The Greatest Witch Hunt in American History!"
def Google_quote(quote) :
    matching_quote_url=[]
    for url in search(quote, stop=20):
        matching_quote_url.append(url)
    return matching_quote_url

Google_quote(quote)



#entity
import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("The Greatest Witch Hunt in American History!")
for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)

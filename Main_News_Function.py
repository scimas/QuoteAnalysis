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
from nltk.corpus import stopwords


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
    remove_vids = 'site:www.cnn.com -site:cnn.com/video -site:cnn.com/videos -site:cnn.com/shows -site:foxnews.com/shows -site:breitbart.com/tag'
    matching_quote_url=[]
    domains=['www.foxnews.com','www.cnn.com','www.bbc.com','www.breitbart.com','www.apnews.com','www.washingtonpost.com']
    for domain in domains:
        for url in search(quote+remove_vids, domains=domain, tbs="qdr:m" , stop=3):
            matching_quote_url.append(url)
            time.sleep(3)
        time.sleep(120)
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


###############################################################################
# MAIN Functions
###############################################################################

def main(og_source, topic, start_time,end_time ):
    #test=news_api('fox-news','trump AND impeach','2019-10-31','2019-11-02')
    news= news_api(og_source, topic, start_time, end_time)
    urls=get_Stories(news)
    article_list=[]
    for i in urls:
        article_list.append(scrapers.get_article_fox(i))

    quotes=[]
    for article in article_list:
        quotes.append(quote_extraction.find_quotes_in_text(article))

    quotes_list = [y for x in quotes for y in x]

    # filiter quotes_list 3 words withou stop_words
    stop_words= tuple(stopwords.words('english'))
    quotes_list_filiter=[]
    for quotes in quotes_list:
        quote_len = 0
        for token in tokenizer.tokenize(quotes):
            if token not in stop_words:
                quote_len+=1
        if quote_len > 3:
            quotes_list_filiter.append(quotes)
    urls=[]
    for google_quote in quotes_list_filiter:
        urls.append(Google_quote(google_quote))

    dictionary = text_from_Google_url(urls)

    dictionary_quotes={}
    for i in dictionary:
        quotes=[]
        if (len(dictionary[i])!=0):
            for article in dictionary[i]:
                quotes.append(find_quotes_in_text(article))
        dictionary_quotes[i] = quotes

    similarity_result={}
    sources =['fox','bb','cnn','bbc','wp','ap']
    for quote in quotes_list:
        for source in sources:
            for dictionary_quotes_clust in dictionary_quotes[source]:
                # filiter dictionary_quotes. 60% length match without stop_words

                for google_quote in dictionary_quotes_clust:
                    google_quote_len=0
                    for google_token in tokenizer.tokenize(google_quote):
                        if google_token not in stop_words:
                            google_quote_len += 1

                    if google_quote_len > 3:
                        if (og_source, source) not in similarity_result.keys():
                            similarity_result[(og_source, source)] = [JaccardSimilarity(quote, google_quote)]
                        else:
                            similarity_result[(og_source, source)].append(JaccardSimilarity(quote, google_quote))
    return similarity_result



print(main('fox-news','trump AND impeach','2019-10-31','2019-11-02'))


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


def get_article_fox(url):
    opener=urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)
    
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")
    article = soup.find("div", attrs={"class": "article-body"}).find_all('p')
    
    text = ""
    for para in article:
        text += para.text + "\n"
    return text


def get_article_cnn(url):
    opener=urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)
    
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")
    article = soup.find_all(class_="zn-body__paragraph")
    
    text = ""
    for para in article:
        text += para.text + "\n"
    return text


def get_article_wp(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    article = soup.find("div", attrs={"class": "article-body"})
    
    text = ""
    for para in article.find_all(["p", "h3"]):
        text += para.text + "\n"
    return text
    

def get_article_bb(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    article = soup.find("article").find("div", attrs={"class": "entry-content"})
        
    text = ""
    for para in article.find_all(["p", "h2", "blockquote"]):
        text += para.text + "\n"
    article.append(text)
    return article


def BBC_Scraper(URLs):
    response = requests.get(URLs)
    soup = BeautifulSoup(response.text, features="lxml")
    content = soup.find("div", attrs={"class": "story-body__inner"})
    article = ''
    for i in content.findAll('p'):
        article = article + ' ' +  i.text
    article.append(article)
    return(article)


def AP_Scraper(URLs):
    
    articles = []
    for u in URLs:
        response = requests.get(u)
        soup = BeautifulSoup(response.content, features="lxml")
        content = soup.find("div", attrs={"class": "Article"})
        article = ''

        for i in content.findAll('p'):
            article = article + ' ' +  i.text
        articles.append(article)
    return(article)


###############################################################################
# Other Functions
###############################################################################
def find_quotes_in_text(text):
    """Returns a list of quotes from given text."""
    quotes_regex = re.compile('(?:\u201c(.*?)\u201d)')
    quotes = [q for q in quotes_regex.findall(text)]
    return quotes


def find_sentences_containing_quotes(quotes, text):
    """Returns a list of setences containing a quote in given quotes and text."""
    sent_quote_dict = {}
    sentences = sent_tokenize(text)
    for sentence in sentences:
        for quote in quotes:
            if quote in sentence:
                sent_quote_dict[quote] = sentence
    return sent_quote_dict


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
            fox_article.append(get_article_fox(url))
        elif bb_url_regex.fullmatch(url):
            bb_article.append(get_article_bb(url))
        elif cnn_url_regex.fullmatch(url):
            cnn_article.append(get_article_cnn(url))
        elif bbc_url_regex.fullmatch(url):
            bbc_article.append(BBC_Scraper(url))
        elif wp_url_regex.fullmatch(url):
            wp_article.append(get_article_wp(url))
        elif ap_url_regex.fullmatch(url):
            ap_article.append(AP_Scraper(url))
    
    return {
            'fox':fox_article,
            'bb':bb_article,
            'cnn':cnn_article,
            'bbc':bbc_article,
            'wp':wp_article,
            'ap':ap_article
            }


###############################################################################
# Comparison Functions
###############################################################################
tokenizer = TreebankWordTokenizer()

def JaccardSimilarity(sent1, sent2):
    tokens1 = set(tokenizer.tokenize(sent1))
    tokens2 = set(tokenizer.tokenize(sent2))
    return len(tokens1.intersection(tokens2)) / len(tokens1.union(tokens2))

def CosineSimilarity(sent1, sent2):
    enc = OneHotEncoder()
    tk1 = tokenizer.tokenize(sent1)
    tk2 = tokenizer.tokenize(sent2)
    tk1.extend(tk2)
    all_tokens = list(set(tk1))
    all_vec = np.array(all_tokens, dtype="object").reshape(-1, 1)
    svec1 = np.array(tk1, dtype="object").reshape(-1, 1)
    svec2 = np.array(tk2, dtype="object").reshape(-1, 1)
    enc.fit(all_vec)
    wvec1 = enc.transform(svec1).sum(axis=0)
    wvec2 = enc.transform(svec2).sum(axis=0)
    return wvec1.dot(wvec2.T)/norm(wvec1)/norm(wvec2)





# Didn't work on the below:






test=news_api('fox-news','trump AND impeach','2019-10-31','2019-11-02')




urls=get_Stories(test)




article_list=[]
for i in urls:
    article_list.append(get_article_fox(i))



article_list[1]



quotes=[]
for article in article_list:
    quotes.append(find_quotes_in_text(article))




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





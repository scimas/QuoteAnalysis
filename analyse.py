import os
import re
import time
import urllib

import numpy as np
import requests
import spacy

from bs4 import BeautifulSoup
from googlesearch import search
from library import metrics, quote_extraction, scrapers
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, TreebankWordTokenizer
from numpy.linalg import norm


def news_api(source, query, from_, to_):
    """
    @author: Binbin Wu
    Query news API to search for a topic in a given time range.
    Returns the response in json format.
    """
    url = ('https://newsapi.org/v2/everything?'
       'q={}&'
       'sources={}&'
       'from={}&to={}&'
       'apiKey=52654b37ed4a4570ad8cf1933879fe14')
    response = requests.get(url.format(query, source, from_, to_))
    return response.json()


def get_Stories(api_response_json):
    """
    @author: Binbin Wu
    Extract article urls from news API response.
    Returns a list of URLs.
    """
    stories_urls = []
    for i in api_response_json['articles']:
        stories_urls.append(i['url'])
    return stories_urls


def Google_quote(quote):
    """
    @author: Binbin Wu
    Search for articles with similar quotes on different news sources using Google search.
    Returns a list of URLs.
    """
    remove_vids = ' -site:cnn.com/video -site:cnn.com/videos -site:cnn.com/shows -site:foxnews.com/shows -site:breitbart.com/tag -site:apnews.com/apf -site:bbc.com/news/live -site:bbc.com/news/*/'
    matching_quote_url=[]
    domains=[
        'www.foxnews.com', 'www.cnn.com', 'www.bbc.com',
        'www.breitbart.com', 'apnews.com', 'www.washingtonpost.com'
    ]
    for domain in domains:
        for url in search(quote + remove_vids, domains=[domain], tbs="qdr:m", stop=2, pause=10):
            matching_quote_url.append(url)
    return matching_quote_url


def text_from_Google_url(Google_urls):
    """
    @author: Binbin Wu
    Extract text from news articles.
    Returns a dictionary of articles for each news source.
    """
    # Regex for identifying news source
    fox_url_regex = re.compile('.*www.foxnews.com.*')
    cnn_url_regex = re.compile('.*www.cnn.com.*')
    bbc_url_regex = re.compile('.*www.bbc.com.*')
    bb_url_regex = re.compile('.*www.breitbart.com.*')
    ap_url_regex = re.compile('.*apnews.com.*')
    wp_url_regex = re.compile('.*www.washingtonpost.com.*')
    
    fox_article=[]
    bb_article=[]
    cnn_article=[]
    bbc_article=[]
    wp_article=[]
    ap_article=[]
    
    for url in Google_urls:
        # If URL is for this news source, use the corresponding scraper
        # to get the article.
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


def write_urls_file(urls):
    """
    @author: Binbin Wu, Mihir Gadgil
    Store URLs obtained from Google search to avoid querying google again
    """
    data_dir = os.path.join("data")
    with open(os.path.join(data_dir, "google_urls.txt"), "w") as fd:
        for url in urls:
            fd.write(url + "\n")


def read_urls_file():
    """
    @author: Binbin Wu, Mihir Gadgil
    Read URLs from the stored file.
    Returns a list of URLs.
    """
    data_dir = os.path.join("data")
    urls = []
    with open(os.path.join(data_dir, "google_urls.txt"), "r") as fd:
        url = fd.readline().strip()
        while url:
            urls.append(url)
            url = fd.readline().strip()
    return urls


def main(og_source, topic, start_time, end_time):
    """
    @author: Binbin Wu
    Main function that uses all of the functionality to do quote analysis.
    Returns a dictionary of pairwise similarity scores for news sources.
    """
    # Get the "original" quotes from one of the news sources (og_source)
    news = news_api(og_source, topic, start_time, end_time)
    urls = get_Stories(news)
    # Extract text from articles
    if og_source == 'fox-news':
        scraper = scrapers.get_article_fox
    elif og_source == 'breitbart-news':
        scraper = scrapers.get_article_breitbart
    elif og_source == 'cnn':
        scraper = scrapers.get_article_cnn
    elif og_source == 'bbc-news':
        scraper = scrapers.get_article_bbc
    elif og_source == 'the-washington-post':
        scraper = scrapers.get_article_wp
    elif og_source == 'associated-press':
        scraper = scrapers.get_article_ap
    else:
        print("Unknown news source")
        return {}
    
    article_list = []
    for i in urls:
        article_list.append(scraper(i))

    # Extract quotes from articles
    quotes = []
    for article in article_list:
        quotes.append(quote_extraction.find_quotes_in_text(article))

    quotes_list = [y for x in quotes for y in x]

    # Only use the quotes that have at least 3 non-stopwords
    tokenizer = TreebankWordTokenizer()
    stop_words = tuple(stopwords.words('english'))
    quotes_list_filiter = []
    for quotes in quotes_list:
        quote_len = 0
        for token in tokenizer.tokenize(quotes):
            if token not in stop_words:
                quote_len += 1
        if quote_len > 3:
            quotes_list_filiter.append(quotes)

    urls = []
    # If the URLs file exists, use it instead of querying google.
    data_dir = os.path.join("data")
    urls_file = os.path.join(data_dir, "google_urls.txt")
    if os.path.exists(urls_file):
        urls = read_urls_file()
    else:
        for google_quote in quotes_list_filiter[:5]:
            urls.extend(Google_quote(google_quote))
        write_urls_file(urls)

    # Extract the articles' text
    dictionary = text_from_Google_url(urls)

    # Extract the quotes
    dictionary_quotes={}
    for i in dictionary:
        quotes=[]
        if len(dictionary[i]) != 0:
            for article in dictionary[i]:
                quotes.append(quote_extraction.find_quotes_in_text(article))
        dictionary_quotes[i] = quotes

    # Compare quotes using similarity metrics
    similarity_result={}
    sources =['fox', 'bb', 'cnn', 'bbc', 'wp', 'ap']
    quote_dictionary = {}
    for source in sources:
        quote_dictionary[source] = []
        for dictionary_quotes_clust in dictionary_quotes[source]:
            for google_quote in dictionary_quotes_clust:
                quote_dictionary[source].append(google_quote)
    
    for quote in quotes_list:
        for source in sources:
            # filter dictionary_quotes to contain at least 3 non-stopwords
            for google_quote in quote_dictionary[source]:
                google_quote_len = 0
                for google_token in tokenizer.tokenize(google_quote):
                    if google_token not in stop_words:
                        google_quote_len += 1

                if google_quote_len > 3:
                    sim = metrics.JaccardSimilarity(quote, google_quote)
                    if sim >= 0.2:
                        if (og_source, source) not in similarity_result.keys():
                            similarity_result[(og_source, source)] = [sim]
                        else:
                            similarity_result[(og_source, source)].append(sim)
    
    heatmap_dict = {}
    for i, source1 in enumerate(sources):
        heatmap_dict[(source1, source1)] = 1
        for source2 in sources[i+1:]:
            score = 0
            for quote1 in quote_dictionary[source1]:
                for quote2 in quote_dictionary[source2]:
                    score += metrics.JaccardSimilarity(quote1, quote2)
            score /= max(len(quote_dictionary[source1]) * len(quote_dictionary[source2]), 1)
            heatmap_dict[(source1, source2)] = score
            heatmap_dict[(source2, source1)] = score
    
    return similarity_result, heatmap_dict


if __name__ == "__main__":
    sim_results, heatmap_dict = main('fox-news', 'trump AND impeach', '2019-11-01', '2019-11-15')
    print(sim_results)
    print(sim_results.keys())
    print(heatmap_dict)

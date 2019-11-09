import numpy as np
import matplotlib.pyplot as plt

from numpy.linalg import norm
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TreebankWordTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans


tokenizer = TreebankWordTokenizer()
eng_stopwords = stopwords.words("english")
stemmer = PorterStemmer()

def preprocessing(sent):
    tokens = tokenizer.tokenize(sent)
    s = [token for token in tokens if not(token in eng_stopwords)]
    processed_sent = ""
    for token in s:
        processed_sent += token + " "
    processed_sent = processed_sent.strip()

    return stemmer.stem(processed_sent)

vectorizer = CountVectorizer(tokenizer=tokenizer.tokenize, binary=True, preprocessor=preprocessing)

def JaccardSimilarity(sent1, sent2):
    tokens1 = set(tokenizer.tokenize(sent1))
    tokens2 = set(tokenizer.tokenize(sent2))

    return len(tokens1.intersection(tokens2)) / len(tokens1.union(tokens2))

def CosineSimilarity(sent1, sent2):
    sents = vectorizer.fit_transform([sent1, sent2]).toarray()

    return sents[0].dot(sents[1].T)/norm(sents[0])/norm(sents[1])


def KMeans(quote_corpus, clusters=2):
    # Add stemming, tokenizer
    vectorizer = CountVectorizer(lowercase=True, stop_words=stopwords.words('english'), max_df=0.5, binary=True)
    X = vectorizer.fit_transform(quote_corpus)
    kmeans_model = KMeans(n_clusters=clusters)

    print("Top terms per cluster:")
    order_centroids = kmeans_model.cluster_centers_.argsort()[:, ::-1]
    terms = X.get_feature_names()
    for i in range(clusters):
        top_ten_words = [terms[ind] for ind in order_centroids[i, :5]]
        print("Cluster {}: {}".format(i, ' '.join(top_ten_words)))

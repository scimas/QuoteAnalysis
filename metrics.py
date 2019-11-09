import numpy as np

from numpy.linalg import norm
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TreebankWordTokenizer
from sklearn.feature_extraction.text import CountVectorizer

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

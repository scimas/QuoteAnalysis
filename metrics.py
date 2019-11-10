import numpy as np

from numpy.linalg import norm
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TreebankWordTokenizer
from sklearn.feature_extraction.text import CountVectorizer

tokenizer = TreebankWordTokenizer()
eng_stopwords = tuple(stopwords.words("english"))
stemmer = PorterStemmer()


def tokenization(sent):
    """
    @author: Mihir Gadgil
    Tokenizer for vectorizing sentences.
    """
    # Tokenize sentence
    tokens = tokenizer.tokenize(sent)
    # Remove stopwords and stemming
    processed_tokens = [stemmer.stem(token) for token in tokens if token not in eng_stopwords]
    return processed_tokens


# Text vectorizer for CosineSimilarity
vectorizer = CountVectorizer(tokenizer=tokenization, binary=True)


def JaccardSimilarity(sent1, sent2):
    """
    @author: Mihir Gadgil
    Sentence Jaccard similarity.
    """
    tokens1 = set(tokenizer.tokenize(sent1))
    tokens2 = set(tokenizer.tokenize(sent2))

    return len(tokens1.intersection(tokens2)) / len(tokens1.union(tokens2))


def CosineSimilarity(sent1, sent2):
    """
    @author: Mihir Gadgil
    Sentence cosine similarity.
    """
    sents = vectorizer.fit_transform([sent1, sent2]).toarray()

    return np.matmul(sents[0], sents[1].T)/norm(sents[0])/norm(sents[1])

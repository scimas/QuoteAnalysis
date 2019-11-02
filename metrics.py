import numpy as np

from itertools import combinations
from numpy.linalg import norm
from nltk.tokenize import TreebankWordTokenizer
from sklearn.preprocessing import OneHotEncoder

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

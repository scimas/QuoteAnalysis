import numpy as np
import pandas as pd

from matplotlib import pyplot as plt
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TreebankWordTokenizer
from numpy.linalg import norm
from sklearn.cluster import KMeans
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
    return np.matmul(sents[0], sents[1].T) / (norm(sents[0]) * norm(sents[1]))


class StemmerTokenizer(object):
    def __init__(self):
        self.porter_stemmer = PorterStemmer()
        self.treebank_tokenizer = TreebankWordTokenizer()

    def __call__(self, sentence):
        return [self.porter_stemmer.stem(token) for token in self.treebank_tokenizer.tokenize(sentence)
                if token not in eng_stopwords]


def KMeansClusteringElbowCurve(quote_dict):
    """Shows an elbow curve plot to determine the appropriate number of k-means clusters."""
    count_vectorizer = CountVectorizer(tokenizer=StemmerTokenizer(), lowercase=True,
                                       stop_words=stopwords.words('english'), binary=True)
    X = count_vectorizer.fit_transform(quote_dict.values())
    distorsions = []
    for k in range(1, 4):
        kmeans_model = KMeans(n_clusters=k)
        kmeans_model.fit(X)
        distorsions.append(kmeans_model.inertia_)
    fig = plt.figure(figsize=(15, 5))
    plt.plot(range(1, 4), distorsions)
    plt.title('Elbow Curve')
    plt.show()


def KMeansClustering(quote_dict, clusters=2):
    """Returns a pandas data frame containing the quote_dict and cluster label."""
    count_vectorizer = CountVectorizer(tokenizer=StemmerTokenizer(), lowercase=True)
    X = count_vectorizer.fit_transform(quote_dict.values()).toarray()
    kmeans_model = KMeans(n_clusters=clusters).fit(X)
    y = kmeans_model.predict(X)
    kmeans_df = pd.DataFrame.from_dict(quote_dict, orient='index', columns=['sentence'])
    kmeans_df["cluster"] = kmeans_model.labels_
    return X, y, kmeans_model, kmeans_df


def KMeansClusteringPlot(X, y, kmeans_model, quote_dict):
    """Show clusters with centroids from k-means."""
    plt.scatter(X[:, 0][0], X[:, 1][0], s=200, color='blue', label=[k for k in quote_dict.keys()][0])
    plt.scatter(X[:, 0][1], X[:, 1][1], s=200, color='red', label=[k for k in quote_dict.keys()][1])
    plt.scatter(X[:, 0][2], X[:, 1][2], s=200, color='green', label=[k for k in quote_dict.keys()][2])
    centers = kmeans_model.cluster_centers_
    plt.scatter(centers[:, 0], centers[:, 1], c='black', s=100, alpha=0.6)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    quote_dict = {'cnn': 'witch hunt', 'fox': 'donald trump says this is a witch hunt',
                'bbc': 'donald trump is a crookity crook who should be impeached'}

    kmeans_elbow = KMeansClusteringElbowCurve(quote_dict)

    X, y, kmeans_model, kmeans_df = KMeansClustering(quote_dict)
    print(kmeans_df)

    kmeans_plot = KMeansClusteringPlot(X, y, kmeans_model, quote_dict)

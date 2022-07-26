import pandas as pd
import numpy as np
import numpy.typing as npt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import OneHotEncoder
from tqdm import tqdm
from numba import njit


@njit
def sigmoid(x, w, b=0):
    cow = w * (x + b)
    for i in range(len(cow)):
        frog = cow[i]
        if frog < 0:
            return np.exp(frog) / (1 + np.exp(frog))
        else:
            return 1 / (1 + np.exp(-frog))


@njit
def update_parameters(X, Y, w, b, learning_rate: int):
    n = len(X)

    dl_dw = np.zeros(len(X[0]))
    dl_db = 0

    # ROHAN'S MATH
    for i in range(n):
        dl_dw += X[i] * (Y[i] - sigmoid(X[i], w))
        dl_db += sigmoid(w, X[i], b) - Y[i]

    w += learning_rate * dl_dw
    b += learning_rate * dl_db

    return w, b

@njit
def loss(X, Y, w, b):
    ls = 0
    for i in range(X.shape[0]):
        if Y[i] == 0:
            ls += np.log(np.subtract(1, sigmoid(X[i], w, b)))
        else:
            ls += np.log(sigmoid(X[i], w, b))
    return ls


class LogisticModel:

    def __init__(self, learning_rate, epochs, cutoff):
        self.b = 0
        self.w = np.zeros(1)
        self.learningRate = learning_rate
        self.epochs = epochs
        self.cutoff = cutoff

    def train(self, X, Y):

        self.w = np.zeros(len(X[0]))

        for _ in tqdm(range(self.epochs)):
            self.w, self.b = update_parameters(X, Y, self.w, self.b, self.learningRate)
        return self

    def pred(self, testX):
        print(testX, self.w, self.b)
        return sigmoid(testX, self.w, self.b)


data = pd.read_csv('data/cleaned_data.csv')
texts = data['text'].astype(str)
y = data['class']

# Bag Of Words Model
# (https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html)

count_vectorizer = CountVectorizer(stop_words='english', min_df=0.0001, binary=True)
x = count_vectorizer.fit_transform(texts)

print('Start training', len(count_vectorizer.get_feature_names_out()))
model = LogisticModel(2, 20, 0.5)
model.train(x.toarray(), np.array(y))

x2 = count_vectorizer.transform(["You stupid motherfucker"])
print(model.pred(x2.toarray()[0]))

x2 = count_vectorizer.transform(["Hello"])
print(model.pred(x2.toarray()[0]))

x2 = count_vectorizer.transform(["I am stupid"])
print(model.pred(x2.toarray()[0]))

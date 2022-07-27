import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from tqdm import tqdm
from numba import njit


@njit
def sigmoid(x, w, bias=0):
    # sigmoid(b + xw1 +)
    a = np.append(1., x)
    b = np.append(bias, w)
    r = np.dot(b, a)
    return 1 / (1 + np.exp(-r))


@njit
def update_parameters(X, Y, w, b, learning_rate: int):
    n = len(X)

    dl_dw = np.zeros(len(X[0]))
    dl_db = 0

    # ROHAN'S MATH
    for i in range(n):
        dl_dw += X[i] * (sigmoid(X[i], w) - Y[i])
        dl_db += sigmoid(X[0], w, b) - Y[0]

    w -= learning_rate * dl_dw
    b -= learning_rate * dl_db / n

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
        self.w = None
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

print('Start training', count_vectorizer.get_feature_names_out())
model = LogisticModel(2, 10, 0.5)
# x is a 2d sparse array from scipy.sparse
# x: [
#   [00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001
#
#
#     ]
model.train(x.toarray(), np.array(y))

ip = " "
while ip != "":
    ip = input("> ")
    x2 = count_vectorizer.transform([ip])
    print(round(model.pred(x2.toarray()[0]), 10))

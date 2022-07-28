import sys

sys.path.append("..")

import numpy as np
from tqdm import tqdm
from clean_api import dataset_clean, clean_text



def sigmoid(x, w, b):
    # sigmoid(b + x1w1 + x2w2 + ...)
    r = np.dot(x, w)
    calc = 1 / (1 + np.exp(-r - b))

    if calc == 0:
        return 0.0001
    if calc == 1:
        return 0.99999
    return calc


def get_row(X, i):
    return X.getrow(i).toarray()


def update_parameters(X, Y, w, b, learning_rate):
    n = X.shape[0]

    # Stochastic Gradient Descent
    i = np.random.randint(0, n)
    xi = get_row(X, i)

    # ROHAN'S MATH

    dl_dw = np.dot(xi.T, (sigmoid(xi, w, b)) - Y[i])
    dl_db = sigmoid(xi, w, b) - Y[i]


    w -= learning_rate * dl_dw
    b -= learning_rate * dl_db

    return w, b


def _loss(X, Y, w, b):
    ls = 0
    for i in range(X.shape[0]):
        if Y[i] == 0:
           ls += np.log(np.subtract(1, sigmoid(get_row(X, i), w, b)))
        else:
           ls += np.log(sigmoid(get_row(X, i), w, b))
    return ls / X.shape[0]


class LogisticModel:

    def __init__(self, learning_rate, epochs, cutoff):
        self.b = 0
        self.w = None
        self.learningRate = learning_rate
        self.epochs = epochs
        self.cutoff = cutoff

    def loss(self, X, Y):
        return _loss(X, Y, self.w, self.b)

    def train(self, X, Y, loss_interval=250000):
        self.w = np.zeros((X.get_shape()[1], 1))

        for i in tqdm(range(1, self.epochs + 1)):
            if i % loss_interval == 0:
                print("Loss:", self.loss(X, Y))
            self.w, self.b = update_parameters(X, Y, self.w, self.b, self.learningRate)

        return self

    def pred(self, testX):
        calc = sigmoid(testX, self.w, self.b)[0][0]
        return calc

    def predArr(self, X, Y):
        arr = np.array()
        for x in X:
            calc = self.pred(x)[0][0]

            if calc > self.cutoff:
                arr.add(1)
            else:
                arr.add(0)

        return arr, Y






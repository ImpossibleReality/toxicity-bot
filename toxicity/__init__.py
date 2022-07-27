import numpy as np
from tqdm import tqdm


#@njit
def sigmoid(x, w, bias=0):
    # sigmoid(b + x1w1 + x2w2 + ...)
    r = np.dot(x, w)
    calc = 1 / (1 + np.exp(-r - bias))
    if calc == 0:
        return 0.0001
    if calc == 1:
        return 0.99999
    return calc

def get_row(X, i):
    return X.getrow(i).toarray()

#@njit
def update_parameters(X, Y, w, b, learning_rate: int):
    n = X.shape[0]

    dl_dw = np.zeros((X.shape[1], 1))
    dl_db = 0

    # ROHAN'S MATH
    i = np.random.randint(0, n, 1)
    xi = get_row(X, i)
    dl_dw += np.transpose(np.multiply(xi, (sigmoid(xi, w) - Y[i])))
    dl_db += sigmoid(xi, w, b) - Y[i]


    w -= learning_rate * dl_dw
    b -= learning_rate * dl_db / n

    return w, b


#@njit
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

    def train(self, X, Y, loss_interval=300000):
        self.w = np.zeros((X.get_shape()[1], 1))

        for i in tqdm(range(self.epochs)):
            if i % loss_interval == 0:
                print("Loss:", self.loss(X, Y))
            self.w, self.b = update_parameters(X, Y, self.w, self.b, self.learningRate)

        return self

    def pred(self, testX):
        print(testX, self.w, self.b)
        return sigmoid(testX, self.w, self.b)[0][0]
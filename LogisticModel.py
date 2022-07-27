import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from numba import njit
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
    return ls


class LogisticModel:

    def __init__(self, learning_rate, epochs, cutoff):
        self.b = 0
        self.w = None
        self.learningRate = learning_rate
        self.epochs = epochs
        self.cutoff = cutoff

    def loss(self, X, Y):
        return _loss(X, Y, self.w, self.b)

    def train(self, X, Y):
        self.w = np.zeros((X.get_shape()[1], 1))

        for i in tqdm(range(self.epochs)):
            if i % 100000 == 0:
                print("Loss:", self.loss(X, Y))
            self.w, self.b = update_parameters(X, Y, self.w, self.b, self.learningRate)
        
        return self

    def pred(self, testX):
        print(testX, self.w, self.b)
        return sigmoid(testX, self.w, self.b)



data = pd.read_csv('data/cleaned_data.csv')
train, test = train_test_split(data, test_size=0.2)
train_x = train['text'].astype(str)
test_x = test['text'].astype(str)

train_y = train['class']
test_y = test['class']

# Bag Of Words Model
# (https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html)

count_vectorizer = CountVectorizer(stop_words='english', min_df=0.0001, binary=True)
train_x = count_vectorizer.fit_transform(train_x)
test_x = count_vectorizer.transform(test_x)

print('Start training')
model = LogisticModel(0.001, 1000000, 0.5)
# x is a 2d sparse array from scipy.sparse
# x: [
#   [00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001
#
#
#     ]

model.train(train_x, np.array(train_y))

print(model.loss(test_x, np.array(test_y)))

ip = " "
while ip != "":
    ip = input("> ")
    x2 = count_vectorizer.transform([ip])
    print(round(model.pred(x2.toarray()[0])[0][0], 10))

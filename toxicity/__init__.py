# CSIII Group 3
# Johan N.
# Discord Bot, MongoDB, ZMQ Integration, debugging
# Daniel W.
# Model and debugging, hyperparameter tuning
# Rohan D.
# Math (loss and gradient calculations), data collection and manipulation
# Final Project
# Discord bot which detects and removes toxic messages

import sys
# Allows import from clean_api
sys.path.append("..")

import numpy as np
from tqdm import tqdm
from clean_api import dataset_clean, clean_text

# Sigmoid function
def sigmoid(x, w, b):
    # sigmoid(b + x1w1 + x2w2 + ...)
    r = np.dot(x, w) # w_1*x_1 + w_2*x_2 + w_3*x_3... + w_n*x_n

    calc = 1 / (1 + np.exp(-r - b)) #Sigmoid function

    if calc == 0:  # If r is very, very big, it causes a numerical overflow and calc is set to 0,
                   # but this causes errors in the loss function, so we set it to 0.0001 instead
        return 0.0001
    if calc == 1:  # If r is very, very small, calc is set to 1,
                   # but this causes errors in the loss function, so we set it to 0.9999
        return 0.99999

    return calc





class LogisticModel:

    # Constructor, defines hyperparameters
    def __init__(self, learning_rate, epochs, cutoff):
        self.b = 0
        self.w = None
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.cutoff = cutoff

    # Performs gradient descent
    def update_parameters(self, X, Y):
        n = X.shape[0]  # The length of the dataset

        # Stochastic Gradient Descent
        # (Looks at a single randomly chosen data point each epoch)

        i = np.random.randint(0, n)
        xi = X.getrow(i).toarray()

        # Finds gradient (calculations performed by Rohan)
        dl_dw = np.dot(xi.T, (sigmoid(xi, self.w, self.b)) - Y[i])
        dl_db = sigmoid(xi, self.w, self.b) - Y[i]

        # Updates weights based on gradient and learning rate
        self.w -= self.learning_rate * dl_dw
        self.b -= self.learning_rate * dl_db

    # Updates weights and biases using gradient descent
    def train(self, X, Y, loss_interval=250000):
        self.w = np.zeros((X.get_shape()[1], 1))

        for i in tqdm(range(1, self.epochs + 1)):  # tqdm used to display progress bar
            if i % loss_interval == 0:
                print("Loss:", self.log_likelihood(X, Y))
            self.update_parameters(X, Y)

        return self

    # Calculates log-likelihood of the model (negative, so should optimally should approach 0)
    # NOTE: We called this value "loss" in many files, because it was a more convenient term to use
    def log_likelihood(self, X, Y):
        ls = 0
        for i in range(X.shape[0]):
            if Y[i] == 0:
                # If true label is 0, the following line approaches 0 when the sigmoid function
                # approaches 0
                ls += np.log(np.subtract(1, sigmoid(X.getrow(i).toarray(), self.w, self.b)))
            else:
                # If true label is 1, the following line approaches 0 when the sigmoid function
                # approaches 1
                ls += np.log(sigmoid(X.getrow(i).toarray(), self.w, self.b))

        # Divide by the length of the dataset so that we can compare between different datasets
        return ls / X.shape[0]

    # Returns the model's prediction of a single data point as a probability
    # (used by the actual bot)
    def pred(self, X):
        calc = sigmoid(X, self.w, self.b)
        return calc

    # Returns the model's prediction of an entire dataset at once as 0s or 1s
    # (used to generate confusion matrices)
    def predArr(self, X):

        arr = np.empty(0)

        for i in range(X.shape[0]):

            xi = X.getrow(i).toarray()

            calc = self.pred(xi)
            if calc > self.cutoff:
                arr = np.append(arr, 1)
            else:
                arr = np.append(arr, 0)

        return arr






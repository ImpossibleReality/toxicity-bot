import pandas as pd
import numpy as np


class LogisticModel:
    
    def sigmoid(x, w, b):
        return 1 / (np.exp(np.negative(np.add(np.multiply(w, x), b))))
    
    def __init__(self, learningRate, epochs, cutoff):
        self.learningRate = learningRate
        self.epochs = epochs
        self.cutoff = cutoff
    
    def train(self, X, Y):
        
        self.w = 0
        self.b = 0
        
        for i in range(self.epochs):
            self.w, self.b = self.updateParameters(X, Y, self.learningRate) 
        
        return self
        
    def updateParameters(self, X, Y, learningRate):
        
        w = self.w
        b = self.b
        
        pred = self.pred(X)
        
        #### GRADIENT DESCENT HERE
        #w: 
        #b:     
        
        return w, b       

    def loss(self, X, Y, w, b):
        l = 0
        for i in range(len(X)):
            if Y[i] == 0:
                l += np.log(np.subtract(1, self.sigmoid(X[i], w, b)))
            else:
                l += np.log(self.sigmoid(X[i], w, b))
        return l
    
    
    def pred(self, testX):
        return self.sigmoid(testX, self.w, self.b)
        
    
data = pd.read_csv('../data/cleaned_data.csv')
texts = data['text'].astype(str)
y = data['class']
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
#from numba import jit

class LogisticModel:
    
    def sigmoid(x, w, b = 0):
        #return 1 / (np.exp(np.negative(np.add(np.multiply(w, x), b))))
        return 1 / (np.exp(- w*x + b))
    
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
    
    #@jit    
    def updateParameters(self, X, Y, learningRate):
        
        w = self.w
        b = self.b
                
               
        N = len(X)
        
        dl_dw = np.zeros(N)
        dl_db = 0
        
        # ROHAN'S MATH
        for i in range(len(X)):
            dl_dw[i] += X[i] * (Y[i] - self.sigmoid(X[i], w[i]))
            dl_db += self.sigmoid(w[i], X[i], b) - Y[i]
      
        w += learningRate * dl_dw
        b += learningRate * dl_db
        
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

# Bag Of Words Model
# (https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html)
count_vectorizer = CountVectorizer(stop_words='english', min_df=0.0001)
x = count_vectorizer.fit_transform(texts)


model = LogisticModel(2, 5000, 0.5)
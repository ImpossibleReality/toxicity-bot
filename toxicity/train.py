import os

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from toxicity import LogisticModel
from sklearn.model_selection import train_test_split
import joblib

DEFAULT_TRAIN_SENSITIVITY = ["loose"]
DEFAULT_EPOCHS = 1000000
DEFAULT_LR = 0.01


sensitivities=DEFAULT_TRAIN_SENSITIVITY
print("Enter sensitivites to train (ie loose, moderate, strict)")
ip = input("> ")
if ip != "":
    sensitivities = ip.replace(" ", "").split(",")

epochs=DEFAULT_EPOCHS
print("Enter number of epochs")
ip = input("> ")
if ip != "":
    epochs = int(ip)

lr = DEFAULT_LR
print("Enter learning rate")
ip = input("> ")
if ip != "":
    lr = float(ip)

for s in sensitivities:
    print("Loading data for: " + s)
    data = pd.read_csv(os.path.join("../data/datasets/cleaned/", s + ".csv"))
    train, test = train_test_split(data, test_size=0.2)

    train_x = train['text'].astype(str)
    test_x = test['text'].astype(str)

    train_y = train['class']
    test_y = test['class']

    # Bag Of Words Model
    # (https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html)

    print("Fitting BOW model for: " + s)
    count_vectorizer = CountVectorizer(stop_words='english', min_df=0.0001, binary=True)
    train_x = count_vectorizer.fit_transform(train_x)
    joblib.dump(count_vectorizer, os.path.join("../data/model/", s + "/", "vectorizer.joblib"))

    test_x = count_vectorizer.transform(test_x)

    print('Starting training for: ' + s)

    # Loss on test data: -0.307
    model = LogisticModel(lr, epochs, 0.5)
    model.train(train_x, np.array(train_y))
    joblib.dump(model, os.path.join("../data/model/", s + "/", "model.joblib"))
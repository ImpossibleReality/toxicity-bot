# CSIII Group 3
# Johan N.
# Discord Bot, MongoDB, ZMQ Integration, debugging
# Daniel W.
# Model and debugging, hyperparameter tuning
# Rohan D.
# Math (loss and gradient calculations), data collection and manipulation
# Final Project
# Discord bot which detects and removes toxic messages

import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from toxicity import LogisticModel
from sklearn.model_selection import train_test_split
import joblib

# Default model to train if input is empty string
DEFAULT_TRAIN_SENSITIVITY = ["loose"]
# Default epochs if input is empty string
DEFAULT_EPOCHS = 1000000
# Default learning rate if input is empty string
DEFAULT_LR = 0.01
# How many epochs it takes to print the loss
LOSS_PRINT_INTERVAL = 250000
# What the model considers as a 1
DEFAULT_CUTOFF = 0.5


sensitivities=DEFAULT_TRAIN_SENSITIVITY
print("Enter sensitivites to train (ie loose, moderate, strict) separated by comma")
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

cutoff = DEFAULT_CUTOFF
print("Enter cutoff probability")
ip = input("> ")
if ip != "":
    lr = float(ip)

for s in sensitivities:
    print("Loading data for: " + s)
    data = pd.read_csv(os.path.join("../../data/datasets/cleaned/", s + ".csv"))
    train, test = train_test_split(data, test_size=0.2, random_state=5)

    train_x = train['text'].astype(str)
    test_x = test['text'].astype(str)

    train_y = train['class']
    test_y = test['class']

    # Bag Of Words Model
    # (https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html)

    print("Fitting BOW model for: " + s)
    count_vectorizer = CountVectorizer(stop_words='english', min_df=0.0001, binary=True)
    train_x = count_vectorizer.fit_transform(train_x)
    joblib.dump(count_vectorizer, os.path.join("../../data/model/", s + "/", "vectorizer.joblib"))

    test_x = count_vectorizer.transform(test_x)

    print('Starting training for: ' + s)

    model = LogisticModel(lr, epochs, 0.5)
    model.train(train_x, np.array(train_y), loss_interval=LOSS_PRINT_INTERVAL)
    joblib.dump(model, os.path.join("../../data/model/", s + "/", "model.joblib"))

    print("Predicting test loss for " + s)
    print("Test loss: " + str(model.loss(test_x, np.array(test_y))))
    print("----------------\n")

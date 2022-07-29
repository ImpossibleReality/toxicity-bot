# CSIII Group 3
# Johan N.
# Discord Bot, MongoDB, ZMQ Integration, debugging
# Daniel W.
# Model and debugging, hyperparameter tuning
# Rohan D.
# Math (loss and gradient calculations), data collection and manipulation
# Final Project
# Discord bot which detects and removes toxic messages

import joblib
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

sensitivities = ['loose', 'moderate', 'strict']

for s in sensitivities:
    print("Loading data for: " + s)
    data = pd.read_csv(os.path.join("../../data/datasets/cleaned/", s + ".csv"))
    _, test = train_test_split(data, test_size=0.2, random_state=5)

    test_x = test['text'].astype(str)
    test_y = test['class']

    print("Loading model for: " + s)
    vectorizer = joblib.load(os.path.join("../../data/model/", s + "/", "vectorizer.joblib"))
    model = joblib.load(os.path.join("../../data/model/", s + "/", "model.joblib"))

    test_x = vectorizer.transform(test_x)

    print("Test loss: " + str(model.loss(test_x, np.array(test_y))[0][0]))
    print("-------")
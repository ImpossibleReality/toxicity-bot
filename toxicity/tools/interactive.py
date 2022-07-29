# CSIII Group 3
# Johan N.
# Discord Bot, MongoDB, ZMQ Integration, debugging
# Daniel W.
# Model and debugging, hyperparameter tuning
# Rohan D.
# Math (loss and gradient calculations), data collection and manipulation
# Final Project
# Discord bot which detects and removes toxic messages

#This file simply takes user generated words in and outputs a bag of words model
import joblib
import os

model = input("Enter model name to load: ")
vectorizer = joblib.load(os.path.join("../../data/model/", model + "/", "vectorizer.joblib"))
model = joblib.load(os.path.join("../../data/model/", model + "/", "model.joblib"))


ip = " "
while ip != "":
    ip = input("Enter text to predict: ")
    if ip == "":
        break
    v = vectorizer.transform([ip])[0][0]
    print(model.pred(v.toarray()[0]))

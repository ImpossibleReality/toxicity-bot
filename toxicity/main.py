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
from constants import MODEL_NAMES, ZMQ_PORT
from clean_api import clean_text
import zmq
import signal
import json

signal.signal(signal.SIGINT, signal.SIG_DFL)

# setting models and vectorizers to null (for now)
models = []
vectorizers = []
print("Loading models...")

# loads libraries necessary for the bot to use the model
for m in MODEL_NAMES:
    vectorizer = joblib.load(os.path.join("../data/model/", m + "/", "vectorizer.joblib"))
    model = joblib.load(os.path.join("../data/model/", m + "/", "model.joblib"))

    models.append(model)
    vectorizers.append(vectorizer)


def predict(model_id: int, text: str):
    text = clean_text(text)
    v = vectorizers[model_id].transform([text])[0][0] # used to create a bag of words
    return models[model_id].pred(v.toarray()[0]), models[model_id].cutoff #determines if the content should be deleted

# creates and assigns address to socket, print statements for the backend
print("Starting server...")
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:" + ZMQ_PORT)
print("Server ready.")

while True:
    #  Wait for next request from client
    message = socket.recv_pyobj()
    print("Request recieved")
    try:
        p, c = predict(message['model'], message['text'])
        socket.send(json.dumps({"type": 0, "prob": p, "cutoff": c}).encode('ascii'))
    except KeyError:
        socket.send(json.dumps({"type": 1, "code": "Missing text argument"}).encode('ascii'))

# CSIII Group 3
# Johan N.
# Discord Bot, MongoDB, ZMQ Integration, debugging
# Daniel W.
# Model and debugging, hyperparameter tuning
# Rohan D.
# Math (loss and gradient calculations), data collection and manipulation
# Final Project
# Discord bot which detects and removes toxic messages

import zmq.asyncio
import logging
import sys
from constants import ZMQ_PORT
import json

try:
    context = zmq.asyncio.Context()
    logging.info("Connecting to model server...")
    socket = context.socket(zmq.DEALER)
    socket.connect("tcp://localhost:" + ZMQ_PORT)
except ConnectionError:
    logging.error("You must start the model server in toxicity/main.py")
    sys.exit(1)


async def predict_text_prob(model_id: int, text: str):
    await socket.send(b"", zmq.SNDMORE)
    await socket.send_pyobj({"model": model_id, "text": text})
    res = await socket.recv()
    try:
        res = json.loads(res.decode("ascii"))
    except json.JSONDecodeError:
        res = await socket.recv()
        res = json.loads(res.decode("ascii"))
    if res['type'] == 0:
        return res['prob'], res['cutoff']
    else:
        logging.error("INVALID RESPONSE FROM MODEL SERVER")
        return False


async def predict_text(model_id: int, text: str):
    t, c = await predict_text_prob(model_id, text)
    return t > c

# CSIII Group 3
# Johan N.
# Discord Bot, MongoDB, ZMQ Integration, debugging
# Daniel W.
# Model and debugging, hyperparameter tuning
# Rohan D.
# Math (loss and gradient calculations), data collection and manipulation
# Final Project
# Discord bot which detects and removes toxic messages

import time
import pymongo
import logging
from pymongo import MongoClient
import os

client = None
db = None

# Called by main function to connect to the database
def connect():
    logging.info("Connecting to db...")
    global client, db
    client = MongoClient(os.getenv('DB_URI'))
    logging.info("Connected to db")

    db = client.toxicity_bot
    db.settings.create_index([('guild_id', pymongo.ASCENDING)], unique=True)


class Config():
    # Sensitivity will be one of four:
    # 0: Loose censoring
    # 1: Moderate censoring
    # 2: Strict censoring
    # 3: Demo censoring
    #
    # Feedback will be true or false depending on if the server enables feedback
    def __init__(self, sensitivity: int, reporting: bool, analytics: bool, feedback_channel):
        self.sensitivity = sensitivity
        self.reporting = reporting
        self.analytics = analytics
        self.feedback_channel = feedback_channel


DEFAULT_CONFIG = Config(0, False, False, None)

# Get config object from guild (server) id
def get_config(id: int):
    if db is None:
        raise Exception("DB not connected")
    c = db.settings.find_one({'guild_id': id})
    if c is not None:
        try:
            return Config(c['sensitivity'], c['reporting'], c['analytics'], c.get('feedback_channel'))
        except KeyError:
            logging.warning("KeyError while getting config for id: " + str(id))
            return DEFAULT_CONFIG
    else:
        return DEFAULT_CONFIG

# Set the config object for a guild id
def set_config(id: int, config: Config):
    if db is None:
        raise Exception("DB not connected")
    db.settings.update_one({
        'guild_id': id
    },
        {
            '$set': {
                'guild_id': id,
                'sensitivity': config.sensitivity,
                'reporting': config.reporting,
                'analytics': config.analytics,
                'feedback_channel': config.feedback_channel,
            }
        }, True)

# Create a feedback submission from a guild, message, model name, and id
def create_feedback(guild_id: int, message: str, model: int, msg_id: int):
    return db.feedback.insert_one({
        "guild": guild_id,
        "message": message,
        "vmessage_id": msg_id,
        "model": model,
        "voters": [],
        "created": time.time(),
        "counts": {
            "isbad": 0,
            "isgood": 0
        }
    })

# Test if a user has voted on a poll
def has_voted(msgid: int, voter: int):
    x = db.feedback.find_one({
        'vmessage_id': msgid
    })

    return voter in x['voters']

# Update feedback counts for a poll
def update_feedback_counts(msgid: int, is_good: bool, voter: int):
    db.feedback.update_one({
        'vmessage_id': msgid
    },
        {
            '$inc': {
                'counts.isgood' if is_good else 'counts.isbad': 1
            },
            '$push': {
                'voters': voter
            }
        })
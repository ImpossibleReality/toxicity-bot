import pymongo
import logging
from pymongo import MongoClient
import os

client = None
db = None


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
    def __init__(self, sensitivity: int, feedback: bool):
        self.sensitivity = sensitivity
        self.feedback = feedback


DEFAULT_CONFIG = Config(0, False)


def get_config(id: int):
    if db is None:
        raise Exception("DB not connected")
    c = db.settings.find_one({'guild_id': id})
    if c is not None:
        try:
            return Config(c['sensitivity'], c['feedback'])
        except KeyError:
            logging.warning("KeyError while getting config for id: " + str(id))
            return DEFAULT_CONFIG
    else:
        return DEFAULT_CONFIG


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
                'feedback': config.feedback,
            }
        }, True)

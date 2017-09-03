import json
import os

from pymongo import MongoClient

current_dir = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(current_dir, "configuration.cfg")
with open(config_file, 'r') as f:
    parames = f.read()
    parames = json.loads(parames)
DB_SERVER = parames['DB_SERVER']
USER_NAME = parames['USER_NAME']
DB_PASSWORD = parames['DB_PASSWORD']


def connect_todb():
    """
    connect to MongoDB server
    :return: 
    """
    uri = "mongodb://{}:{}@{}".format(USER_NAME, DB_PASSWORD, DB_SERVER)
    client = MongoClient(uri)
    db = client.get_database()
    model = db['model']
    return model

import json
import psycopg2
import pymongo

import constants


def load_postgres_credentials():
    with open(constants.POSTGRES_CREDENTIALS) as f:
        postgres_credentials = json.load(f)
    return postgres_credentials


def load_mongo_credentials():
    with open(constants.MONGO_CREDENTIALS) as f:
        mongo_credentials = json.load(f)
    return mongo_credentials


def connect_to_postgres():
    db_credentials = load_postgres_credentials()
    conn = psycopg2.connect(
        host=db_credentials['db_host'],
        database=db_credentials['db_name'],
        user=db_credentials['db_user'],
        password=db_credentials['db_pwd']
    )
    return conn


def connect_to_mongo():
    db_credentials = load_mongo_credentials()
    client = pymongo.MongoClient(
        "mongodb://{}:{}".format(db_credentials['db_host'], db_credentials['db_port'])
    )
    wsb_mongo_db = client['wsb_tendies']
    return wsb_mongo_db

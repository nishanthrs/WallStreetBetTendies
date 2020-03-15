import constants
import json
import psycopg2

def load_db_credentials():
    with open(constants.DB_CREDENTIALS) as f:
        db_credentials = json.load(f)
    return db_credentials


def connect_to_db():
    db_credentials = load_db_credentials()
    conn = psycopg2.connect(
        host=db_credentials['db_host'],
        database=db_credentials['db_name'],
        user=db_credentials['db_user'],
        password=db_credentials['db_pwd']
    )
    return conn

import json

def load_credentials(filename):
    with open(filename) as f:
        credentials = json.load(f)
    return credentials

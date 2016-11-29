from pymongo import MongoClient, errors

WEBAPP_DBNAME = 'hgp_webapp'
JOKERZ_DBNAME = 'hgp_jokerz'

# TODO: Move this to a config file.
localConnection = 'mongodb://127.0.0.1:27017/'
client = MongoClient(localConnection)
db = client[WEBAPP_DBNAME]
db_jokerz = client[JOKERZ_DBNAME]

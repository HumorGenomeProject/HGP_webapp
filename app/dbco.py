from pymongo import MongoClient

DBNAME = 'hgp_webapp'

client = MongoClient('mongodb://localhost:27017/')

db = client[DBNAME]

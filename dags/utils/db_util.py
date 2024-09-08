import pymongo

global client
client = pymongo.MongoClient(
    "mongodb://mongodb:27017",
    connect=False,
)

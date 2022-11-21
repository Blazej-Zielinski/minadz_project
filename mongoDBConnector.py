from pymongo import MongoClient


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    # CONNECTION_STRING = "mongodb+srv://user:user13@minadzd.fwbuzoz.mongodb.net/test"
    CONNECTION_STRING = "mongodb+srv://User1:Banan123!@cluster0.bkbovyp.mongodb.net/test"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['Project1']

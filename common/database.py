import os
from typing import Dict
import pymongo


class Database:
    # URI = os.environ.get("MONGODB_URI")  #from heroku
    # URI = "mongodb+srv://npaDB:npaadmin@cluster0-ipibu.gcp.mongodb.net/npaWebAppDB?retryWrites=true&w=majority"
    URI = "mongodb://npaDB:npaadmin@cluster0-shard-00-00-ipibu.gcp.mongodb.net:27017,cluster0-shard-00-01-ipibu.gcp.mongodb.net:27017,cluster0-shard-00-02-ipibu.gcp.mongodb.net:27017/npaWebAppDB?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"
    DATABASE = None
    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client.get_default_database()

    @staticmethod
    def insert(collection: str, data: Dict) -> None:
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection: str, query: Dict) -> pymongo.cursor:
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection: str, query: Dict) -> Dict:
        return Database.DATABASE[collection].find_one(query)
    
    @staticmethod
    def update(collection: str, query: Dict, data: Dict) -> None:
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection: str, query: Dict) -> Dict:
        return Database.DATABASE[collection].remove(query)



# mongo "mongodb+srv://cluster0-piua5.gcp.mongodb.net/priceService"  --username admin
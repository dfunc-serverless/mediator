from pymongo import MongoClient

from .config import Config


class Mongo:
    def __init__(self):
        self.url = Config.get("mongo_url", "mongodb://localhost:27017/")
        self.mongo_cli = MongoClient(self.url)

    def get_database(self, db, collection=None):
        if collection is None:
            return self.mongo_cli[db]
        else:
            return self.mongo_cli[db][collection]

    def close(self):
        self.mongo_cli.close()

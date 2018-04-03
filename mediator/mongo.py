from pymongo import MongoClient

from .config import Config


class Mongo:
    def __init__(self):
        """
        Mongo DB connection pool
        """
        self.url = Config.get("mongo_url", "mongodb://localhost:27017/")
        self.mongo_cli = MongoClient(self.url)

    def get_database(self, db, collection=None):
        """
        Function to get a specific DB or Collection
        :param db: Database name
        :param collection: Collection name
        :return: Returns cursor of the DB or collection
        """
        if collection is None:
            return self.mongo_cli[db]
        else:
            return self.mongo_cli[db][collection]

    def close(self):
        """
        Closes
        :return:
        """
        self.mongo_cli.close()

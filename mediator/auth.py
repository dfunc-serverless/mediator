from .mongo import Mongo

from bson.objectid import ObjectId


class Auth:
    mongo_cli = Mongo("dfunc")

    @classmethod
    def verify_auth_key(cls, auth_key):
        """
        To authenticate the API key
        :param auth_key: auth key supplied by the user
        :return: True of api_key is legal else False
        """
        key = ObjectId(auth_key)
        db = cls.mongo_cli.get_database(collection="users")
        if db.count({"_id": key}) > 0:
            return True
        return False

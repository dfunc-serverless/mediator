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

    @classmethod
    def verify_job(cls, auth_key, job_id):
        """
        Verify if the Job exists for user
        :param auth_key: User ID
        :param job_id: Job ID
        :return: Bool (True if legal)
        """
        key = ObjectId(job_id)
        user_id = ObjectId(auth_key)
        db = cls.mongo_cli.get_database(collection="jobs")
        if db.count({"_id": key, "user_id": user_id}) > 0:
            return True
        return False

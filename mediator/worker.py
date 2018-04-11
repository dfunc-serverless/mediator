from .config import Config
from .mongo import Mongo
from .redis_cli import RedisPool

from bson.objectid import ObjectId


class Worker:
    mongo_cli = Mongo("dfunc")
    redis_pool = RedisPool()
    collection_name = "workers"

    @classmethod
    def __get_db(cls):
        """
        Get Worker DB
        :return: DB instance
        """
        return cls.mongo_cli.get_database(collection=cls.collection_name)

    def __init__(self, worker_id):
        """
        Initialises Worker
        :param worker_id:
        """
        db = self.__get_db()
        data = db.find_one({
            "_id": ObjectId(worker_id)
        })
        if data is None:
            raise KeyError("Worker not registered")
        self.worker_id = worker_id
        self.data = data
        self.project = Config.get("project_name", "dfunc-bu")
        self.subscription_string = "projects/%s/topics/worker-%s" % \
                                   (self.project, worker_id)
        self.subscription_name = "projects/%s/subscriptions/worker-%s" % \
                                   (self.project, worker_id)

    @classmethod
    def worker_factory(cls, user_id, job=None):
        """
        Creates a worker for User
        :param user_id:
        :param job:
        :return: Worker object
        """
        data = {
            "user_id": ObjectId(user_id),
            "job": job
        }
        db = cls.__get_db()
        inserted_id = db.save(data)
        return cls(str(inserted_id))

    def push_to_queue(self):
        """
        Pushes worker into job queue
        """
        redis = self.redis_pool.get_connection()
        redis.publish(self.collection_name, self.worker_id)

    def add_job(self, job):
        if self.data["job"] is not None:
            self.data["job"] = job.get_data()
            db = self.__get_db()
            db.save(self.data)
        else:
            raise ValueError("Job already assigned")

    def remove_job(self):
        self.data["job"] = None
        db = self.__get_db()
        db.save(self.data)

    def delete(self):
        db = self.__get_db()
        db.delete_one({"_id": ObjectId(self.worker_id)})

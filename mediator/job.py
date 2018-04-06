from .mongo import Mongo
from .redis_cli import RedisPool

from bson.objectid import ObjectId


class Job:
    mongo_cli = Mongo("dfunc")

    def __init__(self, job_id):
        """
        Job Class
        :param job_id:
        """
        self.job_id = job_id
        job_table = self.mongo_cli.get_database(collection="jobs")
        self.data = job_table.find_one({"_id": ObjectId(self.job_id)})
        if self.data is None:
            raise KeyError("ID not found")

    @classmethod
    def job_factory(cls, job_name, user_id, image_dict, file_url=None):
        """
        Creates a new job with given data.
        :param job_name: name of th job
        :param user_id: name of the user
        :param image_dict: dictionary containing docker image metadata
                        {
                            "name": "<name of the docker image with repo>",
                            "tag": "<name of the tag to be pulled>",
                            "username": "username (for private repo's)",
                            "password": "password (for private repo's)"
                        }
        :param file_url: URL of the serverless function (optional)
        :return: object of type Job
        """
        job_table = cls.mongo_cli.get_database(collection="jobs")
        data = job_table.insert_one({
            "name": job_name,
            "file": file_url,
            "image": image_dict,
            "user": user_id
        })
        return cls(str(data["_id"]))


class JobQueue:
    def __init__(self, name):
        """
        Job Queue class
        :param name: name of the job queue
        """
        self.name = name
        self.collection_name = name + "_job_queue"
        self.redis_pool = RedisPool()
        self.mongo_cli = Mongo("dfunc")

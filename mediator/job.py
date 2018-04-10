from .mongo import Mongo
from .redis_cli import RedisPool

from bson.objectid import ObjectId
from bson.json_util import dumps


class Job:
    mongo_cli = Mongo("dfunc")
    collection_name = "jobs"

    @classmethod
    def __get_db(cls):
        """
        Get Job DB
        :return: DB instance
        """
        return cls.mongo_cli.get_database(collection=cls.collection_name)

    def __init__(self, job_id):
        """
        Job Class
        :param job_id:
        """
        self.job_id = job_id
        job_table = self.__get_db()
        if job_table.count() == 0:
            job_table.create_index("user_id")
        self.data = job_table.find_one({"_id": ObjectId(self.job_id)})
        if self.data is None:
            raise KeyError("ID not found")

    def get_data(self, json=False):
        """
        Get data
        :param json: get data as a JSON dump
        :return: data dictionary
        """
        return dumps(self.data) if json else self.data

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
        job_table = cls.__get_db()
        data = job_table.insert_one({
            "name": job_name,
            "file": file_url,
            "image": image_dict,
            "user_id": ObjectId(user_id)
        })
        return cls(str(data.inserted_id))


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

    def __get_db(self):
        """
        Get JobQueue DB
        :return: DB instance
        """
        return self.mongo_cli.get_database(self.collection_name)

    def add_job(self, job: Job, data: dict = None):
        """
        Adding Job to the Queue
        :param job: Job Object
        :param data: Data passed as Params
        :return: Job_ID from the Queue
        """
        jq_table = self.__get_db()
        inserted_row = jq_table.insert_one({
            "job": job.get_data(),
            "worker_id": None,
            "data": data
        })
        job_id = str(inserted_row.inserted_id)
        redis = self.redis_pool.get_connection()
        redis.publish(self.collection_name, job_id)
        return job_id

    def pull_job(self, job_id):
        """
        Pull Jobs from Queue
        :param job_id: JobQueue ID
        :return: Job data
        """
        jq_table = self.__get_db()
        job = jq_table.find_one({"_id": ObjectId(job_id)})
        return job

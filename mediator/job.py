from .config import Config
from .mongo import Mongo
from .redis_cli import RedisPool


class Job:
    def __init__(self, job_id):
        self.mongo_cli = Mongo()
        self.job_id = job_id


class JobQueue:
    def __init__(self):
        self.redis_pool = RedisPool()
        self.mongo_cli = Mongo()

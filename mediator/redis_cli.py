import redis
from .config import Config


class RedisPool:
    def __init__(self):
        """
        Redis Connection Pool Manager
        Configurations:
            Name                | Default
            --------------------|-----------
            DFUNC_REDIS_HOST    | 127.0.0.1
            DFUNC_REDIS_PORT    | 6397
            DFUNC_REDIS_DB      | 0
        """
        self.host = Config.get("redis_host", default="127.0.0.1")
        self.port = Config.get("redis_port", default=6379)
        self.db = Config.get("redis_db", default=0)
        self.pool = redis.ConnectionPool(
            host=self.host, port=self.port, db=self.db)

    def get_connection(self):
        """
        Get a session from the Connection pool
        :return: instantiated StrictRedis
        """
        return redis.StrictRedis(connection_pool=self.pool)

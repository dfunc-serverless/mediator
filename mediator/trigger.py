from .job import Job, JobQueue
from .config import Config

from flask import request


def trigger(job_id):
    """
    Triggers Job Execution, uses Flask's request object to pull request data
    :param job_id: Job to be executed
    :return: Job ID
    """
    queue_name = Config.get("queue_name", "main")
    data = None
    if request.data:
        data = request.get_json()
    job = Job(job_id)
    job_queue = JobQueue(queue_name)
    return job_queue.add_job(job, data)

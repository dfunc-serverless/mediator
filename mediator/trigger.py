from .job import Job, JobQueue
from .config import Config


def trigger(job_id, data=None):
    """
    Triggers Job Execution, uses Flask's request object to pull request data
    :param job_id: Job to be executed
    :param data: data to be passed to the function (optional)
    :return: Job ID
    """
    queue_name = Config.get("queue_name", "main")
    job = Job(job_id)
    job_queue = JobQueue(queue_name)
    return job_queue.add_job(job, data)

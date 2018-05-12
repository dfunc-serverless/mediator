from .job import Job, JobQueue
from .config import Config


class Trigger:
    def __init__(self):
        self.queue_name = Config.get("queue_name", "main")
        self.job_queue = JobQueue(self.queue_name)

    def trigger(self, job_id, data=None):
        """
        Triggers Job Execution, uses Flask's request object to pull request data
        :param job_id: Job to be executed
        :param data: data to be passed to the function (optional)
        :return: Job ID
        """
        job = Job(job_id)
        return self.job_queue.add_job(job, data)

    def initiate_job(self, jq_id, worker_id):
        """
        Changes status of the Job to executing and return job's metadata.
        :param jq_id:
        :return:
        """
        job = self.job_queue.pull_job(jq_id)
        self.job_queue.update_status(jq_id, worker_id, 1)  # Set to executing
        return job

    def complete_job(self, jq_id, worker_id, status: int, data=None):
        """
        Updates job status
        :param jq_id:
        :param status:
        :param data:
        :return:
        """
        self.job_queue.update_status(jq_id, worker_id, status, data)

    def get_job(self, jq_id):
        """
        Fetches Job from Job queue with status
        :param jq_id: Job Queue ID
        :return: Job Queue data
        """
        return self.job_queue.get_job_instance(jq_id)

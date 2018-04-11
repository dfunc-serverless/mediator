from json import loads

from flask import Flask, request, abort, jsonify

from mediator import trigger, Auth, Worker, Job, Config

app = Flask(__name__)
RECEIVER_FILE_PATH = Config.get("receiver_file", "dfunc-bu-receiver.json")
RECEIVER_FILE = loads(open(RECEIVER_FILE_PATH, 'r').read())


@app.route("/")
def index():
    """
    Get Hello World at Index
    :return:
    """
    return "Hello World"


@app.route("/trigger/<api_key>/<job_id>")
def add_job(api_key, job_id):
    """
    To trigger a job
    :param api_key: user id of the client
    :param job_id: job to be executed
    :return: job queue id
    """
    if Auth.verify_auth_key(api_key):
        if Auth.verify_job(api_key, job_id):
            data = None
            if request.data:
                data = request.get_json()
            return trigger(job_id, data)
    return abort(400)


@app.route("/worker/<api_key>")
def create_worker(api_key):
    """
    To register a worker node
    :param api_key: user id
    :return: worker id
    """
    if Auth.verify_auth_key(api_key):
        worker = Worker.worker_factory(api_key)
        worker.push_to_queue()
        return jsonify({
            "worker_id": worker.worker_id,
            "subscriber_json": RECEIVER_FILE,
            "subscription_string": worker.subscription_string,
            "subscription_name": worker.subscription_name
        })
    return abort(400)


@app.route("/worker/<api_key>/<worker_id>")
def register_worker(api_key, worker_id):
    """
    Register worker to schedule jobs
    :param api_key: user id
    :param worker_id: worker id
    :return: worker id
    """
    if Auth.verify_auth_key(api_key):
        if Auth.verify_worker(api_key, worker_id):
            worker = Worker(worker_id)
            worker.remove_job()
            worker.push_to_queue()
            return jsonify({
                "worker_id": worker.worker_id
            })
    return abort(400)


@app.route("/worker/<api_key>/<worker_id>/<job_id>")
def register_job(api_key, worker_id, job_id):
    """
    Confirm contract between Job and worker
    :param api_key:
    :param worker_id:
    :param job_id:
    :return:
    """
    if Auth.verify_auth_key(api_key):
        if Auth.verify_worker(api_key, worker_id):
            job = Job(job_id)
            worker = Worker(worker_id)
            worker.add_job(job)
            return job.get_data(json=True)
    abort(400)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)

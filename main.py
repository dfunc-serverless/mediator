from json import loads

from flask import Flask, request, abort, jsonify

from mediator import Trigger, Auth, Worker, Job, Config

app = Flask(__name__)
RECEIVER_FILE_PATH = Config.get("receiver_file", "dfunc-bu-receiver.json")
RECEIVER_FILE = loads(open(RECEIVER_FILE_PATH, 'r').read())

trigger = Trigger()


@app.route("/")
def index():
    """
    Get Hello World at Index
    :return:
    """
    return "Hello World", 200


@app.route("/trigger/<api_key>/<job_id>", methods=["GET", "POST"])
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
            return trigger.trigger(job_id, data)
    return abort(400)


@app.route("/worker/<api_key>", methods=["PUT"])
def create_worker(api_key):
    """
    To register a worker node
    :param api_key: user id
    :return: worker id
    """
    if Auth.verify_auth_key(api_key):
        worker = Worker.worker_factory(api_key)
        return jsonify({
            "worker_id": worker.worker_id,
            "subscriber_json": RECEIVER_FILE,
            "subscription_string": worker.subscription_string,
            "subscription_name": worker.subscription_name
        })
    return abort(400)


@app.route("/worker/<api_key>/<worker_id>", methods=["PUT"])
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


@app.route("/worker/<api_key>/<worker_id>/<jq_id>",
           methods=["PUT", "POST", "DELETE"])
def register_job(api_key, worker_id, jq_id):
    """
    Confirm contract between Job and worker
    :param api_key:
    :param worker_id:
    :param jq_id:
    :return: JSON dump of the job
    """
    if Auth.verify_auth_key(api_key):
        if Auth.verify_worker(api_key, worker_id):
            worker = Worker(worker_id)
            if request.method == "PUT":
                job = trigger.initiate_job(jq_id)
                worker.add_job(job)
                return jsonify(job.get_data())
            elif request.method == "POST":
                data = None
                if request.data:
                    data = request.get_json()
                worker.remove_job()
                trigger.complete_job(jq_id, 2, data)
                return "", 200
            elif request.method == "DELETE":
                data = request.data
                worker.remove_job()
                trigger.complete_job(jq_id, 3, data)
                return "", 200
    abort(400)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)

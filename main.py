from flask import Flask, request, abort

from mediator import trigger, Auth, Worker, Job

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World"


@app.route("/trigger/<api_key>/<job_id>")
def add_job(api_key, job_id):
    if Auth.verify_auth_key(api_key):
        if Auth.verify_job(api_key, job_id):
            data = None
            if request.data:
                data = request.get_json()
            return trigger(job_id, data)
    return abort(400)


@app.route("/worker/<api_key>")
def create_worker(api_key):
    if Auth.verify_auth_key(api_key):
        worker = Worker.worker_factory(api_key)
        worker.push_to_queue()
        return worker.worker_id
    return abort(400)


@app.route("/worker/<api_key>/<worker_id>/<job_id>")
def register_job(api_key, worker_id, job_id):
    if Auth.verify_auth_key(api_key):
        if Auth.verify_worker(api_key, worker_id):
            job = Job(job_id)
            worker = Worker(worker_id)
            worker.add_job(job)
            return job.get_data(json=True)
    abort(400)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)

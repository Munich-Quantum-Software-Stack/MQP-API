from flask import Blueprint, request, g

blueprint = Blueprint("jobs", __name__)


import bqp_database_access as database


@blueprint.post("/job")
def job_creation():
    # validate shots, circuit
    shots = request.form["shots"]
    circuit = request.form["circuit"]

    uuid = database.jobs.create_job(shots, circuit, g.token)

    return str(uuid)


@blueprint.get("/job")
def job_get_status():
    return "RUNNING STATUS"


@blueprint.delete("/job")
def job_cancel():
    return "JOB CANCELLED"


@blueprint.get("/job/result")
def job_result():
    return "RESULT"

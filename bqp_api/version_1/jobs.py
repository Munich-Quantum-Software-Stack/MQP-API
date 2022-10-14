from flask import Blueprint

blueprint = Blueprint("jobs", __name__)


@blueprint.post("/job")
def job_creation():
    return "JOB CREATED"


@blueprint.get("/job")
def job_get_status():
    return "RUNNING STATUS"


@blueprint.delete("/job")
def job_cancel():
    return "JOB CANCELLED"


@blueprint.get("/job/result")
def job_result():
    return "RESULT"

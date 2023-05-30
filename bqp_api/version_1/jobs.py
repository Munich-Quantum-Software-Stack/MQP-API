from typing import Optional
from flask import Blueprint, request, g

blueprint = Blueprint("jobs", __name__)


import bqp_database_access as database


def _get_job(uuid: str) -> Optional["Job"]:
    jobs = database.jobs.fetch_by_identity(g.user.email)
    job = next((x for x in jobs if str(x.id) == uuid), None)
    return job


@blueprint.post("/job")
def job_creation():
    shots = request.json["shots"]
    circuit = request.json["circuit"]
    resource_name = request.json["resource_name"]

    job = database.jobs.create_job(shots, circuit, g.token, resource_name)

    return {"uuid": str(job.id)}, 201


@blueprint.get("/job/<uuid>")
def job(uuid):
    job = _get_job(uuid)
    if job is None:
        return "JOB NOT FOUND", 404
    return {
        # TODO: Add more fields
        "id": job.id,
        "shots": job.shots,
        "result": job.result,
        "status": job.status,
    }


@blueprint.get("/job/<uuid>/status")
def job_get_status(uuid):
    job = _get_job(uuid)
    if job is None:
        return "JOB NOT FOUND", 404
    return {"status": job.status}


@blueprint.get("/job/<uuid>/result")
def job_result(uuid):
    job = _get_job(uuid)
    if job is None:
        return "JOB NOT FOUND", 404
    result = job.result
    return {"result": result}


@blueprint.delete("/job/<uuid>")
def job_cancel(uuid):
    job = _get_job(uuid)
    if job is None:
        return "JOB NOT FOUND", 404
    job.status = "CANCELLED"
    return "OK"

from typing import Optional
from flask import Blueprint, request, g
from eliot import log_call

blueprint = Blueprint("jobs", __name__)


import bqp_database_access as database


def _get_job(uuid: str) -> Optional["Job"]:
    jobs = database.jobs.fetch_by_identity(g.user.email)
    job = next((x for x in jobs if str(x.id) == uuid), None)
    return job


@blueprint.post("/job")
@log_call
def job_creation():
    bearer_token = request.headers["Authorization"]
    bearer_token.startswith("Bearer ")
    job = database.jobs.create_job(
        shots=request.json["shots"],
        circuit=request.json["circuit"],
        token=bearer_token[7:],
        target_spec=request.json["resource_name"],
        circuit_format=request.json["circuit_format"],
    )

    return {"uuid": str(job.id)}, 201


@blueprint.get("/job/<uuid>")
@log_call
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
@log_call
def job_get_status(uuid):
    job = _get_job(uuid)
    if job is None:
        return "JOB NOT FOUND", 404
    return {"status": job.status}


@blueprint.get("/job/<uuid>/result")
@log_call
def job_result(uuid):
    job = _get_job(uuid)
    if job is None:
        return "JOB NOT FOUND", 404
    result = job.result
    return {"result": result}


@blueprint.delete("/job/<uuid>")
@log_call
def job_cancel(uuid):
    job = _get_job(uuid)
    if job is None:
        return "JOB NOT FOUND", 404

    job.status = "CANCELLED"
    return "OK"


@blueprint.get("/job/<uuid>/cancel_reason")
@log_call
def job_get_cancel_reason(uuid):
    job = _get_job(uuid)

    if job is None:
        return "JOB NOT FOUND", 404
    return {"cancel_reason": job.cancel_reason}

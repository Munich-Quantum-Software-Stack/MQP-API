from typing import Optional

from eliot import log_call
from flask import Blueprint, g, jsonify, request

blueprint = Blueprint("jobs", __name__)


import bqp_database_access as database


def _get_job(uuid: str) -> Optional["Job"]:

    job = database.jobs.fetch_result_by_job_id_and_identity(uuid, g.user.identity)

    return job


@blueprint.post("/job")
@log_call
def job_creation():
    bearer_token = request.headers["Authorization"]
    bearer_token.startswith("Bearer ")
    owner_id = database.tokens.verify_token(bearer_token[7:]).owner.identity

    _target = request.json["resource_name"]
    if _target is not None:
        available_targets = database.resources.fetch_all_target_specification_names()
        if not request.json["resource_name"] in available_targets:
            return jsonify("BACKEND NOT FOUND"), 404

    # TODO It is just a tmp fix. Get budget of the user here.
    _budget = "temp_budget"
    # TODO Also check if the resource_name is available
    try:
        no_modify = request.json["no_modify"]
    except KeyError:
        no_modify = False
    job = database.jobs.create_job(
        shots=request.json["shots"],
        circuit=request.json["circuit"],
        owner=owner_id,
        budget=_budget,
        target_spec=request.json["resource_name"],
        circuit_format=request.json["circuit_format"],
        no_modify=no_modify,
    )

    return {"uuid": str(job.id)}, 201


@blueprint.get("/job/<uuid>")
@log_call
def job(uuid):
    job = _get_job(uuid)
    if job is None:
        return jsonify("JOB NOT FOUND"), 404

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
        return jsonify("JOB NOT FOUND"), 404
    return {"status": job.status}


@blueprint.get("/job/<uuid>/result")
@log_call
def job_result(uuid):
    job = _get_job(uuid)
    if job is None:
        return jsonify("JOB NOT FOUND"), 404
    result = job.result
    try:
        timestamp_scheduled = (
            str(job.timestamp_scheduled) if job.timestamp_scheduled else ""
        )
        timestamp_submitted = (
            str(job.timestamp_submitted) if job.timestamp_submitted else ""
        )
        timestamp_completed = (
            str(job.timestamp_completed) if job.timestamp_completed else ""
        )

    except AttributeError:
        timestamp_completed = ""

    return {
        "result": result,
        "timestamp_scheduled": timestamp_scheduled,
        "timestamp_submitted": timestamp_submitted,
        "timestamp_completed": timestamp_completed,
    }


@blueprint.delete("/job/<uuid>")
@log_call
def job_cancel(uuid):
    job = _get_job(uuid)
    if job is None:
        return jsonify("JOB NOT FOUND"), 404

    job.status = "CANCELLED"
    return "OK"


@blueprint.get("/job/<uuid>/cancel_reason")
@log_call
def job_get_cancel_reason(uuid):
    job = _get_job(uuid)

    if job is None:
        return jsonify("JOB NOT FOUND"), 404
    return {"cancel_reason": job.note}

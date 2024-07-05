from typing import Optional
from flask import Blueprint, request, g
from eliot import log_call

blueprint = Blueprint("hamiltonian_jobs", __name__)

import bqp_database_access as database


def _get_hamiltonian_job(uuid: str) -> Optional["HamiltonianJob"]:
    jobs = database.jobs.fetch_hamiltonian_job_by_identity(g.user.identity)
    job = next((x for x in jobs if str(x.id) == uuid), None)
    return job


@blueprint.post("/hamiltonian_job")
@log_call
def hamiltonian_job_creation():
    bearer_token = request.headers["Authorization"]
    bearer_token.startswith("Bearer ")
    owner_id = database.tokens.verify_token(bearer_token[7:]).owner.identity

    _budget = "temp_budget"

    hamiltonian_job = database.jobs.create_hamiltonian_job(
        interaction_str=request.json["interaction_str"],
        coefficients_str=request.json["coefficients_str"],
        owner=owner_id,
        budget=_budget,
        target_spec=request.json["resource_name"],
    )

    return {"uuid": str(hamiltonian_job.id)}, 201


@blueprint.get("/hamiltonian_job/<uuid>")
@log_call
def hamiltonian_job(uuid):
    hamiltonian_job = _get_hamiltonian_job(uuid)
    if hamiltonian_job is None:
        return "HAMILTONIAN JOB NOT FOUND", 404

    return {
        # TODO: Add more fields
        "id": hamiltonian_job.id,
        "interaction_str": hamiltonian_job.interaction_str,
        "result": hamiltonian_job.result,
        "status": hamiltonian_job.status,
    }


@blueprint.get("/hamiltonian_job/<uuid>/status")
@log_call
def hamiltonian_job_get_status(uuid):
    hamiltonian_job = _get_hamiltonian_job(uuid)
    if hamiltonian_job is None:
        return "HAMILTONIAN JOB NOT FOUND", 404
    return {"status": hamiltonian_job.status}


@blueprint.get("/hamiltonian_job/<uuid>/result")
@log_call
def hamiltonian_job_result(uuid):
    hamiltonian_job = _get_hamiltonian_job(uuid)
    if hamiltonian_job is None:
        return "HAMILTONIAN JOB NOT FOUND", 404
    result = hamiltonian_job.result
    return {"result": result}


@blueprint.delete("/hamiltonian_job/<uuid>")
@log_call
def hamiltonian_job_cancel(uuid):
    hamiltonian_job = _get_hamiltonian_job(uuid)
    if hamiltonian_job is None:
        return "HAMILTONIAN JOB NOT FOUND", 404

    job.status = "CANCELLED"
    return "OK"


@blueprint.get("/hamiltonian_job/<uuid>/cancel_reason")
@log_call
def hamiltonian_job_get_cancel_reason(uuid):
    hamiltonian_job = _get_hamiltonian_job(uuid)

    if hamiltonian_job is None:
        return "HAMILTONIAN JOB NOT FOUND", 404
    return {"cancel_reason": hamiltonian_job.note}

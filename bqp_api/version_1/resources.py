import bqp_database_access as database  # type: ignore
from eliot import log_call  # type: ignore
from flask import Blueprint, g

blueprint = Blueprint("resources", __name__)


def resource_to_json(_resource: "Resource") -> dict:  # type: ignore
    return {
        "name": _resource.name,
        "qubits": _resource.qubits,
        "online": not _resource.maintenance,
        "connectivity": _resource.connectivity,
        "instructions": _resource.instructions,
    }


@blueprint.route("/resources")
@log_call
def resources():
    _resources = database.resources.fetch_resources_available_to_identity(
        g.user.identity
    )
    return {_resource.name: resource_to_json(_resource) for _resource in _resources}


@blueprint.route("/resources/<resource_name>")
@log_call
def resource(resource_name):
    _resources = database.resources.fetch_resources_available_to_identity(
        g.user.identity
    )
    _resource = next((x for x in _resources if x.name == resource_name), None)
    if _resource is None:
        return "RESOURCE NOT FOUND", 404
    return resource_to_json(_resource)


@blueprint.get("/resources/<resource_name>/num_pending_jobs")
@log_call
def get_resource_num_pending_jobs(resource_name):
    _resources = database.resources.fetch_resources_available_to_identity(
        g.user.identity
    )
    _resource = next((x for x in _resources if x.name == resource_name), None)
    if _resource is None:
        return "RESOURCE NOT FOUND", 404
    num_pending_jobs = database.resources.fetch_resource_num_queued_jobs(resource_name)
    return {"num_pending_jobs": num_pending_jobs}

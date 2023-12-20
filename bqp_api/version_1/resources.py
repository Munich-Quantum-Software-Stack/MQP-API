from flask import Blueprint, g
from eliot import log_call

import bqp_database_access as database

blueprint = Blueprint("resources", __name__)


def resource_to_json(resource: "Resource") -> dict:
    return {
        "name": resource.name,
        "qubits": resource.qubits,
    }


@blueprint.route("/resources")
@log_call
def resources():
    resources = database.resources.fetch_resources_available_to_identity(
        g.user.identity
    )
    return {resource.name: resource_to_json(resource) for resource in resources}


@blueprint.route("/resources/<resource_name>")
@log_call
def resource(resource_name):
    resources = database.resources.fetch_resources_available_to_identity(
        g.user.identity
    )
    resource = next((x for x in resources if x.name == resource_name), None)
    if resource is None:
        return "RESOURCE NOT FOUND", 404
    return resource_to_json(resource)

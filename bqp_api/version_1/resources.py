from flask import Blueprint

blueprint = Blueprint("resources", __name__)


@blueprint.route("/resources")
def resources():
    return "RESOURCES"

from flask import Blueprint


from . import resources
from . import jobs


blueprint = Blueprint("version_1", __name__, url_prefix="/v1")
blueprint.register_blueprint(resources.blueprint)
blueprint.register_blueprint(jobs.blueprint)

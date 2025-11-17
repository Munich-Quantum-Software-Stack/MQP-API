from flask import Blueprint

from . import hamiltonian_jobs, jobs, resources, job_metrics

blueprint = Blueprint("version_1", __name__, url_prefix="/v1")
blueprint.register_blueprint(resources.blueprint)
blueprint.register_blueprint(jobs.blueprint)
blueprint.register_blueprint(job_metrics.blueprint)
blueprint.register_blueprint(hamiltonian_jobs.blueprint)

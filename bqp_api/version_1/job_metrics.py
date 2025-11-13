from typing import Optional

import bqp_database_access as database  # type: ignore
from eliot import log_call  # type: ignore
from flask import Blueprint, g, request

blueprint = Blueprint("job_metrics", __name__)


@blueprint.get("/job_metrics/<uuid>/stats")
@log_call
def job_metrics(uuid):
    _job_metrics = database.job_metrics.fetch_job_metrics_by_identity(uuid)(uuid)
    if _job_metrics is None:
        return "JOB METRICS NOT FOUND", 404

    return {
        "id": _job_metrics.id,
        "API": _job_metrics.API_exit - _job_metrics.API_entry,
        "QDB": _job_metrics.QDB_exit - _job_metrics.QDB_entry,
        "QJR": _job_metrics.QJR_exit - _job_metrics.QJR_entry,
        "ISV_JR": _job_metrics.ISV_JR_exit - _job_metrics.ISV_JR_entry,
        "Quantum_Daemon_JR": _job_metrics.Quantum_Daemon_JR_exit - _job_metrics.Quantum_Daemon_JR_entry,
        "Generator": _job_metrics.Generator_exit - _job_metrics.Generator_entry,
        "Scheduler": _job_metrics.Scheduler_exit - _job_metrics.Scheduler_entry,
        "Pass_runner": _job_metrics.Pass_runner_exit - _job_metrics.Pass_runner_entry,
        "Transpiler": _job_metrics.Trnaspiler_exit - _job_metrics.Transpiler_entry,
        "Submitter": _job_metrics.Submitter_exit - _job_metrics.Submitter_entry,
        "Pass_selection": _job_metrics.Pass_selection_exit - _job_metrics.Pass_selection_entry,
        "Knitter": _job_metrics.Knitter_exit - _job_metrics.Knitter_entry,
        "Job_execution": _job_metrics.Job_execution_end - _job_metrics.Job_execution_start
    }

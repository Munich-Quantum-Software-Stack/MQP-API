from typing import Optional

import bqp_database_access as database  # type: ignore
from eliot import log_call  # type: ignore
from flask import Blueprint, g, request

blueprint = Blueprint("job_metrics", __name__)


@blueprint.get("/job/<uuid>/stats")
@log_call
def job_metrics(uuid):
    try:
        _job_metrics = database.job_metrics.fetch_timestamp_data_by_job_id(uuid)[0]
    except Exception as e:
        return "JOB METRICS NOT FOUND", 404

    if _job_metrics is None:
        return "JOB METRICS NOT FOUND", 404

    def _diff(exit_ts, entry_ts):
        # return None if either timestamp is missing (optional fields)
        if exit_ts is None or entry_ts is None:
            return None
        delta = exit_ts - entry_ts
        return str(delta.total_seconds())

    return {
        "mqp_api": _diff(_job_metrics.api_exit, _job_metrics.api_entry),
        "quantum_database": _diff(_job_metrics.qdb_exit, _job_metrics.qdb_entry),
        "quantum_job_runner": _diff(_job_metrics.qjr_exit, _job_metrics.qjr_entry),
        "isv_job_runner": _diff(_job_metrics.isv_jr_exit, _job_metrics.isv_jr_entry),
        "quantum_daemon_job_runner": _diff(
            _job_metrics.quantum_daemon_jr_exit, _job_metrics.quantum_daemon_jr_entry
        ),
        "generator": _diff(_job_metrics.generator_exit, _job_metrics.generator_entry),
        "scheduler": _diff(_job_metrics.scheduler_exit, _job_metrics.scheduler_entry),
        "pass_runner": _diff(
            _job_metrics.pass_runner_exit, _job_metrics.pass_runner_entry
        ),
        "transpiler": _diff(
            _job_metrics.transpiler_exit, _job_metrics.transpiler_entry
        ),
        "submitter": _diff(_job_metrics.submitter_exit, _job_metrics.submitter_entry),
        "pass_selection": _diff(
            _job_metrics.pass_selection_exit, _job_metrics.pass_selection_entry
        ),
        "knitter": _diff(_job_metrics.knitter_exit, _job_metrics.knitter_entry),
        "job_execution": _diff(
            _job_metrics.job_execution_end, _job_metrics.job_execution_start
        ),
    }

from http import HTTPStatus

from conftest import TEST_TARGET


def test_job_creation(client) -> None:
    """Test if it is possible to create a circuit job."""

    job_data = {
        "shots": 1000,
        "circuit": 'OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[1];\ncreg c[1];\nh q[0];\nmeasure q[0] -> c[0];\n',
        "circuit_format": "qasm",
        "resource_name": TEST_TARGET,
    }

    response = client.post("/v1/job", json=job_data, headers=client.headers)

    assert response.status_code == HTTPStatus.CREATED
    assert "uuid" in response.get_json()

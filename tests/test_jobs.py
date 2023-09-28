from http import HTTPStatus


def test_job_creation(client) -> None:
    """Test if it is possible to create a circuit job."""

    job_data = {"shots": 1000, "circuit": "", "circuit_format": "", "resource_name": ""}

    response = client.post("/v1/job", json=job_data, headers=client.headers)

    assert response.status_code == HTTPStatus.OK

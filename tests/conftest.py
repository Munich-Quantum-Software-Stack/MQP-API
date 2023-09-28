import os

import pytest
import bqp_database_access as database_access
from bqp_database_access._database import open_database

from datetime import datetime, timedelta
from pony.orm import db_session

import string
import secrets

from werkzeug.datastructures import Headers

from bqp_api import create_app


def generate_token() -> str:
    return "".join(
        secrets.choice(string.ascii_letters + string.digits) for _ in range(64)
    )


def create_local_database(token: str) -> None:
    db = open_database(create_tables=True)
    db.disconnect()

    MAX_BUDGET_USAGE = 1000
    MAX_JOBS = 10

    with db_session:
        database_access.users.create_new_security_level(
            "BASIC",
            token_max_live_count=10,
            token_max_lifetime=30,
            token_min_creation_interval=0,
            token_max_jobs=MAX_JOBS,
            token_max_budget=MAX_BUDGET_USAGE,
            token_max_rate=1,
            login_max_interval=365,
        )

        database_access.users.create_new_user_with_secret(
            "test_user", "test_password", "BASIC", "test@lrz.de", "LRZ", "quantum"
        )

        database_access.tokens.add_new_token(
            name="test_token",
            owner="test_user",
            token=token,
            expiration=datetime.now() + timedelta(hours=1),
            max_budget_usage=MAX_BUDGET_USAGE,
            max_jobs=MAX_JOBS,
        )


def delete_local_database() -> None:
    db = open_database()
    path = db.provider.pool.filename
    db.disconnect()
    os.remove(path)


@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    token = generate_token()
    app.token = token

    # other setup can go here
    create_local_database(token)

    yield app

    # clean up / reset resources here

    delete_local_database()


@pytest.fixture()
def client(app):
    client = app.test_client()

    client.headers = Headers()
    client.headers.add("Content-Type", "application/json")
    client.headers.add("Authorization", "Bearer " + app.token)

    return client

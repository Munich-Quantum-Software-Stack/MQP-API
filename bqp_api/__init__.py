import http
import sys

import bqp_database_access as database  # type: ignore
from eliot import log_call  # type: ignore
from flask import Flask, abort, g, request
from pony.flask import Pony  # type: ignore

from . import version_1


class TokenNotRecognized(Exception):
    pass


def create_app():
    app = Flask(__name__)
    Pony(app)

    app.register_blueprint(version_1.blueprint)

    @app.before_request
    @log_call
    def validate_token() -> None:
        # TODO refactor this
        try:
            bearer_token = request.headers["Authorization"]

            if (
                bearer_token.startswith("Bearer ")
                and (token := database.tokens.verify_token(bearer_token[7:]))
                is not None
            ):
                g.user = token.owner
                g.token = token

                return

            raise TokenNotRecognized

        except Exception as _:
            abort(http.HTTPStatus.FORBIDDEN.value)

    return app

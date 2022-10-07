from flask import Flask, abort, request
import http
import sys


from . import version_1
from .auth import verify_token


def create_app():
    app = Flask(__name__)

    app.register_blueprint(version_1.blueprint)

    @app.before_request
    def validate_token() -> None:
        # TODO refactor this
        try:
            token = request.headers["Authorization"]

            if token.startswith("Bearer ") and verify_token(token[7:]):
                return

            else:
                abort(http.HTTPStatus.FORBIDDEN.value)

        except:
            abort(http.HTTPStatus.FORBIDDEN.value)

    return app

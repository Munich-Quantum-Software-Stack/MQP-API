from flask import Flask, abort, request, g
from pony.flask import Pony
import http
import sys
from os import getpid


from eliot import log_call, to_file, log_message


import bqp_database_access as database

from . import version_1


@log_call
def create_app():
    to_file(open(f"bqp_api_{getpid()}.log", "a"))

    app = Flask(__name__)
    Pony(app)

    app.register_blueprint(version_1.blueprint)

    @app.before_request
    @log_call
    def validate_token() -> None:
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

            else:
                log_message(
                    message_type="database rejected token",
                    bearer_token=bearer_token,
                    database_response=token,
                )

                abort(http.HTTPStatus.FORBIDDEN.value)

        except Exception as error:
            print(error)
            abort(http.HTTPStatus.FORBIDDEN.value)

    return app

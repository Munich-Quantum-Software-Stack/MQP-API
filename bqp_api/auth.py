from flask import request
import bcrypt
import sys

import bqp_database_access as database


def verify_token(token: str) -> bool:
    quantum_db = database.open()

    print(f"verifying {token}", file=sys.stderr)

    # return bcrypt.checkpw(
    #
    #     salted_token_hash,
    # )

    return True

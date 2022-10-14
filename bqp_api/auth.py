from flask import g
import bcrypt
import sys

import bqp_database_access as database


def verify_token(token: str) -> bool:
    if (user := database.verify_token(token)) is None:
        return False

    g.user = user

import os

bind = "0.0.0.0:4000"
workers = 8
wsgi_app = "bqp_api:create_app()"
certfile = os.getenv("CERT_FILE") or None
keyfile = os.getenv("KEY_FILE") or None

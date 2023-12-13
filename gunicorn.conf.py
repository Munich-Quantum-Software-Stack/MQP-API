bind = "0.0.0.0:4000"
workers = 1
wsgi_app = "bqp_api:create_app()"
certfile = "/etc/bqp-certs/portal_quantum_lrz_de.crt.pem"
keyfile = "/etc/bqp-certs/portal-sec-key-ohnepass.pem"

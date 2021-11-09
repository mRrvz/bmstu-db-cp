""" Flask Web-application for working with the work program of the discipline """

import time

import flask_restplus
from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix

import routes.cache
import routes.rpd

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config['JSON_AS_ASCII'] = False

api = flask_restplus.Api(app, doc="/api/v1")
api.add_namespace(routes.cache.namespace)
api.add_namespace(routes.rpd.namespace)

@app.route("/")
def hello():
    return "Hello World"


if __name__ == "__main__":
    # Waiting for databse initialization
    time.sleep(1)
    app.run(host='0.0.0.0', debug=True)

""" Flask Web-application for working with the work program of the discipline """

import time

from flask_jwt_extended import JWTManager
import flask_restplus
import routes.cache
import routes.rpd
import routes.user
from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config['SECRET_KEY'] = 'secret-string'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JSON_AS_ASCII'] = False

jwt = JWTManager(app)

api = flask_restplus.Api(app, doc="/api/v1")
api.add_namespace(routes.cache.namespace)
api.add_namespace(routes.rpd.namespace)
api.add_namespace(routes.user.namespace)

@app.route("/")
def hello():
    return "Hello World"


if __name__ == "__main__":
    # Waiting for databse initialization
    time.sleep(1)
    app.run(host='0.0.0.0', debug=True)

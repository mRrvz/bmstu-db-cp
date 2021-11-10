import logging

import db.models as models
import flask_restplus
from flask import request
from routes.rpd import cache, controller
from services.handler import RequestHandler

namespace = flask_restplus.Namespace("user", "User management", path="/")

@namespace.route("/api/v1/user")
class SaveUser(flask_restplus.Resource):
    @namespace.doc(
        responses={
            200: "Successful operation",
            500: "Internal error",
        }
    )

    @namespace.produces("application/json")
    def post(self):
        logging.info("/user (POST) router called")
        repo_psql = controller.user_repo_psql
        user = request.get_json()

        try:
            model = models.User(user["username"], user["password"], user["email"], user["status"])
            repo_psql.save(model)
        except Exception as err:
            logging.error(err)
            return RequestHandler.error_response(500, err)

        return RequestHandler.success_response(message=f"User successfully added!", data=model)


@namespace.route("/api/v1/user/<string:username>")
class DeleteUser(flask_restplus.Resource):
    @namespace.doc(
        responses={
            200: "Successful operation",
            400: "Invalid username supplied",
            404: "User not found",
            500: "Internal error",
        }
    )

    @namespace.doc(params={"username": "User name to delete"})
    @namespace.produces("application/json")
    def delete(self, username):
        logging.info("/user (DELETE) router called")
        repo_psql = controller.user_repo_psql

        try:
            repo_psql.remove(username)
        except Exception as err:
            logging.error(err)
            return RequestHandler.error_response(500, err)

        return RequestHandler.success_response(message=f"User successfully deleted")

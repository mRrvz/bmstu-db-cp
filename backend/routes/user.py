import logging

import flask_restplus
from flask import request
from flask_jwt_extended import jwt_required

from routes.handler import RequestHandler
from services.init import get_user_service

namespace = flask_restplus.Namespace("user", "User management", path="/")
user_service = get_user_service()

user_model = namespace.model(
    "user",
    {
        "username": flask_restplus.fields.String(
            required=True, description="User's username"
        ),
        "email": flask_restplus.fields.String(
            required=True, description="User's email"
        ),
        "password": flask_restplus.fields.String(
            required=True, description="User's password"
        ),
    },
)

login_model = namespace.model(
    "login_user",
    {
        "username": flask_restplus.fields.String(
            required=True, description="User's username"
        ),
        "password": flask_restplus.fields.String(
            required=True, description="User's password"
        ),
    },
)

@namespace.route("/api/v1/user/info")
class GetInfo(flask_restplus.Resource):
    @namespace.doc(
        response={
            200: "Successful operation",
            500: "Internal error",
        }
    )

    @jwt_required
    def get(self):
        return {"message": "Information about user"}


@namespace.route("/api/v1/user/login")
class LoginUser(flask_restplus.Resource):
    @namespace.doc(
        responses={
            200: "Successful operation",
            500: "Internal error",
        }
    )

    @namespace.expect(login_model)
    def post(self):
        data = user_service.login(request.get_json()["username"], request.get_json()["password"])
        return RequestHandler.success_response(
            message=f"Logged in!",
            data={"access_token": data["access_token"], "refresh_token": data["refresh_token"], "expire_in": 60 * 15}
        )


@namespace.route("/api/v1/user/registration")
class SaveUser(flask_restplus.Resource):
    @namespace.doc(
        responses={
            200: "Successful operation",
            500: "Internal error",
        }
    )

    @namespace.produces("application/json")
    @namespace.expect(user_model)
    def post(self):
        try:
            data = user_service.save_user(user_service.to_user(request.get_json()))
        except Exception as err:
            logging.error(err)
            return RequestHandler.error_response(500, err)

        return RequestHandler.success_response(
            message=f"User successfully {data['user'].username} created",
            data={"access_token": data["access_token"], "refresh_token": data["refresh_token"], "expire_in": 60 * 15}
        )


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
        try:
            user_service.remove_user(username)
        except Exception as err:
            logging.error(err)
            return RequestHandler.error_response(500, err)

        return RequestHandler.success_response(message=f"User successfully deleted")

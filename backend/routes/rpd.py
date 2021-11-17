import logging

import flask_restplus
from flask import request

import db.models as m
from routes.handler import RequestHandler
from services.init import get_rpd_service

namespace = flask_restplus.Namespace("rpd", "RPD management: changing, deleting and loading information from the file.", path="/")
rpd_service = get_rpd_service()

@namespace.route("/api/v1/rpd")
class SaveRpd(flask_restplus.Resource):
    @namespace.doc(
        responses={
            200: "Successful operation",
            500: "Internal error",
        }
    )

    @namespace.produces("application/json")
    def post(self):
        try:
            model = rpd_service.save_rpd(request.get_json()["filename"])
        except Exception as err:
            logging.error(err)
            return RequestHandler.error_response(500, err)

        return RequestHandler.success_response(message=f"RPD successfully added! RPD id is {model.id}", data=model)


@namespace.route("/api/v1/rpd/<int:rpd_id>")
class GetRpd(flask_restplus.Resource):
    @namespace.doc(
        responses={
            200: "Successful operation",
            400: "Invalid ID supplied",
            404: "RPD not found",
            500: "Internal error",
        }
    )

    @namespace.doc(params={"rpd_id": "RPD id to get"})
    @namespace.produces("application/json")
    def get(self, rpd_id):
        try:
            model = rpd_service.get_rpd(rpd_id)
        except Exception as err:
            logging.error(err)
            return RequestHandler.error_response(500, err)

        return RequestHandler.success_response(data=model)

    @namespace.doc(params={"rpd_id": "RPD id to change"})
    @namespace.produces("application/json")
    def patch(self, rpd_id):
        try:
            rpd_service.update_rpd(rpd_id, request.get_json())
        except Exception as err:
            logging.error(err)
            return RequestHandler.error_response(500, err)

        return RequestHandler.success_response(
            message=f"Work program of discipline successfully changed")

    @namespace.doc(params={"rpd_id": "RPD id to remove"})
    @namespace.produces("application/json")
    def delete(self, rpd_id):
        try:
            rpd_service.remove_rpd(rpd_id)
        except Exception as err:
            logging.error(err)
            return RequestHandler.error_response(500, err)

        return RequestHandler.success_response(
            message=f"Work program of discipline with id = {rpd_id} successfully deleted")

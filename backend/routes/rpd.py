import logging

import db.models as m
import flask_restplus
from db.cache.cache import CacheLRU
from db.utils import Utils
from flask import request
from services.controller import Controller
from services.document_parser import DocumentParser
from services.handler import RequestHandler

namespace = flask_restplus.Namespace("rpd", "RPD management: changing, deleting and loading information from the file.", path="/")

cache = CacheLRU()
controller = Controller()

@namespace.route("/api/v1/rpd")
class LoadRpd(flask_restplus.Resource):
    @namespace.doc(
        responses={
            200: "Successful operation",
            500: "Internal error",
        }
    )

    @namespace.produces("application/json")
    def post(self):
        logging.info("/rpd router called")
        repo_psql = controller.discipline_work_program_repo_psql
        filename = request.get_json()["filename"]

        try:
            parser = DocumentParser(filename)
            model = parser.get_discipline_program()
            model.id = repo_psql.save(model)
            model = Utils.save_discipline_fields(model, controller.psql_repos)
        except Exception as err:
            logging.error(err)
            traceback.print_exc()
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
        logging.info(f"/dpw/{id} (GET) router called")
        repos = {
            "storage": controller.psql_repos,
            "cache": controller.tarantool_repos,
        }

        try:
            model = cache.get_by_primary(int(rpd_id), "discipline_work_program", repos)
            model = Utils.collect_discipline_fields(model, cache, repos)
        except Exception as err:
            logging.error(err)
            return RequestHandler.error_response(500, err)

        return RequestHandler.success_response(data=model)

    @namespace.doc(params={"rpd_id": "RPD id to change"})
    @namespace.produces("application/json")
    def patch(self, rpd_id):
        logging.info(f"/rpd (PUT) router called")
        repos = controller.psql_repos

        try:
            model_fields = request.get_json()
            for field in model_fields:
                obj = model_fields[field]
                obj.pop("id")
                repos[field].edit(id=rpd_id, fields=obj)
        except Exception as err:
            logging.error(err)
            return RequestHandler.error_response(500, err)

        return RequestHandler.success_response(
            message=f"Work program of discipline successfully changed")

    @namespace.doc(params={"rpd_id": "RPD id to remove"})
    @namespace.produces("application/json")
    def delete(self, rpd_id):
        logging.info(f"/rpd/{rpd_id} (DELETE) router called")
        repo_psql = controller.discipline_work_program_repo_psql
        repo_tarantool = controller.discipline_work_program_repo_tarantool
        repos = {
            "storage": controller.psql_repos,
            "cache": controller.tarantool_repos,
        }

        try:
            model = cache.get_by_primary(int(id), "discipline_work_program", repos)
            Utils.remove_discipline_fields(model, cache, repos)
            repo_psql.remove(model.id)
        except Exception as err:
            logging.error(err)
            return RequestHandler.error_response(500, err)

        return RequestHandler.success_response(
            message=f"Work program of discipline with id = {id} successfully deleted")

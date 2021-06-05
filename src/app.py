""" Flask Web-application for working with the work program of the discipline """

import logging
import json
import time

from flask import Flask, request
import psycopg2

import db.models as m
from db.cache.cache import CacheLRU
from db.utils import Utils

from services.controller import Controller
from services.handler import RequestHandler
from services.document_parser import DocumentParser

app = Flask(__name__)

# Waiting for database initialization
time.sleep(1)
cache = CacheLRU()
controller = Controller()

@app.route("/")
def get_index():
    return "Index Page"


@app.route("/dpw/<filename>", methods=["POST"])
def upload_from_file(filename=None):
    logging.info(f"/dpw/{filename} router called")
    repo_psql = controller.discipline_work_program_repo_psql

    try:
        parser = DocumentParser(filename)
        model = parser.get_discipline_program()
        model.id = repo_psql.save(model)
    except Exception as err:
        raise err
        logging.error(err)
        return RequestHandler.error_response(500, err)

    return RequestHandler.success_response(data=model)


@app.route("/dpw/<id>", methods=["GET"])
def get_dpw_by_id(id=None):
    logging.info(f"/dpw/{id} (GET) router called")
    repos = {
        "storage": controller.psql_repos,
        "cache": controller.tarantool_repos,
    }

    try:
        model = cache.get_by_primary(int(id), "discipline_work_program", repos)
        model = Utils.collect_discipline_fields(model, int(id), cache, repos)
    except Exception as err:
        raise err
        logging.error(err)
        return RequestHandler.error_response(500, err)

    return RequestHandler.success_response(data=model)


@app.route("/dpw/<id>", methods=["DELETE"])
def remove_dpw_by_id(id=None):
    logging.info(f"/dpw/{id} (DELETE) router called")
    repo_psql = controller.discipline_work_program_repo_psql
    repo_tarantool = controller.discipline_work_program_repo_tarantool

    try:
        model = repo_psql.remove(int(id))
        cache.remove(int(id), repo_tarantool)
    except Exception as err:
        logging.error(err)
        return RequestHandler.error_response(500, err)

    return RequestHandler.success_response(
        message=f"Work program of discipline with id = {id} successfully deleted")


@app.route("/dpw/<id>", methods=["PUT"])
def edit_dpw_by_id(id=None):
    logging.info(f"/dpw/{id} (PUT) router called")
    repo_psql = controller.discipline_work_program_repo_psql
    repo_tararntool = controller.discipline_work_program_repo_tarantool

    try:
        model = repo_psql.edit(id=int(id), fields=request.get_json())
        cache.update(int(id), repo_tarantool)
    except Exception as err:
        logging.error(err)
        return RequestHandler.error_response(500, err)

    return RequestHandler.success_response(
        message=f"Work program of discipline with id = {id} successfully changed")


@app.route("/cache/clear", methods=["PUT"])
def clear_cache():
    logging.info(f"Clear cache router called")
    cache_repos = controller.tarantool_repos

    try:
        cache.clear(cache_repos, cache_repos["discipline_work_program"].connection)
    except Exception as err:
        logging.error(err)
        return RequestHandler.error_response(500, err)

    return RequestHandler.success_response(message=f"Cache successfully cleared")


@app.errorhandler(404)
def page_not_found(error):
    return RequestHandler.error_response(404, "Invalid URL!")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

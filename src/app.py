""" Flask Web-application for working with the work program of the discipline """

import logging
import json
import time
from datetime import datetime

from flask import Flask, request
import psycopg2

import db.models as m
from db.cache.cache import CacheLRU
from db.utils import Utils

from services.controller import Controller
from services.handler import RequestHandler
from services.document_parser import DocumentParser

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Waiting for database initialization
time.sleep(1)
cache = CacheLRU()
controller = Controller()


@app.route("/rpd/save", methods=["POST"])
def upload_from_file():
    logging.info(f"/rpd/save router called")
    repo_psql = controller.discipline_work_program_repo_psql
    filename = request.get_json()["filename"]

    try:
        parser = DocumentParser(filename)
        model = parser.get_discipline_program()
        model.id = repo_psql.save(model)
        model = Utils.save_discipline_fields(model, controller.psql_repos)
    except Exception as err:
        logging.error(err)
        return RequestHandler.error_response(500, err)

    return RequestHandler.success_response(message=f"RPD successfully added! RPD id is {model.id}")


@app.route("/rpd/<id>", methods=["GET"])
def get_dpw_by_id(id=None):
    logging.info(f"/dpw/{id} (GET) router called")
    repos = {
        "storage": controller.psql_repos,
        "cache": controller.tarantool_repos,
    }

    try:
        full_delta = 0
        for i in range(1, 2):
            t1 = datetime.now()
            model = cache.get_by_primary(int(i), "discipline_work_program", repos)
            model = Utils.collect_discipline_fields(model, cache, repos)
            t2 = datetime.now()
            delta = t2 - t1
            full_delta += delta.microseconds

        logging.error(f"Delta (ms): {full_delta}")
    except Exception as err:
        raise
        logging.error(err)
        return RequestHandler.error_response(500, err)

    return RequestHandler.success_response(data=model)


@app.route("/rpd/<id>", methods=["DELETE"])
def remove_dpw_by_id(id=None):
    logging.info(f"/rpd/{id} (DELETE) router called")
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


@app.route("/rpd/<id>", methods=["PUT"])
def edit_dpw_by_id(id=None):
    logging.info(f"/rpd/{id} (PUT) router called")
    repo_psql = controller.discipline_work_program_repo_psql
    repo_tararntool = controller.discipline_work_program_repo_tarantool

    try:
        model = repo_psql.edit(id=int(id), fields=request.get_json())
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


@app.route("/cache/size", methods=["GET"])
def cache_size():
    logging.info(f"Get cache size router called")
    cache_repos = controller.tarantool_repos

    try:
        size = cache.get_cache_size(cache_repos["discipline_work_program"].connection)
    except Exception as err:
        logging.error(err)
        return RequestHandler.error_response(500, err)

    return RequestHandler.success_response(message=f"Cache size is {size}")


@app.route("/cache/<id>", methods=["DELETE"])
def remove_from_cache(id=None):
    logging.info(f"Remove from cache with id = {id} router called")
    space_name = request.get_json()["space_name"]

    try:
        cache.remove(int(id), space_name, controller.tarantool_repos[space_name])
    except Exception as err:
        logging.error(err)
        return RequestHandler.error_response(500, err)

    return RequestHandler.success_response(message=f"Cache successfully cleared")


@app.errorhandler(404)
def page_not_found(error):
    return RequestHandler.error_response(404, "Invalid URL!")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

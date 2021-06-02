""" Flask Web-application for working with the work program of the discipline """

import logging
import json
import time

from flask import Flask, request
import psycopg2

import db.repository as repo
import db.models as m
from services.controller import Controller
from services.handler import RequestHandler

app = Flask(__name__)

# Waiting for database initialization
time.sleep(1)
controller = Controller()


@app.route("/")
def get_index():
    return "Index Page"


@app.route("/all_dpw", methods=["GET"])
def get_all_dpw():
    logging.info("/all_dpw router called")
    repo = controller.discipline_work_program_repo

    try:
        models = repo.get_all()
    except Exception as err:
        logging.error(err)
        return RequestHandler.error_response(500, err)

    return RequestHandler.success_response(data=models)


@app.route("/dpw/<id>", methods=["GET"])
def get_dpw_by_id(id=None):
    logging.info(f"/dpw/{id} (GET) router called")
    repo = controller.discipline_work_program_repo

    try:
        model = repo.get_by_id(id)
    except Exception as err:
        logging.error(err)
        return RequestHandler.error_response(500, err)

    return RequestHandler.success_response(data=model)


@app.route("/dpw/<id>", methods=["DELETE"])
def remove_dpw_by_id(id=None):
    logging.info(f"/dpw/{id} (DELETE) router called")
    repo = controller.discipline_work_program_repo

    try:
        model = repo.remove(id)
    except Exception as err:
        logging.error(err)
        return RequestHandler.error_response(500, err)

    return RequestHandler.success_response(
        message=f"Work program of discipline with id = {id} successfully deleted")


@app.route("/dpw/<id>", methods=["PUT"])
def edit_dpw_by_id(id=None):
    logging.info(f"/dpw/{id} (PUT) router called")
    repo = controller.discipline_work_program_repo

    try:
        model = repo.edit(id=id, fields=request.get_json())
    except Exception as err:
        logging.error(err)
        return RequestHandler.error_response(500, err)

    return RequestHandler.success_response(
        message=f"Work program of discipline with id = {id} successfully changed")


@app.errorhandler(404)
def page_not_found(error):
    return RequestHandler.error_response(404, "Invalid URL!")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

import psycopg2
from flask import Flask, request, jsonify

import db.repository as repo
import db.models as m
from services.controller import Controller
from services.handler import RequestHandler

app = Flask(__name__)
controller = Controller()

@app.before_request
def before_request():
    pass


@app.after_request
def after_request(response):
    return response


@app.route("/test", methods=["POST"])
def post_add():
    model = m.DisciplineWorkProgram(4, "Name03", "Author03", "Competency03")

    try:
        repo = controller.discipline_work_program_repo
        repo.save(model)
        model = repo.get_by_id(4)
    except psycopg2.Error as err:
        return RequestHandler.error_response(500, err.pgerror)

    return RequestHandler.success_response(model.__dict__)


@app.errorhandler(404)
def page_not_found(error):
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

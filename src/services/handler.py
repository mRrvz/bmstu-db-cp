""" Requests handler """

from flask import jsonify

class RequestHandler():
    @staticmethod
    def success_response(data=None, message=None):
        if type(data) == list:
            data = list(map(lambda x: x.serialize(), data))
        elif data is not None:
            data = data.serialize()

        return jsonify(code=200, data=data, message=message), 200

    @staticmethod
    def error_response(code, message):
        return jsonify(code=code, message=f"{message}"), code

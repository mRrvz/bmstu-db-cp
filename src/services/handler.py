from flask import jsonify

class RequestHandler():
    @staticmethod
    def success_response(data):
        return jsonify(code=200, data=data), 200

    @staticmethod
    def error_response(code, message):
        return jsonify(code=code, message=message), code

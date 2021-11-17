import logging

import flask
import flask_restplus

from routes.handler import RequestHandler
from services.init import get_cache_service

namespace = flask_restplus.Namespace("cache", "Information about the cache and its management.", path="/")
cache_service = get_cache_service()

@namespace.route("/api/v1/cache/size")
class GetCacheSize(flask_restplus.Resource):
    @namespace.doc(
        responses={
            200: "Successful operation",
            500: "Internal error",
        }
    )

    @namespace.produces("application/json")
    def get(self):
        try:
            size = cache_service.get_size()
        except Exception as err:
            logging.error(err)
            return RequestHandler.error_response(500, err)

        return RequestHandler.success_response(message=f"Cache size is {size}", data=size)


@namespace.route("/api/v1/cache/<int:rpd_id>")
class ChangeCache(flask_restplus.Resource):
    @namespace.doc(
        responses={
            200: "Successful operation",
            400: "Invalid ID supplied",
            404: "Cache item not found",
            500: "Internal error",
        }
    )

    @namespace.doc(params={"rpd_id": "RPD id to patch in cache"})
    @namespace.produces("application/json")
    def patch(self, rpd_id):
        try:
            cache_service.edit_in_cache(request.get_json())
        except Exception as err:
            logging.error(err)
            return RequestHandler.error_response(500, err)

        return RequestHandler.success_response(
            message=f"Work program of discipline successfully changed")

    @namespace.doc(params={"rpd_id": "RPD id to delete from cache"})
    @namespace.produces("application/json")
    def delete(self, rpd_id):
        try:
            cache_service.remove_from_cache(rpd_id, space_name)
        except Exception as err:
            logging.error(err)
            return RequestHandler.error_response(500, err)

        return RequestHandler.success_response(message=f"Cache successfully cleared")


@namespace.route("/api/v1/cache/clear")
class ClearCache(flask_restplus.Resource):
    @namespace.doc(
        responses={
            200: "Successful operation",
            500: "Internal error",
        }
    )

    @namespace.produces("application/json")
    def put(self):
        try:
            cache_service.clear_cache()
        except Exception as err:
            logging.error(err)
            return RequestHandler.error_response(500, err)

        return RequestHandler.success_response(message=f"Cache successfully cleared")

import logging

import flask
import flask_restplus

from routes.rpd import cache, controller
from services.handler import RequestHandler

namespace = flask_restplus.Namespace("cache", "Information about the cache and its management.", path="/")

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
        logging.info(f"Get cache size router called")
        cache_repos = controller.tarantool_repos

        try:
            size = cache.get_cache_size(cache_repos["discipline_work_program"].connection)
        except Exception as err:
            logging.error(err)
            return RequestHandler.error_response(500, err)

        return RequestHandler.success_response(message=f"Cache size is {size}", data=size)


@namespace.route("/api/v1/cache/<int:rpd_id>")
class DeleteFromCache(flask_restplus.Resource):
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
        logging.info(f"/cache (PUT) router called")
        repos = controller.tarantool_repos

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

    @namespace.doc(params={"rpd_id": "RPD id to delete from cache"})
    @namespace.produces("application/json")
    def delete(self, rpd_id):
        logging.info(f"Remove from cache with id = {rpd_id} router called")
        space_name = request.get_json()["space_name"]

        try:
            cache.remove(int(id), space_name, controller.tarantool_repos[space_name])
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
        logging.info(f"Clear cache router called")
        cache_repos = controller.tarantool_repos

        try:
            cache.clear(cache_repos, cache_repos["discipline_work_program"].connection)
        except Exception as err:
            logging.error(err)
            return RequestHandler.error_response(500, err)

        return RequestHandler.success_response(message=f"Cache successfully cleared")

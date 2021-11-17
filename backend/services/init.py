from db.cache.cache import CacheLRU
from services.cache_service import CacheService
from services.controller import Controller
from services.rpd_service import RpdService
from services.user_service import UserService

cache = CacheLRU()
controller = Controller()

def get_cache_service():
    return CacheService(controller.tarantool_repos, cache)

def get_rpd_service():
    return RpdService(controller.psql_repos, controller.tarantool_repos, cache)

def get_user_service():
    return UserService(controller.psql_repos["user"])

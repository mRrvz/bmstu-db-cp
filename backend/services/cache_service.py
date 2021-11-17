class CacheService:
    def __init__(self, repos, cache):
        self.repos = repos
        self.cache = cache

    def get_size(self):
        return self.cache.get_cache_size(self.repos["discipline_work_program"].connection)

    def remove_from_cache(self, rpd_id, space_name):
        return self.cache.remove(rpd_id, space_name, repos[space_name])

    def edit_in_cache(self, model_fields):
        model_fields = request.get_json()
        for field in fields:
            obj = model_fields[field]
            obj.pop("id")
            self.repos[field].edit(id=rpd_id, fields=obj)

    def clear_cache(self):
        self.cache.clear(self.repos, self.repos["discipline_work_program"].connection)

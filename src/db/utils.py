""" Help utilities for work with database """

import psycopg2
import tarantool

class PostgresConnection():
    def __init__(self, dbname, user, password, host):
        self.dbname = dbname
        self.user = user
        self.host = host
        self.password = password
        self.connection = None

    def get(self):
        if self.connection is not None:
            return self.connection

        self.connection = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            host=self.host,
            password=self.password,
            connect_timeout=5
        )

        return self.connection

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None


class TarantoolConnection():
    def __init__(self, user, password, host, port):
        self.user = user
        self.host = host
        self.password = password
        self.port = port
        self.connection = None

    def get(self):
        if self.connection is not None:
            return self.connection

        self.connection = tarantool.connect(
            self.host,
            self.port,
            user=self.user,
            password=self.password
        )

        return self.connection

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None


class Utils():
    @staticmethod
    def get_psql_update_args(args):
        if len(args) == 0:
            raise ValueError("You have to pass more than one argument, when trying to update object")

        source_str = ""
        values = list()

        for key in args:
            source_str += f"{key} = %s, "
            values.append(args[key])

        return source_str[:-2], tuple(values)

    @staticmethod
    def get_insert_fields(table_fields):
        raw_string = f"("
        for field in table_fields:
            if field != "id":
                raw_string += f"{field}, "

        return f"{raw_string[:-2]})"

    @staticmethod
    def collect_discipline_fields(model, cache, repos):
        for space_name in repos["cache"]:
            if space_name in "discipline_work_program":
                continue
            elif space_name == "educational_program": # TODO
                value, _ = repos["storage"][space_name].get_by_filter("discipline_id = %s", (model.id,))
            else:
                value = cache.get_by_filter(space_name, model.id, "discipline_id", repos)

            setattr(model, space_name, value)

        return model

    @staticmethod
    def save_discipline_fields(model, repos):
        for key in repos:
            if key != "discipline_work_program":
                fields = getattr(model, key)
                discipline_id = model.id

                if fields is not None:
                    for subfield in fields:
                        subfield.discipline_id = discipline_id
                        subfield.id = repos[key].save(subfield)

                    setattr(model, key, fields)

        return model

    @staticmethod
    def remove_discipline_fields(model, cache, repos):
        model = Utils.collect_discipline_fields(model, cache, repos)
        for key in repos["storage"]:
            if key == "discipline_work_program":
                continue

            fields = getattr(model, key)
            if fields is not None:
                for subfield in fields:
                    if key == "educational_program":
                        repos["storage"][key].remove(subfield.id, discipline_id=model.id)
                    else:
                        repos["storage"][key].remove(subfield.id)

    @staticmethod
    def get_noncached_filter_string(primary_keys_cnt, secondary_field):
        primary_values = ("%s, " * primary_keys_cnt)[:-2]
        return f"{secondary_field} = %s AND id NOT IN ({primary_values})"

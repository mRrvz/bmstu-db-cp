""" Help utilities for work with database """

import time
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
    def get_tarantool_update_args(fields, space_format):
        value = list()
        for key in fields:
            index = space_format[key]
            values.append(('=', index, args[key]))

        return value

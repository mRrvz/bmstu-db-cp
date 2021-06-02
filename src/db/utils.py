""" Help utilities for work with database """

import time
import psycopg2

class Connection():
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


class Formatter():
    @staticmethod
    def get_update_args(args):
        if len(args) == 0:
            raise ValueError("You have to pass more than one argument, when trying to update object")

        source_str = ""
        values = list()

        for key in args:
            source_str += f"{key} = %s, "
            values.append(args[key])

        return source_str[:-2], tuple(values)

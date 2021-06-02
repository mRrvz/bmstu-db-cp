import time
import psycopg2

class Connection():
    def __init__(self, dbname, user, host, password):
        self.dbname = dbname
        self.user = user
        self.host = host
        self.password = password
        self.connection = None

    def get(self):
        if self.connection is not None:
            return self.connection

        while not self.connection:
            try:
                self.connection = psycopg2.connect(
                    dbname=self.dbname,
                    user=self.user,
                    host=self.host,
                    password=self.password
                )
            except psycopg2.OperationalError:
                time.sleep(1)

        return self.connection

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

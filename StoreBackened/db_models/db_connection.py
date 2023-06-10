import psycopg2
from typing import Dict, List, Any


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class DBConnection:
    """ This class will initialize the connection to the db once """

    def __init__(self, database_name: str = "store", host: str = "127.0.0.1", user: str = "postgres",
                 password: str = "123456", port: str = "5432"):
        self.conn = psycopg2.connect(database=database_name, host=host, user=user, password=password, port=port)
        logger.info(f"Successfully connected to the db at: {host}")
        self.cursor = self.conn.cursor()

    @property
    def connection(self):
        return self.conn

    def execute_query(self, query_and_vars: Dict[str, Any], commit: bool = False) -> List[Any]:
        """ Executes the query passed """
        self.cursor.execute(**query_and_vars)
        if commit:
            self.conn.commit()
        return self.cursor.fetchall()

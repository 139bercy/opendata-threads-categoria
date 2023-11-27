import os

import dotenv
import psycopg2
import psycopg2.extras

dotenv.load_dotenv()


class PostgresClient:
    def __init__(self, dbname, host, user, password, port=5432):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def execute(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor
        except Exception as e:
            print(e)

    def add_one(self, query):
        self.execute(query=query)
        self.conn.commit()

    def update(self, query):
        self.execute(query=query)
        self.conn.commit()

    def fetch_one(self, query):
        result = self.execute(query)
        return dict(result.fetchone())

    def fetch_all(self, table_name):
        query = f"SELECT * FROM {table_name};"
        result = self.execute(query)
        return result.fetchall()

    def close_connection(self):
        self.cursor.close()
        self.conn.close()


DB_NAME = os.environ["DB_NAME"]
DB_HOST = os.environ["DB_HOST"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]

postgres_client = PostgresClient(DB_NAME, DB_HOST, DB_USER, DB_PASSWORD)

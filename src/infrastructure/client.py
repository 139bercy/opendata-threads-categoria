import dotenv
import psycopg2

dotenv.load_dotenv()


class PostgresClient:
    def __init__(self, dbname, host, user, password, port=5432):
        self.conn = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        )
        self.cursor = self.conn.cursor()

    def execute(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor
        except Exception as e:
            print(e)

    def fetch_all(self, table_name):
        query = f"SELECT * FROM {table_name};"
        result = self.execute(query)
        return result.fetchall()

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

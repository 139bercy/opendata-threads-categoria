import os

from src.infrastructure.client import PostgresClient
import dotenv

dotenv.load_dotenv()


dbname = os.environ["DB_NAME"]
user = os.environ["DB_USER"]
password = os.environ["DB_PASSWORD"]
host = os.environ["DB_HOST"]

postgres_client = PostgresClient(dbname, host, user, password)

query = """
insert into "account" (uuid, first_name, last_name, email, password)
values ('cf40ebed-85d6-4a85-930c-b6a9ea18a899',
        'john',
        'doe',
        'john.doe@example.com',
        '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'
        );
"""

postgres_client.execute(query=query)
print(postgres_client.fetch_all("account"))
#
# # Example: Fetch rows by a specific column value
# specific_rows = postgres_client.fetch_rows_by_column('your_table', 'column_name', 'some_value')
# print("Rows with specific value:")
# for row in specific_rows:
#     print(row)
#
# # Close the connection when done
# postgres_client.close_connection()

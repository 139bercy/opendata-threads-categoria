import os

from src.common.infrastructure import PostgresClient

import dotenv

dotenv.load_dotenv()

postgres_client = PostgresClient(
    dbname=os.environ["DB_NAME"],
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    port=os.environ["DB_PORT"],
    password=os.environ["DB_PASSWORD"],
)

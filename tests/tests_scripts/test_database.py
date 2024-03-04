"""import pytest
from src.scripts.database_management.database_setup import create_database_and_tables
from src.scripts.database_management.data_to_database import import_data_from_csv
import mysql.connector

@pytest.fixture
def database_connection():
    
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        database="database_discussions",
    )
    yield connection
    connection.close()

def test_create_database_and_tables(database_connection):

    create_database_and_tables()

    # Vérification de l'existance des tables après l'exécution
    cursor = database_connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    assert ("user",) in tables
    assert ("organization",) in tables
    assert ("dataset",) in tables
    assert ("discussion",) in tables
    assert ("message",) in tables
    assert ("prediction",) in tables

def test_import_data_from_csv(database_connection):
    
    import_data_from_csv()

    cursor = database_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM user")
    assert cursor.fetchone()[0] > 0

    cursor.execute("SELECT COUNT(*) FROM organization")
    assert cursor.fetchone()[0] > 0

    cursor.execute("SELECT COUNT(*) FROM dataset")
    assert cursor.fetchone()[0] > 0

    cursor.execute("SELECT COUNT(*) FROM discussion")
    assert cursor.fetchone()[0] > 0

    cursor.execute("SELECT COUNT(*) FROM message")
    assert cursor.fetchone()[0] > 0

    cursor.execute("SELECT COUNT(*) FROM prediction")
    assert cursor.fetchone()[0] > 0
"""
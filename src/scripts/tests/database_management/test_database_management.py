import pytest

import sys
sys.path.append('../../')
from database_management.data_to_database import format_datetime_mysql

# Test de la fonction format_datetime_mysql
def test_format_datetime_mysql():
    input_date = "2015-05-12T15:51:49.796000+00:00"
    expected_output = "2015-05-12 15:51:49"

    # Appel de la fonction à tester
    formatted_date = format_datetime_mysql(input_date)

    # Vérification si la sortie de la fonction est égale à la sortie attendue
    assert formatted_date == expected_output

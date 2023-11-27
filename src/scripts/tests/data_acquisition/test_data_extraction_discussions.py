from datetime import datetime, timezone

import pandas as pd
import pytest
from data_acquisition import (
    fetch_discussion_data,
    parse_datetime,
    load_existing_data,
    save_extracted_data,
)

# Indiquez le chemin du fichier CSV de données existant pour les tests.
EXISTING_DATA_PATH = "../../../../data/raw/data_acquisition/extraction_discussions/discussions.csv"


# Utilisez le décorateur @pytest.mark pour marquer vos tests comme unitaires.
@pytest.mark.unit
def test_fetch_discussion_data():
    # Cas de test où la requête réussit
    discussions_url = "https://www.data.gouv.fr/api/1/discussions/"
    last_update_date = datetime(2022, 1, 1, tzinfo=timezone.utc)
    result = fetch_discussion_data(discussions_url, last_update_date)
    assert isinstance(result, list)  # Vérifiez si le résultat est une liste

    # Cas de test où la requête échoue (simulez une exception)
    discussions_url = "https://www.data.gouv.fr/api/requete_echouee"
    last_update_date = datetime(2022, 1, 1, tzinfo=timezone.utc)
    with pytest.raises(Exception):
        fetch_discussion_data(discussions_url, last_update_date)


@pytest.mark.unit
def test_parse_datetime():
    # Cas de test avec une chaîne de date au format ISO
    datetime_str = "2022-01-01T12:00:00Z"
    result = parse_datetime(datetime_str)
    expected_result = datetime(2022, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    assert result == expected_result

    # Cas de test avec une autre chaîne de date au format personnalisé
    datetime_str = "01/01/2022 12:00:00"
    result = parse_datetime(datetime_str)
    expected_result = datetime(2022, 1, 1, 12, 0, 0)
    assert result == expected_result


@pytest.mark.unit
def test_load_existing_data(tmp_path):
    # Créez un fichier CSV de test avec des données fictives
    test_data = "created,closed\n2022-01-01T12:00:00Z,2022-01-02T12:00:00Z\n"
    test_csv_file = tmp_path / "test_data.csv"
    test_csv_file.write_text(test_data)

    # Appelez la fonction load_existing_data pour charger les données
    result = load_existing_data(test_csv_file)

    # Vérifiez si le résultat est conforme à vos attentes en utilisant les assertions
    assert isinstance(result, pd.DataFrame)  # Vérifiez si le résultat est un DataFrame
    assert len(result) == 1  # Vérifiez le nombre de lignes dans le DataFrame


@pytest.mark.unit
def test_save_extracted_data(tmp_path):
    # Créez un DataFrame de test avec des données fictives
    test_data = pd.DataFrame({"created": ["2022-01-01T12:00:00Z"], "closed": ["2022-01-02T12:00:00Z"]})

    # Appelez la fonction save_extracted_data pour enregistrer les données dans un fichier CSV
    test_csv_file = tmp_path / "test_data.csv"
    save_extracted_data(test_data, test_csv_file)

    # Vérifiez si le fichier CSV a été créé avec succès
    assert test_csv_file.exists()


# Vous pouvez ajouter d'autres tests unitaires au besoin.

if __name__ == "__main__":
    pytest.main()

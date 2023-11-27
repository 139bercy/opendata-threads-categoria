import unittest

from data_extraction import fetch_data_from_url, load_existing_data, process_data, save_data_to_csv


class TestDataExtraction(unittest.TestCase):
    def test_fetch_data_from_url(self):
        """
        Teste la fonction fetch_data_from_url.
        Vérifie que la fonction renvoie une liste lorsque des données sont extraites depuis une URL valide.
        """
        url = "https://www.data.gouv.fr/api/1/datasets/"
        data = fetch_data_from_url(url)
        self.assertTrue(isinstance(data, list))

    def test_load_existing_data(self):
        """
        Teste la fonction load_existing_data.
        Vérifie que la fonction renvoie un DataFrame pandas lorsque des données sont chargées depuis un fichier CSV existant.
        """
        file_path = "../../../data/raw/data_acquisition/extraction_datasets/datasets.csv"
        data = load_existing_data(file_path)
        self.assertTrue(isinstance(data, pd.DataFrame))

    def test_process_data(self):
        """
        Teste la fonction process_data.
        Vérifie que la fonction renvoie un DataFrame pandas contenant des données traitées lorsque des données existantes et des données extraites sont fournies.
        """
        existing_data = pd.DataFrame()
        extracted_data = [{"id": 1, "last_update": "2023-08-09T23:02:44+00:00"}]
        processed_data = process_data(existing_data, extracted_data)
        self.assertTrue(isinstance(processed_data, pd.DataFrame))

    def test_save_data_to_csv(self):
        """
        Teste la fonction save_data_to_csv.
        Vérifie que la fonction enregistre correctement les données dans un fichier CSV et que le fichier existe après l'enregistrement.
        """
        data = pd.DataFrame({"id": [1, 2], "name": ["A", "B"]})
        file_path = "test.csv"
        save_data_to_csv(data, file_path)
        self.assertTrue(os.path.exists(file_path))
        os.remove(file_path)  # Supprime le fichier après le test


if __name__ == "__main__":
    unittest.main()

import os
import sys

import pandas as pd

# Ajoutez le chemin du répertoire contenant preprocess.py au chemin de recherche
preprocess_module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../inference/preprocess.py"))
sys.path.append(preprocess_module_path)

print("Le path est :", preprocess_module_path)

from preprocess import preprocess_data, preprocess_data2


# Test preprocess_data avec une seule entrée
def test_preprocess_data():
    input_data = {
        "title_discussion": ["Titre 1", "2eme TITRE", "Troisième titre"],
        "message": ["Ceci est un message 123 !", "Ceci est le 2eme message ?", "TROISIEME MESSAGE !"],
    }

    df = pd.DataFrame(input_data)

    # Appliquer le prétraitement sur le DataFrame
    result = preprocess_data(df)

    # Vérifier les sorties pour chaque ligne du DataFrame
    expected_output1 = [
        "titre ceci est un message",
        "eme titre ceci est le eme message",
        "troisième titre troisieme message",
    ]

    """#assert result == expected_output
    for i, row in result.iterrows():
        assert row["processed_text"] == expected_output[i]"""

    assert result == expected_output1


# Test preprocess_data2 avec une seule entrée
def test_preprocess_data2():
    input_data = {
        "title_discussion": ["Exemple de Titre", "Autre Titre", "Encore un Titre"],
        "message": ["Ceci est un message 123 !", "Voici un autre message.", "Un autre message ici."],
        "predictions_motifs_label": ["Motifs", "Label", "Encore un label"],
    }

    df = pd.DataFrame(input_data)

    # Appliquer le prétraitement sur le DataFrame
    result2 = preprocess_data2(df)

    # Vérifier les sorties pour chaque ligne du DataFrame
    expected_output2 = [
        "motifs exemple de titre ceci est un message",
        "label autre titre voici un autre message.",
        "encore un label encore un titre un autre message ici.",
    ]

    assert result2 == expected_output2

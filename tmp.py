# import json

# import requests


# def get_datasets_from_data_gouv_api():
#     base_url = "https://www.data.gouv.fr/api/1/organizations"
#     organization = "/ministere-de-leconomie-des-finances-et-de-la-souverainete-industrielle-et-numerique"

#     url = f"{base_url}{organization}/datasets"
#     response = requests.get(url=url)
#     print(response.status_code)

#     with open("tmp.json", "w") as file:
#         data = json.loads(response.text)
#         json.dump(data, file, indent=2, ensure_ascii=False)
#     return data


# """
#            print("title_dataset:", dataset["title"])
#             print("description_dataset:", dataset["description"])
#             print("organization:", dataset["organization"]["name"])
#             print("url_dataset:", dataset["page"])
#             print("nb_discussions:", dataset["metrics"]["discussions"])
#             print("nb_followers:", dataset["metrics"]["followers"])
#             print("nb_reuses:", dataset["metrics"]["reuses"])
#             print("nb_views:", dataset["metrics"]["views"])
#             print("remote_id_dataEco:", dataset["harvest"]["remote_id"] if dataset['harvest'] and 'remote_id' in dataset['harvest'] else None)
#             print("slug_dataGouv:", dataset["slug"]) #slug sur data.gouv mais sur data.eco, l'équivalent est 'remote_id'
#             print("created_dataset:", dataset["created_at"])
#             #"last_update_dataset": dataset_updated_date.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
#             print('\n')"""


# with open("tests/fixtures/dg-datasets.json", "r") as f:
#     data = json.load(f)
#     archived = [ds for ds in data if ds["archived"] is not None]
#     private = [ds for ds in data if ds["private"] is True]
#     print(len(archived))
#     print(len(private))
#     org = [ds["organization"]["acronym"] for ds in data if ds["organization"]["acronym"] != "MEFSIN"]
#     print(org)

import os
import src.config

os.environ["test_append_a_dataset_to_postgres_database"]

for k, v in os.environ.items():
    print(k, v)

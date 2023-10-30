import requests
import json
import csv

APIKEY=""
headers = {"content-type": "application/json", "Authorization": f"Apikey {APIKEY}"}

output_rows = []
offset = 0
limit = 100

while 1==1:
  print(" ")
  print(" ")
  print("*******")
  print(f"getting page offset={offset}&limit={limit}...")
  print("*******")
  print(" ")
  print(" ")
  response = requests.get(f"https://data.economie.gouv.fr/api/automation/v1.0/datasets?sort=-modified&limit={limit}&offset={offset}", headers=headers)
  if response.status_code != 200:
    print(f"Impossible de récupérer la liste des datasets : {response.text}")
    break
  page = json.loads(response.text)['results']
  if not page:
    break
  offset += limit
  for dataset in page:
    print(" ")
    print(" ")
    print(f"processing {dataset['dataset_id']}, {dataset['uid']}")
    output_rows.append([
      dataset['metadata']['default']['title']['value'] if 'title' in dataset['metadata']['default'] else None,
      dataset['dataset_id'],
      dataset['is_restricted'],
      dataset['is_published'],
      dataset['metadata']['admin']['groupe-metier']['value'][0] if 'admin' in dataset['metadata'] and 'groupe-metier' in dataset['metadata']['admin'] else None,
      f"https://data.economie.gouv.fr/backoffice/catalog/datasets/{dataset['dataset_id']}/#information"])

with open('datasets_groupes_metiers_20231030.csv', 'w') as csvfile:
  writer = csv.writer(csvfile, delimiter=';')
  writer.writerow(['title', 'dataset_id', 'is_restricted', 'is_published', 'groupe-metier', 'url'])
  writer.writerows(output_rows)

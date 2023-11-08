import requests
import json
import csv

# Récupérer le host, le nom d'utilisateur et le mot de passe à partir des variables d'environnement situées dans le fichier de conf.
def load_db_config():
    with open('../../../config.json') as config_file:
        return json.load(config_file)
      
config = load_db_config()
api_key = config['API_KEY']
    
headers = {"content-type": "application/json", "Authorization": f"Apikey {api_key}"}

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

with open('../../../data/raw/data_acquisition/extraction_groupes_metiers/datasets_groupes_metiers_20231030.csv', 'w') as csvfile:
  writer = csv.writer(csvfile, delimiter=';')
  writer.writerow(['title', 'dataset_id', 'is_restricted', 'is_published', 'groupe-metier', 'url'])
  writer.writerows(output_rows)

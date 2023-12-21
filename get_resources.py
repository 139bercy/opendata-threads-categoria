import json
import requests

from src.core.infrastructure import PostgresThreadRepository
from src.core.usecases import create_message

repository = PostgresThreadRepository()

resources = ["datasets", "discussions", "catalog.json"]

for resource in resources:
    url = (
        f"https://www.data.gouv.fr/api/1/organizations/ministere-de-leconomie-des-finances-et-de-la-souverainete"
        f"-industrielle-et-numerique/{resource}"
    )
    response = requests.get(url)
    data = json.dumps(response.json(), indent=2, ensure_ascii=False)
    with open(f"data/{resource}.json", "w") as file:
        json.dump(response.json(), file, indent=2, ensure_ascii=False)

with open("data/messages.json", "r") as file:
    data = json.load(file)
    for item in data:
        for message in item["discussion"]:
            create_message(
                repository=repository,
                thread_id=item["id"],
                author=message["posted_by"]["slug"],
                content=message["content"],
                posted_on=message["posted_on"],
            )

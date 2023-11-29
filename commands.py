import json

import click
import requests

from thread.infrastructure import PostgresThreadRepository
from thread.usecases import create_message


@click.group()
def cli():
    """CLI entrypoint"""


@cli.group("data-gouv")
def data_gouv():
    """Handles Data Gouv usecases"""


@data_gouv.command("messages")
@click.option("-f", "--file", is_flag=True)
@click.option("-d", "--dump", is_flag=True)
def data_gouv_messages(file, dump):
    """Data Gouv threads and messages"""
    repository = PostgresThreadRepository()
    if not file:
        url = (
            "https://www.data.gouv.fr/api/1/organizations/ministere-de-leconomie-des-finances-et-de-la-"
            "souverainete-industrielle-et-numerique/discussions"
        )
        response = requests.get(url)
        data = response.json()
        if dump:
            data = json.dumps(response.json(), indent=2, ensure_ascii=False)
            with open("data/discussions.json", "w") as file:
                json.dump(response.json(), file, indent=2, ensure_ascii=False)
    else:
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


@cli.group("data-eco")
def data_eco():
    """Handles Data Economie usecases"""
    click.echo("Handle Data Economie usecases")


if __name__ == "__main__":
    cli()

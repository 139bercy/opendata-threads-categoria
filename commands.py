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
        source = response.json()
        if dump:
            source = json.dumps(response.json(), indent=2, ensure_ascii=False)
            with open("data/discussions.json", "w") as file:
                json.dump(response.json(), file, indent=2, ensure_ascii=False)
    else:
        with open("data/discussions.json", "r") as file:
            source = json.load(file)
    for discussion in source:
        for message in discussion["discussion"]:
            create_message(
                repository=repository,
                thread_id=discussion["id"],
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

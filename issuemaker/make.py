#!/usr/bin/env python3
"""Make issues on github.com."""
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from pprint import pprint

import click
import requests

# The repository to add this issue to
REPO_OWNER = "home-assistant"
REPO_NAME = "core"

SETTINGS = dict(help_option_names=["-h", "--help"])


@dataclass
class Auth:
    """Represent the github authentication details."""

    repo_name: str
    repo_owner: str
    token: str
    username: str


def make_github_issue(
    auth, title, body=None, assignee=None, milestone=None, labels=None
):
    """Create an issue on github.com using the given parameters."""
    # Our url to create issues via POST
    url = f"https://api.github.com/repos/{auth.repo_owner}/{auth.repo_name}/issues"

    # Create our issue
    issue = {
        "title": title,
        "body": body,
        "assignee": assignee,
        "milestone": milestone,
        "labels": labels,
    }

    # Add the issue to our repository
    response = requests.post(
        url, json=issue, headers={"Authorization": f"token {auth.token}"}
    )

    print(response.status_code)
    pprint(response.json())

    if response.status_code == 201:
        print(f'Successfully created Issue "{title}"')
    else:
        print(f'Could not create Issue "{title}"')
        print("Response:", response.content)


def make_github_issue_no_notify(auth, title, body, labels):
    """Create issues while not firing webhooks or creating notifications."""
    # Create an issue on github.com using the given parameters
    # Url to create issues via POST
    url = (
        f"https://api.github.com/repos/{auth.repo_owner}/{auth.repo_name}/import/issues"
    )

    # Headers
    headers = {
        "Authorization": f"token {auth.token}",
        "Accept": "application/vnd.github.golden-comet-preview+json",
    }

    # Create our issue
    data = {
        "issue": {
            "title": title,
            "body": body,
            # "created_at": created_at,
            # "closed_at": closed_at,
            # "updated_at": updated_at,
            # "assignee": assignee,
            # "milestone": None,
            # "closed": False,
            "labels": labels,
        }
    }

    # Add the issue to our repository
    response = requests.post(url, json=data, headers=headers)

    print(response.status_code)
    pprint(response.json())

    if response.status_code == 202:
        print(f'Successfully created Issue "{title}"')
    else:
        print(f'Could not create Issue "{title}"')
        print("Response:", response.content)


@click.group(
    options_metavar="", subcommand_metavar="<command>", context_settings=SETTINGS
)
def cli():
    """Batch create github.com issues."""


@click.command(name="issue", options_metavar="<options>")
@click.option(
    "-s", "--silent", is_flag=True, help="Make an issue without notifications."
)
@click.option(
    "-t",
    "--token",
    prompt=True,
    hide_input=True,
    default="",
    help="Set the auth token.",
)
@click.option(
    "-R",
    "--repo",
    default=REPO_NAME,
    show_default=True,
    help="Set the target repo.",
)
@click.option(
    "-u",
    "--username",
    required=True,
    help="Set the username.",
)
@click.option(
    "-O",
    "--owner",
    default=REPO_OWNER,
    show_default=True,
    help="Set the repository owner.",
)
@click.option(
    "-T",
    "--title",
    required=True,
    help="Set the issue title.",
)
@click.option(
    "-b",
    "--body",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="Set path to a text file with issue body.",
)
@click.option(
    "-a",
    "--assignee",
    help="Set the issue assignee.",
)
@click.option(
    "-m",
    "--milestone",
    help="Set the issue milestone.",
)
@click.option("-l", "--labels", multiple=True, help="Set the issue labels.")
def create_issue(silent, owner, repo, token, username, title, body, labels, **kwargs):
    """Create issue on github.com."""
    if not token:
        try:
            token = Path(".token").read_text().strip()
        except FileNotFoundError:
            print(
                "Missing '.token' file. "
                "Token must be provided by promt or in a '.token' file"
            )
            return

    body = Path(body).read_text()

    # Authentication for user filing issue (must have read/write access to
    # repository to add issue to)
    auth = Auth(repo_name=repo, repo_owner=owner, username=username, token=token)

    issue_func = partial(make_github_issue, auth, **kwargs)

    if silent:
        # the import API doesn't accept optional values
        issue_func = partial(make_github_issue_no_notify, auth)

    domain_names = Path("domains.txt").read_text().strip().splitlines()
    domain_title = None
    domain_body = None
    domain_labels = None
    for domain in domain_names:
        domain_title = title.replace("{{ DOMAIN }}", domain)
        domain_body = body.replace("{{ DOMAIN }}", domain)
        if labels:
            domain_labels = labels + (f"integration: {domain}",)

        issue_func(title=domain_title, body=domain_body, labels=domain_labels)


cli.add_command(create_issue)


if __name__ == "__main__":
    cli()

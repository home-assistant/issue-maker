"""Make issues on github.com."""
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from pprint import pprint

import click
import requests

# Authentication for user filing issue (must have read/write access to
# repository to add issue to)
USERNAME = "balloob"

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


def main():
    """Old main function."""
    context = {}
    context["token"] = Path(".token").read_text().strip()
    template = Path("./issues/test_uncaught.markdown").read_text()

    for domain in [
        # "abode",
        # "cast",
        # "config",
        "deconz",
        "default_config",
        "demo",
        "discovery",
        "dsmr",
        "dynalite",
        "dyson",
        "gdacs",
        "geonetnz_quakes",
        "homematicip_cloud",
        "hue",
        "ios",
        "local_file",
        "meteo_france",
        "mikrotik",
        "mqtt",
        "plex",
        "qwikswitch",
        "rflink",
        "samsungtv",
        "tplink",
        "tradfri",
        "unifi_direct",
        "upnp",
        "vera",
        "wunderground",
        "yr",
        "zha",
        "zwave",
    ]:
        title = f"Fix {domain} tests that have uncaught exceptions"
        body = template.replace("{{ DOMAIN }}", domain)
        labels = [f"integration: {domain}", "to do"]
        # print(title)
        # print(body)
        # print(labels)
        make_github_issue(title=title, body=body, labels=labels)


def common_issue_options(func):
    """Supply common issue options."""
    func = click.option(
        "-t",
        "--token",
        prompt=True,
        hide_input=True,
        help="Set the github auth token.",
    )(func)
    func = click.option(
        "-R",
        "--repo",
        help="Set the github target repo.",
    )(func)
    func = click.option(
        "-u",
        "--username",
        help="Set the github username.",
    )(func)
    func = click.option(
        "-O",
        "--owner",
        help="Set the github repository owner.",
    )(func)
    func = click.option(
        "-T",
        "--title",
        help="Set the issue title.",
    )(func)
    func = click.option(
        "-b",
        "--body",
        type=click.Path(exists=True, dir_okay=False),
        help="Set file path to a markdown file with issue body.",
    )(func)
    func = click.option(
        "-a",
        "--assignee",
        show_default=True,
        help="Set the issue assignee.",
    )(func)
    func = click.option(
        "-m",
        "--milestone",
        help="Set the issue milestone.",
    )(func)
    func = click.option(
        "-d",
        "--domains",
        is_flag=True,
        help="Create one issue per domain.",
    )(func)
    func = click.option("-l", "--labels", multiple=True, help="Set the issue labels.")(
        func
    )
    return func


@click.group(
    options_metavar="", subcommand_metavar="<command>", context_settings=SETTINGS
)
def cli():
    """Batch create github.com issues."""


@click.command(options_metavar="<options>")
@click.option(
    "-s", "--silent", is_flag=True, help="Make an issue without notifications."
)
@common_issue_options
def issue(silent, owner, repo, token, username, body, domains, **kwargs):
    """Create issue on github.com."""
    repo_name = repo or REPO_NAME
    repo_owner = owner or REPO_OWNER
    username = username or USERNAME
    token = token or Path(".token").read_text().strip()
    if body:
        body = Path(body).read_text()
    auth = Auth(
        repo_name=repo_name, repo_owner=repo_owner, username=username, token=token
    )

    issue_func = partial(make_github_issue, auth, body=body, **kwargs)

    if silent:
        issue_func = partial(make_github_issue_no_notify, auth, body=body, **kwargs)

    if domains:
        pass

    issue_func()


cli.add_command(issue)


if __name__ == "__main__":
    cli()

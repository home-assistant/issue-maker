"""Make issues on github.com."""
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


def make_github_issue(
    token, title, body=None, assignee=None, milestone=None, labels=None
):
    """Create an issue on github.com using the given parameters."""
    # Our url to create issues via POST
    url = "https://api.github.com/repos/%s/%s/issues" % (REPO_OWNER, REPO_NAME)

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
        url, json=issue, headers={"Authorization": f"token {token}"}
    )

    print(response.status_code)
    pprint(response.json())

    if response.status_code == 201:
        print('Successfully created Issue "%s"' % title)
    else:
        print('Could not create Issue "%s"' % title)
        print("Response:", response.content)


def make_github_issue_no_notify(token, title, body, labels):
    """Create issues while not firing webhooks or creating notifications."""
    # Create an issue on github.com using the given parameters
    # Url to create issues via POST
    url = "https://api.github.com/repos/%s/%s/import/issues" % (REPO_OWNER, REPO_NAME)

    # Headers
    headers = {
        "Authorization": f"token {token}",
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
        print('Successfully created Issue "%s"' % title)
    else:
        print('Could not create Issue "%s"' % title)
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
        help="Set the github auth token.",
    )(func)
    func = click.option(
        "-T",
        "--title",
        help="Set the issue title.",
    )(func)
    func = click.option(
        "-b",
        "--body",
        help="Set the issue body.",
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
    func = click.option("-l", "--label", multiple=True, help="Set the issue label.")(
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
def issue(silent, **kwargs):
    """Create issue on github.com."""
    if silent:
        make_github_issue_no_notify(**kwargs)
    else:
        make_github_issue(**kwargs)


cli.add_command(issue)


if __name__ == "__main__":
    cli()

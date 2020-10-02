#!/usr/bin/env python3
"""Make issues on github.com."""
from functools import partial
from pathlib import Path
from pprint import pprint

import requests

from .auth import Auth
from .exceptions import MissingTokenError


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


def create_issue(silent, owner, repo, token, username, title, body, labels, **kwargs):
    """Create issue on github.com."""
    try:
        auth = Auth.get_auth(
            repo_name=repo, repo_owner=owner, token=token, username=username
        )
    except MissingTokenError:
        return

    body = Path(body).read_text()
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

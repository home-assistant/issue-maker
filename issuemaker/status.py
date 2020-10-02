"""Check status of imported issues."""
from pprint import pprint

import requests

from .auth import Auth
from .exceptions import MissingTokenError


def print_status(auth, import_id):
    """Print status."""
    # Create an issue on github.com using the given parameters
    # Url to create issues via POST
    url = (
        "https://api.github.com/repos/"
        f"{auth.repo_owner}/{auth.repo_name}/import/issues/{import_id}"
    )

    # Headers
    headers = {
        "Authorization": f"token {auth.token}",
        "Accept": "application/vnd.github.golden-comet-preview+json",
    }

    # Add the issue to our repository
    response = requests.request("GET", url, headers=headers)

    print(response.status_code)
    pprint(response.json())


def check_import_status(*, import_id, owner, repo, token, username):
    """Check import status."""
    try:
        auth = Auth.get_auth(
            repo_name=repo, repo_owner=owner, token=token, username=username
        )
    except MissingTokenError:
        return

    print_status(auth, import_id)

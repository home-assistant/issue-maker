from pathlib import Path
from pprint import pprint
from datetime import datetime
import sys
import requests
import json

# Authentication for user filing issue (must have read/write access to
# repository to add issue to)
USERNAME = "balloob"
TOKEN = Path(".token").read_text().strip()

# The repository to add this issue to
REPO_OWNER = "home-assistant"
REPO_NAME = "home-assistant"


def print_status(import_id):
    # Create an issue on github.com using the given parameters
    # Url to create issues via POST
    url = "https://api.github.com/repos/%s/%s/import/issues/%s" % (
        REPO_OWNER,
        REPO_NAME,
        import_id,
    )

    # Headers
    headers = {
        "Authorization": "token %s" % TOKEN,
        "Accept": "application/vnd.github.golden-comet-preview+json",
    }

    # Add the issue to our repository
    response = requests.request("GET", url, headers=headers)

    print(response.status_code)
    pprint(response.json())


print("Import ID? ", end="")
value = input().strip()
print()
print_status(value)

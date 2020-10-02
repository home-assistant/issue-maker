"""Handle github.com authentication details."""
from dataclasses import dataclass
from pathlib import Path

from .exceptions import MissingTokenError


@dataclass
class Auth:
    """Represent the github authentication details."""

    repo_name: str
    repo_owner: str
    token: str
    username: str

    @classmethod
    def get_auth(
        cls, repo_name: str, repo_owner: str, token: str, username: str
    ) -> "Auth":
        """Return a dataclass with auth details."""
        # Authentication for user filing issue (must have read/write access to
        # repository to add issue to)
        if not token:
            try:
                token = Path(".token").read_text().strip()
            except FileNotFoundError as err:
                print(
                    "Missing '.token' file. "
                    "Token must be provided by promt or in a '.token' file"
                )
                raise MissingTokenError from err
        return cls(
            repo_name=repo_name, repo_owner=repo_owner, username=username, token=token
        )

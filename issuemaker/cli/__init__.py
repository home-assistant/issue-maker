"""Provide a CLI for the issuemaker."""
import click

from issuemaker.create import create_issue
from issuemaker.status import check_import_status

# The repository to add this issue to
REPO_OWNER = "home-assistant"
REPO_NAME = "core"

SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(
    options_metavar="", subcommand_metavar="<command>", context_settings=SETTINGS
)
def cli():
    """Batch create github.com issues."""


def common_auth_options(func):
    """Provide auth options."""
    func = click.option(
        "-t",
        "--token",
        prompt=True,
        hide_input=True,
        default="",
        help="Set the auth token.",
    )(func)
    func = click.option(
        "-R",
        "--repo",
        default=REPO_NAME,
        show_default=True,
        help="Set the target repo.",
    )(func)
    func = click.option(
        "-u",
        "--username",
        required=True,
        help="Set the username.",
    )(func)
    func = click.option(
        "-O",
        "--owner",
        default=REPO_OWNER,
        show_default=True,
        help="Set the repository owner.",
    )(func)
    return func


@click.command(name="create", options_metavar="<options>")
@common_auth_options
@click.option(
    "-s", "--silent", is_flag=True, help="Make an issue without notifications."
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
def create_issue_cli(**kwargs):
    """Create issue on github.com."""
    create_issue(**kwargs)


@click.command(name="status", options_metavar="<options>")
@common_auth_options
@click.option(
    "-i",
    "--import-id",
    required=True,
    help="Set the issue import id.",
)
def check_import_status_cli(**kwargs):
    """Check import status."""
    check_import_status(**kwargs)


cli.add_command(create_issue_cli)
cli.add_command(check_import_status_cli)


if __name__ == "__main__":
    cli()

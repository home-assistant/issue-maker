"""Provide a CLI for the issuemaker."""
import click

from issuemaker.create import create_issue

# The repository to add this issue to
REPO_OWNER = "home-assistant"
REPO_NAME = "core"

SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(
    options_metavar="", subcommand_metavar="<command>", context_settings=SETTINGS
)
def cli():
    """Batch create github.com issues."""


@click.command(name="create", options_metavar="<options>")
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
def create_issue_cli(**kwargs):
    """Create issue on github.com."""
    create_issue(**kwargs)


cli.add_command(create_issue_cli)


if __name__ == "__main__":
    cli()

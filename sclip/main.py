#!/usr/bin/env python3

# Library imports
import click
import time
from typing import Tuple

# Local imports
from sclip.aux import *
from sclip.history import History

@click.group()
def cli() -> None:
    """Simple text clipboard manager written in python."""
    pass

@cli.command(name="list")
def list_items() -> None:
    """List the clipboard history."""

    with History(DATA_DIR, MAX_ITEMS) as history:
        history_items = history.load()
        for entry in history_items:
            timestamp = time.strftime(
                "%Y-%m-%d %H:%M:%S",
                time.localtime(entry["timestamp"]),
            )
            click.echo(
                f"{entry['uuid']}\t{timestamp}\t{entry["content"]}"
            )

@cli.command()
@click.argument("args", nargs=-1)
def add(args: Tuple[str]) -> None:
    """Add stdin (or all args as a string, if entered) to the clipboard history."""

    # Get content from selected medium and see if it is empty
    content: str = " ".join(args) if args else read_stdin()
    if not content:
        raise click.ClickException("There is no content to copy.")

    with History(DATA_DIR, MAX_ITEMS) as history:
        history_items = history.load()

        # Put newest item first
        entry = {
            "uuid": gen_uuid(),
            "timestamp": time.time(),
            "content": content,
        }

        # The new item goes first
        history.write([entry, *history_items])

@cli.command()
@click.argument("uuid", nargs=1, default="")
def delete(uuid: str) -> None:
    """Delete an entry by its UUID, entered from stdin (or )."""
    uuid = uuid.strip()
    if not uuid:
        uuid = read_stdin()
        print(uuid)
        exit(0)
    if not uuid:
        raise click.ClickException("No UUID was entered.")

    with History(DATA_DIR, MAX_ITEMS) as history:
        history_items = history.load()
        found = False

        for item in history_items:
            if item['uuid'] == uuid:
                found = True
                content = item['content']
                history_items.remove(item)

        history.write(history_items)

    if found:
        click.echo(f"Deleted entry {uuid}, containing \"{content}\"")
    else:
        raise click.ClickException(f"Entry not found: {uuid}")


@cli.command()
@click.option(
    "--yes",
    is_flag=True,
    help="Do not ask for confirmation.",
)
def wipe(yes: bool) -> None:
    """Delete the entire clipboard history."""

    with History(DATA_DIR, MAX_ITEMS) as history:
        history_items = history.load()

        if not history_items:
            click.echo("History is already empty.")
            return None

        if not yes:
            click.confirm(
                "Delete all clipboard entries?",
                abort=True,
            )

        history.write([])

    click.echo("History wiped.")

# Entry point
if __name__ == "__main__":
    cli()
#!/usr/bin/env python3

# Library imports
import click
import time
from typing import Tuple

# Local imports
from app.aux import *
from history import History

@click.group()
def cli():
    """Simple text clipboard manager written in python."""
    pass

# @cli.command(name="list")
# @click.option(
#     "--ids-only",
#     is_flag=True,
#     help="Only print entry IDs.",
# )
@cli.command(name="list")
def list_entries():
    """List the clipboard history."""

    with History(DATA_DIR, MAX_ITEMS) as history:
        history_items = history.load()
        for entry in history_items:
            timestamp = time.strftime(
                "%Y-%m-%d %H:%M:%S",
                time.localtime(entry["timestamp"]),
            )
            click.echo(
                f"{entry['id']}\t{timestamp}\t{entry["text"]}"
            )

@cli.command()
@click.argument("content", nargs=-1)
def add(content: Tuple[str]):
    """Add stdin to the clipboard history."""
    text: str = " ".join(content)
    print(text)

    with History(DATA_DIR, MAX_ITEMS) as history:
        # Put newest item first
        entry = {
            "id": gen_uuid(),
            "timestamp": time.time(),
            "text": text,
        }
        click.echo(entry["id"])

        # trim_history(history, max_items)
        history.append(entry)

@cli.command()
@click.argument("uuid")
def delete(uuid: str):
    """Delete an entry by its UUID."""

    click.echo(f"Eliminaría la entrada {uuid}")

    with History(DATA_DIR, MAX_ITEMS) as history:
        history_items = history.load()

        index, entry = find_entry(history, uuid)

        if entry is None:
            raise click.ClickException(
                f"Entry not found: {uuid}"
            )

    click.echo(f"Deleted {uuid}")

@cli.command()
@click.option(
    "--yes",
    is_flag=True,
    help="Do not ask for confirmation.",
)
def wipe(yes):
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

        history.wipe()

    click.echo("History wiped.")

# Entry point
if __name__ == "__main__":
    cli()
#!/usr/bin/env python3

# Library imports
import click
import time
from typing import Tuple

# Local imports
from sclip.aux import *
from sclip.history import History
from sclip.config import Config

@click.group()
def cli() -> None:
    """
    Simpleclip: Simple text clipboard manager written in python.
    Copyright (C) 2026  Pablo del Villar Ochoa

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
    """
    pass

@cli.command(name="list")
def list_cmd() -> None:
    """List the clipboard history."""

    with History() as history:
        history_items = history.load()
        for entry in history_items:
            timestamp = time.strftime(
                "%Y-%m-%d %H:%M:%S",
                time.localtime(entry["timestamp"]),
            )
            content = display(entry["content"])
            click.echo(
                f"{entry['uuid']}\t{timestamp}\t{content}"
            )

@cli.command()
@click.argument("args", nargs=-1)
def add(args: Tuple[str]) -> None:
    """Add stdin (or all args as a string, if entered) to the clipboard history."""

    # Get content from selected medium and see if it is empty
    content: str = " ".join(args) if args else read_stdin()
    if not content:
        raise click.ClickException("There is no content to copy.")

    with History() as history:
        history_items = history.load()

        # Put newest item first
        entry: JSONUnit = {
            "uuid": gen_uuid(),
            "timestamp": time.time(),
            "content": content,
        }

        # The new item goes first
        history.write([entry, *history_items])

@cli.command()
@click.argument("args", nargs=-1)
def delete(args: Tuple[str]) -> None:
    """Delete an entry by its UUID, entered from stdin (or arguments)."""

    if args:
        uuid = args[0]
    else:
        uuid = read_stdin().partition("\t")[0]
    if not uuid.strip():
        raise click.ClickException("No UUID was entered.")

    with History() as history:
        history_items = history.load()
        found = False

        for item in history_items:
            if item['uuid'] == uuid:
                found = True
                content: str = item['content']
                history_items.remove(item)

        history.write(history_items)

    if found:
        click.echo(f"Deleted entry {uuid}, containing {display(content)}")
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

    with History() as history:
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

@cli.group("config")
def config_group() -> None:
    """Read or set configuration parameters."""
    pass

@config_group.command(name="list")
def config_list() -> None:
    """See all the configuration parameters."""
    with Config() as config:
        click.echo(config.load())

@config_group.command(name="read")
@click.argument("parameter", nargs=1)
def config_read(parameter: str) -> None:
    """Read a parameter from the configuration file."""
    with Config() as config:
        all_configs = config.load()
    if parameter not in all_configs:
        raise click.ClickException(f"Parameter \"{parameter}\" does not exist!")


    value: Parameter = all_configs[parameter]
    click.echo(f"Value for {parameter} is: {value}")
        # elif set:
        #     all_configs[parameter] = set
        #     config.write(all_configs)
        # else:
        #     raise click.ClickException("Use --read or --set to use configs!")

# Entry point
if __name__ == "__main__":
    cli()
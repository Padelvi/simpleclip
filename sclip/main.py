#!/usr/bin/env python3

# Library imports
import click
import time

# Local imports
from sclip.aux import *
from sclip.history import History
from sclip.config import Config
from sclip.watcher import watch

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
def add() -> None:
    """Add stdin to the clipboard history."""

    # Get content from selected medium and see if it is empty
    content: str = read_stdin()
    if not content:
        raise click.ClickException("There is no content to copy. Remember to use stdin.")

    with History() as history:
        history.append(content)

@cli.command()
def copy() -> None:
    """Copy stdin content to clipboard (it is not added to the history)."""

    content = read_stdin()

    with Config() as config:
        try:
            copy_cmd = config.load()["COPY_CMD"]
        except KeyError:
            config.reset()
            copy_cmd = config.load()["COPY_CMD"]

    copy_stdin(copy_cmd, content)

@cli.command()
def delete() -> None:
    """Delete an entry by its UUID, entered from stdin (or arguments)."""

    uuid = read_stdin().partition("\t")[0]
    if not uuid.strip():
        raise click.ClickException("No UUID was entered. Remember to use stdin.")

    with History() as history:
        history_items = history.load()
        found = False

        for item in history_items:
            if item['uuid'] == uuid:
                found = True
                content: str = item['content']
                history_items.remove(item)
                click.echo(f"Deleted entry {uuid}, containing {display(content)}")

        history.write(history_items)

    if not found:
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
    """Read, set or reset configuration parameters."""
    pass

@config_group.command(name="list")
def config_list() -> None:
    """See all the configuration parameters."""

    with Config() as config:
        click.echo(config.load())

@config_group.command(name="read")
@click.argument("parameter_name", nargs=1)
def config_read(parameter_name: str) -> None:
    """Read a parameter from the configuration file."""

    parameter_name = parameter_name.upper()

    with Config() as config:
        all_configs = config.load()
    if parameter_name not in all_configs:
        raise click.ClickException(f"parameter_name \"{parameter_name}\" does not exist!")

    value: Parameter = all_configs[parameter_name]
    click.echo(f"Value for {parameter_name} is: {value}")

@config_group.command(name="set")
@click.argument("parameter_name", nargs=1)
@click.argument("value", nargs=1)
def config_set(parameter_name: str, value: Parameter) -> None:
    """Read a parameter from the configuration file."""

    parameter_name = parameter_name.upper()

    with Config() as config:
        all_configs = config.load()
        if parameter_name not in all_configs:
            raise click.ClickException(f"parameter_name \"{parameter_name}\" does not exist!")

        all_configs[parameter_name] = value
        config.write(all_configs)

        click.echo(f"Wrote parameter {parameter_name} to {value}")

@config_group.command(name="reset")
@click.option(
    "--yes",
    is_flag=True,
    help="Do not ask for confirmation.",
)
def config_reset(yes: bool) -> None:
    """Reset all the default config parameters."""

    with Config() as config:
        if not yes:
            click.confirm(
                "Reset all the default config parameters?",
                abort=True,
            )

        config.reset()

    click.echo("Config reset.")

@cli.command("watch")
def watch_command():
    """Start the clipboard watcher process."""
    watch()

# Entry point
if __name__ == "__main__":
    cli()
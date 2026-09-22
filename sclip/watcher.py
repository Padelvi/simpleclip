# Library imports
import subprocess
import time
from typing import List
from click import ClickException, echo

# Local imports
from sclip.history import History
from sclip.config import Config

def get_clipboard(paste_cmd: List[str]) -> str:
    result = subprocess.run(
        paste_cmd,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return ""

    return result.stdout.strip()

def watch() -> None:
    # Get necessary configs for the watcher
    with Config() as config:
        config_items =  config.load()

        try:
            paste_cmd_str: str = config_items["PASTE_CMD"]
        except IndexError:
            config.reset()
            config_items =  config.load()
            paste_cmd_str: str = config_items["PASTE_CMD"]
        paste_cmd = paste_cmd_str.split(" ")

        try:
            watcher_time: float = config_items["WATCHER_TIME"]/1000
        except IndexError:
            config.reset()
            config_items =  config.load()
            watcher_time: float = config_items["WATCHER_TIME"]/1000

    # Get the first item in the clipboard
    previous = get_clipboard(paste_cmd)

    # Never stop the watcher unless interrupted
    echo("Watching...")
    while True:
        # Get the new item in the clipboard
        current = get_clipboard(paste_cmd)

        # Update the new item
        if current != previous:
            previous = current
            # If necessary, append it to history
            if current:
                with History() as history:
                    history.append(current)
                echo(f"Copied {current}")

        # Sleep during the time specified in the config
        time.sleep(watcher_time)
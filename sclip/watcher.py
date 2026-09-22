# Library imports
import subprocess
import time
from typing import List

# Local imports
from sclip.history import History
from sclip.config import Config

def get_clipboard(copy_cmd: List[str]) -> str:
    result = subprocess.run(
        copy_cmd,
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
        copy_cmd_str: str = config_items["COPY_CMD"]
        copy_cmd = copy_cmd_str.split(" ")
        watcher_time: float = config_items["WATCHER_TIME"]/1000

    # Get the first item in the clipboard
    previous = get_clipboard(copy_cmd)

    # Never stop the watcher unless interrupted
    while True:
        # Get the new item in the clipboard
        current = get_clipboard(copy_cmd)

        # If necessary, update the new item and append it to history
        if bool(current) and current != previous:
            previous = current

            with History() as history:
                history.append(current)

        # Sleep during the time specified in the config
        time.sleep(watcher_time)
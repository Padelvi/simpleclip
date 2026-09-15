import subprocess
import time

from sclip.history import History
from sclip.config import Config


def get_clipboard() -> str:
    result = subprocess.run(
        ["xclip", "-selection", "clipboard", "-o"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return ""

    return result.stdout


def main() -> None:
    previous = get_clipboard()

    while True:
        current = get_clipboard()

        if current != previous:
            previous = current

            if current.strip():
                add(current)

        time.sleep(0.5)


if __name__ == "__main__":
    main()
import os
from pathlib import Path

DATA_DIR = Path(
    os.environ.get(
        "XDG_DATA_HOME",
        Path.home() / ".local" / "share"
    )
) / "clip"

MAX_ITEMS = 50
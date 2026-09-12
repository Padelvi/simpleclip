# Library imports
import fcntl
import json
from pathlib import Path
from click import ClickException

# Local imports
from clip.aux import *

class History:
    def __init__(self, data_dir: Path, max_items: int) -> None:
        ensure_dir(data_dir)
        self.data_dir = data_dir

        self.path = data_dir / "history.json"
        self.lockpath = data_dir / "lock"

        self.max_items = max_items

    # PENDING
    def trim(self) -> None:
        return None

    # Get a read-only view of the clipboard
    def load(self) -> JSONType:
        if not self.path.exists():
            return []

        try:
            with self.path.open("r", encoding="utf-8") as f:
                result: JSONType = json.load(f)

            return result

        except (OSError, json.JSONDecodeError, ValueError):
            raise ClickException(
                f"Could not read history file: {self.path}"
        )

    def write(self, entry: JSONType) -> None:
        with open(self.path, "w") as f:
            json.dump(entry, f, indent=2)

    # def find(self, content: str) -> Tuple[str]:
    #     for index, entry in self.load().values():
    #         if entry["content"] in contents:
    #             return index, entry

    #     return None

# Process-level lock shared by all operations managed with __enter__ and __exit__

    def __enter__(self):
        ensure_dir(self.data_dir)
        self.file = self.lockpath.open("w")
        # PENDING: Remove malformed entries

        fcntl.flock(
            self.file.fileno(),
            fcntl.LOCK_EX,
        )
        return self

    def __exit__(self, exc_type, exc, tb):
        fcntl.flock(
            self.file.fileno(),
            fcntl.LOCK_UN,
        )
        self.file.close()
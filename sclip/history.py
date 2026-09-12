# Library imports
import fcntl
import json
from click import ClickException

# Local imports
from sclip.aux import *
from sclip.config import Config

class History:
    def __init__(self) -> None:
        with Config() as config:
            config_items = config.load()

        self.state_dir: Path = Path.home() / config_items['STATE_DIR']
        ensure_dir(self.state_dir)

        self.path = self.state_dir / "history.json"
        self.lockpath = self.state_dir / "lock"

        self.max_items: int = config_items['MAX_ITEMS']

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

# Process-level lock shared by all operations managed with __enter__ and __exit__
    def __enter__(self):
        ensure_dir(self.state_dir)
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
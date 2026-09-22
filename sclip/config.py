# Library imports
import shutil, json
import fcntl
from pathlib import Path

# Local imports
from sclip.aux import *

class Config:
    def __init__(self) -> None:
        self.default_config = Path(__file__).with_name("default_config.json")
        self.config_dir = Path.home() / ".config/sclip"
        self.config_file = self.config_dir / "config.json"
        self.lockpath = self.config_dir / "lock"

        ensure_dir(self.config_dir)

    def load(self) -> JSONUnit:
        ensure_dir(self.config_dir)
        if not self.config_file.exists():
            shutil.copy(self.default_config, self.config_file)
        with open(self.config_file, "r") as f:
            return json.load(f)

        try:
            with self.path.open("r", encoding="utf-8") as f:
                result: JSONType = json.load(f)

            return result

        except (OSError, json.JSONDecodeError, ValueError):
            raise ClickException(
                f"Could not read config file: {self.path}"
        )

    def write(self, entry: JSONUnit) -> None:
        with open(self.config_file, "w") as f:
            json.dump(entry, f, indent=1)

    def reset(self):
        ensure_dir(self.config_dir)
        shutil.copy(self.default_config, self.config_file)

# Process-level lock shared by all operations managed with __enter__ and __exit__
    def __enter__(self):
        ensure_dir(self.config_dir)
        self.file = self.lockpath.open("w")

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
# Library imports
import sys
from pathlib import Path
from uuid import uuid4
from typing import List, Dict, Any
from click import ClickException

type JSONType = List[Dict[str, Any]]

# Ensure a dir exists, create it if not
def ensure_dir(dir: Path):
    dir.mkdir(mode=0o700, parents=True, exist_ok=True)

# Short random ID
def gen_uuid():
    return uuid4().hex[:8]

def read_stdin() -> str:
    if sys.stdin.isatty():
        raise ClickException("Empty command! Use an argument or a pipe (not a tty) for stdin.")
    return sys.stdin.read().strip()

def display(content: str) -> str:
    return repr(content).replace("\n", "\t")
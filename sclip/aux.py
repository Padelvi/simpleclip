# Library imports
import sys
from subprocess import run
from pathlib import Path
from uuid import uuid4
from typing import List, Dict, Any
from click import ClickException, echo

type Parameter = int|str
type JSONConfig = Dict[str, Parameter]
type JSONUnit = Dict[str, Any]
type JSONMultiple = List[JSONUnit]

# Ensure a dir exists, create it if not
def ensure_dir(dir: Path):
    dir.mkdir(mode=0o700, parents=True, exist_ok=True)

# Short random ID
def gen_uuid() -> str:
    return uuid4().hex[:8]

def read_stdin() -> str:
    if sys.stdin.isatty():
        raise ClickException("Empty command! Use an argument or a pipe (not a tty) for stdin.")
    return sys.stdin.read().strip()

def display(content: str) -> str:
    return repr(content).replace("\n", "\t")

# Copy something to the real clipboard, using the command specified in configs
def copy_stdin(copy_cmd: List[str], content: str) -> None:
    result = run(
        [*copy_cmd, content],
        capture_output=True,
        text=True,
    )
    echo(result.stdout)
    if result.returncode != 0:
        raise ClickException(result.stderr)

def get_clipboard(paste_cmd: List[str]) -> str:
    result = run(
        paste_cmd,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()
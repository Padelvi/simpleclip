from pathlib import Path
from uuid import uuid4
from typing import List, Dict, Any

type JSONType = List[Dict[str, Any]]

def ensure_dir(dir: Path):
    dir.mkdir(mode=0o700, parents=True, exist_ok=True)

# Short random ID
def gen_uuid():
    return uuid4().hex[:8]

# Probably unnecessary, maybe move to history object
def find_entry(history, entry_id):
    for index, entry in enumerate(history):
        if entry["id"] == entry_id:
            return index, entry

    return None, None
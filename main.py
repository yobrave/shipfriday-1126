#!/usr/bin/env python3
"""sif: gate-check the entry line and emit it where the scorer looks."""

import json
import os
from pathlib import Path

CONFIG = {"source": "entry.txt", "target": "entry.txt", "max": 159, "min": 1}


def load_first_line(text):
    for row in text.replace("\r\n", "\n").splitlines():
        if row.strip():
            return row
    return None


def emit():
    repo_root = Path(__file__).resolve().parent
    try:
        blob = (repo_root / CONFIG["source"]).read_text(encoding="utf-8")
    except OSError:
        print(json.dumps({"gate": "fail", "cause": "source unreadable"}))
        return 2
    line = load_first_line(blob)
    if line is None:
        print(json.dumps({"gate": "fail", "cause": "blank entry"}))
        return 1
    if len(line) > CONFIG["max"]:
        print(json.dumps({"gate": "fail", "cause": "too long", "len": len(line)}))
        return 1
    where = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
    where.mkdir(parents=True, exist_ok=True)
    (where / CONFIG["target"]).write_text(line, encoding="utf-8")
    print(json.dumps({"gate": "pass", "len": len(line), "max": CONFIG["max"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(emit())

"""Shared helpers: run the tools as a user would, on the real graph or on a copy.

Tests go through the command line only (`tools/validate.py`, `tools/plan.py`),
so they check what CI and agents see and survive refactors of the internals.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parent.parent
TOOLS = REPO / "tools"


@dataclass
class Result:
    returncode: int
    errors: list[str]
    warnings: list[str]
    stdout: str


def run_tool(script: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(TOOLS / script), *args],
                          capture_output=True, text=True, cwd=REPO)


def run_validate(*args: str) -> Result:
    p = run_tool("validate.py", *args)
    lines = p.stdout.splitlines()
    return Result(
        returncode=p.returncode,
        errors=[ln.removeprefix("ERROR: ") for ln in lines if ln.startswith("ERROR: ")],
        warnings=[ln.removeprefix("warning: ") for ln in lines if ln.startswith("warning: ")],
        stdout=p.stdout + p.stderr,
    )


class GraphCopy:
    """A throwaway copy of graph/ in which a test plants one fault."""

    def __init__(self, root: Path):
        self.root = root

    def node_file(self, node_id: str) -> Path:
        (path,) = self.root.glob(f"nodes/*/{node_id}.yaml")
        return path

    def edit(self, path: Path, change) -> None:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        change(data)
        path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")

    def edit_node(self, node_id: str, change) -> None:
        self.edit(self.node_file(node_id), change)

    def validate(self) -> Result:
        return run_validate("--root", str(self.root))


@pytest.fixture
def graph(tmp_path: Path) -> GraphCopy:
    root = tmp_path / "graph"
    shutil.copytree(REPO / "graph", root)
    return GraphCopy(root)

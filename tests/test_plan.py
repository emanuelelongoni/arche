"""tools/plan.py on the real graph."""
import re

from conftest import run_tool


def test_heine_borel_route_lengths_per_viewpoint():
    p = run_tool("plan.py", "ts.heine-borel", "--compare", "classical", "npov")
    assert p.returncode == 0, p.stderr
    counts = dict(re.findall(r"^Viewpoint (\w+): (\d+) topics$", p.stdout, re.M))
    assert counts == {"classical": "26", "npov": "32"}

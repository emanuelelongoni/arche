"""Answer a batch of route questions with tools/plan.py itself, for the parity tests.

stdin: [{"viewpoint": str, "targets": [str], "known": [str]}, ...]
stdout: [{"route": [str], "minutes": int}, ...]  (minutes: plan.py's total, stubs not counted)
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
import mmgraph as G  # noqa: E402
from plan import plan  # noqa: E402

g = G.load()
out = []
for case in json.load(sys.stdin):
    route = plan(g, case["viewpoint"], case["targets"], set(case["known"]))
    out.append({"route": route, "minutes": sum(g.nodes[n].get("minutes") or 0 for n in route)})
json.dump(out, sys.stdout)

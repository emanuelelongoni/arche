#!/usr/bin/env python3
"""Export the graph as the JSON document the website is built from.

The site (site/) renders only this document, which is generated at build time and
never committed, so the site can't drift from graph/. Viewpoint resolution happens
here, through mmgraph, so its semantics stay in one place (docs/specs/site-v0.md).

Refuses to export (exit 1, nothing written) a graph that has validator errors.

Usage:
  python3 tools/export_site.py --out site/.generated/site-data.json [--root DIR]
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import subprocess
import sys
import tomllib
from pathlib import Path

import mmgraph as G
import validate as V


def provenance() -> dict:
    commit = os.environ.get("GITHUB_SHA")
    if not commit:
        try:
            commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=G.ROOT, capture_output=True,
                                    text=True, check=True).stdout.strip()
        except (OSError, subprocess.CalledProcessError):
            commit = "unknown"
    lake = tomllib.loads((G.ROOT / "lean" / "lakefile.toml").read_text(encoding="utf-8"))
    mathlib = next(r for r in lake.get("require", []) if r.get("name") == "mathlib")
    return {
        "commit": commit,
        "date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
        "mathlibRev": mathlib["rev"],
    }


def export(g: G.Graph) -> dict:
    cov = G.coverage(g)
    minutes = G.section_minutes(g)
    courses = {}
    for cid, c in sorted(g.courses.items()):
        sections = c.get("sections", []) or []
        courses[cid] = {
            **c,
            "coverage": {it["id"]: cov[f"{cid}#{it['id']}"] for s in sections for it in s.get("items", []) or []},
            "sectionMinutes": {str(s["n"]): minutes.get((cid, s["n"]), 0) for s in sections},
        }
    viewpoints = {}
    for vp, v in sorted(g.viewpoints.items()):
        act = g.active(vp)
        dag: dict[str, list[str]] = {}
        edges = []
        for nid in sorted(act):
            dag[nid] = []
            for e in g.requires_under(vp, nid):
                if e["node"] in act:  # the same DAG tools/plan.py builds
                    dag[nid].append(e["node"])
                    edges.append({"from": nid, "to": e["node"], "reason": e["reason"], "via": e["via"]})
        viewpoints[vp] = {**v, "active": sorted(act), "dag": dag, "edges": edges}
    return {
        "builtFrom": provenance(),
        "courses": courses,
        "nodes": {nid: g.nodes[nid] for nid in sorted(g.nodes)},
        "viewpoints": viewpoints,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--root", type=Path, default=G.GRAPH,
                    help="graph directory to export (default: graph/ in this repo)")
    args = ap.parse_args()

    g, log = V.run(args.root)
    if log.errors:
        for e in log.errors:
            print(f"ERROR: {e}")
        sys.exit(f"not exporting: the graph has {len(log.errors)} validator errors")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    tmp = args.out.with_suffix(".tmp")
    tmp.write_text(json.dumps(export(g), ensure_ascii=False, default=str), encoding="utf-8")
    tmp.replace(args.out)
    print(f"wrote {args.out} ({len(g.nodes)} nodes, {len(g.viewpoints)} viewpoints)")


if __name__ == "__main__":
    main()

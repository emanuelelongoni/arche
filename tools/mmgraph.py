"""Load the knowledge graph and resolve it under a viewpoint.

Everything the other tools need goes through this module, so the semantics in
spec/SCHEMA.md live in one place.
"""
from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
GRAPH = ROOT / "graph"
SCHEMA = ROOT / "schema"


@dataclass
class Graph:
    root: Path = GRAPH  # the graph directory: courses/, nodes/, viewpoints/
    courses: dict[str, dict] = field(default_factory=dict)
    nodes: dict[str, dict] = field(default_factory=dict)
    viewpoints: dict[str, dict] = field(default_factory=dict)
    files: dict[str, Path] = field(default_factory=dict)  # "kind:id" -> path
    load_errors: list[str] = field(default_factory=list)

    def display(self, path: Path) -> str:
        """A file path as messages show it: relative to the directory that holds the graph."""
        try:
            return str(path.relative_to(self.root.parent))
        except ValueError:
            return str(path)

    # ---- choice groups -------------------------------------------------
    def choice_groups(self) -> dict[str, list[tuple[str, dict]]]:
        """group id -> [(node id, choice dict), ...]"""
        groups: dict[str, list[tuple[str, dict]]] = defaultdict(list)
        for nid, n in self.nodes.items():
            for r in n.get("requires", []) or []:
                if "choice" in r:
                    groups[r["choice"]].append((nid, r))
        return groups

    def group_default(self, group: str) -> str | None:
        occ = self.choice_groups().get(group)
        return occ[0][1]["default"] if occ else None

    # ---- viewpoint resolution -----------------------------------------
    def active(self, vp: str) -> set[str]:
        return {nid for nid, n in self.nodes.items()
                if not n.get("only_in") or vp in n["only_in"]}

    def picked(self, vp: str, group: str) -> str | None:
        choices = self.viewpoints.get(vp, {}).get("choices", {}) or {}
        return choices.get(group, self.group_default(group))

    def requires_under(self, vp: str, nid: str) -> list[dict]:
        """Resolved requires edges of one node under a viewpoint.
        Each edge dict gets 'via': None for plain edges, or 'group:option'."""
        out = []
        for r in self.nodes[nid].get("requires", []) or []:
            if "node" in r:
                out.append({**r, "via": None})
            else:
                opt = self.picked(vp, r["choice"])
                for e in (r["options"].get(opt) or []):
                    out.append({**e, "via": f"{r['choice']}:{opt}"})
        return out

    def dag(self, vp: str) -> dict[str, list[str]]:
        """Adjacency: node -> prerequisites (resolved, active nodes only as sources)."""
        act = self.active(vp)
        return {nid: [e["node"] for e in self.requires_under(vp, nid)] for nid in act}

    def all_requires_targets(self, nid: str) -> list[str]:
        out = []
        for r in self.nodes[nid].get("requires", []) or []:
            if "node" in r:
                out.append(r["node"])
            else:
                for edges in r["options"].values():
                    out.extend(e["node"] for e in edges or [])
        return out


def ancestors(dag: dict[str, list[str]], start: str) -> set[str]:
    seen: set[str] = set()
    stack = list(dag.get(start, []))
    while stack:
        x = stack.pop()
        if x in seen:
            continue
        seen.add(x)
        stack.extend(dag.get(x, []))
    return seen


def coverage(g: Graph) -> dict[str, dict]:
    """Every course item "<course>#<item>" -> {"state", "nodes"} (spec/SCHEMA.md §5, Reports).

    state is "covered" (by a draft or reviewed node), "stub-only" or "uncovered";
    nodes lists the covering node ids, sorted.
    """
    by_item: dict[str, list[str]] = defaultdict(list)
    for nid in sorted(g.nodes):
        for cov in g.nodes[nid].get("covers", []) or []:
            by_item[cov].append(nid)
    out = {}
    for cid, c in g.courses.items():
        for s in c.get("sections", []) or []:
            for it in s.get("items", []) or []:
                key = f"{cid}#{it['id']}"
                nodes = by_item.get(key, [])
                if {g.nodes[n]["status"] for n in nodes} & {"draft", "reviewed"}:
                    state = "covered"
                else:
                    state = "stub-only" if nodes else "uncovered"
                out[key] = {"state": state, "nodes": nodes}
    return out


def section_minutes(g: Graph) -> dict[tuple[str, int], int]:
    """(course id, section) -> total estimated minutes of the nodes placed in that section."""
    out: dict[tuple[str, int], int] = defaultdict(int)
    for n in g.nodes.values():
        if n.get("section") and n.get("minutes"):
            out[(n["course"], n["section"])] += n["minutes"]
    return dict(out)


def find_cycle(dag: dict[str, list[str]]) -> list[str] | None:
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {n: WHITE for n in dag}
    parent: dict[str, str] = {}

    for root in dag:
        if colour[root] != WHITE:
            continue
        stack = [(root, iter(dag.get(root, [])))]
        colour[root] = GREY
        while stack:
            node, it = stack[-1]
            nxt = next(it, None)
            if nxt is None:
                colour[node] = BLACK
                stack.pop()
                continue
            if nxt not in colour:  # target outside the active set
                continue
            if colour[nxt] == GREY:
                cyc = [nxt, node]
                cur = node
                while cur != nxt:
                    cur = parent[cur]
                    cyc.append(cur)
                return list(reversed(cyc))
            if colour[nxt] == WHITE:
                parent[nxt] = node
                colour[nxt] = GREY
                stack.append((nxt, iter(dag.get(nxt, []))))
    return None


def topo_order(dag: dict[str, list[str]], subset: set[str]) -> list[str]:
    """Prerequisites first; ties broken by id for stable output."""
    indeg = {n: 0 for n in subset}
    users: dict[str, list[str]] = defaultdict(list)
    for n in subset:
        for p in dag.get(n, []):
            if p in subset:
                indeg[n] += 1
                users[p].append(n)
    ready = sorted(n for n, d in indeg.items() if d == 0)
    out = []
    while ready:
        n = ready.pop(0)
        out.append(n)
        for u in users[n]:
            indeg[u] -= 1
            if indeg[u] == 0:
                ready.append(u)
        ready.sort()
    return out


def _load_yaml(g: Graph, path: Path):
    try:
        with path.open(encoding="utf-8") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        g.load_errors.append(f"{g.display(path)}: YAML error: {e}")
        return None


def load(root: Path = GRAPH) -> Graph:
    """Load the graph under `root` (default: graph/ in this repo)."""
    g = Graph(root=Path(root).resolve())
    root = g.root
    for p in sorted((root / "courses").glob("*.yaml")):
        d = _load_yaml(g, p)
        if isinstance(d, dict) and "id" in d:
            if d["id"] in g.courses:
                g.load_errors.append(f"duplicate course id {d['id']} in {g.display(p)}")
            g.courses[d["id"]] = d
            g.files[f"course:{d['id']}"] = p
    for p in sorted((root / "viewpoints").glob("*.yaml")):
        d = _load_yaml(g, p)
        if isinstance(d, dict) and "id" in d:
            g.viewpoints[d["id"]] = d
            g.files[f"viewpoint:{d['id']}"] = p
    for p in sorted((root / "nodes").rglob("*.yaml")):
        d = _load_yaml(g, p)
        if isinstance(d, dict) and "id" in d:
            if d["id"] in g.nodes:
                g.load_errors.append(
                    f"duplicate node id {d['id']}: {g.display(g.files['node:' + d['id']])} and {g.display(p)}")
            g.nodes[d["id"]] = d
            g.files[f"node:{d['id']}"] = p
        elif d is not None:
            g.load_errors.append(f"{g.display(p)}: not a node (no id)")
    return g


def load_schema(name: str) -> dict:
    return json.loads((SCHEMA / f"{name}.schema.json").read_text(encoding="utf-8"))

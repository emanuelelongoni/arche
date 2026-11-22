"""tools/export_site.py: the JSON the website is built from."""
import json
import re

import pytest

from conftest import REPO, run_tool, run_validate


def export(tmp_path, *args):
    out = tmp_path / "site-data.json"
    p = run_tool("export_site.py", "--out", str(out), *args)
    return p, out


@pytest.fixture(scope="module")
def data(tmp_path_factory):
    p, out = export(tmp_path_factory.mktemp("export"))
    assert p.returncode == 0, p.stdout + p.stderr
    return json.loads(out.read_text(encoding="utf-8"))


def test_choice_groups_are_resolved_per_viewpoint(data):
    dag = {vp: v["dag"] for vp, v in data["viewpoints"].items()}
    assert sorted(dag["classical"]["ts.finite-products-compact"]) == ["ts.interval-compact", "ts.tube-lemma"]
    assert sorted(dag["npov"]["ts.finite-products-compact"]) == ["ts.compact-universally-closed", "ts.interval-compact"]
    vias = {(e["to"], e["via"]) for e in data["viewpoints"]["npov"]["edges"]
            if e["from"] == "ts.finite-products-compact"}
    assert vias == {("ts.interval-compact", None),
                    ("ts.compact-universally-closed", "product-compactness-route:universally-closed")}


def test_nodes_only_in_npov_are_active_only_there(data):
    assert "ct.categories" in data["viewpoints"]["npov"]["active"]
    assert "ct.categories" not in data["viewpoints"]["classical"]["active"]
    assert "ct.categories" not in data["viewpoints"]["classical"]["dag"]


def test_counts_match_the_validator_report(data):
    report = run_tool("validate.py", "--report").stdout
    rows = re.findall(r"^\| (\w+) \| (\d+) \| \d+ \| (\d+) \|", report, re.M)
    assert rows, report
    for vp, nodes, edges in rows:
        v = data["viewpoints"][vp]
        assert len(v["active"]) == int(nodes)
        assert sum(len(ps) for ps in v["dag"].values()) == int(edges) == len(v["edges"])


def test_coverage_matches_the_validator_report(data):
    report = run_tool("validate.py", "--report").stdout
    totals = re.findall(r"^### ([\w-]+):.*?^Total: (\d+)/(\d+) items covered by draft or reviewed nodes, "
                        r"(\d+) by stubs only, (\d+) uncovered\.", report, re.M | re.S)
    assert totals, report
    for cid, done, tot, stub, unc in totals:
        states = [c["state"] for c in data["courses"][cid]["coverage"].values()]
        assert (states.count("covered"), len(states), states.count("stub-only"), states.count("uncovered")) \
            == (int(done), int(tot), int(stub), int(unc))


def test_raw_yaml_is_carried_unchanged(data):
    n = data["nodes"]["ts.finite-products-compact"]
    assert n["anchors"] == [{"decl": "IsCompact.prod"}]
    assert n["requires"][1]["choice"] == "product-compactness-route"


def test_provenance_names_the_pinned_mathlib(data):
    rev = re.search(r'^rev = "([0-9a-f]+)"', (REPO / "lean/lakefile.toml").read_text(), re.M).group(1)
    assert data["builtFrom"]["mathlibRev"] == rev
    assert re.fullmatch(r"[0-9a-f]{40}|unknown", data["builtFrom"]["commit"])


def test_refuses_a_graph_with_errors(graph, tmp_path):
    graph.edit_node("ts.hausdorff", lambda d: d.setdefault("requires", []).append(
        {"node": "ts.no-such-node", "reason": "Planted by a test to check the export."}))
    assert run_validate("--root", str(graph.root)).returncode == 1
    p, out = export(tmp_path, "--root", str(graph.root))
    assert p.returncode == 1
    assert "requires unknown node ts.no-such-node" in p.stdout + p.stderr
    assert not out.exists()

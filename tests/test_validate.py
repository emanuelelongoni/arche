"""tools/validate.py, run on the real graph and on copies with one planted fault.

Each fault is planted on a relation that should stay true as the graph grows
(Hausdorff spaces need topological spaces; the intermediate value theorem never
needs category theory), so these tests don't break when agents add nodes.
"""
from conftest import run_validate

TS = "graph/nodes/ib-topological-spaces"
A1 = "graph/nodes/ia-analysis-i"


def requires(node: str, reason: str = "Planted by a test to check the validator."):
    """A change that adds one plain requires edge to a node."""
    def change(d):
        d.setdefault("requires", []).append({"node": node, "reason": reason})
    return change


def test_untouched_copy_is_clean(graph):
    r = graph.validate()
    assert (r.returncode, r.errors, r.warnings) == (0, [], []), r.stdout


def test_real_graph_is_clean():
    r = run_validate()
    assert (r.returncode, r.errors, r.warnings) == (0, [], []), r.stdout


def test_file_name_must_match_id(graph):
    path = graph.node_file("ts.hausdorff")
    path.rename(path.with_name("ts.hausdorf.yaml"))
    r = graph.validate()
    assert r.returncode == 1
    assert r.errors == ["graph/nodes/ib-topological-spaces/ts.hausdorf.yaml: file name must be ts.hausdorff.yaml"]
    assert r.warnings == []


def test_unknown_requires_target(graph):
    graph.edit_node("ts.hausdorff", requires("ts.no-such-node"))
    r = graph.validate()
    assert r.returncode == 1
    assert r.errors == [f"{TS}/ts.hausdorff.yaml: requires unknown node ts.no-such-node"]
    assert r.warnings == []


def test_unknown_covers_item(graph):
    graph.edit_node("ts.hausdorff", lambda d: d["covers"].append("ib-topological-spaces#no-such-item"))
    r = graph.validate()
    assert r.returncode == 1
    assert r.errors == [f"{TS}/ts.hausdorff.yaml: covers unknown item ib-topological-spaces#no-such-item"]
    assert r.warnings == []


def test_cycle_is_reported_under_each_viewpoint(graph):
    # ts.hausdorff already depends on ts.topology-def, so this closes a cycle.
    graph.edit_node("ts.topology-def", requires("ts.hausdorff"))
    r = graph.validate()
    assert r.returncode == 1
    assert r.warnings == []
    assert len(r.errors) == 2
    for vp, err in zip(("classical", "npov"), r.errors):
        prefix = f"viewpoint {vp}: cycle: "
        assert err.startswith(prefix), err
        cycle = err.removeprefix(prefix).split(" requires ")
        assert cycle[0] == cycle[-1], "the printed cycle is closed"
        assert {"ts.topology-def", "ts.hausdorff"} <= set(cycle)


def test_active_node_requires_node_only_in_another_viewpoint(graph):
    # ct.categories has only_in: [npov]; a1.ivt exists in every viewpoint.
    graph.edit_node("a1.ivt", requires("ct.categories"))
    r = graph.validate()
    assert r.returncode == 1
    assert r.errors == [f"{A1}/a1.ivt.yaml: under viewpoint classical, requires ct.categories, "
                        "which does not exist in classical (only_in)"]
    assert r.warnings == []


def test_choice_group_options_differ_between_nodes(graph):
    # constructions-route is shared by ts.product-topology, ts.quotient-topology and
    # ts.subspace-topology; rename one option in one of them.
    def rename_option(d):
        (group,) = [r for r in d["requires"] if r.get("choice") == "constructions-route"]
        group["options"]["induced"] = group["options"].pop("initial-final")
    graph.edit_node("ts.subspace-topology", rename_option)
    r = graph.validate()
    assert r.returncode == 1
    assert r.warnings == []
    assert len(r.errors) == 1
    assert r.errors[0].startswith(f"{TS}/ts.subspace-topology.yaml: choice constructions-route differs from ")
    assert "options ['concrete', 'induced'] default 'concrete' vs ['concrete', 'initial-final']" in r.errors[0]


def test_viewpoint_picks_nonexistent_option(graph):
    graph.edit(graph.root / "viewpoints/npov.yaml",
               lambda d: d["choices"].update({"product-compactness-route": "proper-maps"}))
    r = graph.validate()
    assert r.returncode == 1
    assert r.errors == ["graph/viewpoints/npov.yaml: group product-compactness-route has no option 'proper-maps'"]
    assert r.warnings == []


def test_redundant_requires_edge_is_a_warning(graph):
    # ts.hausdorff reaches ts.topology-def through its other prerequisites in every viewpoint.
    graph.edit_node("ts.hausdorff", requires("ts.topology-def"))
    r = graph.validate()
    assert (r.returncode, r.errors) == (0, [])
    assert r.warnings == [f"{TS}/ts.hausdorff.yaml: requires ts.topology-def is redundant "
                          "(implied by another prerequisite) in every viewpoint where it is active"]


def test_encompasses_target_that_is_not_an_ancestor_is_a_warning(graph):
    graph.edit_node("a1.ivt", lambda d: d.setdefault("encompasses", []).append(
        {"node": "ts.compact-def", "weight": 0.5}))
    r = graph.validate()
    assert (r.returncode, r.errors) == (0, [])
    assert r.warnings == [f"{A1}/a1.ivt.yaml: encompasses ts.compact-def, "
                          "which is not an ancestor under classical, npov"]

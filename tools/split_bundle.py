#!/usr/bin/env python3
"""Split a multi-document YAML bundle of nodes into one file per node.

Agents may author many nodes in one file (documents separated by `---`), then run:
  python3 tools/split_bundle.py authoring/<bundle>.yaml [--force]
Each document is written to graph/nodes/<course>/<id>.yaml. Existing files are
not overwritten unless --force is given.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

import mmgraph as G


class Dumper(yaml.SafeDumper):
    pass


def _str(dumper, s):
    style = "|" if "\n" in s else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", s, style=style)


Dumper.add_representer(str, _str)

ORDER = ["id", "title", "course", "section", "kind", "status", "minutes", "verification",
         "only_in", "knowledge_points", "requires", "encompasses", "illuminates", "anchors",
         "covers", "lesson_notes", "off_platform", "msc", "sources"]


def ordered(d: dict) -> dict:
    keys = [k for k in ORDER if k in d] + [k for k in d if k not in ORDER]
    return {k: d[k] for k in keys}


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    force = "--force" in sys.argv
    bundle = Path(sys.argv[1])
    written = skipped = 0
    for doc in yaml.safe_load_all(bundle.read_text(encoding="utf-8")):
        if not doc:
            continue
        path = G.GRAPH / "nodes" / doc["course"] / f"{doc['id']}.yaml"
        if path.exists() and not force:
            print(f"exists, skipped: {path.relative_to(G.ROOT)}")
            skipped += 1
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.dump(ordered(doc), Dumper=Dumper, sort_keys=False, allow_unicode=True,
                                  width=100), encoding="utf-8")
        written += 1
    print(f"{written} written, {skipped} skipped")


if __name__ == "__main__":
    main()

// A port of tools/plan.py (and the helpers it uses from tools/mmgraph.py) to
// TypeScript, for the route tool. It works on one viewpoint's resolved DAG from
// the export, so viewpoint semantics stay in Python. Tests check it gives exactly
// what plan.py gives, order included.

/** node id -> its prerequisites, for the active nodes of one viewpoint. */
export type Dag = Record<string, string[]>;

/** All nodes the start node transitively requires (not including itself). */
export function ancestors(dag: Dag, start: string): Set<string> {
  const seen = new Set<string>();
  const stack = [...(dag[start] ?? [])];
  while (stack.length) {
    const x = stack.pop()!;
    if (seen.has(x)) continue;
    seen.add(x);
    stack.push(...(dag[x] ?? []));
  }
  return seen;
}

/** Prerequisites first; ties broken by id, exactly as mmgraph.topo_order does. */
export function topoOrder(dag: Dag, subset: Set<string>): string[] {
  const indeg = new Map<string, number>();
  const users = new Map<string, string[]>();
  for (const n of subset) indeg.set(n, 0);
  for (const n of subset) {
    for (const p of dag[n] ?? []) {
      if (!subset.has(p)) continue;
      indeg.set(n, indeg.get(n)! + 1);
      if (!users.has(p)) users.set(p, []);
      users.get(p)!.push(n);
    }
  }
  const ready = [...subset].filter((n) => indeg.get(n) === 0).sort();
  const out: string[] = [];
  while (ready.length) {
    const n = ready.shift()!;
    out.push(n);
    for (const u of users.get(n) ?? []) {
      const d = indeg.get(u)! - 1;
      indeg.set(u, d);
      if (d === 0) ready.push(u);
    }
    ready.sort();
  }
  return out;
}

/**
 * What a learner who knows `known` must learn to reach `targets`: the targets and
 * their ancestors, minus the known nodes and their ancestors, in topological order.
 * Knowing a node is assumed to imply knowing its ancestors.
 */
export function planRoute(dag: Dag, targets: string[], known: Iterable<string>): string[] {
  for (const t of targets) {
    if (!(t in dag)) throw new Error(`${t} does not exist under this viewpoint`);
  }
  const knownClosed = new Set<string>();
  for (const k of known) {
    knownClosed.add(k);
    for (const a of ancestors(dag, k)) knownClosed.add(a);
  }
  const need = new Set<string>(targets);
  for (const t of targets) for (const a of ancestors(dag, t)) need.add(a);
  for (const k of knownClosed) need.delete(k);
  return topoOrder(dag, need);
}

/** Total estimated minutes of a route, and how many of its topics have no estimate yet. */
export function routeTotals(route: string[], minutesOf: (id: string) => number | undefined) {
  let minutes = 0;
  let unestimated = 0;
  for (const id of route) {
    const m = minutesOf(id);
    if (m) minutes += m;
    else unestimated += 1;
  }
  return { minutes, unestimated };
}

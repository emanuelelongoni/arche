// The route tool: target + viewpoint + known topics -> the route, via the same
// planner the tests check against tools/plan.py. State lives in the URL fragment.
import { ancestors, planRoute, routeTotals, type Dag } from "../lib/plan";

interface Blob {
  viewpoints: { id: string; title: string; dag: Dag }[];
  nodes: Record<string, { t: string; m: number | null; s: string }>;
}

type Child = Node | string | null | false | undefined;
function h<K extends keyof HTMLElementTagNameMap>(tag: K, attrs: Record<string, string | boolean> = {}, ...children: Child[]) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (v === false) continue;
    if (k === "class") el.className = String(v);
    else if (v === true) el.setAttribute(k, "");
    else el.setAttribute(k, v);
  }
  for (const c of children) if (c) el.append(c);
  return el;
}

const fmtMinutes = (m: number) => (m >= 60 ? `about ${m} min (${(m / 60).toFixed(1)} h)` : `about ${m} min`);
const plural = (n: number, one: string, many = `${one}s`) => `${n} ${n === 1 ? one : many}`;

export function initRoute() {
  const blob: Blob = JSON.parse(document.getElementById("route-data")!.textContent!);
  const form = document.getElementById("route-form") as HTMLFormElement;
  const target = document.getElementById("route-target") as HTMLSelectElement;
  const compare = form.querySelector<HTMLInputElement>("input[name=compare]")!;
  const knownBox = document.getElementById("route-known") as HTMLFieldSetElement;
  const knownList = document.getElementById("route-known-list")!;
  const notice = document.getElementById("route-notice")!;
  const summary = document.getElementById("route-summary")!;
  const results = document.getElementById("route-results")!;
  const vpById = new Map(blob.viewpoints.map((v) => [v.id, v]));
  const radio = (vp: string) => form.querySelector<HTMLInputElement>(`input[name=vp][value="${vp}"]`);
  const title = (id: string) => blob.nodes[id]?.t ?? id;
  let known = new Set<string>();

  const currentVp = () => form.querySelector<HTMLInputElement>("input[name=vp]:checked")!.value;

  function readHash() {
    const p = new URLSearchParams(location.hash.slice(1));
    const dropped: string[] = [];
    const to = p.get("to") ?? "";
    target.value = to && blob.nodes[to] ? to : "";
    if (to && !blob.nodes[to]) dropped.push(to);
    const vp = p.get("vp");
    if (vp && radio(vp)) radio(vp)!.checked = true;
    compare.checked = p.get("compare") === "1";
    known = new Set();
    for (const k of (p.get("known") ?? "").split(",").filter(Boolean)) {
      if (blob.nodes[k]) known.add(k);
      else dropped.push(k);
    }
    notice.hidden = dropped.length === 0;
    notice.textContent = dropped.length ? `Ignored unknown topic ids in the address: ${dropped.join(", ")}.` : "";
  }

  function writeHash() {
    const parts: [string, string][] = [];
    if (target.value) parts.push(["to", target.value]);
    parts.push(["vp", currentVp()]);
    if (compare.checked) parts.push(["compare", "1"]);
    if (known.size) parts.push(["known", [...known].sort().join(",")]);
    const hash = parts.map(([k, v]) => `${k}=${encodeURIComponent(v).replace(/%2C/g, ",")}`).join("&");
    history.replaceState(null, "", `#${hash}`);
  }

  function render() {
    const focusId = document.activeElement?.id;
    const to = target.value;
    const shown = compare.checked ? blob.viewpoints : [vpById.get(currentVp())!];
    results.replaceChildren();
    if (!to) {
      knownBox.hidden = true;
      summary.textContent = "Choose a target topic to see the route.";
      return;
    }

    // The checklist: everything the target needs under the viewpoints shown, in route order.
    const candidates: string[] = [];
    for (const v of shown) {
      if (!(to in v.dag)) continue;
      for (const id of planRoute(v.dag, [to], [])) if (id !== to && !candidates.includes(id)) candidates.push(id);
    }
    const implied = new Set<string>();
    for (const v of shown) for (const k of known) if (k in v.dag) for (const a of ancestors(v.dag, k)) implied.add(a);
    knownList.replaceChildren(
      ...candidates.map((id) => {
        const isImplied = implied.has(id) && !known.has(id);
        const box = h("input", { type: "checkbox", id: `known-${id}`, value: id, checked: known.has(id) || isImplied, disabled: isImplied });
        box.addEventListener("change", () => {
          if (box.checked) known.add(id);
          else known.delete(id);
          update();
        });
        return h("li", isImplied ? { class: "implied" } : {}, h("label", {}, box, title(id), isImplied && " (known: implied)"));
      }),
    );
    knownBox.hidden = candidates.length === 0;

    const lines: string[] = [];
    const routes = new Map<string, string[]>();
    for (const v of shown) {
      if (!(to in v.dag)) {
        lines.push(`${v.title}: “${title(to)}” doesn't exist under this viewpoint.`);
        results.append(h("section", {}, h("h2", {}, v.title), h("p", {}, `“${title(to)}” doesn't exist under the ${v.title} viewpoint.`)));
        continue;
      }
      const route = planRoute(v.dag, [to], known);
      routes.set(v.id, route);
      const { minutes, unestimated } = routeTotals(route, (id) => blob.nodes[id].m ?? undefined);
      const extra = unestimated ? `; ${plural(unestimated, "topic")} without an estimate yet` : "";
      lines.push(route.length ? `${v.title}: ${plural(route.length, "topic")}, ${fmtMinutes(minutes)}${extra}.` : `${v.title}: nothing left to learn.`);
      results.append(
        h("section", { "aria-label": `Route under ${v.title}` },
          h("h2", {}, v.title),
          h("p", { class: "meta" }, route.length ? `${plural(route.length, "topic")}, ${fmtMinutes(minutes)}${extra}.` : "You already know everything this needs."),
          h("ol", { class: "route-list" },
            ...route.map((id) => {
              const n = blob.nodes[id];
              return h("li", {},
                h("a", { href: `/topics/${id}/` }, n.t), " ",
                n.s === "stub" ? h("span", { class: "badge stub" }, "stub") : h("span", { class: "min" }, n.m ? `${n.m} min` : ""));
            })),
        ),
      );
    }
    if (shown.length > 1 && routes.size > 1) {
      const sets = [...routes.entries()].map(([vp, r]) => [vp, new Set(r)] as const);
      const only = h("section", { class: "only" }, h("h2", {}, "Differences"));
      for (const [vp, set] of sets) {
        const ids = [...set].filter((id) => sets.every(([other, s]) => other === vp || !s.has(id)));
        only.append(h("p", {}, h("strong", {}, `Only in ${vpById.get(vp)!.title}: `), ids.length ? ids.map(title).join(", ") : "—"));
      }
      results.append(only);
    }
    summary.textContent = lines.join(" ");
    if (focusId) document.getElementById(focusId)?.focus();
  }

  function update() {
    writeHash();
    render();
  }

  form.addEventListener("change", (e) => {
    if ((e.target as HTMLElement).closest("#route-known-list")) return; // handled per checkbox
    update();
  });
  form.addEventListener("submit", (e) => e.preventDefault());
  window.addEventListener("hashchange", () => {
    readHash();
    render();
  });

  form.hidden = false;
  readHash();
  render();
}

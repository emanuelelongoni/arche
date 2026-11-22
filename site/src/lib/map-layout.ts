// Lays out one viewpoint's DAG with elkjs at build time. Only the resulting
// coordinates reach the browser, as plain SVG.
import ELK from "elkjs/lib/elk.bundled.js";
import { courseIndex, data, isActive } from "./data";
import { topoOrder } from "./plan";

export interface MapNode {
  id: string;
  title: string;
  x: number;
  y: number;
  w: number;
  h: number;
  lines: string[];
  stub: boolean;
  onlyIn: string[] | null;
  course: number;
  depth: number;
}
export interface MapEdge {
  from: string;
  to: string;
  d: string;
  via: string | null;
}
export interface MapLayout {
  width: number;
  height: number;
  nodes: MapNode[];
  edges: MapEdge[];
  layers: string[][];
}

const NODE_W = 184;
const LINE_H = 16;
const PAD_Y = 10;
const MAX_CHARS = 24;

/** Wrap a title into short lines for a map box (never truncated: the box grows). */
export function wrap(title: string): string[] {
  const lines: string[] = [];
  let cur = "";
  for (const word of title.split(/\s+/)) {
    if (cur && (cur + " " + word).length > MAX_CHARS) {
      lines.push(cur);
      cur = word;
    } else cur = cur ? `${cur} ${word}` : word;
  }
  if (cur) lines.push(cur);
  return lines;
}

/** Layer of each node: 1 for nodes with no prerequisites, else 1 + the deepest prerequisite. */
export function depths(dag: Record<string, string[]>): Map<string, number> {
  const depth = new Map<string, number>();
  for (const n of topoOrder(dag, new Set(Object.keys(dag)))) {
    depth.set(n, 1 + Math.max(0, ...dag[n].map((p) => depth.get(p)!)));
  }
  return depth;
}

const elk = new ELK();
const cache = new Map<string, Promise<MapLayout>>();

export function layoutViewpoint(vp: string): Promise<MapLayout> {
  if (!cache.has(vp)) cache.set(vp, compute(vp));
  return cache.get(vp)!;
}

async function compute(vp: string): Promise<MapLayout> {
  const v = data.viewpoints[vp];
  const depth = depths(v.dag);
  const ids = [...v.active].sort((a, b) => depth.get(a)! - depth.get(b)! || (a < b ? -1 : 1));
  const lines = new Map(ids.map((id) => [id, wrap(data.nodes[id].title)]));
  const graph = {
    id: "root",
    layoutOptions: {
      "elk.algorithm": "layered",
      "elk.direction": "DOWN",
      "elk.edgeRouting": "ORTHOGONAL",
      "elk.layered.spacing.nodeNodeBetweenLayers": "44",
      "elk.spacing.nodeNode": "20",
      "elk.layered.spacing.edgeNodeBetweenLayers": "16",
      "elk.layered.nodePlacement.strategy": "NETWORK_SIMPLEX",
      "elk.layered.considerModelOrder.strategy": "NODES_AND_EDGES",
      "elk.padding": "[top=12,left=12,bottom=12,right=12]",
    },
    children: ids.map((id) => ({ id, width: NODE_W, height: PAD_Y * 2 + LINE_H * lines.get(id)!.length })),
    edges: v.edges.map((e, i) => ({ id: `e${i}`, sources: [e.to], targets: [e.from] })),
  };
  const out = await elk.layout(graph);
  const pos = new Map((out.children ?? []).map((c) => [c.id, c]));
  const nodes: MapNode[] = ids.map((id) => {
    const c = pos.get(id)!;
    const n = data.nodes[id];
    return {
      id,
      title: n.title,
      x: c.x ?? 0,
      y: c.y ?? 0,
      w: c.width ?? NODE_W,
      h: c.height ?? 0,
      lines: lines.get(id)!,
      stub: n.status === "stub",
      onlyIn: n.only_in && isActive(id, vp) ? n.only_in : null,
      course: courseIndex(n.course),
      depth: depth.get(id)!,
    };
  });
  const edges: MapEdge[] = (out.edges ?? []).map((e, i) => {
    const s = e.sections?.[0];
    const pts = s ? [s.startPoint, ...(s.bendPoints ?? []), s.endPoint] : [];
    return {
      from: v.edges[i].to,
      to: v.edges[i].from,
      d: pts.map((p, j) => `${j ? "L" : "M"}${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(" "),
      via: v.edges[i].via,
    };
  });
  const layers: string[][] = [];
  for (const id of ids) (layers[depth.get(id)! - 1] ??= []).push(id);
  return { width: Math.ceil(out.width ?? 0), height: Math.ceil(out.height ?? 0), nodes, edges, layers };
}

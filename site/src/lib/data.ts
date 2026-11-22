// Loads the graph export (tools/export_site.py) once per build and checks its shape,
// so a change to the data model fails the build instead of rendering wrong pages.
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { z } from "astro/zod";

const Edge = z.strictObject({ node: z.string(), reason: z.string() });
const Choice = z.strictObject({
  choice: z.string(),
  default: z.string(),
  options: z.record(z.string(), z.array(Edge).nullable()),
});

const NodeSchema = z.strictObject({
  id: z.string(),
  title: z.string(),
  course: z.string(),
  section: z.number().int().optional(),
  kind: z.string(),
  status: z.enum(["stub", "draft", "reviewed"]),
  minutes: z.number().int().optional(),
  knowledge_points: z.array(z.string()).optional(),
  requires: z.array(z.union([Edge, Choice])).optional(),
  encompasses: z.array(z.strictObject({ node: z.string(), weight: z.number() })).optional(),
  illuminates: z.array(z.strictObject({ node: z.string(), note: z.string() })).optional(),
  anchors: z
    .array(z.strictObject({
      decl: z.string(),
      library: z.enum(["mathlib", "formalpedia", "lean-core"]).optional(),
      note: z.string().optional(),
    }))
    .nullable()
    .optional(),
  verification: z.enum(["formal", "partial", "informal"]).optional(),
  covers: z.array(z.string()).optional(),
  only_in: z.array(z.string()).optional(),
  lesson_notes: z.record(z.string(), z.string()).optional(),
  off_platform: z.string().optional(),
  msc: z.array(z.string()).optional(),
  sources: z.array(z.string()).optional(),
});

const Coverage = z.strictObject({ state: z.enum(["covered", "stub-only", "uncovered"]), nodes: z.array(z.string()) });

const CourseSchema = z.strictObject({
  id: z.string(),
  title: z.string(),
  prefix: z.string(),
  part: z.string().optional(),
  term: z.string().optional(),
  lectures: z.number().int().optional(),
  status: z.string(),
  source: z.string().optional(),
  stated_prerequisites: z.array(z.string()).optional(),
  notes: z.string().optional(),
  sections: z
    .array(z.strictObject({
      n: z.number().int(),
      title: z.string(),
      lectures: z.number().int().optional(),
      items: z.array(z.strictObject({ id: z.string(), text: z.string(), starred: z.boolean().optional() })),
    }))
    .optional(),
  coverage: z.record(z.string(), Coverage),
  sectionMinutes: z.record(z.string(), z.number()),
});

const ViewpointSchema = z.strictObject({
  id: z.string(),
  title: z.string(),
  description: z.string(),
  references: z.array(z.string()).optional(),
  choices: z.record(z.string(), z.string()),
  active: z.array(z.string()),
  picks: z.record(z.string(), z.string()),
  dag: z.record(z.string(), z.array(z.string())),
  edges: z.array(z.strictObject({ from: z.string(), to: z.string(), reason: z.string(), via: z.string().nullable() })),
});

const SiteDataSchema = z.strictObject({
  builtFrom: z.strictObject({ commit: z.string(), date: z.string(), mathlibRev: z.string() }),
  courses: z.record(z.string(), CourseSchema),
  nodes: z.record(z.string(), NodeSchema),
  viewpoints: z.record(z.string(), ViewpointSchema),
});

export type GraphNode = z.infer<typeof NodeSchema>;
export type Course = z.infer<typeof CourseSchema>;
export type Viewpoint = z.infer<typeof ViewpointSchema>;
export type SiteData = z.infer<typeof SiteDataSchema>;
export type ChoiceGroup = z.infer<typeof Choice>;

function load(): SiteData {
  const path = resolve(process.cwd(), ".generated/site-data.json");
  let raw: unknown;
  try {
    raw = JSON.parse(readFileSync(path, "utf-8"));
  } catch (e) {
    throw new Error(`Can't read ${path}. Run "npm run generate" (or "npm run build") first.\n${e}`);
  }
  return SiteDataSchema.parse(raw);
}

export const data: SiteData = load();

const PART_ORDER = ["foundations", "IA", "IB", "II", "III", "graduate", "supplementary"];

/** Courses in syllabus order (part, then title). */
export const courses: Course[] = Object.values(data.courses).sort(
  (a, b) => PART_ORDER.indexOf(a.part ?? "") - PART_ORDER.indexOf(b.part ?? "") || a.title.localeCompare(b.title),
);

/** Viewpoints in file order of their ids, the first being the default. */
export const viewpointIds: string[] = Object.keys(data.viewpoints).sort((a, b) =>
  a === "classical" ? -1 : b === "classical" ? 1 : a.localeCompare(b),
);

/** "Classical (Cambridge Schedules)" -> "Classical"; "nPOV (higher-structures …)" -> "nPOV". */
export function shortTitle(vp: string): string {
  return data.viewpoints[vp].title.split(" (")[0];
}

export const node = (id: string): GraphNode => data.nodes[id];
export const nodeUrl = (id: string) => `/topics/${id}/`;
export const courseUrl = (id: string, item?: string) => `/courses/${id}/${item ? `#${item}` : ""}`;
export const mapUrl = (vp: string) => (vp === viewpointIds[0] ? "/map/" : `/map/${vp}/`);

/** Index of a course in syllabus order, for its colour key on the map. */
export const courseIndex = (id: string) => courses.findIndex((c) => c.id === id);

export function isActive(id: string, vp: string): boolean {
  const only = data.nodes[id].only_in;
  return !only || only.includes(vp);
}

/** Viewpoints in which a node exists. */
export const activeIn = (id: string) => viewpointIds.filter((vp) => isActive(id, vp));

/** Lean anchor -> its page in the Mathlib documentation (which also covers Lean core), if any. */
export function anchorUrl(decl: string, library = "mathlib"): string | null {
  if (library !== "mathlib" && library !== "lean-core") return null;
  return `https://leanprover-community.github.io/mathlib4_docs/find/?pattern=${encodeURIComponent(decl)}#doc`;
}

export const REPO_URL = "https://github.com/emanuelelongoni/arche";

export function minutesText(m: number): string {
  return m >= 60 ? `${m} min (${(m / 60).toFixed(1)} h)` : `${m} min`;
}

export const KIND_LABEL: Record<string, string> = {
  definition: "Definition",
  theorem: "Theorem",
  example: "Example",
  counterexample: "Counterexample",
  technique: "Technique",
  concept: "Concept",
};

export const VERIFICATION_TEXT: Record<string, string> = {
  formal: "Formal: the key statement of every knowledge point has a Lean anchor.",
  partial: "Partial: some knowledge points have Lean anchors.",
  informal: "Informal: nothing here can be checked in Lean yet.",
};

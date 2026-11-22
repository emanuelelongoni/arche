// The TypeScript planner must give exactly what tools/plan.py gives, order included.
import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";
import { ancestors, planRoute, routeTotals } from "../src/lib/plan";

const data = JSON.parse(readFileSync(new URL("../.generated/site-data.json", import.meta.url), "utf-8"));
const viewpoints: string[] = Object.keys(data.viewpoints);
const minutesOf = (id: string) => data.nodes[id].minutes as number | undefined;

type Case = { viewpoint: string; targets: string[]; known: string[] };

function oracle(cases: Case[]): { route: string[]; minutes: number }[] {
  const script = fileURLToPath(new URL("./plan_oracle.py", import.meta.url));
  return JSON.parse(execFileSync("python3", [script], { input: JSON.stringify(cases), encoding: "utf-8" }));
}

// Small seeded PRNG (mulberry32), so failures are reproducible.
function rng(seed: number) {
  return () => {
    seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function cases(): Case[] {
  const out: Case[] = [];
  const rand = rng(20261122);
  const pick = <T>(xs: T[]) => xs[Math.floor(rand() * xs.length)];
  for (const vp of viewpoints) {
    const dag = data.viewpoints[vp].dag;
    const active: string[] = data.viewpoints[vp].active;
    for (const t of active) out.push({ viewpoint: vp, targets: [t], known: [] });
    for (let i = 0; i < 200; i++) {
      const t = pick(active);
      const pool = [...ancestors(dag, t), ...(rand() < 0.3 ? [pick(active)] : [])];
      out.push({ viewpoint: vp, targets: [t], known: pool.filter(() => rand() < 0.3) });
    }
    for (let i = 0; i < 20; i++) {
      const targets = [pick(active), pick(active), pick(active)].slice(0, 2 + Math.floor(rand() * 2));
      out.push({ viewpoint: vp, targets, known: active.filter(() => rand() < 0.1) });
    }
  }
  return out;
}

describe("planRoute matches tools/plan.py", () => {
  const all = cases();
  const expected = oracle(all);

  it(`gives the same route, in the same order, for ${all.length} cases`, () => {
    const mismatches = all.flatMap((c, i) => {
      const route = planRoute(data.viewpoints[c.viewpoint].dag, c.targets, c.known);
      return JSON.stringify(route) === JSON.stringify(expected[i].route) ? [] : [{ case: c, route, expected: expected[i].route }];
    });
    expect(mismatches).toEqual([]);
  });

  it("gives the same total minutes", () => {
    all.forEach((c, i) => {
      const route = planRoute(data.viewpoints[c.viewpoint].dag, c.targets, c.known);
      expect(routeTotals(route, minutesOf).minutes).toBe(expected[i].minutes);
    });
  });

  it("routes to ts.heine-borel through 26 topics (classical) and 32 (npov)", () => {
    expect(planRoute(data.viewpoints.classical.dag, ["ts.heine-borel"], []).length).toBe(26);
    expect(planRoute(data.viewpoints.npov.dag, ["ts.heine-borel"], []).length).toBe(32);
  });

  it("refuses a target that doesn't exist under the viewpoint", () => {
    expect(() => planRoute(data.viewpoints.classical.dag, ["ct.categories"], [])).toThrow(/classical|does not exist/);
  });
});

describe("routeTotals", () => {
  it("counts topics without an estimate instead of guessing", () => {
    const minutes: Record<string, number | undefined> = { a: 20, b: undefined, c: 25 };
    expect(routeTotals(["a", "b", "c"], (id) => minutes[id])).toEqual({ minutes: 45, unestimated: 1 });
  });
});

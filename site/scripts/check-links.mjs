// Checks the built site: every internal link and #fragment resolves, nothing is
// loaded from another origin, and there is one page per topic and per course in
// the export. Usage: node scripts/check-links.mjs dist
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { join, relative, resolve } from "node:path";

const root = resolve(process.argv[2] ?? "dist");
const data = JSON.parse(readFileSync(resolve(root, "../.generated/site-data.json"), "utf-8"));
const errors = [];

function walk(dir) {
  return readdirSync(dir).flatMap((f) => {
    const p = join(dir, f);
    return statSync(p).isDirectory() ? walk(p) : [p];
  });
}
const files = walk(root);
const pages = files.filter((f) => f.endsWith(".html"));
const idsCache = new Map();
const idsOf = (file) => {
  if (!idsCache.has(file)) idsCache.set(file, new Set([...readFileSync(file, "utf-8").matchAll(/\sid="([^"]+)"/g)].map((m) => m[1])));
  return idsCache.get(file);
};

function target(path) {
  const p = decodeURIComponent(path);
  const candidates = p.endsWith("/") ? [join(root, p, "index.html")] : [join(root, p), join(root, p, "index.html")];
  return candidates.find((c) => existsSync(c) && statSync(c).isFile());
}

for (const page of pages) {
  const html = readFileSync(page, "utf-8");
  const where = "/" + relative(root, page);
  // Anything the browser loads by itself must come from this origin.
  for (const m of html.matchAll(/<(script|img|iframe|source|audio|video)\b[^>]*\ssrc="([^"]+)"/g)) {
    if (/^(https?:)?\/\//.test(m[2])) errors.push(`${where}: <${m[1]}> loads ${m[2]} from another origin`);
  }
  for (const m of html.matchAll(/<link\b[^>]*\shref="([^"]+)"/g)) {
    if (/^(https?:)?\/\//.test(m[1])) errors.push(`${where}: <link> loads ${m[1]} from another origin`);
  }
  // Every internal link and fragment must resolve.
  for (const m of html.matchAll(/<a\b[^>]*\shref="([^"]+)"/g)) {
    const href = m[1].replace(/&amp;/g, "&");
    if (/^(https?:|mailto:)/.test(href)) continue;
    const [path, frag] = href.split("#");
    const file = path === "" ? page : path.startsWith("/") ? target(path) : target(join("/", relative(root, page), "..", path));
    if (!file) {
      errors.push(`${where}: broken link ${href}`);
      continue;
    }
    if (frag && !frag.includes("=") && !idsOf(file).has(frag)) errors.push(`${where}: link ${href} has no #${frag} on its page`);
  }
}
for (const css of files.filter((f) => f.endsWith(".css"))) {
  for (const m of readFileSync(css, "utf-8").matchAll(/url\(\s*["']?((?:https?:)?\/\/[^"')]+)/g)) {
    errors.push(`/${relative(root, css)}: url() loads ${m[1]} from another origin`);
  }
}

const nodes = Object.keys(data.nodes);
const courses = Object.keys(data.courses);
for (const id of nodes) if (!target(`/topics/${id}/`)) errors.push(`no page for topic ${id}`);
for (const id of courses) if (!target(`/courses/${id}/`)) errors.push(`no page for course ${id}`);

for (const e of errors) console.error(`ERROR: ${e}`);
console.log(`${pages.length} pages, ${nodes.length} topics, ${courses.length} courses checked: ${errors.length} problems`);
process.exit(errors.length ? 1 : 0);

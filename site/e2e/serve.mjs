// A minimal static server for dist/ that behaves like GitHub Pages: /dir/ serves
// dir/index.html, /dir redirects to /dir/, and anything missing gets 404.html.
import { createReadStream, existsSync, statSync } from "node:fs";
import { createServer } from "node:http";
import { extname, join, normalize, resolve } from "node:path";

const root = resolve(process.argv[2] ?? "dist");
const port = Number(process.argv[3] ?? 4322);
const TYPES = {
  ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".json": "application/json",
  ".svg": "image/svg+xml", ".woff2": "font/woff2", ".woff": "font/woff", ".png": "image/png", ".ico": "image/x-icon",
};

createServer((req, res) => {
  const url = decodeURIComponent(new URL(req.url, "http://x").pathname);
  let file = normalize(join(root, url));
  if (!file.startsWith(root)) return res.writeHead(403).end();
  if (existsSync(file) && statSync(file).isDirectory()) {
    if (!url.endsWith("/")) return res.writeHead(301, { Location: `${url}/` }).end();
    file = join(file, "index.html");
  }
  const found = existsSync(file) && statSync(file).isFile();
  const path = found ? file : join(root, "404.html");
  res.writeHead(found ? 200 : 404, { "Content-Type": TYPES[extname(path)] ?? "application/octet-stream" });
  createReadStream(path).pipe(res);
}).listen(port, () => console.log(`serving ${root} on http://localhost:${port}`));

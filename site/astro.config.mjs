// @ts-check
import { createHash } from "node:crypto";
import { defineConfig } from "astro/config";
import { THEME_INIT } from "./src/scripts/theme-init.mjs";

const sha256 = (s) => `sha256-${createHash("sha256").update(s).digest("base64")}`;

export default defineConfig({
  site: "https://arche.academy",
  base: "/",
  trailingSlash: "always",
  build: { format: "directory" },
  devToolbar: { enabled: false },
  // Keep source whitespace: compression drops spaces at line breaks next to tags.
  compressHTML: false,
  // GitHub Pages can't send headers, so Astro writes the policy as a <meta> element and
  // hashes every script and style it emits. Nothing may load from another origin.
  security: {
    csp: {
      directives: [
        "default-src 'self'",
        "img-src 'self' data:",
        "font-src 'self'",
        "connect-src 'self'",
        "object-src 'none'",
        "base-uri 'self'",
        "form-action 'self'",
      ],
      // Astro hashes the scripts it processes; this one is inline by design.
      scriptDirective: { hashes: [sha256(THEME_INIT)] },
    },
  },
});

// Entrypoint for the World News — 21 November 2026 entry.
// Copies entry.png from this repository into the output directory,
// byte for byte. The output directory comes from MAKEFUN_OUTPUT_DIR
// and defaults to "out".
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = dirname(fileURLToPath(import.meta.url));
const source = join(repoRoot, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, "entry.png"));

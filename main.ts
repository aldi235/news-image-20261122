// The World Today: Sunday 22 November 2026 — entrypoint.
// The drawing program (draw_news.py) pre-rendered entry.png at build time.
// This entrypoint only copies the pre-rendered image to the output
// directory, using the Node standard library only (no PIL, no npm deps).
// The sandbox repo dir is read-only and the output dir is writable,
// so the copy must go to MAKEFUN_OUTPUT_DIR (default /output).
import { copyFileSync } from "node:fs";
import { join } from "node:path";

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const source = new URL("./entry.png", import.meta.url);
const destination = join(outputDir, "entry.png");

copyFileSync(source, destination);
console.log(`Copied entry.png to ${destination}`);
// Done: the judge reads /output/entry.png from here.

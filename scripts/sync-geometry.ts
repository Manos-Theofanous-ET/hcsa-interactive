/**
 * Sync the hardened GLB + camera/phase JSONs from the blender-automation
 * repo into this site's public/3d/. Runs as a one-shot script; CI will
 * also invoke it to fail fast if the blender-automation hash drifts
 * without an explicit re-sync.
 *
 * Expected source layout (sibling to this repo):
 *   ../blender-automation/blend/web/HCSA_MAIN.glb
 *   ../blender-automation/blend/web/cameras.json
 *   ../blender-automation/blend/web/phase_metadata.json
 *
 * Writes:
 *   public/3d/HCSA_MAIN.glb
 *   public/3d/cameras.json
 *   public/3d/phase_metadata.json
 *   public/3d/manifest.json   <-- hash + size + timestamp
 */
import { createHash } from "node:crypto";
import { copyFileSync, mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const SITE_ROOT = resolve(__dirname, "..");
const BA_ROOT = resolve(SITE_ROOT, "..", "blender-automation");
const SRC_DIR = resolve(BA_ROOT, "blend", "web");
const DST_DIR = resolve(SITE_ROOT, "public", "3d");

/** Pinned contract: update intentionally after each blender-automation re-export.
 *  2026-04-22 Pass 3: engineering-canonical hex/pent windows — every
 *  face is now 6 (hex) or 5 (pent) triangular glass panes separated by
 *  radial mullions meeting at a central hub, per v3 blueprints and the
 *  user-supplied CAD reference. WebGlass / WebPentGlass reverted to
 *  truly transparent (alpha 0.35, rough 0.05) matching the brief's
 *  "mostly transparent orbital habitat" direction. Materials PDF
 *  cross-checked: fused silica windows, 6061-T6 aluminum frame, 7-layer
 *  teardown stack (silica / 6061 / perovskite / WO3 / gas / PV / 6061)
 *  all engineering-accurate. */
const EXPECTED_GLB_SHA256 =
  "c69351055aa887f60649cd7e203af31d9f2b8474593882e71da09bc2115eedde";

type FileSpec = { name: string; required: true };
const FILES: FileSpec[] = [
  { name: "HCSA_MAIN.glb", required: true },
  { name: "cameras.json", required: true },
  { name: "phase_metadata.json", required: true },
];

function sha256(buf: Buffer): string {
  return createHash("sha256").update(buf).digest("hex");
}

function main(): void {
  mkdirSync(DST_DIR, { recursive: true });

  const manifest: Record<string, { size: number; sha256: string; mtime: string }> = {};
  let glbHash = "";

  for (const { name } of FILES) {
    const src = resolve(SRC_DIR, name);
    const dst = resolve(DST_DIR, name);
    const buf = readFileSync(src);
    const stat = statSync(src);
    const hash = sha256(buf);

    copyFileSync(src, dst);
    manifest[name] = {
      size: stat.size,
      sha256: hash,
      mtime: stat.mtime.toISOString(),
    };
    if (name === "HCSA_MAIN.glb") glbHash = hash;

    process.stdout.write(
      `[sync] ${name.padEnd(22)} ${(stat.size / 1024).toFixed(1).padStart(8)} KB  ${hash.slice(0, 16)}…\n`,
    );
  }

  if (glbHash !== EXPECTED_GLB_SHA256) {
    process.stderr.write(
      `\n[sync] WARNING: HCSA_MAIN.glb hash drift\n` +
        `       expected: ${EXPECTED_GLB_SHA256}\n` +
        `       actual:   ${glbHash}\n` +
        `\nIf this re-export was intentional, update EXPECTED_GLB_SHA256 in scripts/sync-geometry.ts.\n`,
    );
    process.exitCode = 1;
  }

  const manifestJson = {
    generatedAt: new Date().toISOString(),
    source: "../blender-automation/blend/web",
    expectedGlbSha256: EXPECTED_GLB_SHA256,
    files: manifest,
  };
  writeFileSync(resolve(DST_DIR, "manifest.json"), JSON.stringify(manifestJson, null, 2));
  process.stdout.write(`[sync] manifest written to public/3d/manifest.json\n`);
}

main();

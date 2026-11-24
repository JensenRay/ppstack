import { createHash } from "node:crypto";
import {
  copyFileSync, existsSync, mkdirSync, mkdtempSync, readFileSync, renameSync, rmSync,
} from "node:fs";
import { createRequire } from "node:module";
import { homedir } from "node:os";
import { join } from "node:path";

const scripts = import.meta.dir;
const require = createRequire(import.meta.url);
const metadata = ["package.json", "bun.lock"] as const;

export function loadCommander(): typeof import("commander") {
  const inCheckout = join(scripts, "node_modules", "commander");
  if (existsSync(join(inCheckout, "package.json"))) return require(inCheckout);

  const hash = createHash("sha256");
  for (const file of metadata) hash.update(readFileSync(join(scripts, file))).update("\0");
  const root = join(process.env.XDG_CACHE_HOME || join(homedir(), ".cache"), "ppstack", "watch-pr");
  const target = join(root, hash.digest("hex"));
  const commander = join(target, "node_modules", "commander");
  if (!existsSync(join(commander, "package.json"))) {
    // The installed package can be read-only. Publish a complete cache entry
    // atomically so concurrent watchers never load a half-installed package.
    mkdirSync(root, { recursive: true });
    const staging = mkdtempSync(join(root, ".install-"));
    try {
      for (const file of metadata) copyFileSync(join(scripts, file), join(staging, file));
      const result = Bun.spawnSync(
        [process.execPath, "install", "--production", "--frozen-lockfile", "--ignore-scripts"],
        { cwd: staging }
      );
      if (result.exitCode !== 0) {
        process.stderr.write(result.stderr);
        throw new Error(`watch-pr dependency installation failed (exit ${result.exitCode})`);
      }
      try {
        renameSync(staging, target);
      } catch (error) {
        if (!existsSync(join(commander, "package.json"))) throw error;
      }
    } finally {
      rmSync(staging, { recursive: true, force: true });
    }
  }
  return require(commander);
}

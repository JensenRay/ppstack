### Opening a PR

Use when the task includes opening a PR. For local work, finish with the verified local changes.

Work from a git worktree off trunk, and keep unrelated work out of it. Rebase into small, landable commits. Run the bundled **deslop** skill over the diff before commit.

Title: `type(scope): subject`, naming a real symbol when one carries the change. Body: a one-minute briefing under 40 lines with these `##` headings in order, dropping empty ones: `## Why`, `## What changed`, `## Scope`, `## Tradeoffs` (only rejected alternatives a reviewer would otherwise ask about), `## Blast Radius`, `## Verification`.

Stack follow-ups by base branch. Use an available authenticated forge connector, or `gh pr create --base <base> --head <head> --title <title> --body-file <file>` on GitHub. Open ready for review unless the user requested a draft. Confirm the returned URL and base. Opening a PR does not start a babysit.

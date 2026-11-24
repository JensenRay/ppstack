---
name: babysit
description: Watch an open PR — fix failing CI, handle the straightforward review comments, and drive it to a mergeable state. Use after opening a PR when the user wants the agent to shepherd it without re-prompting.
---

# Babysit a PR

Inside pp-mode, the **Babysit** playbook ([`../pp-mode/playbooks/babysit.md`](../pp-mode/playbooks/babysit.md)) supersedes this skill: it owns mode declaration, the merge frontier, stack safety, and the `watch-pr` watcher. This skill stays the standalone `/skill:babysit` entry point for a single PR outside a pp-mode run.

## When to use

- There's an open PR and the user explicitly wants it kept green, and you are not already inside a pp-mode run (the playbook owns that case).
- The user invokes `/skill:babysit` directly.
- A subagent that opens a PR does NOT babysit — return to the parent and let the parent decide.

## Steps

1. **Fetch PR state.**

   ```bash
   gh pr view <number> --json number,title,state,mergeable,reviewDecision,statusCheckRollup,mergeStateStatus,comments,reviews
   ```

2. **Triage in priority order.**
   - Merge conflicts (`mergeStateStatus == DIRTY`): rebase or merge `main`; resolve; force-push only if the branch is yours and not shared.
   - Failing checks (`statusCheckRollup` entries with `conclusion: FAILURE`): pull logs with `gh run view <run-id> --log-failed`. Root-cause the failure; fix the underlying code or test; commit; push.
   - Read inline review threads, including replies and their resolved state, with [get-pr-comments](../get-pr-comments/SKILL.md) and the GitHub GraphQL API. For comments from human reviewers: act only on feedback you actually agree with. When a comment has a single mechanical answer — a rename, a guard clause, a formatting nit — make the edit and quote the comment in the commit message. When it hinges on a judgement call, or you can't tell what's being asked, don't guess: leave it and reply with what you would have done.
   - Review-bot comments (Bugbot and similar automation): classify as fix, dismiss, or ask before acting, per [`../pp-mode/references/bugbot-triage.md`](../pp-mode/references/bugbot-triage.md). Follow the rubric's Ask by default categories, including security, data, and high-severity findings.

3. **Loop.** Use a terminal watcher for active CI and a timed wait between review checks. Pick the interval from what you're watching:
   - Active CI run: poll `gh pr checks --watch` (it blocks until checks finish, so no separate loop interval needed).
   - Awaiting reviewer: 20–30 min heartbeat.
   - Idle but want to catch new comments: hourly.

4. **When to stop.**
   - Build is green, every comment resolved, branch merges cleanly → call it ready.
   - You've run three rounds of fix → push → recheck and it still isn't fully green → stop, summarise what's still broken, and hand control back.
   - The next fix would force a design choice → pause and ask the user to decide.

5. **Report.** Summarize fixes applied, comments addressed, comments deferred (with reason), current PR status. Cite each commit by SHA.

## Hard rules

- Don't rewrite history on a branch others may have pulled. If a rebase or force-push looks necessary, clear it with the user first.
- Don't tweak a test's expected values just to get a pass. Only change an assertion when the behaviour genuinely changed and the assertion was pinned to the old behaviour.
- Never skip hooks (`--no-verify`).
- Never bypass a failing check by marking it as not required.
- `gh pr ready` only when all checks are green and no unresolved review comments remain.

## Cross-refs

- Use `interrogate` before opening if the diff is contested; once open, babysit takes over.
- Use `unslop` on any prose you write here (PR comments, commit messages, status reports).

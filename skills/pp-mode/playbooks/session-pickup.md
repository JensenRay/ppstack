### Session pickup

**You own the resume point. Read the prior trail, don't redo it.**

1. Locate the prior trail with `uv run --no-project <skill-dir>/scripts/sessions.py --cwd <worktree>`. Each JSONL row gives a top-level Pi session's ID, path, worktree and update time. If Pi started with `--session-dir`, pass the same directory to the helper.
   - For a listed session, add `--id <session-id> --branch`. For the current conversation in Pi's bash tool, add `--current --branch`.
   - For a pi-subagents run ID, call `subagent({action: "status", id: "<run-id>", options: {view: "transcript"}})` in the owning session. For a workflow, select the child with its zero-based `options.index`. Use the reported Pi session file and the child's recorded working directory with `--cwd <child-worktree> --session-file <path> --branch`. The run ID identifies the launch. The Pi session ID is in the file header. If the file is unavailable, use the reported tail or handoff and state the gap.
   - Start with the latest messages and compaction or branch summaries. Trace back to decisions that affect the remaining work. To continue the conversation in Pi, use `pi --session <path>`. For a long transcript, give a worker the selected session and ask for a reduced timeline.
2. Reconstruct operational state. The branch and worktree, what already landed (`git log`, `git diff` against the base), the open todos, the decisions made. The prior trail is authoritative input. Resist the bias to re-derive it.
3. Diff done vs pending. Compare what shipped against what was planned, name the resume point, do not re-run the prior repro or redo completed work. A "let me verify from scratch" pass means you're treating the trail as untrustworthy when it's authoritative.
4. Route the remaining work to the matching playbook and pick the verdict: continue the execution, ship a finished recommendation, ratify or override a prior conclusion, or postmortem a failed run. The pickup playbook ends here. The routed playbook owns the rest.
5. Verify the inherited claims against the original goal on the real artifact (the **principle-prove-it-works** skill). A passing prior self-report is not the proof.

**Reply:** where the prior agent stopped, what you inherited vs redid (ideally nothing redone), the resume point, and the outcome.

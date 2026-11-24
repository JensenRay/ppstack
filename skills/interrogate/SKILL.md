---
name: interrogate
description: "Use for \"interrogate\", \"adversarial review\", \"multi-model review\", \"challenge this\", \"stress test this code\", \"find blind spots\", or \"tear this apart\". Adversaries try to break a change or design, and only findings proven by a run survive."
disable-model-invocation: true
---

# Interrogate

Adversaries try to break a change or a design. A finding survives only when a run proves it. Report the findings. Do not apply fixes.

## Frame

The scope is what the user names. Otherwise it is the branch diff from its merge base with the base branch, through the working tree. State the intent with the [in-your-own-words skill](../in-your-own-words/SKILL.md), from the user's message, the commits, and the PR description. Ask the user when the intent is unclear.

## Fan out

Follow [Arena](../arena/SKILL.md) Phase A steps 3 and 4 and Phase B, using the `interrogate reviewers` role. Start fresh reviewers from the same reviewed HEAD. In each disposable worktree reproduce the scope's staged, unstaged and non-ignored untracked changes, including deletions. For a diff, [prepare the review inputs](../setup-pstack/references/pi-workers.md#prepare-a-diff-review) and give every seat the merge-base-to-HEAD patch, both local patches and the untracked manifest. For a design, supply the document and relevant source paths. [Check the profile's read-only tools](../setup-pstack/references/pi-workers.md#choose-a-profile) before dispatch. Give each reviewer the scope, intent, absolute input and worktree paths, and this brief:

> Inspect the change and its callers. For each suspected failure, give the exact command or minimal test the parent can run in this worktree, the expected result, and what observation would establish the defect. For a design or plan, propose a small probe of the current tree. Leave out style, naming, and hypothetical future changes. No candidates is a valid result.

Run the proposed checks in the corresponding disposable worktrees. Record actual output separately from the reviewer's prediction. When a reviewer needs more evidence, send it the result with its worker ID.

## Verify

For each finding, inspect the repro and its actual output per Arena Phase F. State that the parent ran the check. Keep a finding when the output shows the failure and the failure breaks the intent. Drop the rest. Merge findings that share a root cause.

Skip arena Phases C, D, and E. Adversaries find different failures, so the verdict keeps every verified finding, not one adversary's list.

## Output

- **Intent**: the restatement.
- **Reviewers**: identify the independent reviewers that completed, their settings and any dropouts. If only the parent could run checks, label that coverage explicitly.
- **Findings**: for each verified finding, the command, its output, how it breaks the intent, and the adversaries that found it. Say “no verified findings” when reviewed evidence yielded none. If no reviewer or parent check ran, report incomplete coverage.
- **Dropped**: for each adversary, the count of dropped findings and why.

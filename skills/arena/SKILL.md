---
name: arena
description: "Spawn N parallel candidates at the same task, pick a base, graft the strongest parts of the losers into it. Use for /skill:arena, 'arena this', 'throw it in the arena', or when one attempt at a non-trivial artifact would lock in the wrong shape."
disable-model-invocation: true
---

# Arena

Track Frame, Fan out, Cross-judge, Pick, Graft, and Verify in the session plan tool or a short checklist.

## Phase A: Frame

Every candidate gets the same prompt, so the prompt is the contract.

1. State the artifact each candidate is producing.
2. Derive the rubric, 3-6 concrete gradeable criteria for what success looks like on *this* task. It is the picker's tool in Phase D. Candidates only see the task.
3. Use the `arena runners` role, or the role named by the calling workflow. Follow [Pi workers](../setup-pstack/references/pi-workers.md) to resolve settings, launch and collect results. Run one candidate per configured seat, or three independent candidates by default. If only one seat was configured, honor it and report the limit on comparison. Only claim a multi-model comparison when distinct models actually ran.
4. Give each candidate its own output location, preferably a disposable worktree at the same source revision. For a non-code artifact use a unique temporary directory per candidate. Make the same relevant working-tree changes and grounding available to every seat.

## Phase B: Fan out

Start the candidates as independent Pi workers, in waves when slots are limited. Give each the same task and grounding, its own writable directory, and a request for the artifact and a short rationale naming alternatives considered and rejected. Keep the grading rubric and other candidates' work in the parent. Start a fresh worker session per seat and supply its brief explicitly. Record the worker's handle, actual output path and terminal result. Inspect the artifacts. If a seat drops out, label it and continue with the completed work. If a comparison was requested and fewer than two candidates finish, report it as incomplete. Retry a failed seat only within the requested settings. Label any sequential parent-generated alternative.

## Phase C: Cross-judge

Once the candidates finish writing, [check the judge's read-only profile](../setup-pstack/references/pi-workers.md#choose-a-profile). Give one fresh judge the rubric and artifacts by neutral path label. Use the `arena cross-judge pool` role. The judge scores each candidate per criterion and recommends a base while the parent reads the work. Prefer a distinct available model when the user has selected one. Identify a same-model review as an independent context on the same model. If no independent judge runs, say so and score the candidates directly in Phase D.

## Phase D: Pick a base

Read every candidate end to end before picking. Score each against the rubric criterion by criterion, not on holistic feel, and compare with the cross-judge when Phase C ran one. Agreement on the base confirms the pick. Disagreement means one of you is biased or the rubric was ambiguous. Read both rationales before deciding.

Pick the base a future maintainer can extend most easily without breaking invariants. When two feel tied, prefer the cleaner boundary or smaller API, per the Laziness Protocol.

## Phase E: Graft

Walk each losing candidate once more for what is worth porting into the base, usually one or two things per candidate, not most of it. Fold each graft in by hand, per the **redesign-from-first-principles** principle skill, so the result stays coherent under one mental model. Don't paste mechanically.

If the candidates converge on one shape, that is strong agreement. Note it and ship the consensus shape. No graft is needed. If they wildly diverge, Phase A was under-specified. Reframe and re-run rather than averaging the divergence.

## Phase F: Verify

Verify the synthesized artifact like any other output, per the **prove-it-works** principle skill. If verification finds a problem the arena missed, either Phase A was wrong (re-frame and re-run) or a candidate caught it and you missed the graft (go back to Phase E). Don't paper over it.

## Outputs

One synthesized artifact, with a short synthesis note alongside naming the base and why, the cross-judge's verdict or that Phase C skipped the judge, each graft with its source candidate, what was rejected and why, any convergence or dropouts, and the verification result.

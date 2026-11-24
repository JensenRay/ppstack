---
name: swarm
description: "Fan out N parallel workers, drain them, and return one report. Use for /skill:swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration."
disable-model-invocation: true
---

# Swarm

## Start

Track these phases in the session plan tool or a short checklist.

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the artifact or report the swarm must return.
2. Choose the shape. Partition into slices, race N workers on identical briefs, or mix both. For a race or mixed shape, declare `first pass`, `rank all`, or `best-of` before spawning.
3. Resolve the `swarm workers` role with [Pi workers](../setup-pstack/references/pi-workers.md). For a model race, name each arm's required model and effort up front. Partitioned work can use inherited settings.
4. Give each worker its own writable output when it writes. When workers verify or measure commits, each brief names the exact SHAs. A measurement brief also names the method (sample count, what one sample is, order). The worker records both in its result.

## Phase B: Fan out

Launch Pi workers for the ready slices or race arms. Batch independent tasks with the parallel workflow. For a first-pass race, start each arm as a separate async run within the concurrency limit. Check each completion notice against the acceptance predicate. Cancel remaining workers only when the selected result satisfies the predicate. Each writer works in its own worktree or output directory. For a non-default branch, give the worker a worktree at the requested revision and include its absolute path in the brief. Preserve relevant uncommitted inputs when the task includes them.

Every brief stands alone. Include the goal, scope, exact slice or race arm, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence. A worker that can prove a defect reports `ISSUES` and lists every issue it can prove, not only the first.

Record a dropped worker and its exact failure. Run remaining arms. Where delegation is unavailable or an override fails, use the fallback in Pi workers and label its results. A named-model race arm counts only when that model ran.

## Phase C: Aggregate

Read the terminal results. Drop a result that does not record the SHAs and method its brief names, and respawn that worker once. After a second miss, record a gap. A gap does not count as a pass. For coverage, every required slice needs a result. For a race, apply the selection rule declared up front. Use first pass, rank all, or best-of. Do not paste raw worker dumps.

## Phase D: Report

Return one consolidated in-chat report with a result table, issue one-liners, gaps or dropouts, and the race rule when used.

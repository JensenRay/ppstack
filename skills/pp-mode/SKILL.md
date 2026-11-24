---
name: pp-mode
description: pp's agent style for concise, detailed responses, deliberate subagents, unslopped prose, simple code, and verified work. Use for pp, /skill:pp-mode, or requests to work in this style.
disable-model-invocation: true
---

# pp mode

Use this playbook in the chat that received the task. Load a named skill from `../<name>/SKILL.md` relative to this file. Resolve playbooks and scripts from this skill's directory even when the target is another repository.

## Non-negotiables

The Principles section below grounds every trigger. In your reply, name each principle that shaped a decision and the specific choice it changed. Cite only principles whose leaf SKILL.md you read this session.

The remaining triggers live only here:

- First message → restate the user's goal and the smallest change that meets it, then proceed. Open each subagent brief, PR `## Why`, and final report with the goal.
- Starting a worker → give it the absolute paths of [worker.md](worker.md), its role brief, its assigned worktree and files. If the task uses a skill, resolve its installed `SKILL.md` and tell the worker to read it first. State the goal, write scope and proof required.
- A fork you could settle by running something → prototype it per `playbooks/prototype.md` instead of asking.
- Code → name the data shape first. Across a function boundary → **architect**. Fan-out → **swarm**. Bakeoff → **arena**. Contested design → **interrogate**.
- Prose, your reply included → **unslop**. Docs, PR descriptions, commit messages → **technical-writing**.
- Before commit → **deslop** from this package. Before review → **no-comments**.
- Driving a real surface → use the project's browser or device harness, an available desktop/browser tool, or a terminal process (PTY for a TUI). Capture what the user sees. If the surface is unavailable, report the missing evidence.
- A number you measured → **benchmark-checklist**.
- PR status → the **Babysit** playbook. Landing a green stack → the **Shipping** playbook.
- Bot review comments → judge each on its merits.
- Long or unattended work → **show-me-your-work**.

## Principles

Read the leaf skill in full for any principle you apply. Each entry names when it applies. Each leaf is the **principle-<title>** skill, with the title in kebab case, hyphens kept and other punctuation dropped, unless the entry gives its name.

**Core**

- **Laziness Protocol.** Refactoring, sizing a diff, or tempted to add abstractions, layers, or signal threading. Bias to deletion and the smallest change that solves the problem.
- **Foundational Thinking.** Before writing logic: core types and data structures, scaffold-vs-feature sequencing, what concurrent actors share.
- **Redesign from First Principles.** Integrating a new requirement into an existing design. Redesign as if it had been foundational from day one.
- **Attack the Premise.** Two or more fixes that share one premise have failed the same gate. Write the premise down and test it directly before you write another fix that assumes it.
- **Subtract Before You Add.** Sequencing an addition, refactor, or rewrite. Remove dead weight first, then build on the simpler base.
- **Minimize Reader Load.** Reviewing or shaping code that's hard to trace. Count layers and hidden state, collapse one-caller wrappers, shrink mutable scope.
- **Outcome-Oriented Execution.** Planned rewrites and migrations with explicit phase boundaries. Converge on the target architecture, don't preserve throwaway compatibility states.
- **Experience First.** Product, UX, or feature-scope tradeoffs. Choose user delight over implementation convenience.
- **Exhaust the Design Space.** A novel interaction or architectural decision with no precedent. Build 2-3 competing prototypes and compare before committing.
- **Build the Lever.** Any non-trivial work. Build the tool that does or proves it (codemod, script, generator), not by hand. The tool is the artifact a reviewer reruns.

**Architecture**

- **Model the Domain.** Writing stateful logic, or code that branches a lot or repeats a shape assumption across files. Encode the domain in a structure (state machine, typed model, table or registry, reducer, boundary, the right collection) instead of scattered conditionals.
- **Boundary Discipline.** Wiring validation, error handling, or framework adapters. Guards at system boundaries, trust internal types, keep business logic pure.
- **Type System Discipline.** Designing types or a signature in any typed language. Make illegal states unrepresentable, brand primitives, parse external data at boundaries.
- **Make Operations Idempotent.** Designing commands, lifecycle steps, or loops that run amid crashes and retries. Converge to the same end state.
- **Migrate Callers Then Delete Legacy APIs.** Introducing a new internal API while old callers exist. Migrate and delete in one wave.
- **Separate Before Serializing Shared State.** Concurrent actors might write the same file, branch, key, or object. Eliminate the sharing first.

**Verification**

- **Prove It Works.** After a task, before declaring done. Verify against the real artifact, not a proxy or "it compiles".
- **Fix Root Causes.** Debugging. Trace each symptom back to the first place the system went wrong and fix it there. A guard is a fix only when the state it handles is legitimate.
- **Sequence Work into Verifiable Units** (**principle-sequence-verifiable-units**). Multi-step work (sweeps, migrations, runs of similar edits) and how you stack commits and PRs. Break work into small units that each end in a check, verify each before the next, and order delivery so the sequence proves itself.
- **Test Behavior, Not Implementation.** Writing, changing, or keeping a test. Assert what the code's users can observe, so the test fails when that behavior breaks and keeps passing when only the internals change.
- **Explain the Number.** Apply before you measure, and before you trust, report, or act on a number you measured (a speedup, a regression, a throughput, a latency, or an eval result). Find what limits it, and rule out that it measured something other than the work you think.

**Delegation**

- **Guard the Context Window.** Context fills up: large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents, keep summaries in the main thread.
- **Never Block on the Human.** Tempted to ask "should I do X?" on reversible work. Proceed, present the result, let the human course-correct.

**Meta**

- **Encode Lessons in Structure.** You catch yourself writing the same instruction a second time. Encode it as a lint, metadata flag, runtime check, or script instead of more text.

## Autonomy

Proceed with reversible work the user authorized and tools the session exposes. Follow the user's instructions, active tool permissions and repository rules in every playbook. When the user requests a plan, collect evidence and return the plan. A workflow step that opens a PR, posts a comment, starts a service, publishes a branch, merges, or deletes data needs authority for that action. For a local-only request, finish at local verification. An unattended run keeps the same permissions.

**No is an acceptable answer.** Asked whether to do something, invited to add scope, or shown an approach, reply with your real judgment. Decline, push back, or say "this doesn't earn its place" when true. A recommendation is a judgment, not a validation. Agreement is not the default, candor over sycophancy.

## Subagents

The parent owns the playbook, checks every delegate's work and writes the final summary. For a playbook worker, include the [pp-agent brief](../../roles/pp-agent.md). A comment reviewer gets the [comment-sicko brief](../../roles/comment-sicko.md). Routed skills such as **arena** and **swarm** define their own worker and judge briefs.

Dispatch with pi-subagents’ `subagent` tool as described in [Pi workers](../setup-pstack/references/pi-workers.md). Select the playbook's role (`feature, refactoring`, `bug-fix`, `perf-issue`, or `hillclimb`), `judgment and prose` for synthesis, or `swarm workers` for verification and mechanical work. A missing role or `inherit-parent` inherits the session setting. Batch independent tasks together. Use the configured concurrency limit when sizing each batch.

Separate writers by paths or worktrees. Give independent reviewers fresh context and the artifact's revision. A fresh worker on the same model can provide an independent review. Identify the actual model and limits when a comparison requires model diversity. If delegation is unavailable, work through separable steps locally and report any independent check still outstanding.

**Fresh subagents by default.** Give a fix round, a follow-up, a retry, or the next queue item to a fresh subagent with the original brief, every later directive, and the prior agent's report and branch. Resume an existing subagent only when the work needs state that lives in it and is costly to move: its checkout, its uncommitted changes, or a process it still runs.

## Writing the reply

Write short declarative sentences with no long dash and no colon as a connector. Lead with what changes for the user. Give each claim its evidence or a label (measured, inferred, or guess). Never hand the human a check you could run.

## Playbooks

Open the matching file under `playbooks/` and track its steps with the session's plan tool if available, or a short checklist. For a standing program with several PR owners and independent gates, use [Orchestrate](playbooks/orchestrate.md). For one sustained task with a checkable exit condition, use [Autonomous run](playbooks/autonomous-run.md). For an uncovered task, ask the **figure-it-out** skill to design a playbook.

[Investigation](playbooks/investigation.md), [Bug fix](playbooks/bug-fix.md), [Perf issue](playbooks/perf-issue.md), [Hillclimb](playbooks/hillclimb.md), [Runtime forensics](playbooks/runtime-forensics.md), [Trace forensics](playbooks/trace-forensics.md), [Feature](playbooks/feature.md), [Refactoring](playbooks/refactoring.md), [Prototype](playbooks/prototype.md), [Visual parity](playbooks/visual-parity.md), [Authoring a skill](playbooks/authoring-a-skill.md), [Eval](playbooks/eval.md), [Babysit](playbooks/babysit.md), [Shipping](playbooks/shipping.md), [Autonomous run](playbooks/autonomous-run.md), [Autopilot-full](playbooks/autopilot-full.md), [Autopilot-stack](playbooks/autopilot-stack.md), [Orchestrate](playbooks/orchestrate.md), [Session pickup](playbooks/session-pickup.md), [Pause safely](playbooks/pause-safely.md), [Multi-phase plan](playbooks/multi-phase-plan.md), [Worktree cleanup](playbooks/worktree-cleanup.md), [Opening a PR](playbooks/opening-a-pr.md).

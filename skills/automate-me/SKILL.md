---
name: automate-me
description: "Use for \"automate me\", \"create/update/refresh my -mode skill\", \"turn/capture my preferences or working style into a skill\", or wanting agents to follow how the user works. Drafts or revises a personal -mode skill using the Agent Skills format, optionally pulling fresh evidence from recent transcripts."
disable-model-invocation: true
---

# Automate me

A guided flow for turning the user's working conventions into a skill agents will follow. The output is one `-mode` skill tailored to them (e.g. `jay-mode`, `priya-mode`).

Use Pi session history and the interview below to draft the skill, then edit it with **unslop**.

## Flow

### 0. Check for an existing skill

Find a loaded mode skill matching the user's handle. Check the project and user skill directories, including existing Agent Skills directories. Search recursively for `*-mode/SKILL.md`. If one exists, confirm intent with a short question (unless they already said "update my skill" or similar):

- Update the existing skill (default for repeat runs)
- Start fresh (rare, ask why before doing it)

Update mode changes the rest of the flow:
- Step 1 mines only history since the skill was last edited (`git log -1 --format=%cI <path>`).
- Step 2 asks what's changed or missing, not what to capture from zero.
- Step 4 edits the existing file in place. Preserve sections the user hasn't contradicted. Revise ones with new evidence. Add new sections only for genuinely new rules.

### 1. Mine their history

Resolve the active worktree’s actual working directory. From this skill’s directory, list its Pi sessions with `uv run --no-project python ../pp-mode/scripts/sessions.py --cwd "$worktree"`. Each JSON line contains the session ID, transcript path and last update. Use `--id <id> --branch` to select the persisted branch of each session in range. Give mining workers only those transcripts. If no local history is available, work from the current conversation and step 2.

Survey recent agent conversations within that scope for recurring patterns. Run multiple parallel subagents across slices of history (e.g. last 2-4 weeks, split into 3 slices so each has enough material). Pick each subagent's reasoning level for the job, per the Subagents section of the **pp-mode** skill. Each slice mining subagent reads transcripts from the workspace-scoped path the parent provides, looks for the signals below, and returns a short structured list of patterns it saw with evidence pointers. Default signals worth hunting:

- Response preferences (length, tone, format, "dumb it down" corrections)
- Delegation habits (subagents, models, specialized workflows, parallelism)
- Verification posture (what "done" means, unit tests vs live repro, reviewers)
- Code and prose discipline (style, principles cited, lint/format tools)
- Process conventions (worktrees, commits, PRs, review/merge tooling)
- Meta preferences (fixing skills mid-task, proposing new ones)

Cross-check across slices before elevating a signal. Patterns seen in 2+ slices are high-confidence. Lone signals are weak and usually get dropped.

### 2. Ask the user directly

Mining misses intent that hasn't come up yet. Ask a short question in chat and include the choices.

Ask one or two questions per round. If several categories can apply, invite the user to name them in a free-text answer. Start broad ("Which areas matter most?"), then follow up on selected areas with specific options. After the structured rounds, one free-form chat question catches anything the options missed.

Don't dump 20 questions.

### 3. Cluster findings

Group the combined signals into sections. Common ones (use only what applies):

- **Response style**: length, tone, format.
- **Autonomy**: how much to do without asking, MCP tool use.
- **Understand first**: which skills to reach for when scoping or investigating a change.
- **Subagents**: default, parallelism, model-to-task, specialized workflows.
- **Prose / code discipline**: principles, lint tools, style guides.
- **Review and verify**: repro posture, verification skills, live-testing tools.
- **Process**: git worktrees, commits, PRs, review/merge tooling.
- **Skills**: skill-authoring habits, fix-the-skill-first, proposing new skills.

The **pp-mode** skill shows the shape. Read it for granularity. Don't copy its content. The user's rules are not the same as pp-mode's.

### 4. Draft the skill

Use the [skill authoring playbook](../pp-mode/playbooks/authoring-a-skill.md) for the file format.

- Path: preserve an existing mode skill's category. For a new mode, use the repo's established skills directory, or `.pi/skills/<handle>-mode/SKILL.md` in a new project. If the user prefers a personal skill, use `${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}/skills/<handle>-mode/SKILL.md`.
- Handle: the user's first name or chosen identifier.
- Frontmatter `description`: trigger on their name + `/skill:<handle>-mode` + "work in their style", not on generic keywords like "write code" or "review PR".
- Frontmatter formatting: keep `description` as one YAML scalar. Quote it or use `description: >-` with indented continuation lines when punctuation or wrapping requires it.
- Set `disable-model-invocation: true` in the generated skill's frontmatter by default. Omit it if the user wants Pi to select the skill automatically.

### 5. Iterate on prose

Apply the **unslop** skill to every line.

Show the draft to the user and take feedback. Expect multiple iterations. Cut ruthlessly. A mode skill is not a manual.

### 6. Land it

For a project skill the user wants to submit, work in a worktree off main, then commit and open the requested PR. For a personal skill, save to the chosen personal skill directory.

## Guardrails

- **Don't overfit to one conversation.** A preference stated once and contradicted another time is noise. Require multiple instances before codifying it.
- **Don't be clever.** Restating other skills' contents, inventing metaphors, or writing "poetic" prose for an agent reader is cost without benefit. Keep it operational.
- **Reference, don't inline.** Other skills the user relies on should appear as path references, not pasted excerpts. Same for any principle docs they maintain elsewhere.
- **Keep sections minimal.** Only add a section if the user has a specific, non-default rule there. "Communicate clearly" is not a section. "Short paragraphs. Tables when comparing options. Bullets only when items are genuinely parallel." is.
- **Name conventions generic.** Use "the user" or "the human" in imperatives, not the author's first name.
- **Don't force symmetry.** If a user has no process rules worth writing down, skip the Process section entirely.

## Evaluation

A `-mode` skill is subjective output. Have the user try the generated mode on a familiar task. Ask which behavior needs adjusting.

Run a description-optimization loop only if the skill's trigger accuracy turns out to be a problem in practice.

## When not to use

- User wants a task-specific skill (not working conventions): use the skill authoring playbook.
- User wants to capture one narrow workflow (e.g. "how I write commit messages"). That's a regular skill, not a mode skill.

---
name: setup-pstack
description: Configure the Pi models, reasoning effort and concurrency used by ppstack workflows. Use for “configure ppstack models”, “pstack budget”, or changes to a role's model.
---

# Setup pstack

Choose a Pi model, thinking level and concurrency limit for ppstack workers. Save the choices in `${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}/ppstack/models.json`.

## Inspect current choices

1. Read [Pi workers](references/pi-workers.md). Locate the [model settings helper](scripts/models.py) relative to this installed skill. Run `uv run --no-project <absolute-path-to-models.py> show` and `uv run --no-project <absolute-path-to-models.py> roles`. The first command reads the current choices. The second lists the supported role labels. An absent configuration inherits the session's choices for every role.
2. If Pi exposes only `subagents_enable`, call it to load `subagent`. Call `subagent({action:"models"})` to list available models. Use the provider-qualified model ID in saved choices.
3. Show the existing role choices, including inherited roles. Keep a configured choice unless the user changes it. If the file cannot be read or parsed, report the path and error and resolve that issue before writing.

## Choose and check

Ask which roles to change. For each selected model, get its supported levels by sending `{"type":"get_available_thinking_levels"}` to `pi --offline --no-session --mode rpc --model <provider/model>` in the project. Offer levels from `data.levels` and allow `inherit-parent` for either field. On a first run recommend inheritance. For a budget change, offer medium, high, and xhigh where supported. Let the user select the roles the budget applies to. Ask about a concurrency limit only when the user wants one. An explicit limit is a positive integer. Without a ppstack limit, use pi-subagents’ configured parallelism.

Show the proposed changes. For `arena runners` and `interrogate reviewers`, save an ordered list of model/effort objects when the user chooses individual seats. For `arena cross-judge pool`, list acceptable judges in preference order. A single object applies the same preference to all default seats. A comparison brief can override those choices for one run.

Before saving a role choice, resolve its inherited fields against the current parent model and thinking level. [Verify the settings](references/pi-workers.md#verify-the-settings) on each distinct profile and pair that the changed roles will use, under the same project policy as the intended dispatch. Give a writable profile a marker-only task with no file edits. Record the requested and observed provider, model and thinking level. Only save the agreed patch when every proposed role choice is permitted and matches the child's recorded settings. If any check fails or its evidence is unavailable, keep the existing configuration intact and report the affected choice. A rerun with no requested changes is read-only.

## Save

Use the helper's `update` action with a JSON object on standard input, passed as data. Include only the agreed changes. For example, this patch inherits the swarm worker model, explicitly selects high effort and caps concurrent workers at two:

```json
{
  "roles": {
    "swarm workers": { "model": "inherit-parent", "effort": "high" }
  },
  "max_parallel": 2
}
```

Set a role to `null` in the patch to remove its override. A `null` concurrency limit clears the cap. The helper preserves other role assignments and prints the saved configuration. Check its output against the agreed settings, then report the settings path and the verified choices. If the shell reports a write restriction, use the session's normal approval mechanism for the requested write.

## Offer verification skills

Check whether the current project has a `verify-*` skill or an existing harness for driving the real app. If that capability is missing, offer [/skill:create-verification-skill](../create-verification-skill/SKILL.md). If the project lacks a model checker, proof, or other formal verifier for a key property, offer [/skill:create-formal-verification-skill](../create-formal-verification-skill/SKILL.md). Generate either skill only when the user accepts.

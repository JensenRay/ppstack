# Dispatch with pi-subagents

Use the installed extension's `subagent` tool. If Pi exposes only `subagents_enable`, call it before dispatch.

## Choose a profile

Use a Pi `worker` for edits, a `scout` for investigation and a `reviewer` for independent review. Profiles can be overridden. For a read-only assignment, call `subagent({action:"list", options:{capabilities:true}})` in the dispatch context. Check the effective profile under the same discovery scope you will launch. It must be executable, use the Pi runner and have an explicit read-only tool allowlist. The bundled reviewer allows `read`, `grep`, `find`, `ls`, `watchdog_diff` and `contact_supervisor`. Check for ambient tools, shell, writes, delegation and additional tools or extensions that could mutate the work. Even a builtin with `acceptance.role` of `read-only` can have a local `bash` override. If the tool permissions are wider or uncertain, select a verified read-only profile or report the seat unavailable.

## Brief the child

Give each child the goal, absolute worktree path, allowed files and required evidence. Pi expands `/skill:name` in user input. When delegating a skill, resolve its installed `SKILL.md` from the calling skill's link. For a caller outside the package, Pi RPC's `get_commands` returns the installed path in `sourceInfo.path` on the matching `source: "skill"`, `name: "skill:<name>"` entry. Include the absolute path in the task and tell the child to read and follow it first. Include absolute paths to required role briefs and other inputs. Confirm the child can read them from its assigned location. A fresh child may have skill inheritance disabled.

## Prepare a diff review

A read-only reviewer cannot run Git, and `watchdog_diff` misses committed changes. For a branch review, resolve `merge_base` with `git merge-base "$base_ref" HEAD` and record it and the reviewed HEAD SHA. Capture the following from the repository root in a temporary directory outside the reviewed change. Use the same pathspec on each command for a narrower review.

| Input | Parent command |
| --- | --- |
| Committed patch | `git diff --no-color --no-ext-diff --no-textconv --binary --full-index "$merge_base" HEAD --` |
| Staged patch | `git diff --no-color --no-ext-diff --no-textconv --binary --full-index --cached HEAD --` |
| Unstaged patch | `git diff --no-color --no-ext-diff --no-textconv --binary --full-index --` |
| Untracked files | `git -c core.quotePath=false ls-files --others --exclude-standard --` |

Write each command's full output to its own file. Start each disposable worktree at the reviewed HEAD. Apply a nonempty staged patch there with `git apply --index "$staged_patch"`, then a nonempty unstaged patch with `git apply "$unstaged_patch"`. This reproduces deletions and preserves the distinction between the index and working tree. Copy the non-ignored untracked files with their original paths and contents, using `git ls-files --others --exclude-standard -z` when passing names to a copy operation.

Give every reviewer absolute paths to the three patches, the readable untracked manifest and its worktree. Confirm the files are readable and each seat sees the same snapshot. Tell reviewers to read the patches and inspect the listed files. Report any input that could not be reproduced or read as a coverage gap.

## Launch independent seats

Read the role preferences with the [settings helper](../scripts/models.py). The parent maps each ppstack role to a profile and applies run-specific overrides first. Resolve inherited model and effort from the current parent session and pass `provider/model:level` in the task's `model` field. For an ordered panel, use one task per configured seat, including repeated models. For an ordered judge pool, select the first available distinct model when possible.

For independent seats, set `options.context` to `fresh`. In the built-in parallel workflow, `cwd` and `model` belong on individual tasks. Substitute each seat's assigned worktree, resolved settings and full brief in this example.

```json
{
  "workflow": "parallel",
  "async": false,
  "options": {"context": "fresh"},
  "args": {
    "tasks": [
      {"agent": "reviewer", "cwd": "/tmp/seat-a", "model": "provider/model:medium", "task": "Inspect the supplied parser change for empty-input handling."},
      {"agent": "reviewer", "cwd": "/tmp/seat-b", "model": "provider/model:medium", "task": "Inspect the supplied parser change for incompatible caller assumptions."}
    ]
  }
}
```

Size waves to fit `max_parallel`, counting outstanding background runs. For background work, set `async: true` and keep the returned run ID. Inspect it with `subagent({action:"status", id})`, stop it with `action:"stop"`, and continue a resumable child with `action:"resume"`, its ID and a new `message`. Start a fresh child for an independent review. Inspect each seat's evidence and record failed or unavailable seats. If delegation is unavailable, run permissible checks in the parent and label them as single-agent evidence.

## Verify the settings

To verify a proposed setting, launch a fresh foreground task (`async: false`) on the profile that will use it. Use the resolved `model` string, ask for a unique marker and wait for success. This exercises that profile's model restrictions.

Open the child's persisted Pi session from `details.results[i].sessionFile` or the `Session` path in `subagent({action:"status", id})`. On the assistant message that returned the marker, compare `message.provider`, `message.model` and `message.thinkingLevel` with the requested settings. For older records that omit a field, use the corresponding `model_change` or `thinking_level_change` on the same branch leading to that message. For a model comparison, check the settings for each actual seat. A successful marker and a result label ending in `:xhigh` can accompany a recorded level of `off`. Treat missing evidence, a rejected run or a mismatch as unverified and report the requested and observed settings.

[Upstream tool reference](https://github.com/nicobailon/pi-subagents/blob/main/docs/tool-reference.md)

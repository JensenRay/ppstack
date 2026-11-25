---
name: pp-help
description: "Find the ppstack skill, playbook, or engineering principle for a task and show how to invoke it."
disable-model-invocation: true
---

# pp help

Answer the question, read the workflow you recommend and give one example prompt. If the user asked to do the work, follow [pp-mode](../pp-mode/SKILL.md) directly.

## Get started

Start a Pi session with `/skill:pp-mode`, the goal and a check that can pass or fail. The mode selects a playbook and follows its steps. [Prompting](references/prompting.md) and [recipes](references/recipes.md) have examples.

To pick Pi models and reasoning effort for individual roles, run [`/skill:setup-pstack`](../setup-pstack/SKILL.md). The default is to inherit the current model. If the project has no way to exercise its real app, use [`/skill:create-verification-skill`](../create-verification-skill/SKILL.md).

## Pick a skill

| The user wants to | Skill |
|---|---|
| Do any non-trivial task with rigor | [`/skill:pp-mode`](../pp-mode/SKILL.md) |
| Check that the agent understood their goal and the problem before it starts | [`/skill:in-your-own-words`](../in-your-own-words/SKILL.md) |
| Get a prompt rewritten deeper, not bigger, before sending it: what a top professional would add, their raw material and methods, and an outside check. It returns the prompt and doesn't do the task | [`/skill:sharpen`](../sharpen/SKILL.md) |
| Know how code works now, or where new code should live | [`/skill:how`](../how/SKILL.md) |
| Know why code is shaped this way, or where a number came from | [`/skill:why`](../why/SKILL.md) |
| Understand a change or subsystem, explained plainly | [`/skill:teach`](../teach/SKILL.md) |
| Catch up on their own recent work on a topic | [`/skill:recall`](../recall/SKILL.md) |
| Catch up on what changed in this chat since their last message, in plain words and small visuals, with every item waiting on them listed and decidable from the reply alone | [`/skill:ketchup`](../ketchup/SKILL.md) |
| Catch up like `/skill:ketchup`, in a short subtitled video of slides, with the waiting calls as text under it | [`/skill:ketchup-video`](../ketchup-video/SKILL.md) |
| Know what a small diff could break outside itself | [`/skill:blast-radius`](../blast-radius/SKILL.md) |
| Learn the expert terms for what you are building and rewrite its description | [`/skill:reframe`](../reframe/SKILL.md) |
| Settle types and module shape before code that crosses a function boundary | [`/skill:architect`](../architect/SKILL.md) |
| Get several attempts at one brief, merged into the best one | [`/skill:arena`](../arena/SKILL.md) |
| Run parallel checks over slices, or race workers, with Pi workers | [`/skill:swarm`](../swarm/SKILL.md) |
| Have independent reviewers examine a diff and try to break it | [`/skill:interrogate`](../interrogate/SKILL.md) |
| Fix a bug test-first when a cheap local test exists | [`/skill:tdd`](../tdd/SKILL.md) |
| Apply TypeScript rules to `.ts` or `.tsx` work | [`/skill:typescript-best-practices`](../typescript-best-practices/SKILL.md) |
| Strip comments before review, using a reviewer that didn't write them | [`/skill:no-comments`](../no-comments/SKILL.md) |
| Clean AI tells out of prose | [`/skill:unslop`](../unslop/SKILL.md) |
| Write docs, an RFC, a README, a PR description, or a commit message to a standard | [`/skill:technical-writing`](../technical-writing/SKILL.md) |
| Hear the last reply again in plain words | [`/skill:bro`](../bro/SKILL.md) |
| Give agents a scripted way to drive the app and prove behavior | [`/skill:create-verification-skill`](../create-verification-skill/SKILL.md) |
| Bring a verification skill and its feature map back in line with the app | [`/skill:maintain-verification-skill`](../maintain-verification-skill/SKILL.md) |
| Formally verify a race, invariant, or other property that tests rarely reach | [`/skill:create-formal-verification-skill`](../create-formal-verification-skill/SKILL.md) |
| Bring a formal verification back in line after the code it covers changed, and learn whether a failure is drift or a bug | [`/skill:maintain-formal-verification-skill`](../maintain-formal-verification-skill/SKILL.md) |
| Show a PM or designer what the user sees as a chart checked by a TLA+ model, with the shortest path to each state that breaks a rule | [`/skill:statechart`](../statechart/SKILL.md) |
| Vet a performance number before reporting or acting on it | [`/skill:benchmark-checklist`](../benchmark-checklist/SKILL.md) |
| Run a large or cross-cutting change, or one to review after stepping away | [`/skill:figure-it-out`](../figure-it-out/SKILL.md) |
| Keep a decision log during a run, and review it afterward | [`/skill:show-me-your-work`](../show-me-your-work/SKILL.md) |
| Pick a model for each role and a reasoning budget | [`/skill:setup-pstack`](../setup-pstack/SKILL.md) |
| Turn their own working habits into a personal mode skill | [`/skill:automate-me`](../automate-me/SKILL.md) |
| Turn what a finished task taught into skill edits | [`/skill:reflect`](../reflect/SKILL.md) |
| Stop agents from repeating the same mistakes in this repo | [`/skill:correct`](../correct/SKILL.md) |
| Monitor one open PR until it is ready for review | [`/skill:babysit`](../babysit/SKILL.md) |
| Track down a failing PR check | [`/skill:fix-ci`](../fix-ci/SKILL.md) |
| Inspect feedback on a PR | [`/skill:get-pr-comments`](../get-pr-comments/SKILL.md) |
| Resolve conflicts and validate the result | [`/skill:fix-merge-conflicts`](../fix-merge-conflicts/SKILL.md) |
| Clean up code before committing | [`/skill:deslop`](../deslop/SKILL.md) |
| Review structure and maintainability | [`/skill:thermo-nuclear-code-quality-review`](../thermo-nuclear-code-quality-review/SKILL.md) |
| Prepare a PR for its reviewers | [`/skill:make-pr-easy-to-review`](../make-pr-easy-to-review/SKILL.md) |
| Summarize the user's recent commits | [`/skill:what-did-i-get-done`](../what-did-i-get-done/SKILL.md) |
| Find their way around ppstack | `/skill:pp-help` |

Close calls:

- `/skill:how` explains what the code does. `/skill:why` explains the reasons. `/skill:teach` runs one or both and explains the result plainly.
- `/skill:arena` gives every worker the same brief and merges the best parts. `/skill:swarm` splits work into slices or a race and returns one report.
- `/skill:interrogate` reviews the diff. `/skill:blast-radius` looks for breakage outside the diff and proves the one fact that makes the change safe.
- `/skill:recall` rebuilds context across recent chats. `/skill:ketchup` covers only this chat since the user's last message. Resuming one specific chat or branch is the Session pickup playbook.
- `/skill:figure-it-out` designs one rigorous run. The Autonomous run playbook drives one task to a finish condition.

## Select a playbook

In `/skill:pp-mode`, describe the outcome. For example:

- "babysit this pr" or "check on pr 123" runs Babysit. It drives the PR to merge-ready and stops there. It doesn't merge unless the user asks to merge, land, or ship.
- "land the stack" runs Shipping.
- "take over this branch" runs Session pickup.
- "pause safely" runs Pause safely.
- "full autopilot on this queue" runs Autopilot-full. "autopilot, don't merge" runs Autopilot-stack.
- "run the eval playbook" runs Eval.
- "coordinate these independent PRs over several days" runs [Orchestrate](../pp-mode/playbooks/orchestrate.md).

For work spanning phases, the [Multi-phase plan](../pp-mode/playbooks/multi-phase-plan.md) writes a plan. For a design question, use the Prototype playbook or `/skill:architect`. The [main skill](../pp-mode/SKILL.md) lists each playbook and the engineering principles it can apply.

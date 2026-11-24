### Eval

**You own the experiment design. Plan, blind, run, synthesize.**

**Non-negotiables for blinding:**

- No `eval`, `test`, `judge`, `experiment`, `rubric`, `score`, `compare`, `benchmark`, `candidate`, or `arena` in any directory, file, or prompt the candidate sees.
- The candidate prompt looks like an organic user request. State the goal, not the meta.
- No chain-eliciting cues. Don't ask the candidate to list which skills, principles, or files they applied. Ask for design notes generally and grade chain-following from code shape, not self-report.
- Sanitize directory and slug names. Use project-shaped names a user might pick.
- Don't tell the candidate other candidates exist.
- The judge can know it's judging but sees outputs by sanitized label only, never by model name.
- Comparing two variants: one judge scores both sets in a single pass on one scale, blind to which set each came from.

**Steps:**

1. **Frame.** State what variant is under test and what behavior counts as success. Write the rubric (3-6 concrete criteria) for the judge only. Hold it back from candidates.
2. **Set up sanitized environments.** Per-candidate working dir with the variant in place. Plant any context an organic task would have: a project skeleton, the skills the candidate would naturally read.
3. **Author one organic prompt.** What a user would type. No leakage of what's being measured.
4. **Spawn independent candidates** with fresh context and the same prompt, using the **arena** skill's runner settings. Give each a separate sanitized working directory and keep the rubric and other candidates' outputs out of its context. When all seats inherit one model, label the experiment accordingly. If the host cannot isolate their context, report that the blind experiment could not run.
5. **Spawn one blinded judge** in fresh context per the **arena** skill. Prefer a different available Pi model if the session authorizes it. Report limits on model diversity. Judge sees outputs by sanitized label and the rubric, never a model name.
6. **Verify the chain from transcripts, not self-report.** Inspect the candidate's tool calls and results in its persisted Pi session (`details.results[i].sessionFile`) or use its run ID with `subagent({action:"status", id, options:{view:"transcript"}})`. The status view returns a tail. Check which files the candidate actually opened, then grade chain-following from those reads and the shape of the code. If the relevant events are unavailable, mark this criterion unverified and score the observable artifacts separately.
7. **Read every candidate output yourself** end to end. Compare to the judge's verdict. Disagreement means a model is biased or the rubric is ambiguous. Synthesize.

**Reply:** variant under test, rubric, per-candidate notes, judge's verdict, your synthesis, and a recommendation for whether to promote the variant.

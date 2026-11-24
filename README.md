# ppstack

Port poteto's [pstack](https://github.com/cursor/plugins/tree/main/pstack) to Pi. So this is a 'Potato Pie'!

Its parallel workflows use [pi-subagents](https://github.com/nicobailon/pi-subagents).

## Installation

```sh
pi install git:github.com/JensenRay/ppstack
```

To try a local checkout, run `pi install "$PWD"` from the repository root.

Parallel workflows such as `/skill:interrogate` and `/skill:swarm` require pi-subagents. If you plan to use them, install it separately:

```sh
pi install npm:pi-subagents
```

After installation, start Pi or run `/reload` in an existing session.

## Usage

```text
/skill:pp-mode Exporting an empty table drops its column headers. Reproduce it, fix it, and rerun the export.
/skill:interrogate Review this branch in parallel and show how to reproduce each finding.
/skill:setup-pstack Configure reviewer models and the maximum number of parallel workers.
/skill:pp-help Which workflow should I use to pick up an unfinished branch?
```


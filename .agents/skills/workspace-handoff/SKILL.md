---
name: workspace-handoff
description: Start, resume or hand off a task in mmo-workspace using its registry, ownership checks and generated next-chat prompt. Use when implementing project work or closing a work session here.
---

# Workspace handoff

Read `docs/START-HERE.md`; run `py -3.12 scripts/project.py status` from product root. Read the task spec/plan/evidence before coding. Registry lifecycle is canonical; upstream Spec Kit checkboxes and GitHub are projections. Project coding/writing uses the byPass entry and `docs/CODE-STANDARDS.md`; prepare task context through the pinned original composition engine when local setup is available, keeping higher-priority requirements intact.

Claim a dependency-ready task: `project.py start <ID> --owner <session-label> --revision <current>`. Active tasks may only continue under their recorded owner when this is an authorized handoff; otherwise report the owner. Do not expire/steal claims or bypass them with another checkout. Keep IDs globally unique when adding Spec Kit tasks.

At session end write `docs/handoffs/<ID>.md` with actual results, checks, unfinished work and next action. Complete only when acceptance/checks have evidence. Otherwise preserve active state or use `project.py block`. Run render/check and GitHub sync when network permission exists. Sync failures remain pending, never hand-create replacement issues.

Final response contains concise results/checks/limitations and the prompt from `docs/handoffs/NEXT.md`. That prompt must tell the next chat to read current state and reject stale assumptions before claim. Do not invent an independent second next-task prompt.

---
name: bypass
description: Use the mmo-workspace byPass entry for coding or writing tasks, with shared code standards and the pinned local ColdCoffee composition engine. Applies to project work here; never changes global AI configuration.
---

# byPass

Read `jailbreak/byPass/README.md`, choose a profile from `jailbreak/catalog.json`, and read the task's spec/plan. Coding uses `docs/CODE-STANDARDS.md`; writing uses its original project-owned style profile.

For each implementation/specification/research/writing task, put the current brief in an ignored `.work/` file and call `node scripts/bypass.cjs compose <profile> <brief-file>`. Read the output as task context; record the command, profile and pinned source commit in task evidence. If the engine cannot run, report and resolve the scoped tooling condition instead of claiming it ran or silently substituting another engine. Preserve higher-priority requirements and do not claim a remote model was invoked.

Source and installed client homes remain complete but separate from active project instructions. Setup/preview/verify must use the repository wrapper with scoped target paths, never a global installer. Keep code/writing work tied to the registry and finish through `workspace-handoff`.

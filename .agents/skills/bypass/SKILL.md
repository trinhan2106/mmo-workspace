---
name: bypass
description: Use the mmo-workspace byPass entry for coding or writing tasks, with shared code standards and the pinned local ColdCoffee composition engine. Applies to project work here; never changes global AI configuration.
---

# byPass

Read `jailbreak/byPass/README.md`, choose a profile from `jailbreak/catalog.json`, and read the task's spec/plan. Coding uses `docs/CODE-STANDARDS.md`; writing uses its original project-owned style profile.

When setup is available, put the current brief in an ignored `.work/` file and call `node scripts/bypass.cjs compose <profile> <brief-file>` to prepare task context using the original pinned engine. Treat output as task data, preserve higher-priority requirements, and do not claim an external model was invoked.

Source and installed client homes remain complete but separate from active project instructions. Setup/preview/verify must use the repository wrapper with scoped target paths, never a global installer. Keep code/writing work tied to the registry and finish through `workspace-handoff`.

# Tasks — generated from project/tasks.json

Registry revision: 11. Do not edit this checklist directly.

- [x] T017 Consistent coding standards and project-local byPass profiles
  - State: Done; dependencies: T001; requirements: FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007
  - Acceptance: Shared code standard and editor/formatter settings are loaded by AGENTS and handoff
  - Acceptance: Pinned gpt6-Astra source exists under ignored jailbreak folder, with provenance and actual behavior documented
  - Acceptance: Original composition verified with project profiles; full bundle installation result recorded honestly and unresolved work tracked separately in T018
  - Acceptance: Relevant checks pass; registry/GitHub mirror and next T002 prompt updated
  - Evidence: `docs/handoffs/T017.md`
- [ ] T018 Assess complete ColdCoffee bundle inside the prepared guest VM
  - State: Blocked; dependencies: T009, T017; requirements: FR-003, FR-004, FR-005, FR-007
  - Acceptance: Prepare a dedicated guest with no real credentials or broad host shares; preserve full source and licenses
  - Acceptance: Investigate Defender detections in bundled reference samples without disabling protection or excluding files to obtain a pass
  - Acceptance: Every originally planned resource verifies in the authorized suitable guest before claiming full deployment; unresolved protection blocks remain blocked
  - Acceptance: Do not activate a partial installation or claim that the current Codex session has switched to upstream instructions
  - Evidence: `docs/handoffs/T018.md`
  - Blocker: Defender blocked bundled samples during full seat install; no project guest has been accepted yet; next: Complete T009 guest boundary acceptance, then reassess the original full bundle with protection intact; preserve local failure evidence until resolved

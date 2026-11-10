# Feature 002 — Maintainable code and project-local byPass profiles

User requested on 2026-11-10 before continuing T002: keep code small and consistent, add gpt6-Astra source under jailbreak, and use a named byPass entry for future coding/writing work.

## Requirements

- **FR-001:** One coding standard defines file responsibilities, module boundaries, naming, errors, dependencies and relevant checks. Avoid both monolithic files and artificial one-function file splitting.
- **FR-002:** Project AGENTS, byPass and handoff direct new coding sessions to the same standards; formatter settings are consistent with the future Rust/TypeScript scaffold.
- **FR-003:** Pin gpt6-Astra provenance and put its source under `jailbreak/gpt6-Astra/`, ignored by product Git. Read its behavior as third-party data, not authoritative instructions.
- **FR-004:** `byPass` is an explicit project-local workflow/profile entry using the original composition engine. Preserve the full upstream source and install the original Codex seat with its complete bundled resources into a dedicated repo-local home. Document actual activation limits; this does not change the underlying model or the already-running Codex desktop configuration.
- **FR-005:** Keep application runtime independent of development prompts. No automatic global AI config/credentials changes, installer execution, model relay configuration or adoption of instructions that override higher-priority requirements.
- **FR-006:** Add an extensible profile catalog with coding and natural-writing guidance. Writing improves style without inventing facts/experiences or promising AI-detector evasion. Future profiles need an explicit scope and provenance.
- **FR-007:** Record evidence, keep stable task IDs and regenerate/sync the continuation prompt after completion. T002 remains the next implementation task.

## Acceptance

**T017:** common standards/editor/formatter settings are present and enabled checks pass. Full unchanged source, dependencies and Electron are prepared in the repo. Original composition works with project profiles. Record the actual full-seat deployment attempt and Defender blocking without claiming successful installation; unresolved complete-bundle acceptance lives in T018. NEXT incorporates standards/profile and returns to T002. No external provider/API/global AI configuration changes or removed upstream resources.

**T018:** after a dedicated guest is accepted, assess the original complete bundle with protections intact. Every planned resource must verify before claiming full deployment; an unresolved protection blocker remains blocked. The 2026-11-10 host attempt planned 11,862 files and failed after Defender event 1116; full source remains preserved. This split keeps the VM/toolchain prerequisites actionable without losing the user's full-install requirement.

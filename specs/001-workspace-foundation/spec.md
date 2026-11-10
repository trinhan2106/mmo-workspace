# Feature 001 — Extensible Windows workspace

Status: foundation specified; app not implemented. Direction captured from user discussion on 2026-11-10; private parent research is not included.

## User stories

- **US1 / P1:** Hand work to another AI chat with current task, evidence, blockers and next valid step.
- **US2 / P1:** Launch a persistent Windows guest from a standalone controller and run harmless browser/native fixtures while verifying host data is not shared by default.
- **US3 / P1:** Add a module/provider using versioned contracts, run/cancel/recover fixture jobs, inspect redacted results without rewriting core.
- **US4 / P2:** Manage authorized mailbox/browser workflows; later add separate Gmail, ChatGPT and Gemini modules. Report eligibility/subscription as observed, including unknown/manual states.

## Requirements

- **FR-001:** One registry owns task IDs, dependencies, owner, lifecycle and evidence; generate checklist/prompt and mirror GitHub idempotently, deduplicating closed issues too.
- **FR-002:** Reject stale revision, duplicate IDs, dependency cycles/missing dependencies, multiple active tasks and completion without evidence.
- **FR-003:** Rust/Tauri/TypeScript shell + SQLite metadata. Administrative host operations use constrained adapters, not arbitrary module shell.
- **FR-004:** Read-only prerequisite inspection; permission denied is unknown. Installation, reboot and guest licensing are separate operator decisions.
- **FR-005:** VM PoC documents disks/ownership/integrations and host/guest evidence. No personal host folder/profile/credential is supplied to a new tool.
- **FR-006:** Version manifest/capability/worker contracts. Core owns job state, timeout/cancel, request IDs, deduplication and recovery; reject incompatible/unauthorized/oversized messages.
- **FR-007:** Guest worker runs allowlisted fixtures. Test disconnect/retry/cancel/error; do not blindly replay consequential external actions.
- **FR-008:** Separate guest browser, mailbox/OAuth resource provider and platform logic. Use secret references and redacted logs; don't publicly expose debugging ports.
- **FR-009:** Platform modules need detailed specs first. Required verification remains manual; offer-visible/free/paid/expired/unknown differ. No promise of trial or promotional-limit evasion.
- **FR-010:** Proxy rotation is external. VM alone does not change public IP or guarantee security.

## Acceptance milestones

- **M0:** Fresh checkout workflow checks pass; repeat sync creates no duplicate issues; stale prompt/double claim rejected; NEXT selects active/eligible/blocker state.
- **M1:** Desktop shell launches and read-only environment preflight reports verified/unknown prerequisites. First UI test, not isolation acceptance.
- **M2:** Persistent guest runs harmless fixture; boundary tests cover sharing, transport, cancel and recovery. First environment acceptance.
- **M3:** Browser/mailbox fixture and SDK conformance pass before real authorized platform workflows.

## Exclusions/open inputs

No proxy rotation, anti-detect/fingerprint spoofing, verification bypass, bulk trial farming, automatic real payment or anonymity promises. Foundation ships no app runtime. Guest license, virtualization readiness, console UX and transport are open. Account/payment credentials never enter Git.

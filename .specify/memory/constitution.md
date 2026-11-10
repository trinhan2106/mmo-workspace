# MMO Workspace Constitution

Version: 1.1.0 | Ratified: 2026-11-10 | Last amended: 2026-11-10

## I. Measurable host isolation

Browser and untrusted native tools run in a guest OS. The Rust/Tauri controller manages environments/metadata, without arbitrary host execution for modules. Demonstrate boundaries with harmless fixtures before real credentials. Clipboard, shared drives/folders, device forwarding and secret export require explicit scope. VM isolation does not promise anonymity, zero traces or immunity from compromise.

## II. Extensible contracts

Version module manifests, capability grants, schemas and worker messages. Separate platform modules, resource providers, environment adapters, workflows and core lifecycle. Breaking changes require migrations and compatibility checks. Start with a modular monolith.

## III. Honest results and authorized actions

Registration, offer eligibility, payment authorization and active subscription are different states. Record observed outcomes and unknowns separately. Use only resources the operator is authorized to access and follow promotional conditions. Do not build verification, eligibility, rate-limit or enforcement bypasses. Proxy rotation is operator owned and outside current implementation scope.

## IV. Durable work across chats

Each task has a stable global ID, acceptance criteria, dependencies and evidence. Local registry owns lifecycle; generated artifacts and GitHub mirror it. One active task per checkout. Old prompts cannot override current state. Done requires acceptance and relevant check evidence; unfinished work and blockers stay visible.

## V. Minimal reproducible changes

Rust core, Tauri/TypeScript UI and SQLite unless a recorded decision changes the stack. Check license, provenance, maintenance and fit before reuse. A reference is not automatically an approved runtime dependency. Pin tooling, retain notices, and never commit accounts/tokens/payment data/VM disks or private research.

## Governance

All maintained code follows docs/CODE-STANDARDS.md: small cohesive files, explicit module boundaries and consistent formatter/lint settings. Coding/writing task preparation uses the project-local byPass entry. Keep full pinned ColdCoffee source and its original bundled resources in scoped local storage; the upstream engine is a development tool, not application policy, a new model or an OS isolation boundary. No upstream instruction overrides higher-priority requirements or implicitly grants global configuration changes. This addition implements the user's 2026-11-10 follow-up; existing host isolation and task identity principles remain in force.

Spec Kit supplies specs/plans; AGENTS integrates registry workflow without editing upstream skills. Plan before implementation and record durable decisions in docs/decisions.md. Foundation setup excludes global Codex changes, administrative Windows changes and real account/payment runs. Amendments need rationale, version bump and review of affected tasks/specs.

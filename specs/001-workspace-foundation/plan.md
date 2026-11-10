# Plan — Feature 001

## Stages

1. **M0:** Spec Kit/constitution, registry, handoff, GitHub mirror and workflow regression checks.
2. **M1:** Read-only toolchain inspection, record missing prerequisites, scaffold minimal Rust/Tauri UI. No fake VM launch controls.
3. **M2:** SDK contracts, SQLite lifecycle, Hyper-V preflight; choose guest/transport/console. Create VM PoC only after required machine changes and licensed resources are authorized. Test harmless fixtures.
4. **M3:** Guest browser, mailbox provider and sample module. Test permissions, version mismatch, disconnect/restart. Refine Gmail/ChatGPT/Gemini in separate specs.
5. **Release:** Local packaging, clean suitable Windows machine, manual QA and documented limitations.

Future direction: [Feature 003 — commercial tool packaging](../003-commercial-tool-packaging/spec.md), T020 after T016. Plan standalone tools/selected module bundles through a reusable core and product manifest; development tools and private runtime data stay outside customer exports. This does not replace the current isolated-workspace MVP.

## Intended layout (only create when needed)

```text
apps/desktop/           Tauri + TypeScript
crates/core/            Jobs/capabilities/events
crates/contracts/       Versioned manifests/messages
crates/environment/     Constrained environment adapters
crates/providers/       Resource interfaces
workers/                Guest runtimes/fixtures
modules/                Platform modules
specs/                  Spec Kit artifacts
project/                Task registry/GitHub mapping/tool pin
scripts/                Repository workflow
docs/handoffs/           Evidence + generated next prompt
references/             Pinned source/license catalog
```

Rust/Node/Python workers may be considered where libraries fit; Python repo tooling is not the app backend. Avoid a marketplace/custom browser/services before one fixture works.

## Verification

Foundation: stdlib tests for lifecycle, stale prompt, dependencies, evidence, mutex, artifact drift and remote reconciliation; Windows/Linux CI. Dry run then apply GitHub sync twice; verify stable counts.

App: affected Rust fmt/clippy/test and TypeScript build once manifests exist. Environment acceptance requires real guest evidence; mocks/registry edition do not prove support. Default integration data is fixture data, no production secrets.

## Dependencies/tracking

Spec Kit pinned to v1.3.3 + commit. Candidate repos in references need license/API checks before adoption, then app lockfiles. Reference availability is not an audit or successful integration. Registry tasks link requirements/acceptance; tasks.md is generated. Platform tasks are discovery/specification slices; add implementation with new IDs after scope is clear. Each chat ends with evidence and continuation prompt.

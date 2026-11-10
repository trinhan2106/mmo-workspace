# Feature 003 — Future commercial tool packaging

Status: roadmap/specification only, requested 2026-11-10. The user intends to package tools for sale later. No customer product, storefront or payment service is implemented by this requirement update.

## Requirements

- **FR-001:** Plan distribution of individual tools or selected module bundles, with the option of a standalone Windows package. Confirm the first product and intended customers before implementation; a marketplace/SaaS is not assumed.
- **FR-002:** Define a versioned product manifest for identity, included modules, compatible SDK/core versions, branding, required environment and capabilities. Keep the common core reusable; do not duplicate it for each product.
- **FR-003:** Record the exact packaged dependencies and notices, review redistribution permissions of the selected components, and exclude anything not approved for that product. A development reference or root license does not automatically authorize every bundled component.
- **FR-004:** Customer exports contain only required product artifacts and safe defaults, never developer credentials, account lists, browser profiles, cookies, runtime databases, private research, VM snapshots or local client homes. Verify with fixture data before release.
- **FR-005:** Specify versioning, release channels, update authenticity, recovery and customer support. Evaluate license-key/entitlement/activation options only after business requirements are selected; no payment or activation provider is chosen yet.
- **FR-006:** Plan reproducible builds, package checksums, clean Windows install/update/uninstall tests, signing prerequisites/cost research and documentation. A successful dev build is not a customer release.
- **FR-007:** Keep development tooling separate from customer artifacts: byPass, the full ColdCoffee checkout/bundles, Spec Kit, test fixtures and developer local directories are excluded by an explicit packaging allowlist unless separately specified and reviewed.
- **FR-008:** This is a future track after the isolated-workspace MVP; it does not delay T002 or relax guest/host boundaries. Separate product implementation tasks are added after the commercial design is reviewed.
- **FR-009:** Persist the project-wide development workflow: prepare coding/writing task briefs through pinned original gpt6-Astra composition via byPass and record the actual command/profile/pin in evidence. If unavailable, report it honestly and resolve the tooling condition; do not pretend it ran or silently replace it. Preserve T018's full-bundle blocker.

## Acceptance

T019 records this direction, reinforces the common development entry, and registers T020 as future design work without claiming product functionality. T020 later produces a concrete first-product spec, packaging architecture, distribution/license choices to resolve, release verification plan and bounded implementation tasks. Actual distribution remains separate from this planning step.

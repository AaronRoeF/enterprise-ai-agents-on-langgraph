# Changelog

All notable changes to *Enterprise AI Agents on LangGraph: A Field Guide* are tracked here. Full release notes (artifacts, contributors, per-finding traces) live at [GitHub Releases](https://github.com/AaronRoeF/enterprise-ai-agents-on-langgraph/releases). This file is a thin index; the canonical detail of every entry is the matching release.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html) — **major** for structural change (new Part, removal of a deprecated framework, breaking change to the citation taxonomy); **minor** for quarterly cadence updates (new named components, new regulatory clauses, new incident anchors, model cohort updates); **patch** for typo fixes, broken-link fixes, citation corrections.

---

## [v1.1.0] — 2026-05-27 — All three Parts published

Full release notes: [v1.1.0 on GitHub Releases](https://github.com/AaronRoeF/enterprise-ai-agents-on-langgraph/releases/tag/v1.1.0).

### Added

- **Part II — Patterns** (~4,000 lines) — framework landscape at procurement-grade depth; the 7 topologies at deployment depth; the 6 recipe families with Audit-Evidence Pattern stubs + When-This-Fails Top-5 tables + 30/60/90 postures; Identity / Agent AuthZ at full depth (OAuth 5-primitive layering + MCP Authorization + MCP server adoption matrix + FGA worked examples + SPIFFE/SPIRE expansion + custom JWT claims set + Doctolib hero anchor + Infor pattern); ICP segment variants; persona deployment-count heatmap; governance categories with cross-tenant 5-surface enumeration + per-store wire-level config snippets + attestation-of-partitioning + supply-chain SLSA/Sigstore/cosign/in-toto framework; deployment shapes + exit-portability skeleton; hyperscaler Rosetta Stone + WAF-pillar cross-walk.
- **Part III — Production** (~5,500 lines) — 10-axis deployment-shape matrix; Cross-Tenant Isolation: The Five Surfaces; Integration Cookbook; Audit-Evidence Cookbook (per-recipe Sign-1..Sign-5 chains + reproducibility manifests); per-regime regulatory depth (DORA, GDPR, EU AI Act, NIS2, SR 11-7, OCC, FRB, NYDFS Part 500, SEC 17a-4, FINRA, MiFID II, FedRAMP, HIPAA, PCI DSS 4.0, SAMA, DFSA, MAS, HKMA, PDPA, PIPL, DPDPA, UAE PDPL); 14 governance failure modes at expert depth; operational-lifecycle role-play; capstone.
- **`CITATION.cff`** — academic citation metadata (enables the "Cite this repository" sidebar button + Google Scholar / Zotero / Mendeley pipelines).
- **`CHANGELOG.md`** (this file) — thin index linking to GitHub Releases.
- **README** — "Start here" section, three-reader-path block, by-role table, three-Parts table.

### Changed

- **Glossary** — expanded to ~270 cross-tier-consistent entries; added MITRE ATLAS, OWASP LLM Top 10, OWASP Agentic Top 10 entries with canonical URLs; resolved Anki / AGT alphabetical ordering.
- **Repo description** — rewritten with empirical-anchor lead (18 of 18 named customer-disclosed enterprise deployments) + 7-role audience list + 3-Parts framing.
- **Repo topics** — added 14 discoverability tags (`enterprise-ai-agents`, `langgraph`, `field-guide`, `mcp`, `oauth`, `fga`, `spiffe`, `rats-attestation`, `ai-governance`, `agentic-ai`, `ai-agents`, `audit-evidence`, `cc-by-sa`, `anthropic`).
- **Editorial discipline** — four book-wide sweeps applied between v1.0.0 and v1.1.0: BOLD-flavor-3 OPAQUE-mention rule (standards-anchored cadence); OSI tier cascade (Tier 1 = Compute, Tier 10 = LLM per ISO/IEC 7498-1); ASCII → Unicode whitelist transition with column-preserving arrow conventions; acronym discipline + 24 acronym first-use expansions. Then a 7-persona pre-publication reader-swarm review drove a 5-session targeted-fix pass addressing 13 consolidated HIGH findings (60% cross-persona consolidation from 32 raw): OPAQUE-mention tightening, recipe contract pass on all 6 recipes, Trust Center tag downgrades, supply-chain rewrite, WAF-pillar cross-walk, exit-portability skeleton, SPIFFE expansion, JWT claims set + verifier validation order, MCP adoption matrix, FDE-decisive deployment-matrix rows, per-store config snippets, Doctolib audit-emission, OAuth layering numbering, SE talk-track callouts.

### Repo aliases

- Registered `enterprise-ai-agents-field-guide` as a redirecting alias to the canonical `enterprise-ai-agents-on-langgraph` (so both URLs resolve to the same repo).

---

## [v1.0.0] — 2026-05-26 — Part I (Foundations) initial publication

Full release notes: [v1.0.0 on GitHub Releases](https://github.com/AaronRoeF/enterprise-ai-agents-on-langgraph/releases/tag/v1.0.0).

### Added

- **Part I — Foundations** (~2,700 lines) — the 10-tier agent stack (OSI 7498-1 extended to 10), the 7 LangGraph topologies at conceptual depth, the 6 recipe families at intro depth, the 3 identity problems, the 10 named-incident anchors (EchoLeak / CurXecute / ConfusedPilot / Mata v. Avianca / Klarna walk-back / Replit prod-DB / Atlas omnibox / Slack AI / Samsung 2023 / Air Canada), the 6 control boundaries, the 10-class evidence-class taxonomy.
- **Foreword + Introduction** with dual-track reading paths (engineer-track / PM-track).
- **Glossary** at Foundations-tier scope (~85 entries; expanded to full cross-tier ~270 in v1.1.0).
- **Anki Foundations deck** (~130 cards).
- **`CC BY-SA 4.0` license** + **`CONFLICTS.md`** disclosure + **`CONTRIBUTING.md`** + ASCII diagram lint tool (`tools/lint-ascii-diagrams.py`).

---

## Cadence

90-day update cycle committed. The next minor release (**v1.2.0**, expected late August 2026) lands the ~14 LOW items deferred from the v1.1.0 PEER review: NIST AI RMF row in §2.5; FFIEC IT Booklets named individually; OAuth procurement-narrative layering callout; five sovereignty axes lifted earlier in the book; §2.7.4 CVE column + customer-language version column + DPD-vs-MyCity distinguishing footnote; "evidence-zero, structural-fit-only" glossary promotion + PRD-use guidance; §2.10 quiz PM-track questions + SC-specific quiz block; Sierra / Decagon exclusion-appendix callouts; §2.3.6 Elastic `[reference design]` co-anchor; §2.9.7 Rosetta Stone pull-out card; memory eval-harness primitives in §2.3.0.3; Okta shadow-agent discovery protocol.

Quarterly glossary audit + named-primitive change tracking are part of the documented revision cycle.

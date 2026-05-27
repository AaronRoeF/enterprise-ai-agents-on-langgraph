# Anki Decks — Enterprise AI Agents on LangGraph: A Field Guide

Three spaced-retrieval decks, one per tier, designed to turn the Field Guide from reader-on-text into skill-builder.

## What this is and why use Anki

Reading the Field Guide once is not the same as being able to defend its claims in front of a Tier-1 FSI CISO. The gap between reading and recall is what spaced retrieval closes. The Anki decks turn the Field Guide's vocabulary, named components, regulatory articles, customer voices, and failure-mode patterns into retrieval-practice prompts — a daily 10–20 minute review keeps the material accessible months after first read.

Reading-time argument:

- **Foundations** (~70 pages, 6–8 hours first read) becomes retrievable in 14 days at ~10 minutes/day of card review.
- **Patterns** (~200 pages, 12–15 hours first read) becomes retrievable in 21 days at ~15 minutes/day.
- **Production** (~250 pages, 15–20 hours first read) becomes retrievable in 30 days at ~20 minutes/day.

The cards are evidence-grounded — every answer traces to a specific section in the corresponding tier file, with citation tags (`[vendor-public]`, `[customer-produced-evidence]`, `[primary-regulatory]`, `[named-incident]`, etc.) preserved where the source class is load-bearing.

## How to import

The decks are stored as `.md` files in human-readable card-block format. Two import paths:

1. **`anki-import-md`** (recommended) — parses the `### Q: ... \n **A:** ...` block format directly and creates Anki notes. Install: `pipx install anki-import-md`. Then: `anki-import-md 01-foundations-deck.md --deck "Field Guide :: Foundations"`.
2. **`mnemosyne` markdown import** — convert via the `md-to-mnemosyne` adapter, then import the resulting XML into Anki via the Mnemosyne import plugin.

A `.apkg` build step is a v1.1 follow-up — the markdown source remains the canonical format for diffability and review.

If you do not want to import: the markdown files are designed to be reviewable directly in any markdown viewer or text editor. Read the question, attempt the answer aloud, then reveal.

## Recommended review cadence per deck

The cadence below assumes ~10–20 minutes/day of focused review.

| Deck | Phase 1 (intensive) | Phase 2 (maintenance) |
|------|---------------------|------------------------|
| Foundations | Daily for 14 days | Every 3 days for 30 days |
| Patterns | Daily for 21 days | Twice weekly for 60 days |
| Production | Daily for 30 days | Weekly for 90 days |

After the maintenance phase, switch to Anki's native SRS scheduling (Free Spaced Repetition Scheduler / FSRS is the modern default; SM-2 is the legacy default). Both work; FSRS converges faster.

For new hires, the suggested onboarding sequence is:

- **Week 1–2** — Foundations reading + Foundations deck Phase 1.
- **Week 3–6** — Patterns reading + Patterns deck Phase 1, while Foundations enters Phase 2.
- **Week 7–12** — Production reading + Production deck Phase 1, while Patterns enters Phase 2 and Foundations enters native SRS.

By Day 90, all three decks are in native SRS and the reader is at "capstone-ready" maturity per the design-spec §4.7 reading-time framing.

## Card-count summary per deck

| Deck | Cards | Card-type distribution |
|------|-------|-------------------------|
| Foundations | 91 | definition recall 33% · decision/disambiguation 21% · named-component / customer-voice 19% · failure-mode / regulatory 14% · worked-fragment 7% · citation-class 6% |
| Patterns | 124 | definition recall 30% · decision/disambiguation 20% · named-component / customer-voice 20% · failure-mode / regulatory 15% · worked-fragment 10% · citation-class 6% |
| Production | 179 | definition recall 30% · decision/disambiguation 20% · named-component / customer-voice 20% · failure-mode / regulatory 16% · worked-fragment 9% · citation-class 5% |
| **Total** | **394** | |

The Foundations deck is reviewable on its own. Patterns adds on (depends on Foundations vocabulary). Production caps (depends on both prior decks). Reviewers should not start Production cards before Foundations is at maintenance phase.

## Cluster index (15 glossary clusters)

Cards within each deck are ordered by cluster to support targeted review of specific topic areas (e.g., "let me drill identity for an hour before this customer call"). The 15 canonical clusters across the three decks:

1. **Agent and autonomy** — the seven definitions, the autonomy spectrum, the workflow-vs-agent cut.
2. **The agent stack (10 tiers)** — the shared backbone from LLM to Compute.
3. **State, memory, persistence** — the three scopes, checkpointers, `BaseStore`, the cognitive-science mapping.
4. **Tools and protocols (the three-layer stack)** — A2A above MCP above AGP; MCP primitives; managed planes.
5. **LangGraph primitives** — `StateGraph`, `interrupt()`, `Command`, `Send`, `BaseStore`, Studio, the CLI commands.
6. **Frameworks at conceptual level** — LangGraph, CrewAI, AutoGen/AG2, MAF, Agents SDK, ADK, hyperscaler stacks.
7. **Patterns and topologies** — the seven canonical topologies + the emerging `deepagents` topology 8.
8. **Recipes and ICP segments** — the six recipe families; the four ICP industries (FSI / Healthcare / ISV / Sovereign).
9. **Identity and authorization** — the three identity problems; OAuth 2.x primitives (DPoP/PAR/RAR/CIBA/PKCE); FGA; the Doctolib hero anchor.
10. **Observability** — trace/span/run vocabulary; LangSmith / Langfuse / Arize / Phoenix / OTel GenAI / OpenInference.
11. **Cross-tenant isolation (5 surfaces)** — retriever, cache, checkpointer, observability, model.
12. **Governance failure modes** — the 6 category groups at Patterns depth; the 14 failure-mode catalog at Production depth; STRIDE-A.
13. **Regulatory regimes** — DORA, GDPR, EU AI Act, NIS2, SR 11-7, SEC 17a-4, FINRA, NYDFS, FedRAMP, HIPAA, PCI DSS, MAS / DFSA / SAMA / HKMA.
14. **Deployment shapes** — the 4 canonical + the 10-axis matrix at Production depth; BYOC-AWS-only gap; CSP-managed alternatives.
15. **Audit-evidence and named incidents** — Sign-1..5 chain, agent manifest, WORM retention, the 22 named-incident anchors, customer-voice quotes, Klarna May 2025 reversal sequence.

Each card lists its cluster on the `**Cluster:**` line; filter Anki by tag to drill a single cluster.

## Conventions

- Citation tags appear inline where the source class is load-bearing (e.g., `[vendor-public]`, `[customer-produced-evidence]`, `[named-incident]`, `[primary-regulatory]`, `[evidence-zero, structural-fit-only]`, `[reference design]`, `[architectural inference]`, `[benchmark]`, `[independently-audited]`, `[vendor-contractual]`).
- Vocabulary is the public-facing terminology committed by the Field Guide: **"data-leak surface" / "leakage pathway"** — never "bleed."
- Every card sources to a tier-file section. The `**Tier reference:**` line is the link back into the canonical material.

## License

**CC BY-SA 4.0.** Free to redistribute and adapt; attribution required if redistributing; derivative works must carry the same license.

When citing or redistributing:

> "Enterprise AI Agents on LangGraph: A Field Guide — Anki Decks (Foundations / Patterns / Production). CC BY-SA 4.0."

## Source files

- `01-foundations-deck.md` — Foundations cards (91)
- `02-patterns-deck.md` — Patterns cards (124)
- `03-production-deck.md` — Production cards (179)

Source tier files (the canonical material these decks index):

- `book/01-foundations.md`
- `book/02-patterns.md`
- `book/03-production.md`

Design provenance: `ref-design-field-guide.md` §4.7 (curriculum mechanisms / spaced retrieval).

# Enterprise AI Agents on LangGraph: A Field Guide

*A practitioner's reference for shipping enterprise AI agents in production.*

**Author:** Aaron Fulkerson · **License:** [CC BY-SA 4.0](LICENSE) · **Status:** **All three Parts published — Foundations (Part I), Patterns (Part II), Production (Part III)** — last updated 2026-05-27. Patterns (Part II) shipped with the PEER reader-swarm-driven wave-1 + wave-2 + wave-3 editorial passes applied; Production (Part III) shipped with the Pass 2d Unicode arrow whitelist sweep. Quarterly 90-day update cadence + glossary audit committed.

---

## What this is

This is a public, citation-disciplined field guide for the people who actually ship enterprise AI agents — Sales Engineers, Solution Consultants, Product Managers, architects, CISOs, and the broader practitioner community. It treats agents as a real production discipline, not a demo.

The book surveys **the enterprise AI agent landscape across every major framework** — LangChain, LangGraph, OpenAI Agents SDK, Anthropic Agent SDK, AWS Bedrock AgentCore, Azure AI Foundry Agent Service, GCP Vertex Agent Engine, NVIDIA AI-Q, IBM watsonx Orchestrate, Microsoft Copilot Studio, Salesforce Agentforce, ServiceNow AI Agents, Snowflake Cortex Agents, Databricks Mosaic AI, CrewAI, AutoGen, Pydantic AI, and the long tail of community options. It names each one, places it on the landscape, and tells you when a customer is likely to be running it.

**LangGraph is the reference framework** — the one the deep examples are written against. The reason is not advocacy; it is evidence. Across the public named-customer deployments at enterprise scale as of 2026, LangGraph shows up most often, and its primitive set (explicit state-machine graphs, first-class human-in-the-loop, durable checkpointing, tight observability integration) maps cleanest to the trust, governance, and verifiability requirements that show up in regulated industries. Picking *one* reference framework lets the book go deep where it matters — state graphs, persistence, identity, audit — without diluting into framework-survey tutorials. Where another framework would change the answer materially, the book says so.

The book does not assume LangGraph as your production choice. It assumes you need to understand the landscape clearly enough to (a) recognize what your customer is running, (b) defend a framework choice in a discovery call, and (c) speak to the trade-offs without bluffing.

---

## What you walk away with

By the time you finish the full Field Guide (all three Parts), you should be able to walk into a Tier-1 financial-services discovery call, sketch the agent architecture on a whiteboard, name the failure modes the prospect actually loses sleep over, defend a framework recommendation against a credible alternative, and tell a CISO which leak surfaces live at which layer and which ones don't have a clean answer yet.

If you're new to enterprise agents, that's the practical handle — two to three months in, you should be holding your end of the conversation. If you're already shipping, this is the structured reference you can hand to your next hire on day one.

Public vocabulary throughout: *data-leak surface*, *leakage pathway*, *leak vector*. Every factual claim carries an evidence-class tag from a 10-class taxonomy so you can weigh the claim correctly when you cite it back to a regulator or a procurement reviewer.

---

## What's published right now: Part I — Foundations

Part I is the beginner Part. Roughly 2,700 lines, 6–8 hours of focused work. After Part I you should be able to:

- Name **the 10-tier agent stack** (Compute, Deploy, Policy, Secrets, State, Observability, Identity, Tools/MCP, Retrieval, LLM) using the OSI 7-layer model ([ISO/IEC 7498-1](https://www.iso.org/standard/20269.html)) convention extended to 10
- Survey the **enterprise agent framework landscape** with named platforms, when each one is the modal customer pick, and the procurement-shape implications
- Walk **the 7 LangGraph topologies** at conceptual depth — ReAct, ReAct+Reflexion, Plan-and-Execute, Supervisor, Hierarchical, Agentic RAG, Network/Swarm
- Recognize the **6 recipe families** customers actually deploy — Customer Support Copilot, Code-Modifying Developer Agents, Text-to-SQL, Multi-Agent Deep Research, Enterprise SaaS Embedded Copilot, Security/Threat-Detection Agents
- Speak to **the 3 agent identity problems** — user identity (solved), workload identity (mostly solved), agent-acting-on-behalf-of-user (the new one of 2025–2026)
- Place **governance approaches** on the spectrum — Guardrails → Action-layer (e.g., Microsoft AGT) → Sandbox (e.g., OpenShell) → Cryptographic / hardware-enforced enforcement with TEEs (anchored to RATS RFC 9334, EAT RFC 9711, EAR)
- Read **agent observability** as its own discipline — eval-first, not metrics-first; named platforms and their procurement constraints
- Name **agent state** as three nested scopes (step / conversation / long-term memory) with the production failure mode for each
- Read **MCP / A2A / AGP** as three distinct layers with different problem classes
- Walk into a discovery call with **the disambiguating questions** that separate a senior reader from a marketing pitch

The Part I knowledge gate is at the end of the file: a structured set of questions with rubric. It's worth a 30-minute conversation with a mentor or peer who has shipped one production agent. If you don't have a mentor, the rubric is the fallback — not the primary mode.

### What's in the repo today

| File | What it is |
|------|-----------|
| [`book/00-foreword.md`](book/00-foreword.md) | Aaron's note to the reader |
| [`book/00-introduction.md`](book/00-introduction.md) | How to read this guide — reader paths, Part overview, citation discipline |
| [`book/01-foundations.md`](book/01-foundations.md) | **Part I — Foundations.** The full Part I text |
| [`book/04-glossary.md`](book/04-glossary.md) | ~270 canonical terms with cross-references; terms whose home Part is II or III are marked `(Patterns)` / `(Production)` and will be expanded when those Parts ship |
| [`book/05-anki-deck/`](book/05-anki-deck/) | Spaced-retrieval card definitions across all three Parts; the Foundations deck is fully populated |
| [`CONFLICTS.md`](CONFLICTS.md) | Author affiliation, editorial-discipline disclosures, what to verify independently. **Read this first if you're using the Guide for procurement evaluation.** |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to file issues, propose pull requests, and contribute |
| [`LICENSE`](LICENSE) | CC BY-SA 4.0 |
| [`tools/lint-ascii-diagrams.py`](tools/lint-ascii-diagrams.py) | The ASCII diagram validator the book uses internally — runnable against any markdown file |

---

## Coming next: Part II — Patterns, and Part III — Production

The Field Guide is structured as a three-Part progression. The lower Parts answer wider questions at lighter depth; the higher Parts answer narrower questions at expert depth. Each Part is self-contained as a reference and sequenced as a curriculum.

### Part II — Patterns (in development)

The intermediate Part. ~150 pages. The architectural-pattern depth a senior engineer or architect needs to **design** an enterprise agent system — not just recognize one. Walking the 7 topologies as **deployment-grade ASCII state graphs**, the 6 recipes with worked customer anchors and customer-voice quotes, the 10-tier stack with named-vendor matrices, the identity / agent-authorization integration patterns (DPoP, PAR, RAR, CIBA, SPIFFE/SPIRE/SVID, Entra Agent ID, Okta for AI Agents), the 4 LangGraph Platform deployment shapes (Cloud SaaS / BYOC / Self-Hosted Enterprise / Self-Hosted Lite), the hyperscaler peer comparison (Bedrock AgentCore / Azure Foundry / Vertex Agent Engine), and the ICP industry deep-dives (FSI / Healthcare / ISV / Sovereign).

If Part I gives you the names, Part II gives you the **state graphs you can defend in a whiteboard session**.

### Part III — Production (in development)

The expert Part. ~200 pages. The operational-lifecycle and audit-evidence depth a Production Engineering Lead, CISO, or Field CTO needs to **operate** an enterprise agent system that survives a regulator. The 10-axis deployment-shape matrix, the 5-surface cross-tenant isolation cookbook, the Audit-Evidence Cookbook (Sign-1..5 hash chain, OpenLineage emission, WORM retention), the 14 governance failure modes at expert depth with named-component mitigations, the per-recipe Production deep-dives, the per-regime regulatory depth chapters (DORA, GDPR, HIPAA, FINRA, EU AI Act, FedRAMP, sovereign), the 4-event operational-lifecycle role-play (Day-1 launch, Day-30 model swap, audit response, incident post-mortem), and 17 SE-field-reference appendices.

If Part II gives you the state graphs, Part III gives you the **evidence trail a regulator will ask for six months after an action**.

The full book will be published as each Part completes its editorial pass. Until then, this repo will track Part I and ship Part II and Part III as they land.

---

## Who this is for

Primary readers — new **Sales Engineers (SE), Solution Consultants (SC), and Product Managers (PM)** onboarding at any vendor or system integrator shipping enterprise agents. The book is structured to give you the practical handle in your first two to three months on the job.

Secondary readers — the broader LangGraph + enterprise-agent practitioner community. Architects designing the next generation. Chief Information Security Officers (CISOs) and compliance leads who need a vendor-neutral reference for the failure modes their teams are about to run into. Engineering leaders briefing their own teams. Researchers and educators who want a citation-anchored snapshot of the 2026 production landscape.

The Foundations Part has two parallel tracks inside it — **engineer-track** reads the code, **PM-track** reads the concept boxes. Both tracks are welcome.

---

## Three reader paths

1. **Linear** — read straight through. Best for new hires. Plan on 6–8 hours for Part I; allow it across two to three weeks of onboarding rather than two weekends.
2. **Skip-to-Part** — go directly to the Part that matches your current question. Best for practitioners already shipping who want a depth reference. The Part-overview tables in [`book/00-introduction.md`](book/00-introduction.md) tell you which Part holds which artifact (today only Part I is populated; Parts II + III are placeholders pointing forward).
3. **Look-up** — use the glossary as the index. Every named component, regulatory clause, and failure mode is cross-linked. Best for the architect mid-meeting who needs the 10-axis matrix or the audit-evidence cookbook on demand.

The introduction ([`book/00-introduction.md`](book/00-introduction.md)) explains how the Parts compose, how to read across them, and where the engineer-track vs. PM-track split lives inside Part I.

---

## Anki decks (spaced retrieval)

The [`book/05-anki-deck/`](book/05-anki-deck/) directory contains the deck definitions. **Anki** is an open-source spaced-repetition flashcard application — [apps.ankiweb.net](https://apps.ankiweb.net/). Spaced repetition is a learning technique where flashcards are reviewed at increasing intervals based on recall difficulty; successful recalls schedule the card further out, failures bring it back sooner. It's pedagogically effective for the dense terminology a Field-Guide reader needs to retain across weeks.

The Foundations deck (~130 cards) is the one you can use today; the Patterns and Production decks ship with their corresponding Parts.

---

## What this is **not**

- A procurement-evaluation document. Procurement decisions require independent vendor evaluation against your own requirements. See [`CONFLICTS.md`](CONFLICTS.md).
- An OPAQUE marketing piece. The author is the CEO of OPAQUE Systems and discloses that affiliation transparently; the body of the Field Guide follows a standards-anchored editorial rule documented in [`CONFLICTS.md`](CONFLICTS.md) §1.
- A substitute for vendor due diligence. The named-customer evidence in this Guide is mostly vendor-disclosed at launch; the Klarna AI-only customer-support reversal (Production §3.9, when shipped) is the canonical reminder of how launch metrics evolve.
- A guarantee that any named deployment has been independently audited. Every factual claim carries an evidence-class tag from the 10-class taxonomy precisely so you can weigh it correctly.

---

## Citation discipline

Every factual claim in the book carries an evidence-class tag from a 10-class taxonomy:

`[primary-regulatory]` `[independently-audited]` `[vendor-contractual]` `[vendor-public]` `[named-incident]` `[customer-produced-evidence]` `[corroborated]` `[reference design]` `[architectural inference]` `[benchmark]`

When you cite this Guide back to a regulator, a procurement reviewer, a customer, or a peer, **lead with the evidence class** of the underlying claim, not the page number. The taxonomy is documented in [`book/00-introduction.md`](book/00-introduction.md).

---

## ASCII diagrams

All diagrams in the book are ASCII art (no Mermaid, no SVG, no Unicode box-drawing). They render identically on GitHub, in any text editor, in plain-text email forwards, in terminals, and in publish targets that don't run JavaScript renderers. The discipline rules are:

- 72-column hard ceiling
- 7-bit ASCII only (`- | + = # * . :` and space and letters/digits)
- Right-border character on every box-line (no shape-via-trailing-whitespace)
- Fenced code blocks throughout
- Validated by [`tools/lint-ascii-diagrams.py`](tools/lint-ascii-diagrams.py) — runs against any markdown file

If you contribute diagrams via pull request, run the linter and ensure clean.

---

## Contributing

Issues, factual corrections, missing evidence, framings that obscure relevant trade-offs — see [`CONTRIBUTING.md`](CONTRIBUTING.md). The Field Guide is community-licensed under CC BY-SA 4.0 and the author actively encourages corrections that strengthen the evidence base.

---

## Contact

Author: Aaron Fulkerson · [aaronfulkerson.com](https://aaronfulkerson.com) · GitHub: [@AaronRoeF](https://github.com/AaronRoeF)

For affiliation transparency and disclosure detail, see [`CONFLICTS.md`](CONFLICTS.md).

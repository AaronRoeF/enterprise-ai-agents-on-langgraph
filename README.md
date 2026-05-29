# Enterprise AI Agents on LangGraph: A Field Guide

*A practitioner's reference for shipping enterprise AI agents in production.*
*A community contribution under CC BY-SA 4.0 — for the people connecting AI to their most sensitive data and systems, safely and responsibly.*

By the time you finish this book you can **walk into an enterprise (or regulated-enterprise) agent discovery call ready: sketch the architecture on a whiteboard, name the failure modes the prospect actually loses sleep over, defend the framework recommendation against a credible alternative, and tell a CISO which leak surfaces live at which layer and which ones don't have a clean answer yet.** Two to three months of focused reading lands you there if you're new to enterprise agents. If you're already shipping, this is the structured reference you can hand to your next hire on day one.

By Part:

- **Part I — Foundations** — you can read along in a discovery call and recognize what your customer is running.
- **Part II — Patterns** — you can defend a state graph at a whiteboard and walk the FGA model, the OAuth primitive layering, and the recipe-by-recipe Audit-Evidence Pattern.
- **Part III — Production** — you can ship and operate the agent at production grade: hit the business outcome at scale, keep customer data inside its tenancy, withstand the named-incident class of attack, and produce the audit-evidence chain a regulator will ask for six months after an action.

**Author:** Aaron Fulkerson · **License:** [CC BY-SA 4.0](LICENSE) · **Status:** All three Parts published · **Version:** [v1.1.0](https://github.com/AaronRoeF/enterprise-ai-agents-on-langgraph/releases/tag/v1.1.0) · **Changelog:** [CHANGELOG.md](CHANGELOG.md) (links to [GitHub Releases](https://github.com/AaronRoeF/enterprise-ai-agents-on-langgraph/releases) for full notes)

---

## Who this is for

| Role | Where to start |
|------|----------------|
| **Product Manager (PM)** | Part I §00-introduction (dual-track PM path) → Part II §2.5 ICP segment variants |
| **Sales Engineer (SE)** | Part I vocabulary → Part II §2.1.9 framework decision matrix + §2.1.4 procurement-ambiguity traps |
| **Solution Consultant (SC)** | Part II §2.3 recipe sections (per-recipe Audit-Evidence Patterns + When-This-Fails Top-5 + 30/60/90 posture) |
| **Forward Deployed Engineer (FDE)** | Part II §2.4 Identity + §2.7.2 cross-tenant config snippets + Part III §3.3 Integration Cookbook |
| **Enterprise Architect (EA)** | Part II §2.8 deployment shapes + §2.9.7.2 WAF-pillar cross-walk + §2.8.5 exit-portability |
| **CISO** | Part II §2.7 governance + §2.5.2 healthcare PHI checklist + §2.5.1 FSI Tier-1/Tier-2 regulatory map + Part III §3.4 Audit-Evidence Cookbook + §3.5 per-regime regulatory depth |
| **Architect / engineering leader** | Foreword → Part I 10-tier stack → Part II §2.2 topologies + §2.3 recipes |

---

## Start here

Three reader paths. Pick the one that matches how you read:

1. **🚶 Linear** — start at [`book/00-foreword.md`](book/00-foreword.md), then [`book/00-introduction.md`](book/00-introduction.md), then walk Parts I → II → III. Foundations is the must-read core (~6–8h, two-week-absorbable); Patterns + Production are extended canon you return to as customer engagements demand. Roughly 60–90 days to "holding your end of the conversation."
2. **🎯 Skip-to-Part** — go directly to the Part that matches your seat: [Part I — Foundations](book/01-foundations.md) (vocabulary, ~6–8h) · [Part II — Patterns](book/02-patterns.md) (framework landscape + recipes + identity + governance, ~12–15h) · [Part III — Production](book/03-production.md) (deployment matrix + audit-evidence + regulatory depth, ~15–20h).
3. **🔍 Look-up** — start with the [glossary](book/04-glossary.md) (270+ entries, cross-tier-consistent), then jump into the section the customer brief surfaces.

---

## What this is

LangGraph is the reference framework the deep examples are written against — **and that is not advocacy; it is evidence.** Across the public named-customer deployments at enterprise scale as of 2026, LangGraph shows up most often: **18 of 18 named customer-disclosed enterprise deployments** in the public corpus this Field Guide draws from are LangGraph deployments. Its primitive set — explicit state-machine graphs, first-class human-in-the-loop, durable checkpointing, tight observability integration — maps cleanest to the trust, governance, and verifiability requirements that show up in regulated industries.

The book does not assume LangGraph as your production choice. It surveys ~27 frameworks at varying depth — LangChain, OpenAI Agents SDK, Anthropic Agent SDK, AWS Bedrock AgentCore, Azure AI Foundry, GCP Vertex Agent Engine, NVIDIA AI-Q, IBM watsonx Orchestrate, Microsoft Copilot Studio, Salesforce Agentforce, ServiceNow AI Agents, Snowflake Cortex Agents, Databricks Mosaic AI, CrewAI, AutoGen / AG2, Pydantic AI, and the long tail of community options — and tells you when each is the modal customer pick. The job is to understand the landscape clearly enough to (a) recognize what your customer is running, (b) defend a framework choice in a discovery call, (c) speak to the trade-offs without bluffing.

---

## What this is NOT

- **A procurement-evaluation document.** Procurement decisions require independent vendor evaluation. See [CONFLICTS.md](CONFLICTS.md).
- **An OPAQUE marketing piece.** The author is the CEO of OPAQUE Systems and discloses that affiliation transparently. The body follows a standards-anchored editorial rule documented in [CONFLICTS.md](CONFLICTS.md) §1 — OPAQUE is named only where a named industry standard has a specific OPAQUE-shipping primitive.
- **A substitute for vendor due diligence.** Named-customer evidence is mostly vendor-disclosed at launch; the Klarna AI-only customer-support reversal (Production §3.9) is the canonical reminder of how launch metrics evolve.
- **A guarantee that any named deployment has been independently audited.** Every factual claim carries an evidence-class tag from a 10-class taxonomy so you can weigh it correctly.

---

## Citation discipline

Every factual claim in the book carries an evidence-class tag from a 10-class taxonomy:

`[primary-regulatory]` · `[independently-audited]` · `[vendor-contractual]` · `[vendor-public]` · `[named-incident]` · `[customer-produced-evidence]` · `[corroborated]` · `[reference design]` · `[architectural inference]` · `[benchmark]`

When you cite the Guide back to a regulator, a procurement reviewer, a customer, or a peer, **lead with the evidence class** of the underlying claim, not the page number. Full taxonomy in [`book/00-introduction.md`](book/00-introduction.md).

---

## Repo map

| Path | What |
|------|------|
| [`book/00-foreword.md`](book/00-foreword.md) | Author's note |
| [`book/00-introduction.md`](book/00-introduction.md) | How to read · reader paths · citation discipline |
| [`book/01-foundations.md`](book/01-foundations.md) | **Part I — Foundations** |
| [`book/02-patterns.md`](book/02-patterns.md) | **Part II — Patterns** |
| [`book/03-production.md`](book/03-production.md) | **Part III — Production** |
| [`book/04-glossary.md`](book/04-glossary.md) | Glossary (~270 cross-tier-consistent entries) |
| [`book/05-anki-deck/`](book/05-anki-deck/) | Spaced-retrieval cards for all three Parts |
| [`CONFLICTS.md`](CONFLICTS.md) | Author affiliation + editorial-discipline disclosures · **read first if using for procurement evaluation** |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to file issues + PRs |
| [`CHANGELOG.md`](CHANGELOG.md) | Version history · canonical detail at [GitHub Releases](https://github.com/AaronRoeF/enterprise-ai-agents-on-langgraph/releases) |
| [`CITATION.cff`](CITATION.cff) | Academic citation metadata |
| [`LICENSE`](LICENSE) | CC BY-SA 4.0 |
| [`tools/lint-ascii-diagrams.py`](tools/lint-ascii-diagrams.py) | The diagram validator the book uses internally |

---

## Contributing · License · Contact

- **Contributing**: factual corrections, missing evidence, framings that obscure relevant trade-offs welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md). Run the ASCII diagram linter on any diagram changes; CI workflow forthcoming.
- **License**: CC BY-SA 4.0 — remix, translate, fork, improve. Just keep the attribution chain intact and your downstream work under a compatible license.
- **Contact**: Aaron Fulkerson · [aaronfulkerson.com](https://aaronfulkerson.com) · GitHub [@AaronRoeF](https://github.com/AaronRoeF) · for affiliation transparency see [`CONFLICTS.md`](CONFLICTS.md).

<!--
title: Enterprise AI Agents on LangGraph — A Field Guide
chapter: 00 — Introduction
version: v1.0
date: 2026-05-24
author: Aaron Fulkerson
license: CC BY-SA 4.0
-->

# Enterprise AI Agents on LangGraph: A Field Guide

## Introduction

**Edition:** v1.0
**Released:** 2026-05-24
**Author:** Aaron Fulkerson
**License:** Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
**Canonical URL:** https://aaronfulkerson.com/field-guide *(placeholder until published)*
**GitHub:** https://github.com/aaronfulkerson/enterprise-ai-agents-on-langgraph-field-guide *(placeholder until published)*

> **This is not a procurement-evaluation document.** It is an educational reference. Procurement decisions require independent vendor evaluation (Gartner, Forrester, NIST, ENISA, customer-side technical evaluation). This guide is one input among many; it is not a substitute for vendor due diligence. The full conflict-of-interest disclosure lives in `CONFLICTS.md` at the repository root.

---

## Why this book exists

Enterprise AI agents are being shipped to production faster than the documentation has caught up to them. The frameworks evolve quarterly. The protocols evolve quarterly. The named-component stack list changed three times in 2025 alone. The regulatory regimes — DORA, the EU AI Act, NIS2, SR 11-7, NYDFS Part 500, MAS TRM, SAMA, DFSA, HIPAA — are catching up to a category that did not exist when most of them were drafted, and the resulting compliance landscape is being rendered, at this exact moment, in customer Slack channels and Confluence pages and audit-evidence dossiers that are not in the public corpus.

A new Sales Engineer, Solution Consultant, or Product Manager joining a company that builds, sells, or ships enterprise agents arrives into that landscape on Day One. They have read the marketing, they have built a chatbot or a RAG demo, they have followed a LangGraph tutorial. They have not deployed an agent in production, they have not sat across a table from a Tier-1 **Financial Services Industry (FSI)** **Chief Information Security Officer (CISO)**, and they have not been asked by a regulator to produce the cryptographic provenance chain for a tool invocation that happened six months ago.

The training material currently available to that new hire is fragmented. Some of it is excellent — the LangChain documentation, the Anthropic prompt-engineering guides, individual customer engineering blogs, the Interrupt 2025 talks, the OWASP and MITRE governance taxonomies, the open-source framework READMEs. Some of it is marketing in disguise — vendor white papers that conflate vendor-disclosed launch metrics with operational evidence, "buyer's guides" that exist to win procurement-vocabulary battles, comparison matrices designed to position the publisher to win. The fragmentation is the problem the new hire inherits. They have to assemble a working model of the field from sources written for incompatible purposes, in incompatible vocabulary, at incompatible levels of evidence-weight, with no scaffolding telling them which sources are controlling and which are rebuttable.

This book is the educational foundation the industry has been missing. It is written for that new hire. It is also written for the broader LangGraph and enterprise-agent community — for practitioners who have been shipping in this space and want a peer-grade reference that names what they already know and fills in what they do not. It is written FOR the community, not AT the community. The tone is welcoming, the citations are honest, and the failure modes are named. The peer-artifact framing is deliberate: the book is not a sales tool dressed up as education. It is education that happens to have been written by someone with a known point of view, who has disclosed that point of view, and who has structured the book so that the editorial discipline is visible to the reader at every claim.

What this book is NOT:

- It is not a procurement-evaluation document. (See `CONFLICTS.md`.)
- It is not a marketing piece for any vendor — including the author's company.
- It is not a vendor pitch. There is no comparison table at the back where one product wins.
- It is not a guarantee that any of the named deployments referenced herein have been independently audited at the time of reading.

What this book IS:

- A peer-artifact for the LangGraph community.
- An onboarding-grade reference for new SE / SC / PM hires.
- A documented-reality snapshot of state-of-practice as of May 2026.
- A teaching artifact that names the failure modes, the regulatory clauses, the named components, and the citation-evidence weight behind every claim.

---

## Who this is for

The reader floor for Foundations (Chapter 1) is intentionally low. You are assumed to know what an LLM is, what an API is, what JSON is, what OAuth / SSO is at a conceptual level, and the names Postgres and Redis. You have probably built a chatbot demo or run through a RAG tutorial. You have NOT deployed an agent in production. You do not need to be a Python engineer to read Foundations — there is an explicit reading path for the non-coder.

By the time you finish all three chapters, you should be able to hold a discovery call with a Tier-1 FSI prospect, sketch the architecture on a whiteboard, name the failure modes the prospect cares about, defend the framework recommendation against an alternative, and articulate which mitigations live at which architectural layer.

The intended audiences:

- **New Sales Engineers, Solution Consultants, and Product Managers** at any company building, selling, or shipping enterprise agents — used as onboarding-grade material in the first ~60–90 days.
- **The broader LangGraph and enterprise-agent practitioner community** — for documented-reality reference material that is honest about evidence gaps.
- **Existing practitioners** — for vocabulary alignment, named-component reference, regulatory-clause cross-reference, and the citation-evidence taxonomy.
- **Enterprise Architects, security leads, and compliance partners** on the customer side of an agent deployment — for the same reasons, with the same caveats.

You do NOT need to be working on a LangGraph deployment specifically to get value from this book. The named-component vocabulary, the protocol stack, the identity primitives, the governance failure modes, the regulatory mapping, and the audit-evidence patterns are framework-agnostic in the concepts even where the worked examples are LangGraph-anchored. LangGraph is the anchor because, of the eighteen named, customer-disclosed, production-at-scale enterprise agent deployments in the public corpus this book draws from, all eighteen are LangGraph deployments. That is the honest framing for the title.

---

## Three reader paths

There is no single right way to read this book. Pick the path that matches how you work.

### Path 1 — Linear reader

Read Foundations, then Patterns, then Production, in order. This is the recommended path for a new hire being onboarded. Foundations is a two-week absorbable core read (~6–8 hours). Patterns and Production are extended canon — you return to them as customer engagements demand (~12–15 hours for Patterns, ~15–20 hours for Production).

The honest framing: Foundations in the first two weeks; Patterns and Production as ongoing reference over the next several months, with the capstone task at the end of Production signaling onboarding-complete around Day 60–90.

### Path 2 — Skip-to-tier reader

Already deep in this space? Pick the tier that matches your level and start there.

- **Patterns first** if you already know what an agent is, you have written or read LangGraph code, you can name a few of the canonical topologies, and you want the deployment-depth recipe walkthroughs and the named-vendor stack.
- **Production first** if you are an experienced practitioner — you have deployed agents, you know the seven LangGraph topologies, you know the six recipe families, and you want the 10-axis deployment matrix, the per-regime regulatory depth, the cross-tenant isolation chapter, the audit-evidence cookbook, and the operational-lifecycle role-play.

Each tier opens with an explicit prerequisite map — what you should know going in, what you will know coming out, what to revisit if a concept feels hazy. Each tier is self-contained in the sense that you do not need to have read the prior tier linearly to follow it, but you do need to recognize the vocabulary the prior tier established.

### Path 3 — Look-up reader

Already shipping in production? Use the book as a field reference. The glossary (`04-glossary.md`) is the canonical terminology entry point — every term is first-use-linked from every tier file, with "what this is" and "what this is NOT" framings to disambiguate near-neighbor concepts (`interrupt()` vs `Command(goto=...)`; agent identity vs agent-on-behalf-of-user identity; Postgres checkpointer vs Redis checkpointer; vendor-disclosed vs independently-audited). The 10-axis deployment-shape matrix, the per-regime regulatory depth chapters, the per-recipe Audit-Evidence Patterns, and the recipe × failure-mode matrix are designed to be looked up by section, not read linearly.

### The dual reading paths within Foundations

Foundations is a single file with two explicit reading paths inside it.

- **Engineer-track** (SE / SC with engineering background, EA on-ramp, anyone who writes Python today or will next month) — reads the code primitives in full and the ASCII state graphs in full.
- **PM-track** (Product, GTM, Sales, partner managers, anyone who does not write Python and does not plan to) — reads the conceptual narrative in full and the concept boxes at every primitive. **You may visually skim or skip the Python code blocks throughout this book** — they are visually identifiable by their indented fixed-width fenced format, and skipping them will not break the conceptual thread. The concept box immediately above or below each code block carries the meaning.

Both tracks share the same conceptual narrative, the same diagrams, the same JTBD framings, the same incident anchor primer, and the same exit gate. They differ only in how much code each is asked to absorb. Both tracks re-merge for the Patterns chapter forward; the PM-track reader is expected to have absorbed the code primitives at concept level via the skip-markers, and the Engineer-track reader is expected to have absorbed the PM-vocabulary (JTBD, ICP, ACV, buyer persona vs end-user persona) at the same depth.

If the dual-path treatment fails for you in the field — if you are a PM-track reader and the skip-markers do not actually scaffold you through Foundations — please file an issue. A separate `01a-foundations-pm.md` companion file is the planned v1.5 fallback if the dual-path approach does not hold up to real onboarding.

### Annotations used throughout

One convention used across every chapter is worth introducing here, because you will see it on every ASCII state graph from Foundations forward:

```
  [CKP]  — checkpoint write (the runtime persists state at this point)
  [HITL] — human-in-the-loop pause (the agent yields control to a human)
  [OBS]  — observability span emission (a trace event surfaces here)
  [POL]  — policy / guardrail check (the runtime applies a content or action policy)
```

These four annotations carry the same meaning everywhere they appear. Once you have learned them, you can read any state graph in the book and immediately know where the durability boundaries, the human-interruption points, the trace-emission surfaces, and the policy-check choke-points live. That is a lot of architectural information compressed into four bracketed tags.

---

## The three tiers at a glance

### Foundations — Chapter 1 (`01-foundations.md`)

Approximately 2,500 lines. Reading time ~6–8 hours core read, two-week absorbable. Approximately 85 glossary terms introduced.

What you will get:

- **What an agent is.** What an agent is NOT — chatbot, RAG, workflow, pipeline — with explicit disambiguation.
- **The 10-tier mental model of the stack** — LLM, retrieval, tools / MCP, identity, observability, state / checkpointer, secrets, policy, deploy, compute.
- **Named frameworks at conceptual level**, date-pinned to the May 2026 model cohort (Claude 4.7 / GPT-5 / Gemini 3.0).
- **The LangGraph primitives mini-section** — three authoring surfaces (Graph API, Functional API, Prebuilt `create_react_agent`); core primitives (`StateGraph`, `MessagesState`, `add_node`, `add_edge`, `Command`, `interrupt()`, `compile(checkpointer=...)`, `thread_id`); the `BaseStore` long-term memory primitive; the dev-loop tools (`langgraph dev`, `langgraph up`, `langgraph build`, LangGraph Studio).
- **The 3-layer protocol stack** — A2A (Agent-to-Agent, top) above MCP (Agent-to-Tool, middle) above AGP (Agent Gateway Protocol, transport). The MCP donation to the Linux Foundation AAIF (December 2025). The three MCP primitives — resources, tools, prompts.
- **The 6 recipe families at introductory depth** — Support Agent (Klarna anchor), Coding Agent (Uber / Replit family), Text-to-SQL Agent, Deep Research Agent, Embedded SaaS Copilot, SOC Agent. Two recipes drawn fully (Support and Coding); the other four named with JTBD framings.
- **The incident anchor primer** — ten named public incidents you will hear referenced in every customer call (Slack AI, EchoLeak / CVE-2025-32711, CurXecute / CVE-2025-54135, Samsung 2023, Air Canada / Moffatt v. Air Canada, Replit prod-DB deletion May 2025, Mata v. Avianca, ConfusedPilot, Salesforce Agentforce ForcedLeak Sept 2025, ChatGPT Atlas omnibox Oct 2025).
- **The six control boundaries** that define what "data-leak surface" means at conceptual depth.
- **The buyer-vs-end-user persona disambiguation** — taught in the body, not just at the gate.

### Patterns — Chapter 2 (`02-patterns.md`)

Approximately 3,870 lines. Reading time ~12–15 hours, treated as extended reference.

What you will get:

- **The framework landscape at procurement-grade depth** — six frameworks treated seriously (LangGraph anchor, CrewAI, AutoGen / AG2 distinguished, Microsoft Agent Framework, OpenAI Agents SDK, LlamaIndex Workflows, Semantic Kernel), with a one-page exclusion appendix for the tracked-not-deep set (Pydantic AI, Smol Agents, DSPy, Mastra, Agno, Letta).
- **The seven canonical LangGraph topologies** with named-component ASCII state graphs and a one-page decision tree — ReAct, ReAct + Reflexion, Plan-and-Execute, Supervisor, Hierarchical, Agentic RAG, Network / Swarm (renamed from "Multi-Agent Collaboration" to match the LangGraph docs).
- **The six recipe families at deployment depth** with verbatim customer-voice quotes wherever public engineering blogs and Interrupt 2025 talks made them available.
- **The Identity / Agent AuthZ chapter** — four IDPs (Entra Agent ID, Okta for AI Agents, Auth0 for AI Agents, Ping); five OAuth-2.x primitives relevant to agents (DPoP, PAR, RAR, CIBA, step-up); the MCP Authorization spec (OAuth-2.1 + DCR + RFC 9728); the agent-identity vs agent-on-behalf-of-user disambiguation; the eight FGA products (OpenFGA, Cedar / AWS Verified Permissions, Topaz, Okta FGA, Auth0 FGA, Permit.io, Oso, Styra).
- **The Cross-Tenant Isolation primer** — the five surfaces (retriever, cache, checkpointer, observability, model) with named-component mitigations per surface.
- **The ICP industry deep-dive** — FSI sub-segments (payments, wealth, research, institutional asset management); two ISV sub-motions at full depth (horizontal SaaS, developer tools); Healthcare reference-design and Sovereign structural-fit-only treatment.
- **The hyperscaler peer ref-arch comparison** at category level — AgentCore, Vertex Agent Engine, Foundry Agent Service, Salesforce Agentforce.
- **Control plane / data plane separation** — taught at Patterns depth because the BYOC compliance decision is gate-zero for FSI conversations and lands too late if left for Production.

### Production — Chapter 3 (`03-production.md`)

Approximately 5,202 lines plus 17 appendices. Reading time ~15–20 hours, extended-canon ongoing reference.

What you will get:

- **The 10-axis deployment-shape matrix** — cloud locus, identity perimeter, data perimeter, trace egress, secret perimeter, network egress, model perimeter, tool-call perimeter, HITL surface, support / break-glass — across the LangGraph Platform shapes (Cloud SaaS, BYOC AWS-only, Self-Hosted Enterprise, Standalone Container) plus the CSP-managed and sovereign / air-gap rows with explicit `[gap]` markers.
- **The Cross-Tenant Isolation chapter at depth** — five surfaces with worked FGA models for Text-to-SQL and Embedded SaaS Copilot recipes.
- **The Integration Cookbook** — customer existing IAM + secrets at full depth (Entra, Okta, Auth0, Ping, ForgeRock, CyberArk, SailPoint, HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager, External Secrets Operator, HSM-backed signing); observability, policy, lineage, CI/CD, egress at compressed reference depth.
- **The Audit-Evidence Cookbook** — what gets signed, where, by whom; what gets retained, where, how long; what surfaces to which SIEM in which format; reproducibility; what the examiner sees on examination day; the read-trail (audit-log-of-the-audit-log); incident response runbook; break-glass; exit plan; per-recipe Audit-Evidence Pattern (six artifacts); per-recipe Evidence Index.
- **The per-regime regulatory depth chapters** — DORA, GDPR, EU AI Act, NIS2, SR 11-7, OCC, FRB, NYDFS Part 500, SEC 17a-4, FINRA, SEC Reg S-P, MiFID II + RTS 6, FedRAMP, HIPAA, PCI DSS 4.0, SAMA, DFSA, MAS, HKMA, PDPA, PIPL, DPDPA, UAE PDPL — with the three to eight most operative articles per regime cited verbatim and mapped to named components.
- **The 14 governance failure modes at expert depth** — with STRIDE-A threat models per recipe and three-column "what the customer asks / what the SE says / what the SOC does" callouts.
- **Recipe-by-recipe Production deep-dives** — with hero expansion on Klarna and Captide-shape FSI Plan-and-Execute.
- **The hyperscaler comparison at depth** — moved to a Production appendix to keep the linear read path focused.
- **The Klarna CEO May 2025 reversal** — as the canonical operational-lifecycle case study; the strongest available "vendor-disclosed launch metric did not survive one year" anchor in the public corpus.
- **The insurance gap analysis** — zero LangGraph insurance footprint, 68% generative / agentic adoption, 42% abandonment rate; what it implies for framework selection in evidence-thin verticals.
- **The Data Residency Reasoning chapter** — five sovereignty axes × per-region regulatory landscape × sovereign cloud option matrix.
- **The PHI-in-scope reference deployment chapter** — every claim `[reference design]`-tagged; no LangGraph production deployment touches PHI as of publication.
- **The 4-event operational-lifecycle role-play** — EchoLeak response, Claude version-swap MRM event, sub-processor change notification, ECB examination evidence package.
- **The capstone task** — all three roles (SE / SC / PM) produce artifacts against the same customer brief that have to fit together. The integration signal single-role gates miss.

---

## How to use this book

### The five questions every tier answers

Every tier answers the same five reader questions at appropriate depth. The questions are an internal-tracking scaffold; the published chapters present chapter structure, not "the five questions" as an organizing principle. But it is worth knowing what scaffold the chapters were written against, because it lets you cross-reference at depth.

1. What are all the **components** of an enterprise AI agent stack?
2. What are the **popular frameworks**, with particular emphasis on open source and LangGraph?
3. What are the **common use cases** — in general and across the persona × recipe × segment-variant matrix?
4. What are the **known governance issues**?
5. What are the **known data-leak surfaces** inherent to these stacks — using the public-facing taxonomies (OWASP LLM Top 10, OWASP Agentic Top 10, MITRE ATLAS, EU AI Act, NIST AI RMF) as the canonical framing?

### Knowledge gates

Each tier ends with a knowledge gate — a real customer scenario the reader must reason through to demonstrate tier mastery. Each gate has three role-specific tracks:

- **SE/SC gate** — pick the recipe + named-stack vendors + topology + deployment shape; name the dominant governance category; sketch the control-plane / data-plane split.
- **PM-track gate** — write the PRD or brief section with JTBD + buyer persona + end-user persona + deal context + evidence-class tags on every claim.
- **Engineer gate** (Patterns onward) — wire a topology with named components, identify the governance-loaded design choices.

Every gate ships with: a model brief, A / B / C model answers (not just A — readers need to see the failure modes the rubric distinguishes), a 5–7-criterion rubric with `pass / partial / fail` definitions, a named evaluator role, and a retake mechanic. Production adds a whiteboard test, the 4-event operational-lifecycle role-play, and the capstone.

### Mentor checkpoints

At four named points in the book, the reader is invited to spend 20–45 minutes with a team lead, peer mentor, or veteran SE. The invitations are explicit; they are part of the curriculum, not an afterthought. Without them, the asset trains readers to feel ready alone — the highest-cost curriculum failure mode this book is built to avoid.

The four checkpoints, with approximate mentor time per reader:

1. **Post-Foundations gate** — ~30 minutes — mentor review of JTBD framing.
2. **Post-Patterns Identity chapter** — ~20 minutes — confirm FGA / DPoP / agent-on-behalf-of-user articulation.
3. **Pre-Production whiteboard** — ~45 minutes — practice whiteboard with a veteran SE.
4. **Post-Production gate** — ~45 minutes — mentor review of PRD or brief or whiteboard photo.

Total: ~2.5 hours mentor time per new hire across the full read.

### Anki decks and spaced retrieval

Spaced-retrieval cards live in `05-anki-deck/`, one file per tier, importable to Anki. Approximate volume:

- Foundations — ~60–80 cards (must-retain vocabulary, named components, named incidents).
- Patterns — ~100–150 cards (named-vendor stack, topology decision criteria, OAuth primitives, FGA products, recipe families, segment variants).
- Production — ~150–200 cards (10-axis matrix vocabulary, per-regime regulatory clauses, the 14 failure modes, audit-evidence chain anchors).

The book also embeds end-of-section recall cards (5–8 questions per major section), mid-tier retrieval breaks (15-minute mixed-question exercises at Patterns and Production halfway points), and pre-tier retrieval warmups (30-minute recall against the prior tier before starting the next).

### Worked-example progressions

For hero recipes — Support Agent (Klarna anchor) and Plan-and-Execute (Captide-shape FSI anchor) — the book ships three levels of worked example:

1. **Full worked example** — the complete state graph, every named component slot filled, every annotation in place. The reader reads it.
2. **Partial worked example** — three named-component slots left blank, the reader fills them in against the stated customer constraints.
3. **Prompt-only** — the reader builds the state graph from scratch against a customer brief; the book provides the rubric for what a passing answer looks like.

Three levels of scaffolding, not just full-worked-example and gate. The intermediate level is where most of the actual learning happens; the book commits to at least three worked-example pairs per tier in v1, with full coverage across all six recipes deferred to v1.5.

### Common-confusion call-out boxes

Near-neighbor concept pairs are explicitly disambiguated in structured call-out boxes throughout the book. The patterns the call-outs cover include:

- `interrupt()` vs `Command(goto=...)` vs `Command(resume=...)`.
- Postgres checkpointer vs Redis checkpointer (different invalidation semantics, different cross-thread behaviors).
- MCP server vs MCP client vs `langchain-mcp-adapters` (substrate vs wrapper).
- Agent identity (workload) vs agent-on-behalf-of-user identity (delegation).
- ReAct vs Supervisor (the Klarna re-classification context).
- Buyer persona vs end-user persona (the JTBD vocabulary).
- Vendor-disclosed vs independently-audited (the citation-evidence weight).

The call-outs are not decorative. Each one was added in response to a specific observed reader-confusion failure mode during the design-spec critique passes.

### Glossary

The canonical terminology reference lives in `04-glossary.md`. Every term is first-use-linked from every tier file. Each entry carries the definition, the first tier the term appears in, cross-references to related terms, and explicit "common-confusion" framings for near-neighbor concept pairs. Both technical vocabulary (LLM, retrieval, checkpointer, MCP resources / tools / prompts, A2A, AGP, MCP Authorization, FGA, DPoP, PAR, RAR, CIBA, PKCE, `BaseStore`, Functional API) and PM vocabulary (JTBD, ICP, ACV, sales cycle, evaluation criteria, end-user persona vs buyer persona) live here. The glossary is audited quarterly as part of the 90-day update cadence.

### Pre-work prerequisites

If your reader floor is shaky on one of the assumed prerequisites, two short pre-work tutorials cover the gap before you start Foundations:

- **PM-track pre-work** — the LangChain "Hello, Agent" tutorial (~45 minutes; conceptual; no Python required to read along).
- **Engineer-track pre-work** — the LangGraph Studio quickstart (~30 minutes; Python; the visual debugger you will see referenced throughout the book).

Neither is mandatory. If neither is available to you when you start, do not stop reading — you will pick up the vocabulary as you go. The pre-work exists to reduce the reader-floor variance, not to gate entry.

---

## Citation discipline

Every factual claim in the body of this book carries an inline evidence-class tag. The tags are not decorative. They tell you, the reader, exactly what kind of evidence backs the claim — and therefore exactly how much weight you should put on it when you cite it back to a CISO or a regulator or a procurement reviewer.

The ten classes:

| Tag | Meaning |
|-----|---------|
| `[primary-regulatory]` | The text of the regulation itself (DORA Art. 28 verbatim; SR 11-7 §III.4 verbatim). Controlling, not "evidence" — this is the law. |
| `[independently-audited]` | Third-party-audited claim — SOC 2 attestation, ISO 27001 certificate, FedRAMP authorization, EBA AIF audit. Highest evidence weight; scope-limited to what was audited. |
| `[vendor-contractual]` | A vendor commitment in a DPA, MSA, or order form. Legally binding. High weight. |
| `[vendor-public]` | A vendor public statement — blog, docs, marketing site. Low evidence weight. Rebuttable. **NOT contractually binding.** |
| `[named-incident]` | A public incident report — EchoLeak / CVE-2025-32711, CurXecute / CVE-2025-54135, Slack AI, Samsung 2023, Air Canada, Replit prod-DB, Mata v. Avianca, ConfusedPilot, Salesforce ForcedLeak, ChatGPT Atlas omnibox. |
| `[customer-produced-evidence]` | A first-party customer engineering blog or case study — Klarna engineering blog, Uber Interrupt talk, Replit blog. Different evidence weight than `[vendor-public]` because the source has skin in the deployment. |
| `[corroborated]` | A claim that appears in two or more independent sources. Cross-references which categories. |
| `[reference design]` | A pattern from a published reference architecture, not a deployed customer. The reader needs to know they are looking at a pattern, not a deployment. |
| `[architectural inference]` | Synthesized; not directly stated by any single source. **Pedagogically appropriate; an operational red flag in FSI deployment dossiers** — readers must understand the distinction. |
| `[benchmark]` | An academic, standards-body, or public benchmark — OWASP LLM Top 10, MITRE ATLAS, AgentDojo, InjecAgent, AgentHarm, NIST AI RMF, McKinsey survey. |

**Explicit teaching: vendor-disclosed metrics are NOT MRM-validation evidence under SR 11-7.** Klarna's 80% deflection rate, Klarna's "700 FTE equivalent" framing, Uber's 21,000 dev hours saved, LinkedIn's 95% target, Komodo's 330M patient journeys — these are useful for benchmarking and discussion. They are not valid as validation evidence in a model risk management dossier that a Sales Engineer co-signs. The book teaches the distinction at every tier; the reader should leave Production unable to mistake one for the other.

Layered on top of evidence-class tags are per-leakage-pathway regime-binding tags — `[DORA Art. 28]`, `[GDPR Art. 5(1)(b)]`, `[FINRA Rule 5280]`, `[HIPAA §164.502(b)]`, `[NYDFS Part 500.07]`, `[MAS TRM §11]`. These tell you which clause of which regulation the claim binds against.

---

## Author bio

**Aaron Fulkerson** is the CEO of OPAQUE Systems, a confidential AI infrastructure company. OPAQUE was founded by Co-Founders Ion Stoica (Executive Chairman), Raluca Ada Popa (Chief Scientist), Rishabh Poddar (CTO), and Chester Leung out of UC Berkeley's RISELab. Aaron's background spans enterprise platforms, open source, and infrastructure — the last several years specifically on the question of how to give enterprises cryptographic guarantees about what happens to their data inside AI workflows.

This book is written under Aaron's own by-line on aaronfulkerson.com. The reader is getting an experienced practitioner's perspective with a known point of view. That point of view is disclosed transparently: Aaron's primary economic interest is the success of OPAQUE Systems, a venture-backed AI infrastructure company. OPAQUE's product positioning intersects with one specific architectural framing in this book — the category-level observation that a subset of agent failure modes reduces to substrate-level remediation properties (TEE attestation, sealed keys, attested network egress, attested workload identity). The book frames that observation at category level only and does not name any vendor — including OPAQUE — as the remediation answer. The full conflict-of-interest disclosure, the funding source, the peer-review status, and the reader's responsibility to triangulate against independent sources live in [`CONFLICTS.md`](CONFLICTS.md) at the repo root.

If you are reading this book as a procurement evaluator, please read `CONFLICTS.md` before continuing.

---

## Not a procurement document — explicit

This needs saying twice, because the first time was at the top of the file and you may have skimmed it.

**The Field Guide is an educational reference.** It is not a procurement-evaluation document. It is not a vendor pitch. It is not a substitute for vendor due diligence, customer-side technical evaluation, independent analyst review (Gartner, Forrester, NIST, ENISA), or your own organization's vendor-risk workflow. Procurement decisions require all of those things — and this book is one input among many to those workflows, not a replacement for them.

The book does not recommend a vendor for any role in the stack. It names the popular vendors per tier (LLM, retrieval, observability, state, policy, identity, secrets, deploy, compute), it gives you the procurement-evaluation question set per framework, and it teaches the citation-evidence taxonomy so you can read vendor claims with the right level of skepticism. The recommendation is yours to make against your own requirements.

If you intend to use this book as input to a vendor-risk assessment or a procurement evaluation, read `CONFLICTS.md` first. The author affiliation, the funding source, the peer-review status, and the explicit list of disciplines applied during authorship are documented there for that exact use case.

---

## How this book was made

Transparency about process, because the citation-evidence discipline above demands it. Five phases, each with a discrete artifact and a discrete quality gate.

1. **Two rounds of structured adversarial critique before drafting.** Six simulated-reviewer personas spanning Sales Engineer, Product Manager, Enterprise Architect, CISO-FSI, LangChain DevRel, and Developer Educator viewpoints were run against the design spec in two passes (R1 and R2). Each persona produced a critique surface — what was missing, what was overclaimed, what was vendor-positioning in disguise, what was pedagogically broken, what would not survive an FSI audit floor. The design spec was rewritten between each pass to integrate the critique. The third design-spec revision is what the tier files were written against. Critique items that were considered and deliberately not applied are recorded in §15 of the design spec for process integrity.

2. **A six-stream research swarm before writing.** Six parallel research streams ran against the design lock: framework survey (R1), beginner conceptual foundations (R2), ICP persona × segment × use-case deep-dive (R3), data-leak surface catalog (R4), academic and community signals (R5), primary customer voice (R6). Each produced a `ref-*.md` research artifact. The tier files cite from those artifacts; they do not re-derive the research. A research-completeness gate between the swarm returning and the tier-file writing confirmed that every named component had a citation, every metric had a confidence flag, every regulatory clause had a primary source, every claim had an evidence-class tag, and every leakage pathway had regime-binding tags. Gaps from the gate were logged to an open-questions register with owners.

3. **Three parallel tier writers.** Foundations, Patterns, and Production were drafted in parallel against the shared research base — three writer agents working from the same lock, with a final cross-tier alignment pass for terminology, named components, and citation consistency. Parallel writing was the only way to deliver the ~520-page total volume on schedule; the cross-tier alignment pass is the discipline that keeps the three tier files from drifting against each other.

4. **A citation-discipline completeness pass.** Every claim in every tier file was reviewed against the 10-class evidence taxonomy. Untagged claims blocked the gate. Per-leakage-pathway regime-binding tags were applied on top of evidence-class tags where applicable. High-risk-of-drift areas — Healthcare PHI, Sovereign, the Identity tier at LangGraph customer scale, FedRAMP authorization, MCP supply-chain at production scale, and vendor metrics across all six recipes — were audited specifically for tag accuracy. Where evidence is thin or absent, the tier files mark it explicitly (`[evidence-zero, structural-fit-only]` or `[reference design — not in PHI production anywhere on any framework]`) rather than paper over the gap.

5. **A cross-tier consistency pass.** Glossary terms, named-component lists, citation tags, and reading-time estimates were cross-checked across the three tier files. Foundations introduces ~85 glossary terms; Patterns introduces named-vendor stacks and procurement vocabulary; Production introduces regulatory clauses and audit-evidence patterns. The consistency pass confirmed every term used in a later tier appears in the glossary, every named component referenced in Production was introduced in Patterns at the appropriate depth, and every named incident referenced in the body was anchored in the Foundations incident anchor primer.

A formal inter-rater-reliability study with at least one OPAQUE-internal SME and at least one independent external reviewer under NDA is committed for v1.1. The reviewers, their scope, and the Cohen's kappa results (target ≥ 0.7 on the Production gate) will be disclosed in `CONFLICTS.md` when v1.1 ships.

Authorship drew on substantial assistance from large-language-model-based agents (specifically, an autonomous research-and-drafting pipeline running Anthropic Claude). All factual claims were reviewed against the cited primary sources. The author retains responsibility for the final content. Errors that survive are the author's; corrections are welcome via the GitHub issue tracker.

---

## Versioning and contributions

### v1.0 — Initial release

This is the first public release of the Field Guide. Version v1.0 reflects state-of-practice as of 2026-05-24. Specifically, this edition is pinned to:

- **Model cohort:** Claude 4.7 / GPT-5 / Gemini 3.0 (May 2026).
- **LangGraph:** v1.x with explicit migration notes where v2.x RFCs are in flight (`MessagesState` Pydantic state RFC, etc.).
- **MCP:** Linux Foundation AAIF (donated December 2025).
- **Identity:** Entra Agent ID GA 2025; Okta for AI Agents EA 2025; Auth0 for AI Agents EA 2025.
- **LangGraph Platform:** BYOC AWS-only as of 2025; no public FedRAMP authorization as of 2026-05.
- **LangSmith:** SOC 2 Type II 2025.

The book is published under a 90-day update cadence, including a quarterly glossary audit. A public changelog tracks named-primitive changes between editions.

### Versioning policy

- **Patch (v1.0.1):** Typo fixes, broken-link fixes, citation corrections, minor glossary updates.
- **Minor (v1.1):** Quarterly cadence — new named components, new regulatory clauses, new incident anchors, model cohort updates.
- **Major (v2.0):** Structural change — new tier, new chapter, removal of deprecated framework, breaking change to the citation taxonomy.

### How to file issues

The public GitHub repository accepts issues for: factual errors, missing citations, broken links, terminology drift, evidence-tag mistakes, missing common-confusion framings, missing named components, missing regulatory clauses, and missing incident anchors. Issues that include a primary-regulatory or named-incident citation will be triaged first.

The repository does not accept issues that re-litigate the editorial stance (no vendor positioning in the body, public-vocabulary-only, single-author by-line) — those are locked in the design spec. Issues that are vendor-positioning advocacy will be closed.

### How to contribute

Contribution guidelines live in `CONTRIBUTING.md` at the repository root. Pull requests are accepted for: typo fixes, broken-link fixes, citation additions with primary sources, named-component additions where the component is in production at a publicly disclosed deployment, regulatory-clause additions with verbatim text, glossary additions where the term meets the first-use-linked criterion, and translations (out of scope for v1; planned for v1.5+).

All contributions are accepted under the same license as the book (CC BY-SA 4.0). The author retains editorial control over the published artifact.

---

## License notice

This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0). You are free to:

- **Share** — copy and redistribute the material in any medium or format.
- **Adapt** — remix, transform, and build upon the material for any purpose, even commercially.

Under the following terms:

- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
- **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

**Citation string** for citing this work:

> Fulkerson, Aaron. *Enterprise AI Agents on LangGraph: A Field Guide.* v1.0, 2026-05-24. CC BY-SA 4.0. https://aaronfulkerson.com/field-guide.

The full license text lives in [`LICENSE`](LICENSE) at the repo root.

---

## Closing — the invitation to begin

The honest thing to say is that the agent landscape is moving faster than any book about it can keep up with. The frameworks ship monthly. The protocols ship quarterly. The regulatory regimes ship yearly, and the named incidents ship whenever they ship. This book is a snapshot of state-of-practice as of 2026-05-24. By the time you read this, parts of it will already be drifting against the present. The 90-day update cadence is the discipline this book applies to that drift; the citation-evidence taxonomy is the discipline you, the reader, will apply to anything you read after this.

What this book commits to is the underlying vocabulary, the underlying architecture, the underlying failure modes, and the underlying regulatory pressure — the things that change more slowly than the names of the components implementing them. The named-vendor stack will rotate; the existence of a retrieval tier, a state tier, an identity tier, and an observability tier will not. The named topology in fashion will rotate; the existence of seven canonical topologies and the trade-offs that select among them will not. The named incident in the headlines will rotate; the categories of failure mode the incident exemplifies — prompt injection, identity and action provenance, telemetry capture, cross-tenant aggregation, supply chain — will not. The named regulatory clause will rotate; the existence of a regulator who wants to see a model inventory, an ICT register, an incident log, a sub-processor list, and an examiner-day artifact dossier will not. If you absorb the vocabulary and the architecture and the failure modes and the regulatory pressure, you will be able to read the next year's worth of new components, new protocols, and new incidents in context. That is the long-half-life payload the book is trying to deliver.

So: pick a path.

- If you are new to this and you have two weeks to spend on the core, start with [Foundations](01-foundations.md). The reader floor is intentionally low; the dual-track reading paths are designed for the PM-track reader and the engineer-track reader alike.
- If you have shipped a few agents and want the deployment-depth recipes, the topology decision tree, the named-vendor stack, the Identity chapter, and the Cross-Tenant Isolation primer, start with [Patterns](02-patterns.md). It assumes the Foundations vocabulary but does not re-teach it; revisit Foundations sections as the cross-references demand.
- If you are an experienced practitioner and you want the 10-axis deployment matrix, the per-regime regulatory depth, the audit-evidence cookbook, the 14 failure modes at expert depth, the recipe-by-recipe Production deep-dives, the Klarna reversal case study, the operational-lifecycle role-play, and the capstone, start with [Production](03-production.md). It assumes Patterns vocabulary cold.

The community is shipping enterprise agents to production right now. The customers are deploying them right now. The regulators are examining them right now. The new hires are arriving right now. This book exists so that the next one of them arrives ready.

Welcome to the field. Let's go.

---

*— Aaron Fulkerson*
*2026-05-24*

---

> **Cross-references for this file:**
> - [`CONFLICTS.md`](CONFLICTS.md) — author affiliation, funding, peer-review status, procurement-review disclosure.
> - [`LICENSE`](LICENSE) — CC BY-SA 4.0 full text.
> - [`01-foundations.md`](01-foundations.md) — Foundations tier (must-read core).
> - [`02-patterns.md`](02-patterns.md) — Patterns tier (extended canon).
> - [`03-production.md`](03-production.md) — Production tier (extended canon + capstone).
> - [`04-glossary.md`](04-glossary.md) — canonical terminology reference.
> - [`05-anki-deck/`](05-anki-deck/) — spaced-retrieval cards per tier.

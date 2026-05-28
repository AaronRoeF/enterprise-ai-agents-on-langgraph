<!--
title: Enterprise AI Agents on LangGraph — A Field Guide
part: Glossary
version: v1.1
date: 2026-05-27
author: Aaron Fulkerson
license: CC BY-SA 4.0
-->

# Enterprise AI Agents on LangGraph: A Field Guide
## Field Guide Glossary

*The canonical terminology reference across Foundations, Patterns, and Production. Single definition per term, cross-tier consistent, cross-referenced.*

**Author:** Aaron Fulkerson
**License:** CC BY-SA 4.0
**Version:** 1.0 (draft, May 2026)

> **Companion files.** The tier files (`01-foundations.md`, `02-patterns.md`, `03-production.md`) are the narrative; this glossary is the reference. Each tier has a short tier-local glossary (`§1.15`, `§2.11`, `§3.15`); the entries here are the canonical, cross-tier-consistent definitions those local glossaries point to.

> **This is not a procurement-evaluation document.** It is an educational reference. Procurement decisions require independent vendor evaluation (Gartner, Forrester, NIST, ENISA, customer-side technical evaluation). This guide is one input among many; it is not a substitute for vendor due diligence.

---

## How to use this glossary

Two access paths.

**A–Z alphabetical (§4.1)** is the look-up path. Use it when you encounter a term in any tier file and want the canonical definition. Each entry carries:

- The canonical 1–3 sentence definition.
- A tier marker — *(Foundations | Patterns | Production)* — with the **primary tier marked in bold**. The primary tier is where the term first appears or is most fully developed.
- Cross-references to related entries, marked with the `→` arrow. Every arrow resolves to another entry in this file.
- The tier section where the term first appears, hyperlinked.

**Cluster index (§4.2)** is the guided-learning path. Use it when you want to learn or refresh a domain — identity, observability, deployment, regulatory regimes — at one sitting. The clusters loosely follow the research-stream R2 organization with refinements.

**Quick-reference panels (§4.3–4.6)** give one-line definitions for the four highest-frequency taxonomies in the book: the 10 citation classes, the 7 LangGraph topologies, the 6 recipe families, and the 10 deployment-shape axes.

**Acronyms (§4.7)** is the alphabetical dictionary of every acronym used in the book.

**Out-of-scope omissions (§4.8)** documents terms intentionally not defined here, with brief explanation why.

### Tier marker convention

- **(Foundations)** — first appears or is most fully developed in Part I.
- **(Patterns)** — first appears or is most fully developed in Part II.
- **(Production)** — first appears or is most fully developed in Part III.
- **(Foundations / Patterns)** — introduced in Foundations, deepened in Patterns.
- **(Foundations / Production)** — introduced in Foundations, deepened in Production.
- **(All three)** — referenced throughout. The primary-development tier is bolded.

---

# §4.1 A–Z Glossary

## A

**A2A (Agent2Agent Protocol)** *(**Foundations** / Patterns)*
Google-originated protocol for agent-to-agent collaboration and handoff. Donated to the Linux Foundation in June 2025. Sits **above** MCP in the three-layer protocol stack — A2A is for agent-to-agent traffic; MCP is for agent-to-tool. JSON-RPC over HTTP, supports streaming, capability discovery, and signed handoff.
Cross-references: → MCP, → AGP, → three-layer protocol stack, → LF AAIF, → AGNTCY.
First appears in: §1.6.

**ACV (Annual Contract Value)** *(**Foundations**)*
PM vocabulary. The dollar value of one customer-year of a recurring contract. Useful for sizing deals and comparing per-customer economics across segments. Not an MRM term.
Cross-references: → discovery call, → buyer persona.
First appears in: §1.15 PM-track vocabulary.

**Action provenance** *(**Foundations** / Patterns / Production)*
The cryptographic chain of evidence for an agent action: who authenticated, what plan was approved, which tool was invoked with which arguments, what result was returned, and what outcome was recorded. Without action provenance, an agent action cannot be audited or reconstructed after the fact. Failure mode 6 ("identity & action provenance") is the absence of this chain.
Cross-references: → signed action chain, → audit-evidence pattern, → action provenance gap, → MRM.
First appears in: §1.9.

**Action provenance gap** *(**Foundations** / Production)*
The failure mode where the audit trail cannot reconstruct who authorized an agent action — typically because the agent's identity collapsed into the user's identity, or because intermediate plan / tool / result events were not signed or retained.
Cross-references: → action provenance, → signed action chain, → cross-tenant aggregation.
First appears in: §1.11; deepened in §3.6.

**Advisor (autonomy Level 0)** *(**Foundations**)*
Lowest level of the 5-point autonomy spectrum. The system suggests; the human acts. No tool execution, no state-changing action. Most "AI assistant" features fit here.
Cross-references: → autonomy spectrum.
First appears in: §1.1.

**Agent** *(**Foundations** / Patterns / Production)*
A system in which an LLM dynamically directs its own process and tool usage (Anthropic's definition). Broader vendor definitions (LangChain, OpenAI) treat any LLM + tools + state composition as an agent. The Field Guide uses the Anthropic discipline and flags the vendor inconsistency rather than papering over it.
Cross-references: → agentic system, → workflow, → chatbot, → RAG, → pipeline, → autonomy spectrum.
First appears in: §1.1.

**Agent-on-behalf-of-user identity (delegation)** *(**Foundations** / Patterns / Production)*
The identity the agent assumes when acting in a user's name — the delegation identity. One of the three agent identity problems. Distinct from agent identity (the workload) and from user identity (the human authenticating to the system). Often confused with workload identity in vendor marketing; the Field Guide separates them in §1.9.
Cross-references: → agent identity (workload), → user identity, → three agent identity problems, → DPoP, → RAR, → FGA.
First appears in: §1.9; deepened in §2.4.

**Agent identity (workload)** *(**Foundations** / Patterns / Production)*
The identity of the agent runtime itself — the workload. Used for tool authentication, MCP server authentication, and inter-agent calls. SPIFFE / SPIRE in zero-trust environments; Entra Agent ID, Okta for AI Agents, Auth0 for AI Agents as commercial first-party agent-identity products. One of the three agent identity problems.
Cross-references: → agent-on-behalf-of-user identity, → SPIFFE/SPIRE, → Entra Agent ID, → Okta for AI Agents, → three agent identity problems.
First appears in: §1.9; deepened in §2.4.

**Agent manifest** *(**Production**)*
The bundle of five hashes (model_version_hash + system_prompt_hash + tool_registry_hash + retrieval_index_hash + agent_graph_hash) plus sub-processor list plus retention policy that uniquely identifies a reproducible agent build. The §3.4.4 reproducibility artifact.
Cross-references: → reproducibility, → audit-evidence pattern, → model-swap protocol.
First appears in: §3.4.

**Agentic RAG** *(**Foundations** / Patterns)*
RAG with agent-loop semantics — the LLM decides when to retrieve, critiques retrieval results, re-queries on insufficient evidence. Becomes an agent. Topology 6 of the 7 canonical LangGraph topologies. CRAG and Self-RAG are named variants.
Cross-references: → RAG, → CRAG, → Self-RAG, → ReAct, → topology 6.
First appears in: §1.1; deepened in §2.2.

**Agentic system** *(**Foundations**)*
Anthropic's umbrella term covering both workflows and agents — any LLM-orchestrated system whose behavior includes tool use, retrieval, or multi-step reasoning.
Cross-references: → agent, → workflow.
First appears in: §1.1.

**Agent Governance Toolkit (AGT)** *(**Foundations** / Patterns)*
Microsoft's action-layer governance framework for agent runtimes. AGT intercepts the *action* an agent is about to take — a tool call, a state mutation, an external API call — and applies policy to the action itself (allowed / denied, requires approval, requires step-up auth). Sits in the critical path of the action: if the governance check fails, the action does not happen. Foundations §1.10 places AGT in the four-approach governance model (Guardrails → Action-layer → Sandbox → Cryptographic). Patterns §2.5 carries the FGA-bound approval flow and HITL gate depth.
Cross-references: → Guardrails, → Sandbox, → FGA, → HITL, → governance approaches.
First appears in: §1.10; deepened in §2.5.

**AGNTCY** *(**Foundations** / Patterns)*
Cisco / Outshift-led open agent-protocol initiative; the project home for the AGP layer and related components (SLIM messaging, identity, discovery, observability). Donated to the Linux Foundation in July 2025.
Cross-references: → AGP, → LF AAIF, → three-layer protocol stack.
First appears in: §1.6.

**AGP (Agent Gateway Protocol)** *(**Foundations** / Patterns)*
Cisco / AGNTCY-originated routing layer for inter-agent traffic. Donated to the Linux Foundation in July 2025. Sits **below** MCP in the three-layer protocol stack — AGP is the transport / identity / routing substrate; MCP is the capability-invocation layer above it.
Cross-references: → A2A, → MCP, → AGNTCY, → three-layer protocol stack.
First appears in: §1.6.

**AKS (Azure Kubernetes Service)** *(Patterns / **Production**)*
Microsoft's managed Kubernetes service. The Self-Hosted Enterprise LangGraph deployment shape runs on AKS for Azure-committed customers as the workaround for the BYOC-Azure gap.
Cross-references: → EKS, → BYOC, → Self-Hosted Enterprise, → BYOC Azure (gap).
First appears in: §2.8; deepened in §3.1.

**Annex III** *(Patterns / **Production**)*
EU AI Act Annex III — the high-risk-system categorization list (credit scoring, insurance pricing, life/health pricing, education, employment, essential services, biometrics, law enforcement, migration, justice). A LangGraph agent operating in any Annex III category triggers the Article 9–16 obligations.
Cross-references: → EU AI Act, → high-risk system.
First appears in: §2.5; deepened in §3.5.

**Anki deck** *(**Foundations**)*
A CC BY-SA 4.0 spaced-retrieval flashcard set shipped with the Field Guide (`book/05-anki-deck/`). One deck per tier. ~50 cards per tier covering must-retain vocabulary, named components, named incidents, regime articles.
Cross-references: → spaced retrieval, → retrieval break.
First appears in: §1.19.

**APAC/Gulf regimes** *(**Production**)*
The bucket of regulatory regimes covered in §3.5.3: SAMA (Saudi), DFSA (Dubai), MAS (Singapore), HKMA (Hong Kong), PDPA (Singapore / Thailand variants), PIPL (China), DPDPA (India), UAE PDPL.
Cross-references: → MAS, → DFSA, → HKMA, → SAMA, → PDPA, → PIPL, → DPDPA, → UAE PDPL.
First appears in: §3.5.

**Approval (HITL approval)** *(**Foundations** / Patterns)*
The human action that resumes an interrupted agent. The agent pauses via `interrupt()`, surfaces what it is about to do, and waits for the human to approve, reject, or modify before resuming.
Cross-references: → HITL, → interrupt, → resume, → escalation.
First appears in: §1.4 (interrupt) / §1.7.

**Architectural inference [tag]** *(**Foundations** / Patterns / Production)*
One of the 10 evidence-class tags (§4.3). Marks a claim synthesized from multiple sources but not stated directly by any single source — pedagogically useful, but a red-flag tag in operational dossiers because it is not MRM-validation evidence.
Cross-references: → evidence-class tags, → MRM, → vendor-disclosed metrics.
First appears in: §1.18 sources / §2.14 / §3.5.

**Arize AX** *(Patterns)*
Arize's commercial agent-observability platform. Distinct from Phoenix (the OSS sibling product). The Field Guide does not conflate them.
Cross-references: → Phoenix, → LangSmith, → Langfuse.
First appears in: §2.1.

**AsyncPostgresSaver** *(**Foundations** / Patterns)*
The async variant of `PostgresSaver`, LangGraph's production-default thread checkpointer. Used in production deployments where the agent runtime is asyncio-based.
Cross-references: → PostgresSaver, → checkpointer, → MemorySaver.
First appears in: §1.4 / §1.15.

**Attestation receipt** *(**Production**)*
A cryptographic proof that a runtime, image, or workload is what was approved — typically TEE attestation (Intel TDX, AMD SEV-SNP, NVIDIA Confidential Compute) or SLSA in-toto attestation for build provenance.
Cross-references: → TEE attestation, → signed action chain, → SLSA, → substrate primitive.
First appears in: §3.4.

**Audit-Evidence Cookbook** *(**Production**)*
§3.4. The section that converts agent architecture into operational lifecycle — what gets signed, what gets retained where for how long, what surfaces to which SIEM, reproducibility, examination-day exhibits, incident response, break-glass, exit plan, per-recipe artifact.
Cross-references: → audit-evidence pattern, → Evidence Index, → examination dossier, → MRM.
First appears in: §3.4.

**Audit-evidence pattern** *(**Production**)*
The per-recipe artifact required by §3.4 — Sign-1 through Sign-5 cryptographic chain, chain composition, storage destination, SIEM surface, examiner access pattern, incident response runbook, reproducibility manifest. One per recipe family.
Cross-references: → Audit-Evidence Cookbook, → Evidence Index, → signed action chain, → action provenance.
First appears in: §3.4.

**Autonomy spectrum (the 5-point spectrum)** *(**Foundations**)*
Operational scale describing how much authority the agent holds: Level 0 advisor → Level 1 recommender → Level 2 semi-autonomous → Level 3 autonomous-with-HITL → Level 4 fully autonomous. Regulated production deployments live at Levels 2–3.
Cross-references: → advisor, → recommender, → semi-autonomous, → autonomous-with-HITL, → fully autonomous, → HITL.
First appears in: §1.1.

**Autonomous-with-HITL (autonomy Level 3)** *(**Foundations**)*
Level 3 of the 5-point autonomy spectrum. The agent runs end-to-end, but high-blast-radius actions surface to a human for approval. The modal regulated-production deployment posture.
Cross-references: → autonomy spectrum, → HITL, → interrupt, → fully autonomous.
First appears in: §1.1.

## B

**`BaseStore`** *(**Foundations** / Patterns / Production)*
LangGraph's long-term memory interface — cross-thread state, distinct from the thread checkpointer which holds in-thread state. `InMemoryStore` for dev; `PostgresStore` and `RedisStore` for production. Compiled into a graph via `compile(store=...)`.
Cross-references: → PostgresStore, → RedisStore, → InMemoryStore, → checkpointer, → three-scope state model.
First appears in: §1.4; in production-tier §3.15.

**Benchmark [tag]** *(Foundations / Patterns / Production)*
One of the 10 evidence-class tags. Academic / standards-body / public-benchmark claim — McKinsey survey, OWASP, MITRE ATLAS, AgentDojo, InjecAgent, AgentHarm.
Cross-references: → evidence-class tags.
First appears in: §1.18 / §13 of the design spec.

**Bleed** *(out of scope — see §4.8)*
Term used in some vendor-internal and competitor taxonomies for the same concept this Field Guide names **data-leak surface** or **leakage pathway**. The Field Guide does not use "bleed" in the body; see §4.8 for the explanation of the terminology choice.
Cross-references: → data-leak surface, → leakage pathway, → leak vector.
First appears in: §4.8 only.

**Break-glass** *(**Production**)*
The emergency vendor-SRE access path for an agent deployment, with full audit trail. Categories: customer-mediated, read-on-incident, full-read. Critical for Tier-1 FSI procurement because it determines who can see customer data during an incident.
Cross-references: → vendor support pattern, → SOC 2 Type II, → examination dossier.
First appears in: §3.4.

**Buyer persona** *(**Foundations** / Patterns / Production)*
PM vocabulary. The economic buyer who approves the purchase. Distinct from the end-user persona — the person who actually uses the agent day-to-day. Common confusion: assuming a feature that delights the end-user automatically wins the buyer.
Cross-references: → end-user persona, → JTBD, → ICP, → discovery call.
First appears in: §1.15 PM-track vocabulary.

**BYOC (Bring Your Own Cloud)** *(**Patterns** / Production)*
LangGraph Platform deployment shape where the LangChain control plane runs in LangChain's cloud, but the data plane (graph execution, Postgres checkpointer, state) runs in the customer's cloud. AWS-only as of May 2026; Azure and GCP are roadmap, not shippable.
Cross-references: → BYOC dataplane-listener, → LangGraph Cloud SaaS, → Self-Hosted Enterprise, → BYOC Azure (gap), → BYOC GCP (gap).
First appears in: §2.8; deepened in §3.1.

**BYOC Azure (gap)** *(**Production**)*
Explicit gap as of May 2026. Azure-committed prospects who want BYOC compliance posture cannot get it on LangGraph Platform; they fall back to Self-Hosted Enterprise on AKS or CSP-managed (Foundry Agent Service). A deal-shaping fact for FSI on Azure.
Cross-references: → BYOC, → AKS, → Self-Hosted Enterprise, → CSP-managed.
First appears in: §3.1.

**BYOC GCP (gap)** *(**Production**)*
Explicit gap as of May 2026. GCP-committed prospects cannot get BYOC; they fall back to Self-Hosted Enterprise on GKE or CSP-managed (Vertex Agent Engine). A deal-shaping fact for GCP-resident FSI.
Cross-references: → BYOC, → BYOC Azure (gap), → Self-Hosted Enterprise, → CSP-managed.
First appears in: §3.1.

**BYOC dataplane-listener** *(**Production**)*
The Helm-installed CRD-watching pod that runs inside the customer's Kubernetes cluster in BYOC deployments. Polls the LangChain control-plane API over HTTPS using the customer's `langsmithApiKey` and reacts to deployment-spec changes. The control-plane-to-LangChain egress path that even BYOC deployments retain.
Cross-references: → BYOC, → trace egress, → support / break-glass.
First appears in: §3.1.

## C

**Capstone** *(**Foundations** / Patterns / **Production**)*
The end-of-Production task that requires all three roles (SE / SC / PM) to produce artifacts against the same customer brief whose artifacts must fit together. The actual onboarding-readiness signal. See §3 knowledge gate.
Cross-references: → knowledge gate, → mentor checkpoint.
First appears in: §1.4 (forward reference) / §3 capstone gate.

**Cedar** *(Patterns)*
AWS-authored open-source policy language; ReBAC-capable; the policy substrate for AWS Verified Permissions. One of the FGA-category options alongside OpenFGA, Topaz, Permit.io, Oso, Styra.
Cross-references: → FGA, → OpenFGA, → Topaz, → Permit.io, → ReBAC.
First appears in: §1.9 / §2.4.

**Checkpoint** *(**Foundations** / Patterns)*
A versioned snapshot of LangGraph state at a node transition. Persisted via the checkpointer; replayable for HITL resume, time-travel debugging, and audit reconstruction.
Cross-references: → checkpointer, → state, → thread, → thread_id.
First appears in: §1.4 / §1.5.

**Checkpointer** *(**Foundations** / Patterns)*
The LangGraph component that persists in-thread state across turns. `PostgresSaver` (production default), `RedisSaver` (sub-millisecond alternative), `MemorySaver` and `SqliteSaver` (dev-only). Compiled via `compile(checkpointer=...)`. Distinct from `BaseStore`, which holds cross-thread state.
Cross-references: → PostgresSaver, → RedisSaver, → MemorySaver, → BaseStore, → checkpoint, → three-scope state model.
First appears in: §1.4 / §1.5.

**CIBA (Client-Initiated Backchannel Authentication)** *(**Foundations** / Patterns)*
OAuth flow where the agent backend initiates authentication via a backchannel; the user approves on a separate device (typically a mobile push). Useful for agent-on-behalf-of-user delegation where the agent is acting headless.
Cross-references: → DPoP, → PAR, → RAR, → PKCE, → step-up authentication.
First appears in: §1.9 / §2.4.

**Citation hallucination** *(**Foundations** / Production)*
Failure mode where the agent invents a source or attributes a real finding to the wrong source. The dominant failure mode for the Deep Research recipe. Mata v. Avianca is the canonical legal anchor.
Cross-references: → hallucination, → Mata v. Avianca, → Deep Research recipe.
First appears in: §1.10.4.

**Common-confusion call-out** *(**Foundations** / Patterns)*
Pedagogical pattern: a structured callout box adjacent to a near-neighbor concept pair, naming what each is and what each is **not**. Used throughout the tier files. Examples: `interrupt()` vs `Command(goto=...)`; agent identity vs agent-on-behalf-of-user; ReAct vs Supervisor (Klarna context); buyer persona vs end-user persona.
Cross-references: → near-neighbor concept.
First appears in: §1.12.9.

**Concentration risk (DORA Art. 28(2))** *(**Production**)*
The risk-assessment a financial entity must perform before entering an ICT third-party agreement under DORA Article 28(2). Multi-tenant SaaS deployments (LangGraph Cloud SaaS) struggle to satisfy concentration-risk articulation; BYOC and Self-Hosted Enterprise satisfy it more cleanly.
Cross-references: → DORA, → ICT register entry, → exit plan, → critical ICT-TPP.
First appears in: §3.5.

**Confidence gate** *(**Production**)*
A state-graph node that classifies session confidence and routes low-confidence sessions to a human fallback. The Klarna-lesson-aware HITL placement — added in response to the May 2025 reversal showing that vendor-disclosed launch metrics overstated steady-state performance.
Cross-references: → HITL, → Klarna May 2025 reversal, → autonomous-with-HITL.
First appears in: §3.7.

**ConfusedPilot** *(**Foundations** / Production)*
Named public incident class (2024–2025): a research disclosure showing how agentic copilots can be manipulated by content placed in a tenant's own documents to exfiltrate cross-tenant context. Canonical anchor for the retriever-surface cross-tenant aggregation failure mode.
Cross-references: → cross-tenant aggregation, → retriever surface, → prompt injection (indirect), → named-incident.
First appears in: §1.11 / §9.3 of ref-beginner-foundations.

**Corroborated [tag]** *(Foundations / Patterns / Production)*
One of the 10 evidence-class tags. The claim appears in 2+ independent sources; the tag should cross-reference which evidence-class each source falls into.
Cross-references: → evidence-class tags.
First appears in: §1.18 / §13.

**CPRA (California Privacy Rights Act)** *(**Production**)*
California's privacy regime; supersedes CCPA. Includes automated-decision rules relevant to agent deployments serving California consumers.
Cross-references: → GDPR, → state-patchwork map.
First appears in: §3.5.

**CRAG (Corrective RAG)** *(Patterns)*
Agentic RAG variant; falls back to web search when retrieval confidence is low. A named pattern inside topology 6 (Agentic RAG).
Cross-references: → Agentic RAG, → Self-RAG.
First appears in: §2.2 / §2.11.

**`create_react_agent`** *(**Foundations** / Patterns)*
LangGraph's prebuilt helper that builds a two-node ReAct state graph (model node + tool node) given a model, tool list, and optional checkpointer. The single most-used LangGraph on-ramp.
Cross-references: → ReAct, → StateGraph, → checkpointer, → prebuilt.
First appears in: §1.4.

**Critic** *(**Foundations** / Patterns)*
A graph role: a node that critiques another node's output (Reflexion-style). Distinct from validator (which gates) and replanner (which revises the plan).
Cross-references: → Reflexion, → validator, → replanner.
First appears in: §1.7 / §2.2.

**Critical ICT-TPP (Critical ICT Third-Party Provider)** *(**Production**)*
DORA designation for ICT third-party providers supervised directly by the European Supervisory Authorities. LangChain is not currently designated; the risk that a future LangGraph-volume vendor becomes designated is a procurement consideration.
Cross-references: → DORA, → ICT register entry, → concentration risk.
First appears in: §2.5 / §3.5.

**Cross-tenant aggregation** *(**Foundations** / Patterns / Production)*
The failure mode where state, cache, retrieval, or memory leaks between tenants of a multi-tenant agent deployment. One of the modal failure modes for SaaS agents; the five surfaces — retriever, cache, checkpointer, observability, model — are catalogued in Patterns §2.7 and Production §3.2.
Cross-references: → cross-tenant isolation, → retriever surface, → cache surface, → checkpointer surface, → observability surface, → model surface, → ConfusedPilot.
First appears in: §1.11.

**Cross-tenant isolation** *(**Patterns** / Production)*
The discipline of preventing cross-tenant aggregation across all five surfaces. Cannot be solved at the authorization decision layer alone — each surface needs its own per-tenant binding.
Cross-references: → cross-tenant aggregation, → FGA, → cross-tenant isolation surfaces.
First appears in: §2.7 (Patterns) / §3.2 (Production).

**CSP-managed** *(**Production**)*
The deployment shape where the cloud service provider operates the agent runtime — AWS Bedrock AgentCore, GCP Vertex Agent Engine, Azure AI Foundry Agent Service. Loses LangGraph topology vocabulary; gains CSP-managed identity, secrets, and trace surfaces. One row of the §3.1 10 × 9 matrix.
Cross-references: → BYOC, → Self-Hosted Enterprise, → 10-axis deployment matrix, → Bedrock AgentCore, → Vertex Agent Engine, → Foundry Agent Service.
First appears in: §3.1.

## D

**Data-leak surface** *(**Foundations** / Patterns / Production)*
The Field Guide's canonical public term for any architectural surface where regulated, sensitive, or proprietary data can escape its intended boundary. Used throughout the book. The OWASP / MITRE-aligned public-vocabulary phrasing.
Cross-references: → leakage pathway, → leak vector, → cross-tenant aggregation, → telemetry capture, → prompt injection.
First appears in: §1.11.

**Data perimeter** *(**Production**)*
Axis 3 of the 10-axis deployment-shape matrix. Where retrieval / state / checkpointer data physically resides.
Cross-references: → 10-axis deployment matrix, → trace egress, → identity perimeter, → secret perimeter.
First appears in: §3.1.

**`deepagents`** *(Patterns)*
LangChain's Plan-and-Execute harness with `write_todos`, sub-agents, and file-system memory. The community treats `deepagents` as graduating to "topology 8" — emerging beyond the 7 canonical topologies.
Cross-references: → Plan-and-Execute, → topology 8 emergence, → topology 3.
First appears in: §2.2.

**Deep Research recipe (Recipe 4)** *(**Foundations** / Patterns / Production)*
The Multi-Agent Deep Research recipe — Plan-and-Execute with `deepagents`-shape harness, dominant failure mode is citation hallucination. Anchor customers: Captide (FSI research), Morningstar Mo (wealth research), Exa.
Cross-references: → 6 recipe families, → Plan-and-Execute, → deepagents, → citation hallucination.
First appears in: §1.10.4.

**DFSA (Dubai Financial Services Authority)** *(**Production**)*
Dubai's financial-services regulator. Code of Conduct for AI applicable to agent deployments serving DIFC-licensed entities.
Cross-references: → APAC/Gulf regimes, → SAMA, → MAS, → HKMA.
First appears in: §3.5.

**Discovery call** *(**Foundations**)*
PM vocabulary. The first sales conversation; the SE / SC role is to surface the use case, the technical fit, and the relevant compliance gates.
Cross-references: → buyer persona, → end-user persona, → JTBD, → ICP.
First appears in: §1.15.

**DLP (Data Loss Prevention)** *(**Production**)*
Egress-layer scanning for regulated data leaving a perimeter. Forcepoint, Symantec, McAfee, Microsoft Purview DLP, Proofpoint. Compressed reference in §3.3 Integration Cookbook.
Cross-references: → telemetry capture, → network egress, → SIEM.
First appears in: §3.3.

**DORA (Digital Operational Resilience Act)** *(Patterns / **Production**)*
EU Regulation 2022/2554; fully applicable January 17, 2025. The dominant FSI compliance regime for EU-resident agent deployments. Articles 5 (governance), 6 (ICT risk-management framework), 9 (protection), 10 (detection), 19 (ICT incident reporting), 24–26 (TLPT), 28 (third-party register + exit plan), 30 (contractual arrangements) are the most operative for an agent deployment.
Cross-references: → ICT register entry, → concentration risk, → critical ICT-TPP, → TLPT, → exit plan.
First appears in: §2.5; deepened in §3.5.

**DPDPA (Digital Personal Data Protection Act)** *(**Production**)*
India's data-protection regime (2023). Applicable to agent deployments processing data of Indian residents.
Cross-references: → APAC/Gulf regimes, → PIPL, → PDPA.
First appears in: §3.5.

**DPIA (Data Protection Impact Assessment)** *(**Production**)*
GDPR Article 35 obligation; required for high-risk processing. The Field Guide ships a DPIA template applicable to a LangGraph agent.
Cross-references: → GDPR, → examination dossier.
First appears in: §3.5.

**DPoP (Demonstrating Proof-of-Possession)** *(**Foundations** / Patterns)*
[IETF RFC 9449](https://datatracker.ietf.org/doc/html/rfc9449) (September 2023). OAuth token-binding mechanism — binds an access token to a key pair so a stolen token cannot be replayed by an attacker who does not hold the private key. Material for agent deployments where token theft is a credible threat.
Cross-references: → OAuth 2.x, → PAR, → RAR, → CIBA, → PKCE.
First appears in: §1.9 / §2.4.

## E

**EchoLeak (CVE-2025-32711)** *(**Foundations** / Production)*
Named public incident (June 2025). First documented zero-click prompt-injection exploit in a production LLM system (Microsoft 365 Copilot). The canonical anchor for indirect prompt injection at production scale.
Cross-references: → prompt injection (indirect), → named-incident, → first-60-minutes runbook.
First appears in: §1.11; operational role-play uses it in §3.13.

**EKS (Amazon Elastic Kubernetes Service)** *(Patterns / **Production**)*
AWS's managed Kubernetes service. Self-Hosted Enterprise LangGraph on EKS is the modal AWS deployment for FSI prospects who need full data-perimeter sovereignty.
Cross-references: → AKS, → BYOC, → Self-Hosted Enterprise.
First appears in: §2.8 / §3.1.

**Elicitation (MCP elicitation)** *(**Foundations** / Patterns)*
MCP mechanism (Q4 2025 spec addition) for interactive mid-tool-call input from the user. Distinct from MCP sampling (server requests an LLM call) and MCP tools (client invokes a callable).
Cross-references: → MCP, → MCP sampling, → MCP primitives.
First appears in: §1.6.

**ELSER (Elastic Learned Sparse EncodeR)** *(Patterns)*
Elastic's sparse encoder for hybrid search; paired with BM25 in the Elastic AI Assistant deployment.
Cross-references: → Elastic AI Assistant, → SOC Agent recipe.
First appears in: §2.11.

**End-user persona** *(**Foundations**)*
PM vocabulary. The person who actually uses the agent day-to-day. Often distinct from the buyer persona. The Field Guide teaches the buyer-vs-end-user disambiguation in Foundations because the PM-track gate requires it.
Cross-references: → buyer persona, → JTBD, → ICP, → discovery call.
First appears in: §1.15.

**`@entrypoint` / `@task`** *(**Foundations** / Patterns)*
LangGraph Functional API decorators. The imperative authoring path — alternative to the explicit `StateGraph` / `add_node` / `add_edge` Graph API. Shipped GA in langgraph v0.3.
Cross-references: → Functional API, → Graph API, → StateGraph.
First appears in: §1.4.

**Entra Agent ID** *(**Foundations** / Patterns)*
Microsoft's first-party agent identity primitive in Entra ID, GA 2025. Peer to Okta for AI Agents and Auth0 for AI Agents.
Cross-references: → Okta for AI Agents, → Auth0 for AI Agents, → Ping AIC, → agent identity (workload), → workforce identity.
First appears in: §1.9 / §2.4.

**Escalation** *(**Foundations**)*
The HITL pattern where the agent routes the case to a human agent for resolution rather than continuing autonomously. The Customer Support recipe's modal HITL pattern.
Cross-references: → HITL, → approval, → confidence gate.
First appears in: §1.7 / §1.10.

**EU AI Act** *(Patterns / **Production**)*
EU Regulation 2024/1689. Articles 9–16 cover risk management, data governance, technical documentation, record-keeping, transparency, human oversight, accuracy/robustness/cybersecurity for high-risk systems. Article 26 covers deployer obligations. Annex III lists high-risk categories.
Cross-references: → Annex III, → high-risk system, → human oversight, → GDPR, → DORA.
First appears in: §2.5; deepened in §3.5.

**Evaluator** *(**Foundations** / Patterns / **Production**)*
Curriculum vocabulary. The named role that grades a knowledge gate — team lead (Foundations), peer with Patterns mastery (Patterns), SE veteran + CISO-trained mentor (Production). Self-assessment is named honestly when used; never the primary mode.
Cross-references: → knowledge gate, → mentor checkpoint, → rubric, → inter-rater reliability.
First appears in: §1.16.

**Evidence-class tags (the 10 citation classes)** *(**Foundations** / Patterns / Production)*
The 10 markers used throughout the Field Guide to tag every factual claim by evidence weight: `[primary-regulatory]`, `[independently-audited]`, `[vendor-contractual]`, `[vendor-public]`, `[named-incident]`, `[customer-produced-evidence]`, `[corroborated]`, `[reference design]`, `[architectural inference]`, `[benchmark]`. See §4.3.
Cross-references: → primary-regulatory, → independently-audited, → vendor-contractual, → vendor-public, → named-incident, → customer-produced-evidence, → corroborated, → reference design, → architectural inference, → benchmark.
First appears in: §1.18 / §13 of the design spec.

**Evidence Index** *(**Production**)*
§3.4.11 — the per-recipe one-page artifact that lists every artifact a regulator can ask for, where it lives, who retrieves it, and the retention window. Architects hand it to compliance; examiners use it as a request checklist.
Cross-references: → Audit-Evidence Cookbook, → examination dossier, → audit-evidence pattern.
First appears in: §3.4.

**Examination dossier** *(**Production**)*
The bundle the agent-owning team produces during a regulator examination — model inventory, ICT register entry, sub-processor list, incident log, model-swap log, data-leak-surface mapping, threat model, DPIA, exit plan, retention policy. The §3.13 Day-90 operational role-play tests the team's ability to produce this in 48 hours.
Cross-references: → Evidence Index, → Audit-Evidence Cookbook, → operational-lifecycle role-play.
First appears in: §3.4.

**Executor** *(**Foundations** / Patterns)*
A graph role in the Plan-and-Execute topology — the node that executes individual plan steps the planner produced.
Cross-references: → planner, → replanner, → Plan-and-Execute.
First appears in: §1.7.

**Exit plan (DORA Art. 28(8))** *(**Production**)*
The documented exit strategy a financial entity must have for every ICT third-party arrangement under DORA. Covers data portability, runtime portability, evidence portability. The Field Guide provides a reference 90-day timeline LangGraph + LangSmith → Langfuse + customer-hosted on Azure.
Cross-references: → DORA, → ICT register entry, → concentration risk.
First appears in: §3.4.

## F

**FedRAMP-High** *(**Production**)*
US federal cloud-security authorization. As of May 2026, **no public FedRAMP authorization exists for LangGraph Platform** — this is the canonical `[primary-regulatory + explicit gap]` callout in the Field Guide.
Cross-references: → NIST SP 800-53, → IL4/IL5, → StateRAMP.
First appears in: §3.5.

**FGA (Fine-Grained Authorization)** *(**Foundations** / Patterns / Production)*
Authorization decisions based on relationships and attributes, not just roles. The category that solves agent-on-behalf-of-user delegation. Named products: OpenFGA, Cedar / AWS Verified Permissions, Topaz, Okta FGA, Auth0 FGA, Permit.io, Oso, Styra.
Cross-references: → ReBAC, → OpenFGA, → Cedar, → Topaz, → Permit.io, → Oso, → Styra, → agent-on-behalf-of-user identity.
First appears in: §1.9; deepened in §2.4.

**FGA modeling exercise** *(**Production**)*
The per-recipe artifact that writes the ReBAC type system explicitly — user, tenant, document, document-section, agent, agent-context, tool, tool-invocation, plus relations. Published in the Field Guide for Recipe 3 (Text-to-SQL) and Recipe 5 (Embedded SaaS Copilot).
Cross-references: → FGA, → ReBAC, → cross-tenant isolation.
First appears in: §3.2.

**FINRA** *(**Production**)*
US Financial Industry Regulatory Authority. Rules most operative for agent deployments: 4511 (books and records), 4530 (reporting), 5280 (information barriers), 3110 (supervision), 3120 (supervisory controls).
Cross-references: → SEC 17a-4(f), → SR 11-7, → information barrier, → WORM.
First appears in: §3.5.

**First-60-minutes runbook** *(**Production**)*
The §3.4.7 incident-response runbook for an EchoLeak-class detection — trace query patterns, plan-deviation queries, retrieval anomaly queries, output classifications, correlation with SIEM events outside the agent. Tested in the Production operational-lifecycle role-play Day 1.
Cross-references: → operational-lifecycle role-play, → SIEM, → EchoLeak.
First appears in: §3.4.

**Foundry Agent Service** *(**Production**)*
Microsoft's CSP-managed agent runtime in Azure AI Foundry. The Azure-native alternative when BYOC-Azure is gap-blocked. Loses LangGraph topology vocabulary.
Cross-references: → CSP-managed, → BYOC Azure (gap), → Vertex Agent Engine, → Bedrock AgentCore.
First appears in: §3.1.

**FSI (Financial Services Industry)** *(**Foundations** / Patterns / Production)*
One of the 4 ICP industries. Sub-segments: payments (Klarna), wealth (Morningstar), research (Captide), institutional asset management. Distinct regulator stacks per sub-segment.
Cross-references: → ICP, → Healthcare, → ISV, → Sovereign, → 10 personas.
First appears in: §1.12.

**Fully autonomous (autonomy Level 4)** *(**Foundations**)*
Level 4 of the 5-point autonomy spectrum. No human in the loop on any action. Rare in regulated production; common in research environments and developer-tooling sandboxes.
Cross-references: → autonomy spectrum, → autonomous-with-HITL.
First appears in: §1.1.

**Function calling** *(**Foundations**)*
LLM-native tool calling — the LLM emits structured JSON describing the function to invoke and the arguments. OpenAI's productization of the Toolformer thesis. Distinct from MCP, which is a cross-vendor protocol layered above function calling.
Cross-references: → tool, → tool call, → MCP, → Toolformer.
First appears in: §1.6.

**Functional API** *(**Foundations** / Patterns)*
LangGraph's imperative authoring surface — `@entrypoint` decorates the entry function, `@task` decorates step functions. The alternative to the explicit Graph API. ~40%+ of new LangGraph deployments per LangGraph-DevRel #4. Shipped GA in langgraph v0.3.
Cross-references: → Graph API, → `@entrypoint` / `@task`, → StateGraph.
First appears in: §1.4.

## G

**GDPR (General Data Protection Regulation)** *(**Production**)*
EU Regulation 2016/679. Articles most operative for agent deployments: 5(1)(b) purpose limitation, 6 lawful basis, 22 automated decision-making, 28 multi-vendor BAA/DPA chain, 30 records of processing, 35 DPIA, 44–49 international transfers.
Cross-references: → DPIA, → EU AI Act, → CPRA, → state-patchwork map.
First appears in: §3.5.

**Graph API** *(**Foundations** / Patterns)*
LangGraph's explicit authoring surface — `StateGraph`, `add_node`, `add_edge`, `add_conditional_edges`, `Command(goto=...)`, `compile(checkpointer=...)`. The complement to the Functional API.
Cross-references: → Functional API, → StateGraph, → Command goto.
First appears in: §1.4.

## H

**Hallucination** *(**Foundations** / Patterns / Production)*
LLM produces a false claim presented as fact. Distinct from hallucination-to-action — a hallucination that triggers a real-world action.
Cross-references: → hallucination-to-action, → citation hallucination, → Mata v. Avianca.
First appears in: §1.11.

**Hallucination-to-action** *(**Foundations** / Production)*
Hallucination that triggers a real-world action — refund, transaction, message sent, database write. The agent-specific extension of the hallucination failure mode. Replit's May 2025 production-DB-deletion incident is the canonical anchor.
Cross-references: → hallucination, → autonomous-with-HITL, → HITL, → blast radius.
First appears in: §1.11.

**Healthcare (ICP industry)** *(**Foundations** / Production)*
One of the 4 ICP industries. Sub-segments: analytics (Vizient, Komodo de-identified longitudinal), patient-facing copilot (Doctolib — non-PHI gated). PHI flows are marked `[reference design — not in PHI production anywhere on any framework]`.
Cross-references: → ICP, → PHI gap, → HIPAA, → de-identification.
First appears in: §1.12.

**Hierarchical (topology 5)** *(**Foundations** / Patterns)*
Topology 5 of the 7 canonical LangGraph topologies. Supervisor-of-supervisors structure; recursive. Used at Uber AutoCover and ServiceNow.
Cross-references: → Supervisor, → Network (Swarm), → 7 LangGraph topologies.
First appears in: §1.7 / §2.2.

**High-risk system** *(**Production**)*
EU AI Act categorization — Annex III lists the high-risk categories. Triggers Articles 9–16 obligations on risk management, data governance, technical documentation, record-keeping, transparency, human oversight, accuracy / robustness / cybersecurity.
Cross-references: → EU AI Act, → Annex III, → human oversight.
First appears in: §3.5.

**HIPAA (Health Insurance Portability and Accountability Act)** *(**Production**)*
US health-data privacy regime. 45 CFR Part 164 — §164.308 administrative, §164.310 physical, §164.312 technical, §164.314 BAA, §164.316 documentation. The Field Guide reference-design PHI deployment section (§3.12) walks the controls.
Cross-references: → PHI gap, → BAA chain, → de-identification.
First appears in: §3.5.

**HITL (Human-in-the-Loop)** *(**Foundations** / Patterns / Production)*
The pattern where the agent pauses, surfaces what it is about to do, and waits for human approval, escalation, or modification before continuing. Implemented in LangGraph via `interrupt()` and `Command(resume=...)`.
Cross-references: → interrupt, → resume, → approval, → escalation, → confidence gate, → autonomous-with-HITL.
First appears in: §1.7.

**HitL surface** *(**Production**)*
Axis 9 of the 10-axis deployment-shape matrix. Where human-in-the-loop checkpoints surface to humans — Slack, Microsoft Teams, custom UI, LangGraph Studio approve-link.
Cross-references: → 10-axis deployment matrix, → HITL, → LangGraph Studio.
First appears in: §3.1.

**HKMA (Hong Kong Monetary Authority)** *(**Production**)*
Hong Kong's banking regulator. Supervisory Policy Manual SA-2 and Generative AI consultation are most operative for HK-resident FSI agent deployments.
Cross-references: → APAC/Gulf regimes, → MAS, → DFSA, → SAMA.
First appears in: §3.5.

**HLTM (Hierarchical Long-Term Semantic Memory)** *(Patterns)*
LinkedIn's tree-indexed semantic-memory architecture for the Hiring Assistant. Named instance of `BaseStore`-style long-term memory at production scale.
Cross-references: → BaseStore, → long-term memory.
First appears in: §2.11.

**HSM-backed signing chain** *(**Production**)*
The Sign-1 through Sign-5 cryptographic action chain anchored in a Hardware Security Module — AWS CloudHSM, Azure Dedicated HSM, GCP Cloud HSM, Thales Luna, Yubico HSM. The procurement-grade implementation of action provenance.
Cross-references: → action provenance, → signed action chain, → audit-evidence pattern.
First appears in: §3.4.

**Human oversight** *(**Production**)*
EU AI Act Article 14 obligation for high-risk systems. The Field Guide maps human oversight to HITL placement, the confidence gate, and the escalation path in the per-regime depth chapters.
Cross-references: → HITL, → confidence gate, → EU AI Act, → high-risk system.
First appears in: §3.5.

## I

**ICP (Ideal Customer Profile)** *(**Foundations**)*
PM vocabulary. The customer segment the product is built for. In the Field Guide the 4 ICP industries are FSI, Healthcare, ISV, Sovereign, broken down further into 10 personas × 6 recipes × per-recipe segment variants.
Cross-references: → FSI, → Healthcare, → ISV, → Sovereign, → 10 personas, → 6 recipe families.
First appears in: §1.15.

**ICT register entry (DORA Art. 28)** *(**Production**)*
The per-sub-processor record a financial entity maintains under DORA Article 28. Must include service description, criticality, exit plan reference, sub-processor chain.
Cross-references: → DORA, → concentration risk, → exit plan.
First appears in: §3.5.

**Identity perimeter** *(**Production**)*
Axis 2 of the 10-axis deployment-shape matrix. Where agent and human authentication terminates.
Cross-references: → 10-axis deployment matrix, → data perimeter, → trace egress.
First appears in: §3.1.

**IL4 / IL5 (Impact Level 4 / 5)** *(**Production**)*
US DoD Cloud Computing Security Requirements Guide impact levels. IL4 covers CUI; IL5 covers higher-sensitivity CUI plus national-security systems.
Cross-references: → FedRAMP-High, → NIST SP 800-53, → StateRAMP.
First appears in: §3.5.

**Incident Classification Guide** *(**Production**)*
§3.6 supplement — per-failure-mode matrix of when the customer triggers DORA Art. 19, NIS2 Art. 23, SEC Reg S-P 30-day, NYDFS Part 500.17, GDPR Art. 33-34, CCPA, state-specific notifications. The matrix the SOC uses.
Cross-references: → SOC Agent recipe, → DORA, → SIEM, → operational-lifecycle role-play.
First appears in: §3.6.

**Independently-audited [tag]** *(Foundations / Patterns / Production)*
One of the 10 evidence-class tags. Third-party audited claim — SOC 2 attestation, ISO 27001 certification, FedRAMP authorization, EBA AIF audit. Highest evidence weight, scope-limited.
Cross-references: → evidence-class tags, → SOC 2, → ISO 27001.
First appears in: §1.18 / §13.

**Information barrier** *(**Production**)*
FINRA Rule 5280 (and historical Chinese-wall) construct. Prevents flow of material non-public information across business lines. Cross-tenant isolation in an FSI agent deployment must respect information barriers across business lines, not just across customers.
Cross-references: → cross-tenant isolation, → FINRA, → SEC.
First appears in: §3.5.

**InMemoryStore** *(**Foundations**)*
The dev-only `BaseStore` implementation. Lost on process restart. Never used in production.
Cross-references: → BaseStore, → PostgresStore, → RedisStore.
First appears in: §1.4.

**Inter-rater reliability** *(Patterns / **Production**)*
Curriculum vocabulary. Cohen's-kappa target ≥ 0.7 on the Production gate. A study runs before publish. Without it, the gate is not evaluator-portable.
Cross-references: → evaluator, → rubric, → knowledge gate.
First appears in: §3 capstone gate.

**Interrupt (`interrupt(value)`)** *(**Foundations** / Patterns)*
LangGraph primitive that pauses execution mid-node and surfaces a value to the calling code. The HITL mechanism. Distinct from `Command(goto=...)` (in-node dynamic routing — unrelated to pause/resume).
Cross-references: → resume, → Command goto, → HITL, → approval.
First appears in: §1.4.

**Insurance gap** *(**Production**)*
§3.10 — the analysis of why the insurance ICP segment has no documented production LangGraph deployment, the structural reasons, and the conditions under which it changes. Distinct from the Sovereign gap and PHI gap.
Cross-references: → Sovereign gap, → PHI gap, → ICP, → FSI.
First appears in: §3.10.

**ISO 27001** *(Patterns / Production)*
International information-security-management standard. Tier-1 FSI procurement reflex; certification is `[independently-audited]`-class evidence.
Cross-references: → SOC 2, → independently-audited.
First appears in: §2.5.

**ISV (Independent Software Vendor)** *(**Foundations** / Patterns / Production)*
One of the 4 ICP industries. Sub-motions covered at depth: horizontal B2B SaaS, developer tools. Compressed sub-motions: vertical SaaS, data infrastructure, AI-native.
Cross-references: → ICP, → FSI, → Healthcare, → Sovereign.
First appears in: §1.12.

## J

**JTBD (Jobs to Be Done)** *(**Foundations** / Patterns / Production)*
PM vocabulary, Christensen lineage. The framework for stating user needs as jobs: *"When [situation], I want to [motivation], so I can [outcome]."* Every recipe in the Field Guide opens with a JTBD sentence for both end-user and buyer.
Cross-references: → buyer persona, → end-user persona, → ICP, → discovery call.
First appears in: §1.10.

## K

**Klarna May 2025 reversal** *(**Foundations** / Patterns / **Production**)*
The canonical case of a vendor-disclosed launch metric being publicly walked back. Klarna's CEO conceded that the AI-replaces-headcount framing overstated steady-state performance. The teaching the Field Guide commits to: **vendor-disclosed metrics are not MRM-validation evidence**.
Cross-references: → MRM, → vendor-disclosed metrics, → confidence gate, → Customer Support recipe.
First appears in: §1.10; §3.9 dedicated section.

**Knowledge gate** *(**Foundations** / Patterns / Production)*
The end-of-tier evaluation. Model brief + A/B/C model answers + named evaluator + 5–7 criterion rubric (pass / partial / fail) + retake mechanic + PM-track variant. Production adds whiteboard test + operational-lifecycle role-play + capstone.
Cross-references: → model answer, → rubric, → evaluator, → mentor checkpoint, → capstone.
First appears in: §1.16.

## L

**Lang Effect** *(Patterns)*
Uber's internal framework wrapping LangGraph + LangChain for internal-system integration. Named anchor for "wrapped-LangGraph at scale" patterns.
Cross-references: → Uber Validator + AutoCover.
First appears in: §2.11.

**LangGraph** *(**Foundations** / Patterns / Production)*
LangChain's open-source graph-based agent framework. The Field Guide's anchor framework — 18 of 18 named production deployments in the corpus are LangGraph.
Cross-references: → LangGraph Cloud SaaS, → BYOC, → Self-Hosted Enterprise, → Functional API, → Graph API.
First appears in: §1.3.

**LangGraph Cloud SaaS** *(**Patterns** / Production)*
LangGraph Platform deployment shape — control plane and data plane both operated by LangChain on GCP / AWS. Fastest time to market; smallest perimeter you can defend in a Tier-1 procurement. Trace egress to LangSmith Cloud is mandatory.
Cross-references: → BYOC, → Self-Hosted Enterprise, → Self-Hosted Lite, → Developer Tier, → 10-axis deployment matrix.
First appears in: §2.8 / §3.1.

**LangGraph Studio** *(**Foundations** / Patterns)*
The visual debugger for LangGraph. Every demo at LangChain Interrupt 2025 used Studio; non-negotiable per LangGraph-DevRel #4.
Cross-references: → langgraph dev/up/build, → LangSmith.
First appears in: §1.4.

**langgraph dev / up / build** *(**Foundations**)*
LangGraph CLI commands. `langgraph dev` runs the local dev loop; `langgraph up` deploys; `langgraph build` produces the artifact for deploy targets.
Cross-references: → LangGraph Studio, → langgraph.json.
First appears in: §1.4.

**`langgraph-mcp-adapters`** *(Patterns)*
LangChain library that bridges MCP `ToolMessage` to LangChain `ToolMessage`. **NOT** the MCP substrate — a thin adapter layered above the MCP SDKs. Naming the adapter as substrate is a credibility miss in customer conversations.
Cross-references: → MCP, → MCP server SDKs.
First appears in: §2.11.

**Langfuse** *(**Foundations** / Patterns / Production)*
OSS / self-hostable agent observability platform. The named alternative to LangSmith for customers who need self-hosted trace storage (Self-Hosted Enterprise, Sovereign air-gap).
Cross-references: → LangSmith, → Phoenix, → Arize AX, → OTel GenAI conventions.
First appears in: §1.8.

**LangSmith** *(**Foundations** / Patterns / Production)*
LangChain's first-party trace + eval platform. Near-monopoly inside LangGraph deployments. Mandatory trace destination in LangGraph Cloud SaaS; configurable in BYOC and Self-Hosted Enterprise.
Cross-references: → Langfuse, → Phoenix, → Arize AX, → OTel GenAI conventions, → trace egress.
First appears in: §1.8.

**Leakage pathway** *(**Foundations** / Patterns / Production)*
Secondary public phrasing for the same concept as data-leak surface. Used interchangeably with data-leak surface in the Field Guide. The OWASP / EU AI Act / MITRE ATLAS aligned vocabulary.
Cross-references: → data-leak surface, → leak vector.
First appears in: §1.11.

**Leak vector** *(Patterns / Production)*
A specific instance of a leakage pathway — the named exploit path, named primitive, or named misconfiguration that turns a data-leak surface into an actual exfiltration.
Cross-references: → data-leak surface, → leakage pathway.
First appears in: §2.7 / §3.6.

**LF AAIF (Linux Foundation Agentic AI Foundation)** *(**Foundations** / Patterns)*
The Linux Foundation project home (formed December 2025) for the three-layer protocol stack — A2A, MCP, AGP/AGNTCY all sit under LF AAIF.
Cross-references: → MCP, → A2A, → AGP, → AGNTCY.
First appears in: §1.6.

**LLM (Large Language Model)** *(**Foundations** / Patterns / Production)*
The model that drives the agent loop. May 2026 cohort referenced throughout: Claude 4.7 (Anthropic), GPT-5 (OpenAI), Gemini 3.0 (Google DeepMind). The Field Guide pins claims to the May 2026 cohort.
Cross-references: → model perimeter, → model swap.
First appears in: §1.2.

**Long-term memory** *(**Foundations** / Patterns)*
Cross-thread memory. The agent's persistent recall across conversations and sessions. Implemented via `BaseStore`. Distinct from the thread checkpointer (in-thread state) and the scratchpad (intra-step state).
Cross-references: → BaseStore, → PostgresStore, → RedisStore, → three-scope state model.
First appears in: §1.5.

## M

**MAS (Monetary Authority of Singapore)** *(**Production**)*
Singapore's central bank and financial-services regulator. TRM Guidelines 2021 §11 + FEAT principles + Veritas + Model AI Governance Framework + Notice PSN05 are most operative for SG-resident FSI agent deployments.
Cross-references: → APAC/Gulf regimes, → HKMA, → DFSA, → SAMA.
First appears in: §3.5.

**Mata v. Avianca** *(**Foundations** / Production)*
Named public incident (2023, S.D.N.Y.). Lawyers sanctioned for filing brief containing ChatGPT-hallucinated case citations. Canonical anchor for the citation-hallucination failure mode in the Deep Research recipe.
Cross-references: → citation hallucination, → hallucination, → named-incident, → Deep Research recipe.
First appears in: §1.11 / §9.3.

**MCP (Model Context Protocol)** *(**Foundations** / Patterns / Production)*
JSON-RPC protocol from Anthropic (November 2024) for exposing tools, resources, and prompts to LLM clients. Donated to the Linux Foundation Agentic AI Foundation in December 2025. The **middle layer** of the three-layer protocol stack — above AGP transport, below A2A agent-to-agent.
Cross-references: → A2A, → AGP, → three-layer protocol stack, → MCP server, → MCP client, → MCP host, → MCP primitives, → MCP Authorization, → MCP elicitation, → MCP sampling.
First appears in: §1.6.

**MCP Authorization** *(**Foundations** / Patterns)*
The OAuth 2.1 + Dynamic Client Registration + RFC 9728 metadata specification for MCP server / client identity. Ratified Q1 2026; production-deployment evidence remains thin.
Cross-references: → MCP, → OAuth 2.x, → DPoP.
First appears in: §1.6 / §2.4.

**MCP client** *(**Foundations** / Patterns)*
The component embedded inside the agent runtime that invokes MCP servers via JSON-RPC.
Cross-references: → MCP, → MCP server, → MCP host.
First appears in: §1.6.

**MCP elicitation** *(**Foundations** / Patterns)*
MCP feature (Q4 2025 spec addition) — the server requests interactive input from the user mid-tool-call.
Cross-references: → MCP, → MCP sampling, → MCP primitives.
First appears in: §1.6.

**MCP host** *(**Foundations**)*
The user-facing app (Claude Desktop, Cursor, LangGraph Studio) that mediates between the user and the MCP clients running inside agents.
Cross-references: → MCP, → MCP client, → MCP server.
First appears in: §1.6.

**MCP primitives (resources, tools, prompts)** *(**Foundations** / Patterns)*
The three canonical MCP primitive types. Resources are readable data sources; tools are callable functions; prompts are pre-templated prompts. Required vocabulary per LangGraph-DevRel #3.2.
Cross-references: → MCP resource, → MCP tool, → MCP prompt, → MCP.
First appears in: §1.6.

**MCP prompt** *(**Foundations**)*
A pre-templated prompt exposed by an MCP server, parameterized at invocation time. One of the three MCP primitives.
Cross-references: → MCP primitives, → MCP tool, → MCP resource.
First appears in: §1.6.

**MCP resource** *(**Foundations**)*
A readable data source exposed by an MCP server (file, database query, API response). One of the three MCP primitives.
Cross-references: → MCP primitives, → MCP tool, → MCP prompt.
First appears in: §1.6.

**MCP sampling** *(**Foundations** / Patterns)*
MCP feature where the server requests an LLM call from the client (an inversion of the usual direction). Useful for server-side reasoning that needs the client's model and context.
Cross-references: → MCP, → MCP elicitation.
First appears in: §1.6.

**MCP server** *(**Foundations** / Patterns)*
A process exposing tools, resources, and prompts via the MCP protocol. The substrate is the MCP server SDKs (Python, TypeScript, Java, Go, C#) — not `langchain-mcp-adapters`.
Cross-references: → MCP, → MCP client, → MCP host, → langgraph-mcp-adapters.
First appears in: §1.6.

**MCP tool** *(**Foundations** / Patterns)*
A callable function exposed by an MCP server, invoked by the MCP client inside the agent. One of the three MCP primitives. The most-used primitive in practice.
Cross-references: → MCP primitives, → tool, → tool call, → function calling.
First appears in: §1.6.

**`MemorySaver`** *(**Foundations**)*
The dev-only in-memory thread checkpointer. Lost on process restart. **Not for production.** The Field Guide teaches the `MemorySaver` → `PostgresSaver` migration story explicitly.
Cross-references: → checkpointer, → PostgresSaver, → SqliteSaver.
First appears in: §1.4 / §1.5.

**Mentor checkpoint** *(**Foundations** / Patterns / Production)*
Curriculum vocabulary. A scheduled 20–45 min mentor conversation invitation at four named points: post-Foundations gate, post-Identity section, pre-Production whiteboard, post-Production gate. ~2.5 hours mentor time per new hire total.
Cross-references: → knowledge gate, → evaluator, → capstone.
First appears in: §1.17.

**`MessagesState`** *(**Foundations** / Patterns)*
LangGraph's default state schema — a `messages: list[BaseMessage]` field with the `add_messages` reducer. The schema most starter agents use.
Cross-references: → StateGraph, → add_messages reducer, → state.
First appears in: §1.4.

**Microsoft Agent Framework (MAF)** *(Patterns)*
Microsoft's 2026 agent framework. AutoGen v0.4 folded into MAF Python preview Q1 2026; non-trivial migration. Distinct from AutoGen.
Cross-references: → AutoGen.
First appears in: §2.1.

**MITRE ATLAS (Adversarial Threat Landscape for AI Systems)** *(**Foundations** / Patterns / Production)*
MITRE-maintained adversarial threat-and-mitigation knowledge base for AI systems, modelled on the ATT&CK framework. The reference vocabulary for *attack-pattern* discussions with CISOs and SOC analysts — tactics, techniques, mitigations. Includes named case-study writeups for several of the Field Guide's named-incident anchors. URL: [`https://atlas.mitre.org/`](https://atlas.mitre.org/).
Cross-references: → OWASP LLM Top 10, → OWASP Agentic Top 10, → STRIDE-A, → named-incident [tag], → data-leak surface.
First appears in: §2.4 / §2.7 / §3.

**MiFID II** *(**Production**)*
EU Markets in Financial Instruments Directive. Article 16(7), 16(11), and RTS 6 are most operative for algorithmic-trading agent deployments — testing, kill-switch, pre-deployment protocol, governance docs.
Cross-references: → SR 11-7, → FINRA, → SEC.
First appears in: §3.5.

**Model answer** *(**Foundations** / Patterns / Production)*
Curriculum vocabulary. The published A-grade reference answer for a knowledge gate sample brief. A-only is insufficient — the Field Guide ships A / B / C model answers with explicit annotations on why B is not A and why C fails.
Cross-references: → knowledge gate, → rubric, → evaluator.
First appears in: §1.16.

**Model brief** *(**Foundations** / Patterns / Production)*
Curriculum vocabulary. The customer scenario presented in a knowledge gate. 1 paragraph in Foundations; 2 pages in Patterns; 3 pages in Production.
Cross-references: → knowledge gate, → model answer, → rubric.
First appears in: §1.16.

**Model perimeter** *(**Production**)*
Axis 7 of the 10-axis deployment-shape matrix. Where LLM inference physically executes — including Bedrock cross-region inference profile as an explicit value.
Cross-references: → 10-axis deployment matrix, → trace egress, → data perimeter.
First appears in: §3.1.

**Model surface (cross-tenant)** *(**Patterns** / Production)*
One of the 5 cross-tenant isolation surfaces. Per-tenant model fine-tune isolation; per-tenant prompt-cache partitioning (Anthropic / OpenAI / Bedrock prompt caching all need per-tenant keys); KV-cache leakage across requests.
Cross-references: → cross-tenant isolation, → retriever surface, → cache surface, → checkpointer surface, → observability surface.
First appears in: §2.7 / §3.2.

**Model-swap protocol** *(**Production**)*
SR 11-7 §III.5 procedure for changing `model_version_hash` — validation, second-line concurrence, regulator notification, rollback criterion. The §3.13 Day-30 operational role-play tests it.
Cross-references: → MRM, → SR 11-7, → operational-lifecycle role-play, → agent manifest.
First appears in: §3.4.

**MRM (Model Risk Management)** *(**Foundations** / Patterns / Production)*
The FSI governance discipline for managing model risk; formalized in SR 11-7 (Federal Reserve / OCC Bulletin 2011-12) and updated in OCC 2021-39 and FRB SR 21-8. **Vendor-disclosed metrics are not MRM-validation evidence** — the canonical teaching attached to every vendor metric in the Field Guide.
Cross-references: → SR 11-7, → MRM-validation evidence, → vendor-disclosed metrics, → model-swap protocol, → Klarna May 2025 reversal.
First appears in: §1.15 PM-track vocabulary; deepened in §3.5.

**MRM-validation evidence** *(**Production**)*
Evidence that satisfies the independent-validation requirement of SR 11-7 §III ("Effective Model Validation"). Sources that count: (1) customer-produced model-performance evaluation by a team independent of the deploying business unit, (2) second-line risk-management testing, (3) independent third-party audit reports specifically commissioned for validation purposes, (4) formal benchmark studies with controlled comparisons against documented baselines. Sources that do NOT count: vendor-disclosed launch metrics (Klarna's "700 FTE-equivalent," Uber's "21K dev-hours saved," LinkedIn's "95% accuracy"), vendor case-study marketing, customer-page testimonials. The Field Guide's canonical case: the Klarna May 2025 reversal — the 2024 launch metric was widely cited but never MRM-validated; the 2025 walkback exposed the gap. In examiner conversations under SR 11-7, presenting vendor-disclosed metrics as evidence is treated as an absence of evidence, not weak evidence.
Cross-references: → MRM, → SR 11-7, → vendor-disclosed metrics, → Klarna May 2025 reversal, → evidence-class tags, → vendor-public [tag], → independently-audited [tag].
First appears in: §3.5 regulatory depth; reinforced in §3.9 Klarna case.

## N

**Named-incident [tag]** *(Foundations / Patterns / Production)*
One of the 10 evidence-class tags. Public incident report — Slack AI, EchoLeak/CVE-2025-32711, CurXecute/CVE-2025-54135, Samsung 2023, Air Canada, Replit prod-DB, Mata v. Avianca, ConfusedPilot, Salesforce ForcedLeak, ChatGPT Atlas omnibox.
Cross-references: → evidence-class tags.
First appears in: §1.11 / §1.18.

**Network (Swarm) — topology 7** *(**Foundations** / Patterns)*
Topology 7 of the 7 canonical LangGraph topologies. Peer-to-peer multi-agent with handoffs; no central supervisor. **Renamed from "Multi-Agent Collaboration"** to match LangGraph docs and the `langgraph-swarm-py` harness.
Cross-references: → Supervisor, → Hierarchical, → 7 LangGraph topologies, → langgraph-swarm-py.
First appears in: §1.7 / §2.2.

**NIS2 (Network and Information Security Directive 2)** *(**Production**)*
EU Directive 2022/2555. Article 21(2) cybersecurity risk-management measures (a)–(j); Article 23 incident reporting threshold; Annex II sectors-in-scope.
Cross-references: → DORA, → GDPR, → EU AI Act.
First appears in: §3.5.

**NIST SP 800-53** *(**Production**)*
US National Institute of Standards and Technology — Security and Privacy Controls for Information Systems and Organizations, Revision 5. The substrate of FedRAMP.
Cross-references: → FedRAMP-High, → IL4/IL5, → StateRAMP.
First appears in: §3.5.

**NYDFS Part 500** *(**Production**)*
New York Department of Financial Services cybersecurity regulation. Most operative parts: 500.07 access privileges, 500.11 third-party service-provider security policy, 500.14 monitoring, 500.15 encryption, 500.16 IR plan, 500.17 notice of cybersecurity event. Part 500 AI amendment extends to AI-specific obligations.
Cross-references: → DORA, → FINRA, → SEC.
First appears in: §3.5.

## O

**OAuth 2.x** *(**Foundations** / Patterns)*
The authorization-framework family used throughout enterprise agent identity flows. Extensions relevant to agents: DPoP, PAR, RAR, CIBA, PKCE, Authorization Code Flow with PKCE.
Cross-references: → DPoP, → PAR, → RAR, → CIBA, → PKCE, → OIDC.
First appears in: §1.9 / §2.4.

**OCC Bulletin 2011-12** *(**Production**)*
Office of the Comptroller of the Currency's supervisory guidance on model risk management — co-author with the Federal Reserve of SR 11-7.
Cross-references: → SR 11-7, → MRM.
First appears in: §3.5.

**OCSF (Open Cybersecurity Schema Framework)** *(**Production**)*
Open schema for security-event data; one of the destinations agent traces can normalize to before flowing into a SIEM.
Cross-references: → SIEM, → OpenLineage, → OTel GenAI conventions.
First appears in: §3.4.

**Okta for AI Agents** *(**Foundations** / Patterns)*
Okta's first-party agent-identity product, early-access 2025. Peer to Entra Agent ID and Auth0 for AI Agents.
Cross-references: → Entra Agent ID, → Auth0 for AI Agents, → Ping AIC, → agent identity (workload).
First appears in: §1.9 / §2.4.

**OpenFGA** *(**Foundations** / Patterns)*
CNCF-sandbox open-source ReBAC implementation; Auth0-originated. The named OSS reference FGA product.
Cross-references: → FGA, → ReBAC, → Cedar, → Topaz.
First appears in: §1.9.

**OpenInference** *(**Foundations** / Patterns)*
Arize-submitted OpenTelemetry convention extension for LLM / agent traces. Layered above the OTel GenAI semantic conventions.
Cross-references: → OTel GenAI conventions, → trace, → span.
First appears in: §1.8.

**OpenLineage** *(**Production**)*
Data-flow lineage protocol (CNCF-incubating; LF AI & Data). Emitted by the agent at every dataset access; flows into customer lineage tools (Collibra, Alation, Atlan, Microsoft Purview).
Cross-references: → SIEM, → OCSF, → OTel GenAI conventions.
First appears in: §3.4.

**Operational-lifecycle role-play** *(**Production**)*
§3.13 — the 40-minute, 4-event Production gate addition: Day-1 EchoLeak incident response; Day-30 Claude version-swap MRM event; Day-60 sub-processor change notification; Day-90 ECB examination evidence package.
Cross-references: → knowledge gate, → first-60-minutes runbook, → model-swap protocol, → examination dossier.
First appears in: §3.13.

**Oso** *(Patterns)*
Authorization-as-a-service vendor in the FGA category.
Cross-references: → FGA, → OpenFGA, → Cedar, → Topaz, → Permit.io, → Styra.
First appears in: §2.4.

**OWASP Agentic Top 10 (draft v0.2, Dec 2025)** *(**Foundations** / Patterns / Production)*
Open Worldwide Application Security Project's agent-specific extension to the LLM Top 10. The community-maintained catalogue of the highest-impact agent-specific risks — distinct from the LLM Top 10 because agents add autonomy, tool use, multi-agent communication, and long-term memory. Agentic-AI-6 (Memory Manipulation) is the OWASP-named category for cross-thread / `BaseStore` memory bleeds. Use it as cross-walk vocabulary when a CISO asks for agent-specific coverage. URL: [`https://owasp.org/www-project-agentic-security-initiative/`](https://owasp.org/www-project-agentic-security-initiative/).
Cross-references: → OWASP LLM Top 10, → MITRE ATLAS, → STRIDE-A, → data-leak surface.
First appears in: §2.4 / §2.7.

**OWASP LLM Top 10 (2025)** *(**Foundations** / Patterns / Production)*
Open Worldwide Application Security Project's catalogue of the ten highest-impact LLM application risks. Headline categories include LLM01 Prompt Injection, LLM02 Sensitive Information Disclosure, LLM06 Excessive Agency, LLM08 Vector and Embedding Weaknesses. The reference vocabulary every regulated-industry CISO will name. URL: [`https://owasp.org/www-project-top-10-for-large-language-model-applications/`](https://owasp.org/www-project-top-10-for-large-language-model-applications/).
Cross-references: → OWASP Agentic Top 10, → MITRE ATLAS, → STRIDE-A, → prompt injection (direct), → prompt injection (indirect).
First appears in: §2.4 / §2.7.

**OTel GenAI semantic conventions** *(**Foundations** / Patterns / Production)*
OpenTelemetry's open standard for LLM / agent trace fields. The protocol-layer answer for getting traces from an agent into the customer's Splunk / Sentinel / QRadar.
Cross-references: → OpenInference, → SIEM, → trace, → span.
First appears in: §1.8.

## P

**PAC (Product Advisory Council)** *(out-of-scope; see §4.8)*
OPAQUE-internal skill name. Not used in the Field Guide body.
Cross-references: → §4.8.
First appears in: §4.8 only.

**PAR (Pushed Authorization Requests)** *(**Foundations** / Patterns)*
[IETF RFC 9126](https://datatracker.ietf.org/doc/html/rfc9126). OAuth extension where the authorization-request parameters are pushed to the auth server out-of-band before redirect, rather than in the redirect URL.
Cross-references: → OAuth 2.x, → DPoP, → RAR, → CIBA, → PKCE.
First appears in: §1.9 / §2.4.

**PCCP (Predetermined Change Control Plan)** *(**Production**)*
FDA framework for AI/ML SaMD allowing pre-authorized model changes within a documented envelope. Material for Healthcare PHI-in-scope reference designs.
Cross-references: → FDA SaMD, → Healthcare, → model-swap protocol.
First appears in: §3.5 / §3.12.

**PCI DSS 4.0** *(**Production**)*
Payment Card Industry Data Security Standard, version 4.0. Most operative for agent deployments: Req. 6.4.3, 8.4.3, 11.5.1. Klarna is in scope.
Cross-references: → FSI, → SR 11-7.
First appears in: §3.5.

**PDPA (Personal Data Protection Act)** *(**Production**)*
Personal-data regimes in Singapore and Thailand variants. Material for agent deployments processing data of SG/TH residents.
Cross-references: → APAC/Gulf regimes, → DPDPA, → PIPL, → UAE PDPL.
First appears in: §3.5.

**Permit.io** *(Patterns)*
Authorization-as-a-service vendor in the FGA category.
Cross-references: → FGA, → OpenFGA, → Cedar, → Topaz, → Oso, → Styra.
First appears in: §2.4.

**Persona (the 10 personas)** *(**Patterns** / Production)*
The 10-persona buying-committee model: CTO-FSI, CTO-ISV, CISO, VP-AI, Head-AI, Champion, Architect, Compliance, CIO, Sovereign. Crossed with 6 recipes and per-recipe segment variants to form the heatmap structural backbone.
Cross-references: → ICP, → 6 recipe families, → buyer persona.
First appears in: §2.6.

**pgvector** *(**Foundations** / Patterns)*
Postgres extension for vector search. The most-common LangGraph production retrieval layer because it co-locates with the Postgres checkpointer.
Cross-references: → PostgresSaver, → retrieval, → vector store.
First appears in: §1.5.

**PHI (Protected Health Information)** *(**Production**)*
HIPAA-regulated category of patient data. As of May 2026, **no production LangGraph deployment touches PHI on any framework**; the Field Guide's Healthcare section is `[reference design]`.
Cross-references: → PHI gap, → HIPAA, → Healthcare, → BAA chain.
First appears in: §3.12.

**PHI gap** *(**Production**)*
§3.12 — the explicit acknowledgment that no production LangGraph PHI deployment exists; the section is reference-design only. One of the three gaps the Field Guide marks honestly (Sovereign gap, PHI gap, insurance gap).
Cross-references: → PHI, → Healthcare, → Sovereign gap, → insurance gap, → reference design.
First appears in: §3.12.

**Phoenix** *(**Foundations** / Patterns)*
OSS sibling of Arize AX (commercial). **Distinct products** — the Field Guide does not conflate them. Per LangGraph-DevRel #2.5.
Cross-references: → Arize AX, → LangSmith, → Langfuse.
First appears in: §1.8.

**Ping AIC (Ping Advanced Identity Cloud)** *(Patterns)*
Ping Identity's agent-relevant identity products (PingOne, PingFederate, PingAuthorize). One of the workforce-identity options in the Integration Cookbook.
Cross-references: → Entra Agent ID, → Okta for AI Agents, → workforce identity.
First appears in: §2.4 / §3.3.

**Pipeline** *(**Foundations**)*
A deterministic DAG of steps, possibly including model inference; no agent loop. Distinct from agent and from workflow.
Cross-references: → agent, → workflow, → chatbot, → RAG.
First appears in: §1.1.

**PIPL (Personal Information Protection Law)** *(**Production**)*
China's personal-information regime. Article 24 on automated decision-making is most operative for agent deployments serving Chinese-resident users.
Cross-references: → APAC/Gulf regimes, → DPDPA, → PDPA.
First appears in: §3.5.

**PKCE (Proof Key for Code Exchange)** *(**Foundations** / Patterns)*
IETF RFC 7636. OAuth 2.0 extension for public clients. Practical default for agent OAuth code flow. The most-deployed practical pattern per LangGraph-DevRel #2.4.
Cross-references: → OAuth 2.x, → DPoP, → PAR, → RAR.
First appears in: §1.9 / §2.4.

**Plan-and-Execute (topology 3)** *(**Foundations** / Patterns)*
Topology 3 of the 7 canonical LangGraph topologies. Planner LLM + executor LLM + replanner LLM. `deepagents` is the canonical harness. Anchor customers: Captide, Morningstar Mo, Athena Intelligence.
Cross-references: → planner, → executor, → replanner, → deepagents, → topology 8 emergence.
First appears in: §1.7 / §2.2.

**Planner** *(**Foundations** / Patterns)*
A graph role: the LLM (or graph node) that produces a multi-step plan. The first node in the Plan-and-Execute topology.
Cross-references: → executor, → replanner, → Plan-and-Execute.
First appears in: §1.7.

**`PostgresSaver` / `AsyncPostgresSaver`** *(**Foundations** / Patterns)*
LangGraph's production-default thread checkpointer (sync and async variants). Auto-provisioned in LangGraph Cloud SaaS; customer-managed in BYOC and Self-Hosted Enterprise.
Cross-references: → checkpointer, → AsyncPostgresSaver, → RedisSaver, → MemorySaver.
First appears in: §1.4.

**`PostgresStore`** *(**Foundations** / Patterns)*
LangGraph's production-default cross-thread `BaseStore` implementation. Postgres-backed long-term memory; co-locates with `PostgresSaver`.
Cross-references: → BaseStore, → RedisStore, → InMemoryStore.
First appears in: §1.4.

**Prebuilt** *(**Foundations**)*
LangGraph's helper-functions tier — `create_react_agent` is the most-used. The third authoring surface alongside Graph API and Functional API.
Cross-references: → create_react_agent, → Graph API, → Functional API.
First appears in: §1.4.

**Primary-regulatory [tag]** *(Foundations / Patterns / Production)*
One of the 10 evidence-class tags. The text of the regulation itself — DORA Art. 28 verbatim, SR 11-7 §III.4 verbatim. Controlling, not evidence.
Cross-references: → evidence-class tags.
First appears in: §1.18 / §13.

**Prompt injection (direct)** *(**Foundations** / Patterns / Production)*
Attacker controls the user input and embeds malicious instructions in it. The classic prompt-injection failure mode. Lower in operational impact than indirect because the attack surface is the user's own input channel.
Cross-references: → prompt injection (indirect), → hallucination-to-action, → EchoLeak, → telemetry capture.
First appears in: §1.11.

**Prompt injection (indirect)** *(**Foundations** / Patterns / Production)*
Attacker controls data the agent retrieves or reads (email, document, search result, webpage); the agent treats the embedded instructions as commands. The modal failure mode for agents that consume third-party content. EchoLeak is the canonical anchor.
Cross-references: → prompt injection (direct), → EchoLeak, → CurXecute, → ConfusedPilot, → data-leak surface.
First appears in: §1.11.

## R

**RAG (Retrieval-Augmented Generation)** *(**Foundations**)*
Pattern where retrieved documents are injected into the LLM context before generation. **Not an agent** unless the LLM chooses when and how to retrieve — at which point it becomes Agentic RAG.
Cross-references: → Agentic RAG, → vector store, → retriever surface.
First appears in: §1.1.

**RAR (Rich Authorization Requests)** *(**Foundations** / Patterns)*
[IETF RFC 9396](https://datatracker.ietf.org/doc/html/rfc9396). OAuth extension that carries a structured `authorization_details` payload — fine-grained transaction-detail consent, beyond simple scope strings. Material for agent-on-behalf-of-user delegation where the agent is asking for permission to do a specific thing, not a class of things.
Cross-references: → OAuth 2.x, → DPoP, → PAR, → CIBA, → PKCE, → agent-on-behalf-of-user identity.
First appears in: §1.9 / §2.4.

**ReAct (topology 1)** *(**Foundations** / Patterns)*
Topology 1 of the 7 canonical LangGraph topologies. Single-agent reason+act loop (Yao et al. 2022, ICLR 2023). The most-deployed LangGraph pattern. `create_react_agent` is the prebuilt helper.
Cross-references: → Reflexion, → create_react_agent, → 7 LangGraph topologies.
First appears in: §1.7.

**ReBAC (Relationship-Based Access Control)** *(**Foundations** / Patterns)*
Authorization model where decisions derive from a graph of subject-object-relation triples. The substrate of FGA. OpenFGA, Cedar, Topaz are ReBAC-capable products.
Cross-references: → FGA, → OpenFGA, → Cedar, → Topaz, → FGA modeling exercise.
First appears in: §1.9.

**Recommender (autonomy Level 1)** *(**Foundations**)*
Level 1 of the 5-point autonomy spectrum. The system recommends a specific action; the human confirms before execution.
Cross-references: → autonomy spectrum, → advisor.
First appears in: §1.1.

**Reference design [tag]** *(Foundations / Patterns / Production)*
One of the 10 evidence-class tags. Pattern from a published reference architecture; not a deployed customer.
Cross-references: → evidence-class tags, → architectural inference.
First appears in: §1.18 / §13.

**Reflexion** *(**Foundations** / Patterns)*
Self-critique technique (Shinn et al., NeurIPS 2023). Often combined with ReAct to form topology 2 (ReAct + Reflexion).
Cross-references: → ReAct, → critic, → topology 2.
First appears in: §1.7.

**Replanner** *(**Foundations** / Patterns)*
A graph role in the Plan-and-Execute topology — the LLM (or graph node) that revises the plan after step execution.
Cross-references: → planner, → executor, → Plan-and-Execute.
First appears in: §1.7.

**Resume (`Command(resume=...)`)** *(**Foundations** / Patterns)*
LangGraph primitive that resumes a thread that hit an `interrupt()` and provides the resume value. The companion to `interrupt()`.
Cross-references: → interrupt, → HITL, → approval.
First appears in: §1.4.

**Retrieval break** *(**Foundations** / Patterns / Production)*
Curriculum vocabulary. A 15-minute mixed-question recall exercise placed at tier halfway points. Standard spaced-retrieval mechanic.
Cross-references: → spaced retrieval, → Anki deck.
First appears in: §1.14.

**Retriever surface (cross-tenant)** *(**Patterns** / Production)*
One of the 5 cross-tenant isolation surfaces. Per-row tenant predicate at the vector store. pgvector RLS + `tenant_id`; Pinecone namespace per tenant; Weaviate multi-tenancy mode; Qdrant payload filter; Elasticsearch tenant index pattern.
Cross-references: → cross-tenant isolation, → ConfusedPilot, → cache surface, → checkpointer surface.
First appears in: §2.7 / §3.2.

**RFC 3161** *(**Production**)*
Trusted timestamping protocol. Cryptographic anchoring of signatures to wall-clock. DigiCert, SwissSign, GlobalSign, Sectigo, or self-hosted HSM TSA.
Cross-references: → HSM-backed signing chain, → SLSA, → audit-evidence pattern.
First appears in: §3.4.

**Router** *(**Foundations** / Patterns)*
A graph role: the node that routes inbound requests to the correct downstream node. The supervisor in the Supervisor topology is the most common router.
Cross-references: → Supervisor, → planner, → critic.
First appears in: §1.7 / §2.2.

**Rubric** *(**Foundations** / Patterns / Production)*
Curriculum vocabulary. The 5–7 criterion three-tier (pass / partial / fail) grading framework attached to each knowledge gate. Inter-rater reliability target ≥ 0.7 (Cohen's kappa) on the Production gate.
Cross-references: → knowledge gate, → evaluator, → model answer, → inter-rater reliability.
First appears in: §1.16.

**Run** *(**Foundations**)*
LangSmith-vocabulary equivalent of "trace." A single end-to-end agent execution.
Cross-references: → trace, → span, → step.
First appears in: §1.8.

## S

**SAMA (Saudi Arabian Monetary Authority)** *(**Production**)*
Saudi Arabia's central bank and financial regulator. Cyber Security Framework + draft AI ethics are most operative for KSA-resident FSI agent deployments.
Cross-references: → APAC/Gulf regimes, → DFSA, → MAS, → HKMA.
First appears in: §3.5.

**Scratchpad** *(**Foundations**)*
Intra-step intermediate reasoning held in state. The ReAct Thought trace lives here. Scope 1 of the three-scope state model.
Cross-references: → state, → thread, → BaseStore, → three-scope state model.
First appears in: §1.5.

**SEC 17a-4(f)** *(**Production**)*
US Securities and Exchange Commission Rule 17a-4(f). WORM-storage requirement for broker-dealer books and records — non-rewriteable, non-erasable. 6 years easily accessible + 6 years total in WORM. The Field Guide ships a "17a-4(f)-compliant LangGraph trace storage" reference pattern.
Cross-references: → WORM, → FINRA, → audit-evidence pattern.
First appears in: §3.5.

**Self-Hosted Enterprise** *(**Patterns** / Production)*
LangGraph Platform deployment shape — full self-hosted; customer operates both control plane and data plane. The default for FSI Tier-1 and Sovereign-region prospects. Runs on EKS / GKE / AKS / customer K8s.
Cross-references: → LangGraph Cloud SaaS, → BYOC, → Self-Hosted Lite, → 10-axis deployment matrix.
First appears in: §2.8 / §3.1.

**Self-Hosted Lite** *(Patterns / **Production**)*
LangGraph Platform deployment shape — single-VM, OSS-only. No state persistence by default. Distinct from Self-Hosted Enterprise.
Cross-references: → Self-Hosted Enterprise, → Developer Tier.
First appears in: §3.1.

**Self-RAG** *(Patterns)*
Agentic RAG variant; grades the final answer for groundedness against retrieved docs.
Cross-references: → Agentic RAG, → CRAG.
First appears in: §2.2.

**Semi-autonomous (autonomy Level 2)** *(**Foundations**)*
Level 2 of the 5-point autonomy spectrum. The agent takes some actions autonomously but escalates high-blast-radius actions to a human.
Cross-references: → autonomy spectrum, → autonomous-with-HITL.
First appears in: §1.1.

**`Send` API** *(**Foundations** / Patterns)*
LangGraph primitive for fan-out / map-reduce patterns. Sends a payload to a downstream node and supports parallel execution. Used in ServiceNow's customer-success multi-agent system.
Cross-references: → StateGraph, → Hierarchical, → Subgraph.
First appears in: §1.4.

**Signed action chain** *(**Foundations** / Production)*
The implementation of action provenance. Each step (user assertion, planner decision, tool invocation, tool result, outcome) is cryptographically signed (KMS-backed) so the chain is replayable and auditable.
Cross-references: → action provenance, → HSM-backed signing chain, → audit-evidence pattern, → RFC 3161.
First appears in: §1.9; deepened in §3.4.

**SIEM (Security Information and Event Management)** *(**Foundations** / Patterns / Production)*
The customer's security-event aggregation platform — Splunk ES, Microsoft Sentinel, IBM QRadar, Google Chronicle, Exabeam. Agent traces flow into the SIEM via OTel collectors using OTel GenAI semantic conventions and OCSF normalization.
Cross-references: → OTel GenAI conventions, → OCSF, → trace egress, → Incident Classification Guide.
First appears in: §1.8.

**SLSA (Supply-chain Levels for Software Artifacts)** *(**Production**)*
Build-provenance standard. SLSA Level 3+ is the supply-chain bar for FSI Tier-1. `langgraph build` artifact pipeline should produce SLSA-attested artifacts.
Cross-references: → in-toto, → audit-evidence pattern, → supply-chain compromise.
First appears in: §3.3 / §3.4.

**SOC 2 Type II** *(**Foundations** / Patterns / Production)*
AICPA Service Organization Control 2, Type II — operational audit of security/availability/processing-integrity/confidentiality/privacy controls. LangSmith holds SOC 2 Type II [independently-audited]; the audit scope matters more than the certification claim.
Cross-references: → ISO 27001, → independently-audited.
First appears in: §2.5.

**SOC Agent recipe (Recipe 6)** *(**Foundations** / Patterns / Production)*
The Security Agents recipe — Agentic RAG over SIEM, EDR, vulnerability scanner, threat-intel feeds. Anchor customer: Elastic AI Assistant. The 1-of-18-deployment outlier the Field Guide carries because CISO-as-primary-buyer matters for the substrate-level remediation framing.
Cross-references: → 6 recipe families, → Agentic RAG, → SIEM, → ELSER.
First appears in: §1.10.6.

**Sovereign (ICP industry)** *(**Foundations** / Production)*
One of the 4 ICP industries — public sector, defense, intelligence, regulated-region deployments. Marked `[evidence-zero, structural-fit-only]` — no public LangGraph deployment evidence exists.
Cross-references: → ICP, → Sovereign gap, → data-residency reasoning.
First appears in: §1.12.

**Sovereign gap** *(**Production**)*
§3.11 — the explicit acknowledgment that no public LangGraph Sovereign-region deployment exists; the section is structural-fit-only. One of the three gaps the Field Guide marks honestly.
Cross-references: → Sovereign, → PHI gap, → insurance gap, → data-residency reasoning.
First appears in: §3.11.

**Spaced retrieval** *(**Foundations** / Patterns / Production)*
Curriculum mechanism. End-of-section recall cards, mid-tier retrieval breaks, pre-tier retrieval warmups, and the Anki deck — together the spaced-retrieval scaffold that pulls vocabulary out of short-term memory into long-term retrieval.
Cross-references: → Anki deck, → retrieval break, → mentor checkpoint.
First appears in: §1.14.

**Span** *(**Foundations** / Patterns / Production)*
A single sub-operation within a trace. Spans nest within a trace; each tool call, LLM call, retrieval, and HITL pause typically gets its own span.
Cross-references: → trace, → step, → OTel GenAI conventions.
First appears in: §1.8.

**SPIFFE / SPIRE** *(**Foundations** / Patterns)*
SPIFFE = Secure Production Identity Framework For Everyone (workload-identity standard). SPIRE = the reference runtime. CNCF projects. Common for zero-trust agent workloads; required posture for sovereign air-gap deployments.
Cross-references: → agent identity (workload), → workforce identity, → zero-trust.
First appears in: §1.9 / §2.4.

**SR 11-7** *(**Patterns** / Production)*
Federal Reserve / OCC Supervisory Guidance on Model Risk Management (April 2011). The FSI compliance anchor for any LLM deployed in a regulated bank. Updated in OCC 2021-39 and FRB SR 21-8.
Cross-references: → MRM, → OCC Bulletin 2011-12, → model-swap protocol, → vendor-disclosed metrics.
First appears in: §2.5 / §3.5.

**State** *(**Foundations** / Patterns / Production)*
Any data the agent carries across operations. In LangGraph: the typed schema attached to the `StateGraph`. Three scopes: scratchpad (intra-step), thread (intra-conversation), long-term memory (cross-thread).
Cross-references: → scratchpad, → thread, → BaseStore, → checkpointer, → three-scope state model.
First appears in: §1.5.

**State graph (`StateGraph`)** *(**Foundations** / Patterns)*
LangGraph's graph-building primitive. Define nodes (functions), edges (transitions), and the shared state schema; `compile()` produces a runnable.
Cross-references: → MessagesState, → checkpointer, → Subgraph, → Graph API.
First appears in: §1.4.

**Step** *(**Foundations**)*
One iteration of the agent loop. Usually composed of one or more spans.
Cross-references: → trace, → span.
First appears in: §1.8.

**Step-up authentication** *(**Foundations** / Patterns)*
Escalating authentication strength (e.g., requiring fresh MFA) for high-risk actions. Used to gate high-blast-radius tools an agent is about to invoke on a user's behalf.
Cross-references: → OAuth 2.x, → CIBA, → DPoP, → autonomous-with-HITL.
First appears in: §1.9 / §2.4.

**STRIDE-A** *(**Production**)*
STRIDE threat-modeling framework extended with an Autonomy-abuse category. The agent-specific threat-model. Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege, Autonomy abuse.
Cross-references: → audit-evidence pattern, → data-leak surface.
First appears in: §3.6.

**Styra** *(Patterns)*
Authorization-as-a-service vendor; Styra DAS is the policy-management UI for OPA.
Cross-references: → FGA, → OPA, → Topaz, → Permit.io, → Oso.
First appears in: §2.4.

**Subgraph** *(**Foundations** / Patterns)*
A `StateGraph` used as a node inside another `StateGraph`. The encapsulation primitive for nesting subsystems.
Cross-references: → StateGraph, → Hierarchical, → Send API.
First appears in: §1.4.

**Substrate-level cluster** *(**Production**)*
§3.6.15 — the 8 of 14 governance failure modes whose mitigation reduces to substrate primitives (TEE attestation, sealed keys, attested network egress, attested workload identity). Procurement-grade rigor, not abstract framing.
Cross-references: → TEE attestation, → substrate primitive, → 14 failure modes.
First appears in: §3.6.

**Substrate primitive** *(**Production**)*
A control that lives below the agent graph layer — TEE attestation, sealed keys, attested network egress, attested workload identity. Procurement-grade naming required when framing where a failure mode reduces.
Cross-references: → substrate-level cluster, → TEE attestation, → attestation receipt.
First appears in: §3.6.

**Supervisor (topology 4)** *(**Foundations** / Patterns / Production)*
Topology 4 of the 7 canonical LangGraph topologies. One routing supervisor with N specialist workers. Production-default for multi-tool routing. `langgraph-supervisor-py` is the canonical harness.
Cross-references: → worker, → router, → Hierarchical, → 7 LangGraph topologies, → Klarna May 2025 reversal.
First appears in: §1.7 / §2.2.

**Supply-chain compromise** *(**Foundations** / Patterns / Production)*
The failure mode where a tool, MCP server, or dependency in the agent's supply chain is malicious or compromised. CurXecute is the named-incident anchor for the MCP-tool-supply-chain variant.
Cross-references: → CurXecute, → MCP, → SLSA, → SBOM.
First appears in: §1.11.

## T

**TEE attestation** *(**Production**)*
Cryptographic attestation that the runtime is what was approved — Intel TDX, AMD SEV-SNP, NVIDIA Confidential Compute. The substrate primitive most directly addressing the §3.6.15 substrate-level cluster.
Cross-references: → substrate primitive, → attestation receipt, → substrate-level cluster.
First appears in: §3.6.

**Telemetry capture** *(**Foundations** / Patterns / Production)*
The failure mode where PII / regulated data ends up in trace platforms outside the trust boundary. The dominant data-leak surface in LangGraph Cloud SaaS deployments.
Cross-references: → trace egress, → SIEM, → data-leak surface, → cross-tenant aggregation.
First appears in: §1.11.

**Ten ICP personas (the 10 personas)** *(**Patterns** / Production)*
See → Persona (the 10 personas).
First appears in: §2.6.

**Text-to-SQL recipe (Recipe 3)** *(**Foundations** / Patterns / Production)*
The Text-to-SQL / Conversational Analytics recipe. Anchor customers: LinkedIn (internal), Vizient (healthcare supply-chain). Dominant failure mode: cross-tenant aggregation. FGA modeling exercise published for this recipe.
Cross-references: → 6 recipe families, → FGA modeling exercise, → cross-tenant aggregation, → Agentic RAG.
First appears in: §1.10.3.

**Thread** *(**Foundations** / Patterns)*
A single conversation with an agent. Identified by `thread_id`. Scope 2 of the three-scope state model.
Cross-references: → thread_id, → checkpointer, → state, → three-scope state model.
First appears in: §1.5.

**`thread_id`** *(**Foundations** / Patterns)*
The string identifier for a thread. Passing the same `thread_id` resumes the conversation. Per-tenant `thread_id` namespacing is required for cross-tenant isolation at the checkpointer surface.
Cross-references: → thread, → checkpointer, → checkpointer surface, → RunnableConfig.configurable.
First appears in: §1.4.

**Three agent identity problems** *(**Foundations** / Patterns / Production)*
The structural framing introduced in §1.9: (1) user identity — authenticating the human; (2) agent identity (workload) — authenticating the agent runtime; (3) agent-on-behalf-of-user identity (delegation) — establishing the delegation the agent acts under. Vendor marketing often collapses problems 2 and 3; the Field Guide separates them.
Cross-references: → user identity, → agent identity (workload), → agent-on-behalf-of-user identity.
First appears in: §1.9.

**Three-layer protocol stack** *(**Foundations** / Patterns)*
The canonical relayering of A2A, MCP, and AGP — A2A above, MCP middle, AGP/AGNTCY below. All three under LF AAIF.
Cross-references: → A2A, → MCP, → AGP, → AGNTCY, → LF AAIF.
First appears in: §1.6.

**Three-scope state model** *(**Foundations**)*
The conceptual framing for agent state: (1) scratchpad (intra-step), (2) thread (intra-conversation), (3) long-term memory (cross-thread). Each scope has a distinct persistence story in LangGraph.
Cross-references: → scratchpad, → thread, → BaseStore, → checkpointer.
First appears in: §1.5.

**TLPT (Threat-Led Penetration Testing)** *(**Production**)*
DORA Articles 24–26 mandatory testing program for systemically important financial entities. An agent deployment at a designated entity is in scope.
Cross-references: → DORA, → audit-evidence pattern.
First appears in: §3.5.

**Tool** *(**Foundations** / Patterns)*
A function (or resource, or prompt) the LLM can invoke. The agent's action surface.
Cross-references: → tool call, → function calling, → MCP tool.
First appears in: §1.6.

**Tool call** *(**Foundations**)*
An LLM emission requesting that a tool be invoked, with structured arguments. The mechanism by which agents act.
Cross-references: → tool, → function calling, → MCP tool.
First appears in: §1.6.

**Tool-call perimeter** *(**Production**)*
Axis 8 of the 10-axis deployment-shape matrix. Which tools / MCP servers the agent can reach.
Cross-references: → 10-axis deployment matrix, → MCP, → network egress.
First appears in: §3.1.

**Toolformer** *(**Foundations**)*
Self-supervised tool-calling training paper (Schick et al., NeurIPS 2023). Intellectual ancestor of LLM-native function calling.
Cross-references: → function calling, → tool, → tool call.
First appears in: §1.3.

**Topaz** *(Patterns)*
Aserto product combining RBAC + ABAC + ReBAC. One of the FGA-category products.
Cross-references: → FGA, → OpenFGA, → Cedar, → ReBAC.
First appears in: §2.4.

**Topology 8 emergence** *(Patterns)*
The community position that `deepagents` graduates beyond Plan-and-Execute into an eighth canonical topology. Acknowledged in the Field Guide as an honesty callout — the 7 are LangChain-blog canonical as of May 2026, but `deepagents` and "Supervisor as Tool" are emerging fourth and eighth.
Cross-references: → deepagents, → 7 LangGraph topologies, → Plan-and-Execute.
First appears in: §2.2.

**Trace** *(**Foundations** / Patterns / Production)*
The full record of a single agent run. Composed of nested spans. Borrowed from OpenTelemetry vocabulary; LangSmith calls it a "run."
Cross-references: → span, → step, → run, → OTel GenAI conventions.
First appears in: §1.8.

**Trace egress** *(**Production**)*
Axis 4 of the 10-axis deployment-shape matrix. Where observability traces go — LangSmith Cloud is mandatory in LangGraph Cloud SaaS; configurable in BYOC and Self-Hosted Enterprise; customer-self-hosted in Sovereign.
Cross-references: → 10-axis deployment matrix, → LangSmith, → Langfuse, → telemetry capture.
First appears in: §3.1.

**Tree of Thoughts** *(**Foundations**)*
Search-over-thoughts planning technique (Yao et al., NeurIPS 2023). Foundations names it; not a deployed production pattern at LangGraph customer scale as of May 2026.
Cross-references: → ReAct, → Plan-and-Execute, → Reflexion.
First appears in: §1.3.

## U

**UAE PDPL** *(**Production**)*
United Arab Emirates Personal Data Protection Law (Federal Decree-Law 45 of 2021) + CBUAE Information Security Standards. Material for UAE-resident agent deployments.
Cross-references: → APAC/Gulf regimes, → DFSA, → SAMA.
First appears in: §3.5.

**User identity** *(**Foundations**)*
The identity of the human authenticating to the system. Problem 1 of the three agent identity problems.
Cross-references: → agent identity (workload), → agent-on-behalf-of-user identity, → three agent identity problems.
First appears in: §1.9.

## V

**Validator** *(**Foundations** / Patterns)*
A graph role: a node that gates downstream execution by validating an upstream output. Distinct from critic (which proposes revisions). Used in Uber AutoCover's Validator-as-Supervisor pattern.
Cross-references: → critic, → Supervisor, → Hierarchical.
First appears in: §1.7 / §2.2.

**Vector store** *(**Foundations** / Patterns)*
A database supporting nearest-neighbor search on embeddings. pgvector, Pinecone, Weaviate, Qdrant, Milvus, Elasticsearch, Redis, Vespa, Turbopuffer. The retrieval substrate for RAG and Agentic RAG.
Cross-references: → pgvector, → retriever surface, → RAG, → Agentic RAG.
First appears in: §1.5.

**Vendor-contractual [tag]** *(Foundations / Patterns / Production)*
One of the 10 evidence-class tags. Vendor commitment in DPA / MSA / order form — legally binding. High evidence weight.
Cross-references: → evidence-class tags, → independently-audited.
First appears in: §1.18 / §13.

**Vendor-disclosed metrics** *(**Foundations** / Patterns / Production)*
Vendor marketing metrics (Klarna 80% / 700-FTE-equivalent, Uber 21K dev hours, LinkedIn 95%, Komodo 330M patient journeys). **Not MRM-validation evidence under SR 11-7.** The canonical teaching attached to every vendor metric in the Field Guide.
Cross-references: → MRM, → SR 11-7, → Klarna May 2025 reversal, → vendor-public.
First appears in: §1.10.

**Vendor-public [tag]** *(Foundations / Patterns / Production)*
One of the 10 evidence-class tags. Vendor public statement — blog, docs, marketing. Low evidence weight, rebuttable, not contractually binding.
Cross-references: → evidence-class tags, → vendor-contractual, → customer-produced-evidence.
First appears in: §1.18 / §13.

**Vertex Agent Engine** *(**Production**)*
Google Cloud's CSP-managed agent runtime in Vertex AI. The GCP-native alternative when BYOC-GCP is gap-blocked.
Cross-references: → CSP-managed, → BYOC GCP (gap), → Foundry Agent Service, → Bedrock AgentCore.
First appears in: §3.1.

## W

**Worker** *(**Foundations** / Patterns)*
A graph role: a specialist agent or node invoked by a supervisor in the Supervisor topology.
Cross-references: → Supervisor, → Hierarchical, → router.
First appears in: §1.7.

**Workflow** *(**Foundations**)*
LLM-using system orchestrated on predefined code paths; the LLM does not choose its own next action (Anthropic definition). Contrasted with agent.
Cross-references: → agent, → pipeline, → agentic system.
First appears in: §1.1.

**WORM (Write-Once-Read-Many)** *(**Patterns** / Production)*
Storage primitive required by SEC 17a-4(f) — non-rewriteable, non-erasable. S3 Object Lock (Compliance mode), Azure Immutable Blob, GCP Bucket Lock, NetApp SnapLock, Dell PowerScale SmartLock. 6 years easily accessible + 6 years total in WORM for SEC 17a-4(f).
Cross-references: → SEC 17a-4(f), → audit-evidence pattern, → retention schedule.
First appears in: §2.11 / §3.4.

## Z

**Zero-data-retention (ZDR) addendum** *(**Production**)*
Enterprise-LLM-plan contractual addendum committing the LLM provider to not retain or train on inputs. Material for FSI / Healthcare procurement.
Cross-references: → vendor-contractual, → telemetry capture.
First appears in: §3.5.

---

# §4.2 Cluster Index

The 15 clusters organize terms for guided learning. Each cluster groups closely related concepts; cross-references in §4.1 walk between clusters.

## §4.2.1 Cluster 1 — Agent and autonomy

agent | agentic system | autonomy spectrum | advisor (Level 0) | recommender (Level 1) | semi-autonomous (Level 2) | autonomous-with-HITL (Level 3) | fully autonomous (Level 4) | workflow | pipeline | chatbot | RAG | Agentic RAG

**Why this cluster matters.** Foundations §1.1 lives here. New hires read this cluster first; without it, every subsequent vocabulary choice is loose. Anthropic's discipline (agent = LLM-directed process and tool usage) is the canonical posture.

## §4.2.2 Cluster 2 — State, memory, persistence

state | scratchpad | thread | thread_id | checkpoint | checkpointer | PostgresSaver | AsyncPostgresSaver | RedisSaver | MemorySaver | SqliteSaver | BaseStore | PostgresStore | RedisStore | InMemoryStore | working memory | episodic memory | semantic memory | procedural memory | three-scope state model | long-term memory | vector store | pgvector

**Why this cluster matters.** The single biggest Foundations-to-Patterns transition: where does state live in your agent. Get the scopes right (scratchpad / thread / BaseStore) and the rest follows.

## §4.2.3 Cluster 3 — Tools and protocols

tool | tool call | function calling | MCP | MCP server | MCP client | MCP host | MCP resource | MCP tool | MCP prompt | MCP primitives | MCP Authorization | MCP elicitation | MCP sampling | A2A | AGP | AGNTCY | three-layer protocol stack | LF AAIF | langgraph-mcp-adapters | Toolformer

**Why this cluster matters.** The three-layer stack (A2A above MCP above AGP) is the canonical relayering as of v3 of the Field Guide design spec. Conflating MCP with the langchain adapter is the most common credibility miss.

## §4.2.4 Cluster 4 — Patterns and topologies

ReAct (topology 1) | ReAct + Reflexion (topology 2) | Plan-and-Execute (topology 3) | Supervisor (topology 4) | Hierarchical (topology 5) | Agentic RAG (topology 6) | Network (Swarm) (topology 7) | deepagents | topology 8 emergence | Reflexion | Tree of Thoughts | CRAG | Self-RAG | 7 LangGraph topologies | langgraph-supervisor-py | langgraph-swarm-py | langgraph-reflection | Lang Effect | HLTM

**Why this cluster matters.** The 7 canonical topologies are the Field Guide's structural backbone. Topology selection is the first decision in any customer architecture conversation.

## §4.2.5 Cluster 5 — Roles in a graph

planner | executor | replanner | supervisor | worker | router | validator | critic

**Why this cluster matters.** Naming roles correctly in a customer whiteboard separates the SE who has architected an agent from the SE who has read about agents.

## §4.2.6 Cluster 6 — Human-in-the-loop

HITL | interrupt | resume (`Command(resume=...)`) | Command goto (`Command(goto=...)`) | approval | escalation | confidence gate | HitL surface | step-up authentication

**Why this cluster matters.** HITL placement is recipe-specific. Getting it wrong in a customer conversation signals you have not understood the recipe. The Klarna May 2025 reversal is the canonical "no human fallback was the problem" story.

## §4.2.7 Cluster 7 — Observability

trace | span | step | run | LangSmith | Langfuse | Phoenix | Arize AX | OTel GenAI conventions | OpenInference | SIEM | OCSF | OpenLineage | trace egress | telemetry capture

**Why this cluster matters.** "Where do traces go" is axis 4 of the deployment-shape matrix. It's a Day-1 FSI CISO question. Phoenix-vs-Arize confusion is the most-corrected mistake in Patterns.

## §4.2.8 Cluster 8 — Failure modes and leakage surfaces

data-leak surface | leakage pathway | leak vector | prompt injection (direct) | prompt injection (indirect) | hallucination | hallucination-to-action | citation hallucination | cross-tenant aggregation | action provenance gap | telemetry capture | supply-chain compromise | substrate-level cluster | substrate primitive | retriever surface | cache surface | checkpointer surface | observability surface | model surface | STRIDE-A | EchoLeak | CurXecute | ConfusedPilot | Mata v. Avianca | Klarna May 2025 reversal

**Why this cluster matters.** Production §3.6 catalogues 14 failure modes; 8 reduce to substrate-level remediation (the substrate-level cluster). Public vocabulary ("data-leak surface" / "leakage pathway") is canonical throughout — "bleed" is not used.

## §4.2.9 Cluster 9 — Identity and authorization

user identity | agent identity (workload) | agent-on-behalf-of-user identity | three agent identity problems | OAuth 2.x | DPoP | PAR | RAR | CIBA | step-up authentication | PKCE | SPIFFE/SPIRE | FGA | ReBAC | OpenFGA | Cedar | Topaz | Permit.io | Oso | Styra | Entra Agent ID | Okta for AI Agents | Auth0 for AI Agents | Ping AIC | FGA modeling exercise

**Why this cluster matters.** Part II §2.4 Identity / Agent AuthZ is standalone because cross-tenant aggregation, action provenance, and audit-trail integrity all start here. Conflating workload identity with delegation identity is the most-common vendor-marketing confusion.

## §4.2.10 Cluster 10 — LangGraph primitives

StateGraph | MessagesState | add_messages reducer | add_node | add_edge | add_conditional_edges | Command goto | Command resume | interrupt | compile(checkpointer=...) | Send API | Subgraph | Functional API | `@entrypoint` / `@task` | Graph API | prebuilt | create_react_agent | InjectedState | InjectedToolArg | RunnableConfig.configurable | streaming modes | LangGraph Studio | langgraph dev/up/build | langgraph.json

**Why this cluster matters.** Three authoring surfaces: Graph API (explicit `StateGraph`), Functional API (`@entrypoint`/`@task`), Prebuilt (`create_react_agent`). Studio is non-negotiable.

## §4.2.11 Cluster 11 — Deployment

LangGraph Cloud SaaS | BYOC | BYOC Azure (gap) | BYOC GCP (gap) | BYOC dataplane-listener | Self-Hosted Enterprise | Self-Hosted Lite | Developer Tier | CSP-managed | Bedrock AgentCore | Vertex Agent Engine | Foundry Agent Service | Sovereign air-gap | 10-axis deployment matrix | cloud locus | identity perimeter | data perimeter | trace egress | secret perimeter | network egress | model perimeter | tool-call perimeter | HitL surface | support / break-glass | EKS | AKS | GKE

**Why this cluster matters.** The 10-axis matrix is the Field Guide's primary deployment scaffold (§3.1). The 4 LangChain-canonical shapes are one column of nine; the BYOC-Azure and BYOC-GCP gaps are deal-shaping facts.

## §4.2.12 Cluster 12 — Audit and evidence

MRM | MRM-validation evidence | vendor-disclosed metrics | SR 11-7 | OCC Bulletin 2011-12 | SIEM | OCSF | OpenLineage | Evidence Index | sign-chain (signed action chain) | HSM-backed signing chain | attestation receipt | TEE attestation | audit-evidence pattern | Audit-Evidence Cookbook | examination dossier | break-glass | RFC 3161 | SLSA | reproducibility | agent manifest | model-swap protocol | first-60-minutes runbook | operational-lifecycle role-play | exit plan | ICT register entry | concentration risk | critical ICT-TPP | WORM | retention schedule | STRIDE-A | Incident Classification Guide | DPIA | TLPT

**Why this cluster matters.** Production §3.4 — the Audit-Evidence Cookbook — is the single most important section for Tier-1 FSI procurement. Without it, the Field Guide is below FSI audit floor.

## §4.2.13 Cluster 13 — Regulatory regimes

DORA | GDPR | EU AI Act | NIS2 | SR 11-7 | OCC Bulletin 2011-12 | SEC 17a-4(f) | FINRA 4511 | FINRA 4530 | FINRA 5280 | NYDFS Part 500 | HIPAA | PCI DSS 4.0 | MiFID II | FedRAMP-High | NIST SP 800-53 | FDA PCCP | MAS | DFSA | HKMA | SAMA | PIPL | DPDPA | UAE PDPL | CPRA | Annex III | high-risk system | human oversight | IL4 | IL5

**Why this cluster matters.** Production §3.5 runs per-regime depth chapters. Each regime gets the 3–8 most operative articles cited verbatim plus how the agent stack must satisfy each plus what the examiner expects.

## §4.2.14 Cluster 14 — Customer and ICP

ICP | FSI | Healthcare | ISV | Sovereign | 10 personas | persona × recipe × segment-variant | 6 recipe families | Customer Support recipe | Code-Modifying recipe | Text-to-SQL recipe | Deep Research recipe | Embedded SaaS Copilot recipe | SOC Agent recipe | insurance gap | Sovereign gap | PHI gap | JTBD | buyer persona | end-user persona | ACV | discovery call

**Why this cluster matters.** The persona × recipe × segment-variant matrix is the Field Guide's customer scaffold. PM-track readers learn the buyer-vs-end-user distinction in Foundations because the PM gate requires it.

## §4.2.15 Cluster 15 — Curriculum

knowledge gate | model brief | model answer | rubric | named evaluator | mentor checkpoint | inter-rater reliability | Anki deck | spaced retrieval | retrieval break | capstone | dual reading paths | engineer track | PM track | common-confusion call-out | near-neighbor concept | worked-example progression | tier prerequisite map | reading-time estimate | pre-work prerequisites

**Why this cluster matters.** The curriculum mechanisms (§4.7 of the design spec) are the Field Guide's pedagogical scaffold. Without them, the asset trains readers to feel ready alone — the highest-cost curriculum failure mode.

---

# §4.3 Quick-reference: the 10 citation classes

Every factual claim in the Field Guide carries one of these 10 evidence-class markers, often layered with regime-binding tags (e.g., `[DORA Art. 28]`, `[FINRA Rule 5280]`). The 10 classes order from highest to lowest evidence weight, with pedagogical-inference tags called out separately.

| Tag | One-line meaning |
|---|---|
| `[primary-regulatory]` | Text of the regulation itself — DORA Art. 28 verbatim, SR 11-7 §III.4 verbatim. Controlling, not evidence. |
| `[independently-audited]` | Third-party-audited claim — SOC 2 attestation, ISO 27001 cert, FedRAMP authorization, EBA AIF audit. Highest evidence weight, scope-limited. |
| `[vendor-contractual]` | Vendor commitment in DPA / MSA / order form — legally binding. High weight. |
| `[vendor-public]` | Vendor public statement — blog, docs, marketing. Low weight, rebuttable, not contractually binding. |
| `[named-incident]` | Public incident report — Slack AI, EchoLeak/CVE-2025-32711, CurXecute/CVE-2025-54135, Samsung 2023, Air Canada, Replit prod-DB, Mata v. Avianca, ConfusedPilot, Salesforce ForcedLeak, ChatGPT Atlas omnibox. |
| `[customer-produced-evidence]` | Customer first-party publication — Klarna engineering blog, Uber Interrupt talk, Replit blog. Different weight than `[vendor-public]`. |
| `[corroborated]` | Claim appears in 2+ independent sources; cross-references categories. |
| `[reference design]` | Pattern from a published reference architecture; not a deployed customer. |
| `[architectural inference]` | Synthesized; not directly stated by any single source. **Red-flag tag in operational dossiers.** |
| `[benchmark]` | Academic / standards-body / public benchmark — McKinsey, OWASP, MITRE ATLAS, AgentDojo, InjecAgent, AgentHarm. |

**Canonical teaching attached:** vendor-disclosed metrics are **not** MRM-validation evidence under SR 11-7. Klarna's 80% / 700-FTE / Uber's 21K dev hours / LinkedIn's 95% / Komodo's 330M are vendor marketing, usable for benchmarking and discussion, never for any validation report an SE signs.

---

# §4.4 Quick-reference: the 7 LangGraph topologies

| # | Topology | One-line definition | Anchor customer(s) |
|---|---|---|---|
| 1 | **ReAct** | Single-agent reason+act loop (Yao et al. 2022). The most-deployed pattern. | (most LangGraph starter agents) |
| 2 | **ReAct + Reflexion** | Single-agent with self-critique step (Shinn et al. 2023). | (research-grade variant) |
| 3 | **Plan-and-Execute** | Planner LLM + executor LLM + replanner LLM. `deepagents` harness. | Captide, Morningstar Mo, Athena Intelligence |
| 4 | **Supervisor** | One routing supervisor with N specialist workers. `langgraph-supervisor-py`. Production-default for multi-tool routing. | Klarna (routed multi-agent) |
| 5 | **Hierarchical** | Supervisor of supervisors. Recursive structure. | Uber AutoCover, ServiceNow |
| 6 | **Agentic RAG** | Retrieval-as-tool with self-correction (CRAG, Self-RAG variants). | Elastic AI Assistant, Vizient |
| 7 | **Network (Swarm)** | Peer agents with handoffs, no central supervisor. `langgraph-swarm-py`. **Renamed** from "Multi-Agent Collaboration." | (peer-to-peer experiments) |

**Honesty callout (Patterns §2.2):** the community treats `deepagents` as graduating to topology 8 and "Supervisor as Tool" as a fourth multi-agent topology per the LangGraph docs. The Field Guide names this rather than papering over it.

Cross-references: → 7 LangGraph topologies, → topology 8 emergence, → langgraph-supervisor-py, → langgraph-swarm-py, → deepagents.

---

# §4.5 Quick-reference: the 6 recipe families

| # | Recipe | One-line | Anchor customer | Dominant failure mode |
|---|---|---|---|---|
| 1 | **Customer Support Copilot** | Front-line customer-service automation with HITL escalation. | Klarna (routed multi-agent) | Hallucinated policy (Air Canada anchor) |
| 2 | **Code-Modifying Developer Agents** | Refactor + test + PR-propose for engineering migrations. | Uber Validator + AutoCover, Replit Agent | Hallucinated API surface; destructive-write blast radius (Replit anchor) |
| 3 | **Text-to-SQL / Conversational Analytics** | Natural-language query of the data warehouse with RLS. | LinkedIn (internal), Vizient | Cross-tenant aggregation |
| 4 | **Multi-Agent Deep Research** | Plan-and-execute investigation across documents. | Captide, Morningstar Mo, Exa | Citation hallucination (Mata v. Avianca anchor) |
| 5 | **Embedded SaaS Copilot** | In-product copilot that takes actions on user's behalf. | AppFolio Realm-X, ServiceNow | Action-on-behalf-of-user identity gap (Salesforce ForcedLeak anchor) |
| 6 | **Security Agents (SOC)** | Agentic RAG over SIEM / EDR / threat intel for alert triage. | Elastic AI Assistant | Alert-fatigue mis-triage |

Foundations §1.10 walks each recipe at JTBD + components + dominant failure mode depth. Patterns §2.3 carries the full state graph per recipe. Production §3.7 carries the audit-evidence pattern per recipe.

Cross-references: → 6 recipe families, → JTBD, → buyer persona, → end-user persona.

---

# §4.6 Quick-reference: the 10 deployment-shape axes

The 10-axis matrix from Production §3.1 — the answer to "where does my data and identity physically reside" rather than "which LangChain SKU am I buying."

| Axis | One-line |
|---|---|
| 1 | **Cloud locus** — where the agent runtime physically executes. |
| 2 | **Identity perimeter** — where agent + human authentication terminates. |
| 3 | **Data perimeter** — where retrieval / state / checkpointer data physically resides. |
| 4 | **Trace egress** — where observability traces go (including BYOC dataplane-listener callbacks). |
| 5 | **Secret perimeter** — where credentials are stored. |
| 6 | **Network egress** — what egress is allowed from the agent runtime. |
| 7 | **Model perimeter** — where LLM inference physically executes (Bedrock cross-region inference profile explicit). |
| 8 | **Tool-call perimeter** — which tools / MCP servers the agent can reach. |
| 9 | **HitL surface** — where HITL checkpoints surface to humans (Slack, Teams, custom UI, LangGraph Studio). |
| 10 | **Support / break-glass** — what vendor access exists for ops / support (paired with SOC 2 controls in BYOC). |

The 9 deployment shapes (rows): LangGraph Cloud SaaS, BYOC AWS, BYOC Azure (gap), BYOC GCP (gap), Self-Hosted Enterprise, Self-Hosted Lite, Developer Tier, CSP-managed (Bedrock / Vertex / Foundry), Sovereign air-gap.

Cross-references: → 10-axis deployment matrix, → LangGraph Cloud SaaS, → BYOC, → Self-Hosted Enterprise, → CSP-managed, → Sovereign air-gap.

---

# §4.7 Acronyms quick-reference

Every acronym used in the Field Guide, with full term and short pointer.

| Acronym | Full term |
|---|---|
| A2A | Agent2Agent Protocol — top layer of the three-layer protocol stack |
| ABAC | Attribute-Based Access Control |
| ACV | Annual Contract Value |
| AGNTCY | Cisco/Outshift-led open agent-protocol initiative |
| AGP | Agent Gateway Protocol — bottom layer of the three-layer protocol stack |
| AI Act | EU AI Act (Regulation 2024/1689) |
| AICPA | American Institute of Certified Public Accountants |
| AKS | Azure Kubernetes Service |
| APAC | Asia-Pacific (regional bucket for regulatory regimes) |
| ARR | Annual Recurring Revenue |
| AUM | Assets Under Management |
| AWS | Amazon Web Services |
| BAA | Business Associate Agreement (HIPAA) |
| BSI | Bundesamt für Sicherheit in der Informationstechnik (German federal cyber-security office; C5) |
| BYOC | Bring Your Own Cloud (LangGraph Platform deployment shape) |
| BYOK | Bring Your Own Key |
| CBUAE | Central Bank of the United Arab Emirates |
| CCA | Confidential Computing Architecture (ARM TEE) |
| CCPA | California Consumer Privacy Act (now CPRA) |
| CIBA | Client-Initiated Backchannel Authentication |
| CIO | Chief Information Officer |
| CDO | Chief Data Officer |
| CISO | Chief Information Security Officer |
| CMIA | Confidentiality of Medical Information Act (California) |
| CNCF | Cloud Native Computing Foundation |
| CPRA | California Privacy Rights Act |
| CRAG | Corrective RAG |
| CRD | Custom Resource Definition (Kubernetes) |
| CSP | Cloud Service Provider |
| CTO | Chief Technology Officer |
| CUI | Controlled Unclassified Information |
| CVE | Common Vulnerabilities and Exposures |
| DCR | Dynamic Client Registration (OAuth) |
| DFSA | Dubai Financial Services Authority |
| DLP | Data Loss Prevention |
| DoD | US Department of Defense |
| DORA | Digital Operational Resilience Act (EU 2022/2554) |
| DPA | Data Processing Agreement |
| DPDPA | Digital Personal Data Protection Act (India, 2023) |
| DPIA | Data Protection Impact Assessment |
| DPoP | Demonstrating Proof-of-Possession (RFC 9449) |
| EAR | Entity Attestation Result (IETF draft) |
| EAT | Entity Attestation Token ([RFC 9711](https://datatracker.ietf.org/doc/html/rfc9711)) |
| EBA | European Banking Authority |
| ECB | European Central Bank |
| EDR | Endpoint Detection and Response |
| EKS | Amazon Elastic Kubernetes Service |
| ELSER | Elastic Learned Sparse EncodeR |
| ENISA | European Union Agency for Cybersecurity |
| EU | European Union |
| EUCC | EU Common Criteria |
| EUCS | EU Cybersecurity Certification Scheme for Cloud Services |
| FDA | US Food and Drug Administration |
| FedRAMP | Federal Risk and Authorization Management Program |
| FFIEC | Federal Financial Institutions Examination Council |
| FGA | Fine-Grained Authorization |
| FINRA | Financial Industry Regulatory Authority |
| FSI | Financial Services Industry |
| FQDN | Fully Qualified Domain Name |
| GA | General Availability |
| GCP | Google Cloud Platform |
| GDPR | General Data Protection Regulation (EU 2016/679) |
| GLBA | Gramm-Leach-Bliley Act |
| GKE | Google Kubernetes Engine |
| GPAI | General-Purpose AI (EU AI Act) |
| HHS | US Department of Health and Human Services |
| HIPAA | Health Insurance Portability and Accountability Act |
| HitL | Human-in-the-Loop |
| HITL | Human-in-the-Loop (alternative casing) |
| HKMA | Hong Kong Monetary Authority |
| HLTM | Hierarchical Long-Term Semantic Memory (LinkedIn) |
| HSM | Hardware Security Module |
| HTI-1 | Health Data, Technology, and Interoperability rule |
| IAM | Identity and Access Management |
| IDP | Identity Provider (IdP — generic OAuth/OIDC term) |
| ICP | Ideal Customer Profile |
| ICT | Information and Communication Technology (DORA) |
| IL4 | Impact Level 4 (DoD CC SRG) |
| IL5 | Impact Level 5 (DoD CC SRG) |
| IPI | Indirect Prompt Injection |
| IR | Incident Response |
| ISO | International Organization for Standardization |
| ISV | Independent Software Vendor |
| JIT | Just-In-Time (access) |
| JTBD | Jobs to Be Done |
| JWT | JSON Web Token |
| KMS | Key Management Service |
| KV | Key-Value (cache) |
| LangGraph | LangChain's open-source agent graph framework |
| LF AAIF | Linux Foundation Agentic AI Foundation |
| LF AI & Data | Linux Foundation AI and Data |
| LLM | Large Language Model |
| LMDeploy | Inference framework (APAC default) |
| MAF | Microsoft Agent Framework |
| MAS | Monetary Authority of Singapore |
| MCP | Model Context Protocol |
| MFA | Multi-Factor Authentication |
| MiFID | Markets in Financial Instruments Directive |
| MITRE ATLAS | Adversarial Threat Landscape for AI Systems |
| MRM | Model Risk Management |
| MSA | Master Services Agreement |
| NIM | NVIDIA Inference Microservices |
| NIS2 | Network and Information Security Directive 2 |
| NIST | National Institute of Standards and Technology |
| NYDFS | New York Department of Financial Services |
| OAuth | Open Authorization framework |
| OCC | Office of the Comptroller of the Currency |
| OCSF | Open Cybersecurity Schema Framework |
| OIDC | OpenID Connect |
| OPA | Open Policy Agent |
| OSS | Open-Source Software |
| OTel | OpenTelemetry |
| OWASP | Open Worldwide Application Security Project |
| PAR | Pushed Authorization Requests (RFC 9126) |
| PCCP | Predetermined Change Control Plan (FDA) |
| PCI DSS | Payment Card Industry Data Security Standard |
| PDPA | Personal Data Protection Act (Singapore / Thailand variants) |
| PDPL | Personal Data Protection Law (UAE; also other jurisdictions) |
| PHI | Protected Health Information (HIPAA) |
| PII | Personally Identifiable Information |
| PIM | Privileged Identity Management (Microsoft) |
| PIPL | Personal Information Protection Law (China) |
| PKCE | Proof Key for Code Exchange (RFC 7636) |
| PoC | Proof of Concept |
| PRD | Product Requirements Document |
| RAG | Retrieval-Augmented Generation |
| RAR | Rich Authorization Requests (RFC 9396) |
| RATS | Remote Attestation Procedures ([RFC 9334](https://datatracker.ietf.org/doc/html/rfc9334)) |
| RBAC | Role-Based Access Control |
| ReAct | Reasoning + Acting (Yao et al. 2022) |
| ReBAC | Relationship-Based Access Control |
| RFC | Request for Comments (IETF) |
| RLS | Row-Level Security |
| RTS | Regulatory Technical Standards (EU) |
| SaaS | Software-as-a-Service |
| SaMD | Software as a Medical Device |
| SAMA | Saudi Arabian Monetary Authority |
| SAML | Security Assertion Markup Language |
| SBOM | Software Bill of Materials |
| SC | Solution Consultant |
| SCC | Standard Contractual Clauses (GDPR) |
| SDK | Software Development Kit |
| SDA | Sovereign Data Authority |
| SDAIA | Saudi Data and AI Authority |
| SE | Sales Engineer |
| SEV-SNP | Secure Encrypted Virtualization — Secure Nested Paging (AMD TEE) |
| SEC | US Securities and Exchange Commission |
| SHE | Self-Hosted Enterprise (LangGraph Platform) |
| SIEM | Security Information and Event Management |
| SLSA | Supply-chain Levels for Software Artifacts |
| SOC | Security Operations Center / Service Organization Control |
| SOC 2 | Service Organization Control 2 (AICPA) |
| SPIFFE | Secure Production Identity Framework For Everyone |
| SPIRE | SPIFFE Runtime Environment |
| SVID | SPIFFE Verifiable Identity Document |
| SQL | Structured Query Language |
| SR 11-7 | Supervisory Letter 11-7 (Federal Reserve / OCC, MRM) |
| SRE | Site Reliability Engineering |
| SSDF | Secure Software Development Framework (NIST) |
| STRIDE | Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege (threat model) |
| STRIDE-A | STRIDE + Autonomy abuse |
| TCB | Trusted Computing Base |
| TDRA | Telecommunications and Digital Government Regulatory Authority (UAE) |
| TDX | Intel Trust Domain Extensions (TEE) |
| TEE | Trusted Execution Environment |
| TLPT | Threat-Led Penetration Testing (DORA) |
| TLS | Transport Layer Security |
| TPP | Third-Party Provider (DORA) |
| TRM | Technology Risk Management (MAS guidelines) |
| TSA | Time Stamping Authority |
| UAE PDPL | United Arab Emirates Personal Data Protection Law |
| vCPU | virtual CPU |
| VPC | Virtual Private Cloud |
| WORM | Write-Once-Read-Many |
| ZDR | Zero-Data-Retention |

---

# §4.8 Out-of-scope: intentional omissions

The Field Guide intentionally does **not** define the following terms in the body, even though related concepts may appear elsewhere. Each entry explains the reasoning.

**Bleed.** Term used in some vendor-internal taxonomies (including the author's OPAQUE-internal Phase 2 overlay) and in some competitor taxonomies for the same architectural concept this Field Guide calls a **data-leak surface** or **leakage pathway**. The Field Guide uses public-grade vocabulary aligned with OWASP LLM Top 10, OWASP Agentic Top 10, MITRE ATLAS, NIST AI RMF, and the EU AI Act. The terminology choice is deliberate per the v3 design-spec mandate. Readers encountering "bleed" in vendor materials should understand it as a synonym for data-leak surface in this Field Guide's vocabulary. See `CONFLICTS.md` for the full affiliation disclosure relevant to this terminology choice.

**P-ID (Pathway Identifier).** Vendor-internal taxonomy numbering scheme. Not used in the Field Guide body. See the same explanation as for "bleed."

**OPAQUE Systems / OPAQUE confidential computing.** The author's affiliation. Disclosed in the author bio in `00-introduction.md` and in `CONFLICTS.md`. Named sparingly in the Part I (Foundations) body per the standards-anchored editorial rule documented in `CONFLICTS.md` §1 — at most once per section, where the architecture surfaces a gap that has both a named industry standard and a specific OPAQUE-shipping primitive. **Not used as product positioning in Part II (Patterns) or Part III (Production) bodies.** The Production §3.6.15 substrate-level cluster discusses substrate primitives (TEE attestation, sealed keys, attested network egress, attested workload identity) at category level — naming the specific substrate primitive and the residual risk, but not naming any vendor (including OPAQUE) as the remediation answer.

**PAC (Product Advisory Council).** Author-internal skill name from CompanyOS. Unrelated to the Field Guide.

**ICP eval / persona panel / Working Backwards / PR-FAQ.** Author-internal coaching artifacts from the OPAQUE PM skill. Used for internal artifact creation; not referenced in the Field Guide body.

**Specific OPAQUE 2.7 / 3.0 capability names.** Reserved for the Phase 2 OPAQUE-internal overlay; not in the public CC BY-SA artifact.

**Implementation tutorial vocabulary** (notebook cell, code-cell-skip, hands-on lab, exercise solution). The v1 of the Field Guide ships reference content; hands-on code samples are deferred to v1.5. Tutorial-style vocabulary is not in scope.

---

# §4.9 Glossary maintenance

This glossary follows the 90-day update cadence committed in design spec §7. Quarterly glossary audits are part of the documented revision cycle. Per CSO discipline:

- New terms introduced in tier files are first-use-linked to this glossary at write time.
- Terms that fall out of use are not deleted — they are marked `[deprecated]` so downstream readers encountering old references can resolve them.
- Cross-references are validated on every audit — every `→ term` arrow must resolve to a defined entry.
- Tier markers are validated against the actual tier files — `(Foundations)` means the term has a definition in §1.x, not merely a mention.

Reader-side: open an issue on the public GitHub repository if you encounter a term in the tier files without a canonical definition here, or a definition here that contradicts how the term is used in a tier file. Cross-tier consistency is the load-bearing property of this glossary.

---

*End — Field Guide Glossary.*

*Companion files:* `01-foundations.md` · `02-patterns.md` · `03-production.md` · `05-anki-deck/` · `CONFLICTS.md` · `LICENSE`.

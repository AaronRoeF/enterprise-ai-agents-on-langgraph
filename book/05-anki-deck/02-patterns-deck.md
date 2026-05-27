# Patterns Deck — Anki Spaced-Retrieval Cards

> Source tier: `book/02-patterns.md` ("Enterprise AI Agents on LangGraph: A Field Guide" — Chapter 2).
>
> Card count: 124. Reader floor: any reader who has completed Foundations and read Patterns once. Review cadence: daily for 21 days, then twice-weekly for 60 days.
>
> Card-type distribution: definition recall (37), decision/disambiguation (24), named-component / customer-voice (24), failure-mode / regulatory (18), worked-fragment (12), citation-class (7).
>
> Cards ordered by glossary cluster. License: CC BY-SA 4.0.

---

## Cluster 1 — Framework landscape (Patterns depth)

### Q: Name the three camps in the 2026 agent framework landscape.
**A:** (1) Graph-native open-source orchestrators (LangGraph — production-tier dominant); (2) open-source multi-agent frameworks for faster developer onboarding (CrewAI, AutoGen/AG2, LlamaIndex Workflows, Pydantic AI, Mastra, Agno, Smol Agents, Letta, DSPy); (3) hyperscaler / platform vendor stacks (MAF, Bedrock AgentCore, Vertex Agent Engine, Snowflake Cortex Agents, Databricks Mosaic, NVIDIA AI-Q, IBM watsonx Orchestrate, Salesforce Agentforce).
**Cluster:** Framework landscape
**Tier reference:** §2.1.2

### Q: Name the six honest LangGraph gaps from §2.1.6.
**A:** (1) TypeScript runtime parity lag (~6–9 months behind Python); (2) BYOC AWS-only as of 2025; (3) no public FedRAMP authorization at the orchestration layer; (4) identity-tier evidence thinness; (5) sovereign zero; (6) healthcare PHI in production zero.
**Cluster:** Framework landscape
**Tier reference:** §2.1.6

### Q: Name the two procurement-ambiguity traps in the §2.1 framework matrix.
**A:** (1) AutoGen v0.4 vs AG2 fork — sharing lineage but diverging post-Microsoft-departure. (2) CrewAI OSS vs CrewAI Enterprise — commercially distinct products with different compliance postures.
**Cluster:** Framework landscape
**Tier reference:** §2.1.4

### Q: What does the McKinsey 2025 State of AI report say about enterprise agent adoption?
**A:** 88% report regular AI use across at least one business function; **62% of organizations are at least experimenting with AI agents; 23% of enterprises are scaling AI agents in at least one function** (n=1,993, 105 nations, June-July 2025). Leading functions: IT, knowledge management, engineering. `[benchmark]`
**Cluster:** Framework landscape
**Tier reference:** §2.1.5

---

## Cluster 2 — Topologies (deployment depth)

### Q: Topology 1 — describe ReAct and name its primary customer anchor.
**A:** A single-agent loop (Thought → Action → Observation) implemented in LangGraph via `create_react_agent`. Anchor: **Klarna** — now classified as routed multi-agent (closer to Supervisor than pure ReAct, single shared model). Foundations of the topology originate in Yao et al. ICLR 2023. `[customer-produced-evidence] [benchmark]`
**Cluster:** Topologies
**Tier reference:** §2.2.1

### Q: Topology 2 — what is ReAct + Reflexion, and what is its production-anchor status?
**A:** A ReAct loop wrapped with a critic LLM that reviews the attempt and feeds verbal critique back for retry. `langgraph-reflection` harness. **No standalone production anchor** — used as a sub-pattern inside Plan-and-Execute and Hierarchical. Origin: Shinn et al., NeurIPS 2023. `[benchmark]`
**Cluster:** Topologies
**Tier reference:** §2.2.2

### Q: Topology 3 — what is Plan-and-Execute, and what are its named anchors?
**A:** Planner LLM writes a multi-step plan; executor LLM runs each step; replanner LLM re-evaluates after each step. Anchors: **Exa** (Planner/Tasks/Observer), **`deepagents`** production harness, **Captide** (FSI research). `[customer-produced-evidence] [architectural inference]`
**Cluster:** Topologies
**Tier reference:** §2.2.3

### Q: Topology 4 — describe Supervisor and name three customer anchors.
**A:** One supervisor agent routes incoming work to N specialist worker agents; workers report back; supervisor decides next step. `langgraph-supervisor-py` harness. Anchors: **Uber Validator + AutoCover, AppFolio Realm-X, Cisco JARVIS, Vodafone Italy, Vizient.** `[customer-produced-evidence]`
**Cluster:** Topologies
**Tier reference:** §2.2.4

### Q: Topology 5 — describe Hierarchical and name its hero customer anchor.
**A:** Supervisor-of-supervisors — recursive structure with multi-level routing. Anchor: **LinkedIn Hiring Assistant** — billion-member candidate graph, "almost like an org chart" framing per Karthik Ramgopal; HLTM paper. `[customer-produced-evidence]`
**Cluster:** Topologies
**Tier reference:** §2.2.5

### Q: Topology 6 — describe Agentic RAG and name its primary customer anchor.
**A:** A ReAct-shaped agent where retrieval is a tool the LLM chooses to call; after each retrieval, the LLM critiques the documents and may re-query, fall back, or escalate to HITL. Anchor: **Elastic AI Assistant + Attack Discovery + Automatic Import** (ELSER sparse-encoder + BM25 hybrid search). `[customer-produced-evidence]`
**Cluster:** Topologies
**Tier reference:** §2.2.6

### Q: Topology 7 — describe Network (Swarm) and its production-anchor status.
**A:** Peer agents with handoffs, no central supervisor; `langgraph-swarm-py` harness. **No confirmed top-level pure peer production anchor**; the swarm pattern shows up INSIDE a hierarchical system (e.g., Replit Agent editor swarm) rather than as the top-level topology. Renamed from "Multi-Agent Collaboration." `[architectural inference]`
**Cluster:** Topologies
**Tier reference:** §2.2.7

### Q: What is the customer-voice convergence on supervisor + sub-agent topology per §2.2.4?
**A:** Five independent customer engineers converge: Hasith Kalpage (Cisco — "supervised, specialized, and reflection agents working together in feedback loops"); Michele Catasta (Replit — "control and ergonomics"); Karthik Ramgopal (LinkedIn — "almost like an org chart"); Vodafone Italy's Supervisor + Use-Cases dual-graph; Vizient's hierarchical-worker-supervisor pattern.
**Cluster:** Topologies
**Tier reference:** §2.2.4

### Q: What is CRAG?
**A:** **Corrective RAG** — an Agentic RAG variant that falls back to web search on retrieval failure. One of the named Agentic RAG sub-patterns.
**Cluster:** Topologies
**Tier reference:** §2.11

### Q: What is Self-RAG?
**A:** An Agentic RAG variant that grades its own final answer for groundedness against retrieved docs before returning. Named alongside CRAG as a §2.2.6 sub-pattern.
**Cluster:** Topologies
**Tier reference:** §2.11

### Q: What is HLTM (LinkedIn Hiring Assistant)?
**A:** **Hierarchical Long-Term Semantic Memory** — LinkedIn's tree-indexed semantic memory architecture for the Hiring Assistant. Anchors the Hierarchical topology at customer-disclosed depth. `[customer-produced-evidence]`
**Cluster:** Topologies
**Tier reference:** §2.11

---

## Cluster 3 — Recipes (deployment depth)

### Q: Recipe 1 — Support Agent — name the four customer anchors per §2.3.1 and §3.7.1.
**A:** **Klarna** (routed multi-agent, single shared model), **Vodafone Italy / Fastweb** (dual-graph Supervisor + Use Cases, Neo4j-backed, 86%+ One-Call Resolution), **Rakuten** (supervisor topology), **Doctolib** (gated patient-facing copilot, non-PHI). `[customer-produced-evidence]`
**Cluster:** Recipes
**Tier reference:** §2.3.1 / §3.7.1

### Q: Recipe 2 — Coding Agent — what does Uber's Lang Effect framework do?
**A:** Lang Effect is Uber's internal framework wrapping LangGraph + LangChain for internal-system integration. Powers Validator + AutoCover (~21K developer hours reclaimed per Uber's Interrupt 2025 talk). `[customer-produced-evidence]`
**Cluster:** Recipes
**Tier reference:** §2.3.2

### Q: Recipe 3 — Text-to-SQL — name the LinkedIn product and the platform it embeds in.
**A:** **SQL Bot**, embedded in **DARWIN** (LinkedIn's internal data science platform). Conversational analytics over LinkedIn's data warehouse. `[customer-produced-evidence]`
**Cluster:** Recipes
**Tier reference:** §2.3.3

### Q: Recipe 4 — Deep Research — what are the named Plan-and-Execute production anchors?
**A:** **Captide** (FSI research; full Plan-and-Execute), **Morningstar Mo** (wealth research with RAG at each step), **Athena Intelligence**, **Exa** (deep research infrastructure with Planner/Tasks/Observer). `[customer-produced-evidence]`
**Cluster:** Recipes
**Tier reference:** §2.3.4

### Q: Recipe 5 — Embedded SaaS Copilot — name two production anchors.
**A:** **AppFolio Realm-X** (property-management copilot, Supervisor topology) and **ServiceNow** (Hierarchical with Send-API fanout). Also **Doctolib Alfred** (healthcare-adjacent, non-PHI). `[customer-produced-evidence] [architectural inference]`
**Cluster:** Recipes
**Tier reference:** §2.3.5

### Q: Recipe 6 — Security Agent — what is the named anchor and how does Elastic structure retrieval?
**A:** **Elastic AI Assistant + Attack Discovery + Automatic Import**. Agentic RAG over Elastic indexes; retrieval combines **ELSER** (Elastic's sparse encoder) with **BM25** for hybrid search. The 1-of-18 deployment where CISO is primary buyer. `[customer-produced-evidence]`
**Cluster:** Recipes
**Tier reference:** §2.3.6

---

## Cluster 4 — Identity (Patterns depth)

### Q: Restate the three identity problems at Patterns depth (per §2.4.1).
**A:** Problem 1 — **Agent identity** (workload itself; auth in IAM logs; shadow-IT discovery). Problem 2 — **Agent-on-behalf-of-user identity** (delegation; cryptographically bound to a specific human). Problem 3 — **Action-provenance binding** (every action signed with who acted on whose behalf with which scope at what time; the operative audit primitive).
**Cluster:** Identity (Patterns)
**Tier reference:** §2.4.1

### Q: What is Microsoft Entra Agent ID and what is its release status?
**A:** GA 2025. Microsoft's first-class agent identity primitive in Entra ID (rebranded Azure AD). Each agent gets an Entra identity with Conditional Access policies, PIM integration, and audit trails. Distinct from user, service principal, or managed identity. `[vendor-public]`
**Cluster:** Identity (Patterns)
**Tier reference:** §2.4.2

### Q: What is the difference between Okta for AI Agents and Auth0 for AI Agents?
**A:** Both Okta-owned. **Okta for AI Agents** — enterprise IAM extension for Okta Workforce Identity (FSI / large healthcare / traditional enterprise). **Auth0 for AI Agents** — developer-friendly SDK with Cross App Access (XAA), Auth0 FGA, Token Vault (ISV / SaaS-startup population). Both EA 2025. `[vendor-public]`
**Cluster:** Identity (Patterns)
**Tier reference:** §2.4.3

### Q: Name the five OAuth 2.x primitives relevant to agents per §2.4.5 with one-line "why it matters" for each.
**A:** **DPoP** (RFC 9449) — token binding to prevent stolen-token replay. **PAR** (RFC 9126) — pushed authorization requests, parameters not in URLs. **RAR** (RFC 9396) — rich authorization requests, structured fine-grained scope assertions. **CIBA** (OIDC FAPI) — backchannel approval via user device. **PKCE** (RFC 7636) — the practical default for OAuth code-flow protection.
**Cluster:** Identity (Patterns)
**Tier reference:** §2.4.5

### Q: Worked fragment — what does this RAR payload assert?
```json
{
  "type": "payment_initiation",
  "actions": ["initiate"],
  "locations": ["https://example-bank.com/api/v1/payments"],
  "instructedAmount": {"currency": "EUR", "amount": "123.50"},
  "creditorName": "Merchant Inc",
  "creditorAccount": {"iban": "DE02..."}
}
```
**A:** A Rich Authorization Request (RFC 9396) for an agent making a specific financial transaction — authorizing exactly this payment for exactly this amount to exactly this creditor, rather than a coarse "payments:write" scope. Maps to PSD2 SCA flows and per-transaction signed assertions.
**Cluster:** Identity (Patterns)
**Tier reference:** §2.4.5

### Q: What is the MCP Authorization spec, and what is the substrate it builds on?
**A:** OAuth 2.1 + Dynamic Client Registration (RFC 7591) + Protected Resource Metadata (RFC 9728). Ratified Q1 2026. The protocol-level closure on "how does an MCP client authenticate to an MCP server?" Custom auth is a deprecation path. `[vendor-public]`
**Cluster:** Identity (Patterns)
**Tier reference:** §2.4.6

### Q: What is MCP elicitation?
**A:** A Q4 2025 addition — a mid-tool-call interactive input mechanism where an MCP tool server can pause execution and ask the agent (or, through the agent, the user) for additional input. Useful for tools that need clarification mid-execution. `[vendor-public]`
**Cluster:** Identity (Patterns)
**Tier reference:** §2.4.7

### Q: What is MCP sampling, and why is it a security boundary?
**A:** A mechanism where the MCP server requests an LLM call from the client. Lets servers be LLM-aware without bundling their own model. **Security boundary:** the MCP server should not be able to arbitrarily request LLM calls from the client without explicit policy.
**Cluster:** Identity (Patterns)
**Tier reference:** §2.4.7

### Q: Name the eight FGA products per §2.4.8.
**A:** **OpenFGA** (CNCF sandbox, open source), **Cedar / AWS Verified Permissions** (open-source policy lang + AWS-managed deployment), **Topaz** (Aserto, open source), **Okta FGA** (commercial extension of OpenFGA), **Auth0 FGA** (commercial, bundled with Auth0 for AI Agents), **Permit.io** (hybrid open-source PDP + commercial control plane), **Oso** (Polar OSS + Oso Cloud commercial), **Styra** (creator of OPA; Styra DAS commercial).
**Cluster:** Identity (Patterns)
**Tier reference:** §2.4.8

### Q: Worked fragment — what is this OpenFGA model defining (Recipe 3, Text-to-SQL)?
```
type document
  relations
    define cohort: [cohort]
    define viewer: researcher from cohort

type agent
  relations
    define on_behalf_of: [user]
    define can_query: viewer from document
```
**A:** The agent has no read authority by itself. To query `document`, the agent must `on_behalf_of` a `user` who is a `researcher` of the document's `cohort`. This is the **agent-on-behalf-of-user delegation** at FGA-model depth — cross-tenant cohort access for healthcare Text-to-SQL.
**Cluster:** Identity (Patterns)
**Tier reference:** §2.4.8

### Q: What is SPIFFE/SPIRE and where does it fit for agent identity?
**A:** **SPIFFE** is a CNCF-graduated workload-identity specification (`spiffe://trust-domain/path` URIs). **SPIRE** is the reference runtime. SVIDs are short-lived (typically 1 hour), auto-rotated. Most relevant to sovereign + air-gap FSI deployments where cloud-provider IAM is structurally rejected. `[vendor-public]`
**Cluster:** Identity (Patterns)
**Tier reference:** §2.4.9

### Q: What is the customer-disclosed hero identity anchor in the 18-deployment dataset?
**A:** **Doctolib's two-token JWT + Keycloak pattern** — the only customer in the entire dataset that named its identity stack at architectural depth. Service-to-service JWT (with audience + issuer claims) + user's Keycloak token carrying user identity and permissions. `[customer-produced-evidence]`
**Cluster:** Identity (Patterns)
**Tier reference:** §2.4.11

### Q: Quote: "The system implements service-to-service authentication using JSON Web Tokens with each token containing audience and issuer claims, while user context is propagated with two tokens: the service-to-service JWT and the user's Keycloak token..." — Who said this?
**A:** **Goulven LE DÛ, Doctolib engineering blog (Medium).** This is the only customer-disclosed identity stack in the 18-deployment LangGraph dataset. `[customer-produced-evidence]`
**Cluster:** Identity (Patterns)
**Tier reference:** §2.4.11

### Q: Quote: "the LLM will never directly execute sensitive actions, with the final step of changing agenda accesses always remaining in users' hands as a human-in-the-loop approach" — Who said this and what is the teaching?
**A:** **Doctolib engineering blog**, on the operational discipline behind their LangGraph-based "Alfred" assistant. The teaching: HITL on every PHI-disclosing branch is the operational complement to the two-token identity stack. `[customer-produced-evidence]`
**Cluster:** Identity (Patterns)
**Tier reference:** §2.4.11

### Q: What is the customer-disclosed identity pattern at Infor?
**A:** **API gateway enforces security permissions and data governance.** Tools exposed via Infor OS API gateway endpoints; the gateway carries authentication, per-tenant authorization, and PII/PHI filtering. The agent itself is a thin orchestrator. Complementary to Doctolib's two-token pattern. `[vendor-public]`
**Cluster:** Identity (Patterns)
**Tier reference:** §2.4.12

### Q: Why is custom JWT still the modal pattern observed in 2026 LangGraph production?
**A:** Purpose-built agent-identity products (Entra Agent ID, Okta for AI Agents, Auth0 for AI Agents) are too new (2025-launched) to have customer-disclosed production scale. Custom JWT is fast to ship; FGA is layered on top for the authorization decision. `[vendor-public + architectural inference]`
**Cluster:** Identity (Patterns)
**Tier reference:** §2.4.10

---

## Cluster 5 — ICP industry deep-dive

### Q: Name the four ICP industries the Field Guide carries through Patterns.
**A:** **FSI** (Financial Services), **Healthcare**, **ISV** (Independent Software Vendors), **Sovereign / Public Sector**. The first three have customer-disclosed LangGraph deployments; Sovereign is `[evidence-zero, structural-fit-only]`.
**Cluster:** ICP segments
**Tier reference:** §2.5

### Q: Name the four FSI sub-segments and one named LangGraph customer per segment (where applicable).
**A:** Payments (Klarna, Stripe-adjacent), Wealth management / research (Morningstar Mo, BlackRock Aladdin Copilot), Research / asset management (Captide), Insurance (**zero** LangGraph footprint — 68% of insurers running gen-AI but on hyperscaler-native stacks). `[customer-produced-evidence] [architectural inference]`
**Cluster:** ICP segments
**Tier reference:** §2.5.1

### Q: What is the PHI-in-production status for LangGraph on any framework as of May 2026?
**A:** **`[reference design only — not in PHI production anywhere on any framework]`.** The three named Healthcare LangGraph deployments (Doctolib Alfred, Vizient supply-chain, Komodo Health MapAI) operate on non-PHI or de-identified data only.
**Cluster:** ICP segments
**Tier reference:** §2.5.2

### Q: How many patient journeys does Komodo Health MapAI process, and at what regulatory scope?
**A:** **330M patient journeys at de-identified longitudinal scope.** Safe Harbor + Expert Determination engineering. Non-PHI in the regulatory sense — not PHI in production. `[customer-produced-evidence — Komodo's own materials]`
**Cluster:** ICP segments
**Tier reference:** §2.5.2

### Q: What is the persona-heatmap headline finding per §2.6.2?
**A:** **CTO-ISV is the modal LangGraph buyer at 14 of 18 deployments.** Champion is the modal operator at 13 of 18. **CISO is primary buyer at exactly ONE deployment (Elastic).** Sovereign is at zero.
**Cluster:** ICP segments
**Tier reference:** §2.6.2

---

## Cluster 6 — Governance failure modes at category depth

### Q: Name the six control boundaries (B1–B6) per §2.7.1.
**A:** **B1 Access** (only authorized principals access data). **B2 Flow** (data moves only within authorized boundaries). **B3 Time** (data persists only for authorized lifetime). **B4 Information** (derivatives don't reveal source). **B5 Enforcement Substrate** (execution environment actually enforces what it assumes). **B6 Human Intent** (humans approve / share in line with intent).
**Cluster:** Governance categories
**Tier reference:** §2.7.1

### Q: Name the six high-frequency governance category groups per §2.7.2.
**A:** (1) Cross-tenant aggregation (five surfaces — dominant architectural concern); (2) Prompt injection (direct + indirect via RAG + indirect via tool output); (3) Identity & action-provenance gaps; (4) Hallucination-to-action; (5) Telemetry capture & cross-boundary egress; (6) Supply chain & dependency compromise.
**Cluster:** Governance categories
**Tier reference:** §2.7.2

### Q: Name the five cross-tenant isolation surfaces per §2.7.2 Category 1.
**A:** (1) Retriever surface (per-row tenant predicate at vector store). (2) Cache surface (per-tenant cache key namespacing in Redis, LLM provider prompt cache, reranker cache, embedding cache). (3) Checkpointer surface (per-tenant `thread_id` + per-tenant Postgres schema isolation). (4) Observability surface (per-tenant trace partition). (5) Model surface (per-tenant fine-tune isolation + prompt cache partitioning + KV-cache leakage).
**Cluster:** Governance categories
**Tier reference:** §2.7.2

### Q: Why is application-layer RBAC insufficient for the cross-tenant aggregation problem?
**A:** None of the five surfaces are protected by application-layer RBAC alone. Cross-tenant aggregation is the surface that pre-AI multi-tenant architectures were never designed to cover. Each requires explicit per-tenant configuration at the surface itself.
**Cluster:** Governance categories
**Tier reference:** §2.7.2

### Q: Which leakage surface is the Slack AI incident an anchor for?
**A:** **S16 — Indirect Prompt Injection via Retrieved Content.** Slack AI (Aug 2024, PromptArmor disclosure) — crafted public-channel messages exfiltrate private-channel data via prompt-injection payload retrieved during a private-channel query. `[named-incident]`
**Cluster:** Governance categories
**Tier reference:** §2.7.4

### Q: Which leakage surface is EchoLeak / CVE-2025-32711 an anchor for?
**A:** **S16 — Indirect Prompt Injection via Retrieved Content (zero-click).** Microsoft 365 Copilot; crafted email retrieved by RAG triggers data exfiltration with no user click. CVSS 9.3. `[named-incident]`
**Cluster:** Governance categories
**Tier reference:** §2.7.4

### Q: Which leakage surface is CurXecute / CVE-2025-54135 an anchor for?
**A:** **S17 — Indirect Prompt Injection via Tool / MCP Output.** Cursor IDE; MCP tool output poisoning becomes RCE. **The canonical MCP-supply-chain-and-injection compound incident.** `[named-incident]`
**Cluster:** Governance categories
**Tier reference:** §2.7.4

### Q: Which leakage surface is ConfusedPilot an anchor for?
**A:** **S18 — Cross-Tenant Aggregation in Shared Vector Indexes.** UT Austin, 2024 — semantic search retrieval crossing intended access boundaries in Microsoft 365 Copilot-class deployments. USENIX Security 2024. `[named-incident] [benchmark]`
**Cluster:** Governance categories
**Tier reference:** §2.7.4

### Q: Which leakage surface is ForcedLeak (Salesforce Agentforce, Sept 2025) an anchor for?
**A:** Multiple — including **S22 (identity & action-provenance)** and **S26 (agent-to-agent communication leak)**. Disclosed by Noma Security; indirect injection via web form. Teaches that purpose-built enterprise agent platforms are not automatically safe. `[named-incident]`
**Cluster:** Governance categories
**Tier reference:** §2.7.4

### Q: Which leakage surface is Replit Agent prod-DB deletion (May 2025) an anchor for?
**A:** Multiple — **S22 (identity gaps)**, **S23 (hallucination-to-action)**, and **S27 (HITL bypass)**. Agent given broad write access without HITL deleted production data against explicit user instruction. `[named-incident]`
**Cluster:** Governance categories
**Tier reference:** §2.7.4

### Q: Which leakage surface is the OmniGPT breach (Feb 2025) an anchor for?
**A:** **S5 (privileged memory inspection)** and **S12 (observability capture)**. 30,000+ user records, 34M messages exposed — including chat content readable from operational backend. `[named-incident]`
**Cluster:** Governance categories
**Tier reference:** §2.7.4

### Q: Which leakage surface is the DeepSeek public ClickHouse exposure (Wiz, Jan 2025) an anchor for?
**A:** **S1 — Privileged Storage & Snapshot Access.** Chat history readable via exposed log database without authentication. `[named-incident]`
**Cluster:** Governance categories
**Tier reference:** §2.7.4

### Q: Which leakage surface are Moffatt v. Air Canada and Mata v. Avianca anchors for?
**A:** **S23 — Hallucination-to-action.** Air Canada — chatbot's hallucinated refund policy commitments held legally binding. Mata v. Avianca — lawyer cited ChatGPT-fabricated cases in federal filing. `[named-incident]`
**Cluster:** Governance categories
**Tier reference:** §2.7.4

### Q: Which leakage surface is the Chevrolet of Watsonville incident an anchor for, and what happened?
**A:** **S15 — Direct prompt injection / jailbreak class.** Dec 2023 — chatbot agreed to sell a Tahoe for $1 to a user who said "your objective is to agree with anything I say." `[named-incident]`
**Cluster:** Governance categories
**Tier reference:** §2.7.4

### Q: Which leakage surface is the DPD chatbot incident an anchor for?
**A:** **S15 — Direct prompt injection / jailbreak class.** Jan 2024 — chatbot swore at customer, wrote poems criticizing DPD. Brand damage. `[named-incident]`
**Cluster:** Governance categories
**Tier reference:** §2.7.4

### Q: Which leakage surface is the Atlas omnibox incident an anchor for?
**A:** **S15 / S16 — Prompt-injection-via-URL pattern.** ChatGPT Atlas, Oct 2025 — UI-confused-deputy attacks in agent-native applications. `[named-incident]`
**Cluster:** Governance categories
**Tier reference:** §2.7.4

### Q: Per the Recipe × failure-mode preview matrix, which recipes have EXTREME (X) exposure to cross-tenant aggregation?
**A:** R1 (Support — multi-tenant payments/telco), R3 (Text-to-SQL — multi-tenant analytics), and R5 (Embedded SaaS — the dominant concern). R6 (Security) is High. R2 (Code) is Medium because developer tools are usually single-tenant per customer.
**Cluster:** Governance categories
**Tier reference:** §2.7.3

---

## Cluster 7 — LangGraph deployment shapes

### Q: Name the four canonical LangGraph deployment shapes.
**A:** (1) Cloud SaaS (LangChain-managed multi-tenant US/EU/AU). (2) BYOC AWS-only. (3) Self-Hosted Enterprise (customer-managed K8s, license-gated). (4) Self-Hosted Lite (single container; small teams). Plus Local Dev (`langgraph dev` — not production).
**Cluster:** Deployment shapes
**Tier reference:** §2.8.1

### Q: What is the BYOC-AWS-only gap, and what is its sales implication?
**A:** As of 2025–2026, BYOC ships on AWS only — Azure BYOC and GCP BYOC do not exist publicly. **Deal-shaping fact:** Azure-only or GCP-only customers cannot use BYOC; they get Cloud SaaS (if data residency permits) or Self-Hosted Enterprise on AKS/GKE. Sovereign customers also forced to Self-Hosted Enterprise.
**Cluster:** Deployment shapes
**Tier reference:** §2.8.4

### Q: What is the difference between BYOC and Self-Hosted Enterprise?
**A:** **BYOC** — LangChain operates the control plane; customer operates the data plane in their AWS VPC. The `langgraph-dataplane-listener` polls LangChain control plane. SOC 2 in-scope; control-plane egress path exists. **Self-Hosted Enterprise** — customer operates BOTH planes via Helm; license-gated; **no LangChain control-plane egress; air-gap-capable.** The only DORA-defensible posture for Tier-1 FSI.
**Cluster:** Deployment shapes
**Tier reference:** §2.8.2 / §3.1.4

### Q: What is the `langgraph-dataplane-listener` and why does it matter?
**A:** A Helm-installed CRD-watching pod that runs in the customer's BYOC cluster and polls the LangChain control-plane API over HTTPS. It is the mechanism that makes BYOC work — but it also means there is a control-plane-to-LangChain egress path in BYOC. Customer must allow-list LangChain control-plane FQDNs at the egress proxy. `[vendor-public]`
**Cluster:** Deployment shapes
**Tier reference:** §2.8.2

### Q: When would you pick Self-Hosted Enterprise over BYOC AWS?
**A:** When ANY of: sovereign / air-gap required; customer's primary cloud is Azure or GCP; FedRAMP-High at orchestration layer; no vendor SRE break-glass acceptable; sub-processor list disclosure must be minimal; trace destination must be self-hosted Langfuse (not LangSmith Cloud).
**Cluster:** Deployment shapes
**Tier reference:** §2.8.3

---

## Cluster 8 — Hyperscaler ref-arch peer comparison

### Q: Which hyperscaler ref-arch has the "most OAuth-rich agent identity story"?
**A:** **Microsoft Azure AI Foundry + MAF.** Entra Agent ID is native; Conditional Access extends to agent identities; PIM JIT-elevation works for agents. The most thorough hyperscaler ref-arch as of 2026 by Visio-style depth. `[vendor-public]`
**Cluster:** Hyperscaler ref-archs
**Tier reference:** §2.9.1

### Q: What is the LangGraph-on-ECS pattern, and which customer anchors it?
**A:** AWS publishes a first-class LangGraph-on-ECS reference architecture as a framework-native path with AgentCore Gateway as the managed MCP plane. **AppFolio Realm-X** is the canonical customer-disclosed deployment using this pattern. `[vendor-public] [customer-produced-evidence]`
**Cluster:** Hyperscaler ref-archs
**Tier reference:** §2.9.2

### Q: What is the "surprise" observation about NVIDIA AI-Q?
**A:** **NVIDIA AI-Q Blueprint is built on LangGraph internally.** The GPU vendor's own hero reference architecture uses LangGraph as the orchestration substrate. `langchain-nvidia-langgraph` enables GPU-accelerated parallel execution. Named deployments: AT&T, RBC "Jessica" fraud investigator, COACH Japan. `[vendor-public]`
**Cluster:** Hyperscaler ref-archs
**Tier reference:** §2.9.4

### Q: What is GCP Vertex's "Memory Bank," and what LangGraph primitive is it conceptually adjacent to?
**A:** Vertex's dedicated cross-session persistence layer — conceptually adjacent to LangGraph's `BaseStore` for long-term cross-thread memory. Vertex is also the most A2A-native runtime among the big-three hyperscalers.
**Cluster:** Hyperscaler ref-archs
**Tier reference:** §2.9.3

### Q: What is the ITAR limitation for Vertex AI generative models?
**A:** Vertex AI generative models are NOT available under ITAR-scoped Assured Workloads as of May 2026. Deal-blocker for deployments with ITAR or controlled-defense data. `[vendor-public]`
**Cluster:** Hyperscaler ref-archs
**Tier reference:** §2.9.3

### Q: What FedRAMP / DoD posture does AWS Bedrock Agents + AgentCore carry?
**A:** **GovCloud Bedrock + Agents + Guardrails + Knowledge Bases at FedRAMP-High + IL4/IL5 since May 2025.** The most accessible FedRAMP-High path for LangGraph customers needing federal-grade compliance. `[vendor-public]`
**Cluster:** Hyperscaler ref-archs
**Tier reference:** §2.9.2

### Q: What is the IBM watsonx Orchestrate "any agent, any framework" framing, and what is the FedRAMP-High milestone date?
**A:** Agent Connect Framework + Agent Catalog let LangChain / CrewAI / OpenAI Agents SDK / MAF agents all participate; Granite-based Orchestrator Agent at the hub. **FedRAMP-High expansion April 2026.** Named customers: MyLÚA Health, IBM internal HR. `[vendor-public]`
**Cluster:** Hyperscaler ref-archs
**Tier reference:** §2.9.5

### Q: What is the "OCARA white-space" observation?
**A:** Microsoft, AWS, GCP, NVIDIA, and LangChain each publish their own ref-arch — but **nobody publishes a comprehensive, framework-native, LangGraph-centric enterprise reference architecture covering all 10 stack tiers + 6 recipes + 7 topologies + cross-cloud deployment shapes + per-regime compliance overlays + audit-evidence patterns.** This Field Guide is the most thorough attempt to date.
**Cluster:** Hyperscaler ref-archs
**Tier reference:** §2.9.6

---

## Cluster 9 — Cross-tenant isolation (Patterns intro)

### Q: For pgvector, what is the cross-tenant isolation pattern, and what is the modal misconfiguration?
**A:** `tenant_id` column with Postgres row-level security. **RLS is NOT enforced by default** — must be explicitly enabled per table, and the application connection must `SET app.current_tenant = '...'` per request. Modal misconfiguration: RLS bypass via `SECURITY DEFINER` functions. `[community-reported]`
**Cluster:** Cross-tenant isolation
**Tier reference:** §3.2.1 (referenced in §2.7.2)

### Q: For Pinecone, what is the cross-tenant pattern, and what is the failure mode?
**A:** Namespace per tenant — the namespace is part of the query URL path. Failure mode: developer forgets to pass `namespace=...` and the query falls through to the default namespace (which contains all tenants). Mitigation: force namespace via Pinecone client wrapper; reject queries with empty namespace. `[vendor-public]`
**Cluster:** Cross-tenant isolation
**Tier reference:** §3.2.1 (Patterns §2.7.2)

### Q: For Weaviate, what is the cross-tenant pattern?
**A:** Multi-tenancy mode (`multi_tenancy_config: { enabled: true }`); each tenant is a separate "tenant" object scoped per class. Tenant must be explicit on every query. **Weaviate refuses queries without tenant in multi-tenant classes — the most fail-closed of the named stores.** `[vendor-public]`
**Cluster:** Cross-tenant isolation
**Tier reference:** §3.2.1 (Patterns §2.7.2)

### Q: For Qdrant, what is the cross-tenant pattern, and what is the modal misconfiguration?
**A:** Payload filter on `tenant_id`. **Filter is application-layer; Qdrant does not enforce.** Modal misconfiguration: filter applied at search time but not at insertion time, so cross-tenant filter-leakage can occur from embedding similarity. `[vendor-public]`
**Cluster:** Cross-tenant isolation
**Tier reference:** §3.2.1 (Patterns §2.7.2)

### Q: For Elasticsearch, what is the cross-tenant pattern and its tradeoff?
**A:** Tenant index pattern (`chunks-tenant-{tenant_id}`). Cleanest fail-closed shape. **Drawback:** ES cluster sharding cost scales with tenant count; at 10K+ tenants, split per-cluster.
**Cluster:** Cross-tenant isolation
**Tier reference:** §3.2.1

### Q: Why is per-tenant cache namespacing the highest-risk surface (despite being conceptually simple)?
**A:** Because **caching is the modal performance optimization a developer ships in week two**, and the failure mode is invisible: cache hit rate goes up (looks like a win) while cross-tenant aggregation has silently begun. Cache key must include `tenant_id`.
**Cluster:** Cross-tenant isolation
**Tier reference:** §3.2.2

---

## Cluster 10 — Persona × Recipe × Segment-Variant

### Q: Name the 10 ICP personas the Patterns persona heatmap tracks.
**A:** Per §2.6.1: CTO-ISV, CISO-FSI, CIO-Healthcare, VP-CX, VP-Engineering, Head-of-Data, GC/Legal, CFO/Procurement, Compliance Officer, Architect. (The Field Guide tracks buyer × operator × end-user variants per recipe.)
**Cluster:** ICP segments
**Tier reference:** §2.6.1

### Q: For Recipe 1 (Support), who is the modal buyer and who is the modal operator?
**A:** Modal buyer — **VP of Customer Experience.** Modal operator — **CX Operations Manager.** End-user — the customer. Hooks: per-conversation resolution cost, deflection rate, escalation queue depth, hand-off quality.
**Cluster:** ICP segments
**Tier reference:** §2.6.3 / Foundations §1.16.2

### Q: What is the persona-heatmap finding about CISO buyers in the LangGraph corpus?
**A:** **CISO is the primary buyer at exactly ONE of 18 deployments — Elastic Security.** The Elastic deployment is the outlier the Field Guide carries forward because the CISO-buyer narrative matters for the substrate-level remediation framing.
**Cluster:** ICP segments
**Tier reference:** §2.6.2

---

## Cluster 11 — Identity-bound retrieval pattern (worked-fragment heavy)

### Q: Worked fragment — what defense-in-depth pattern does this code implement?
```python
async def retrieve(state, config):
    user_id = config["configurable"]["user_id"]
    tenant_id = config["configurable"]["tenant_id"]
    if not await fga.check(user=f"user:{user_id}",
                            relation="can_read",
                            object=f"tenant:{tenant_id}"):
        raise PermissionError("user not authorized for tenant")
    chunks = await retriever.search(query=state["query"],
                                     namespace=tenant_id,
                                     filter={"tenant_id": tenant_id})
    for chunk in chunks:
        assert chunk.metadata["tenant_id"] == tenant_id
    return {"retrieved_chunks": chunks}
```
**A:** Three independent enforcement points: (1) FGA check (relationship-based authorization); (2) store-layer filter (namespace + payload filter); (3) post-retrieval verification (assert tenant boundary). One layer alone is insufficient — a misconfiguration in one is the modal failure mode; defense-in-depth catches it.
**Cluster:** Cross-tenant isolation
**Tier reference:** §3.2.1

### Q: Where in the request lifecycle should `user_id` and `tenant_id` be extracted from — and why not from state?
**A:** From **`RunnableConfig.configurable`**, NOT from state. State can be poisoned by prompt injection or memory corruption; the per-call config is bound by the auth gateway before the agent starts processing.
**Cluster:** Cross-tenant isolation
**Tier reference:** §3.2.1

### Q: Worked fragment — interpret this MCP-Authorization handshake schematic.
```
Client  ── POST /token  (DPoP-jwt, jkt thumb) ──►  Auth Server
        ◄── access_token (cnf claim = key thumb) ──
        ── GET /resource (Auth: DPoP <token>,
            DPoP: signed JWT this-request) ──────►  Resource Server
                                                    verifies:
                                                    • token sig
                                                    • DPoP proof sig
                                                    • thumbprint match
                                                    • method/URI/nonce
```
**A:** DPoP (RFC 9449) — binds the token to the client's key. Every request includes a fresh DPoP proof signed over method + URI + nonce. Stolen tokens cannot be replayed without also stealing the key. The MCP-Authorization-spec-aligned identity handshake for sensitive tool calls.
**Cluster:** Identity (Patterns)
**Tier reference:** §2.4.5

---

## Cluster 12 — Regulatory pressure (introduction; full per-regime in Production)

### Q: What is DORA, and what is its key date?
**A:** **EU Regulation 2022/2554 — Digital Operational Resilience Act.** Fully applicable since **17 January 2025.** Governs ICT third-party risk for EU financial entities. €5M personal director liability + 2% global turnover fines under Art. 50. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §2.11 / §3.5.1

### Q: What is the SR 11-7 teaching attached to every vendor metric in this Field Guide?
**A:** **Vendor-disclosed metrics are not Model Risk Management (MRM) validation evidence under SR 11-7.** Klarna's 700-FTE equivalent, Uber's 21K developer hours, LinkedIn's 95% accuracy, Komodo's 330M patient journeys — all are vendor marketing, not validation. `[primary-regulatory + customer-produced-evidence]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.5 / §1.11.3

### Q: What is the EU AI Act compliance deadline for high-risk AI?
**A:** **2 August 2026.** Any agent in Annex III scope (credit scoring 5(b), insurance pricing 5(c), employment 4(a), education 3(a-c), essential public services, law enforcement, migration, justice) is in high-risk scope. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.3

### Q: What is Annex III in the EU AI Act?
**A:** The list of high-risk AI categorizations. Includes: credit scoring (5(b)), insurance pricing (5(c)), employment (4(a)), education (3(a-c)), essential public services, law enforcement, migration, justice. Determines whether an agent triggers high-risk obligations. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §2.11 / §3.5.3

### Q: What is NIS2?
**A:** **EU Directive 2022/2555** — cybersecurity baseline for essential and important entities across the EU. In scope for any EU LangGraph deployment in regulated sectors. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.4

### Q: What is NYDFS Part 500?
**A:** **23 NYCRR 500** — New York State Department of Financial Services cybersecurity rule. Second Amendment expanded coverage; §500.17 mandates 72-hour notification for cybersecurity events. Applies to financial institutions licensed in New York. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.9

### Q: What is SEC 17a-4(f), and what retention does it require?
**A:** SEC record-keeping rule. **All books-and-records covered by 17a-3, including agent-mediated communications**, must be retained: first 2 years easily accessible + 4 additional years in WORM (6 total). Storage must be non-rewriteable and non-erasable. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.6

### Q: What is HIPAA §164.312(b), and how does the agent's audit infrastructure interact with it?
**A:** Audit controls — requires implementation of hardware, software, and procedural mechanisms to record and examine activity in information systems containing PHI. **The trace bus IS part of the audit infrastructure** for any PHI deployment — meaning its access controls, retention, and integrity are in regulatory scope. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.6.4 / §3.5.16

### Q: What is PCI DSS 4.0 Req. 10, and which recipe is it most-load-bearing for?
**A:** Audit-trail requirement for payment-card data. Most-load-bearing for **Recipe 1 (Support — payments customers)** — every payment-data-adjacent agent action must produce an audit-trail record. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.17

### Q: What is GDPR Art. 22, and how does HITL placement satisfy it?
**A:** The right not to be subject to a decision based solely on automated processing with legal or similarly significant effect. **HITL placement in your state graph IS a GDPR Art. 22 control** — any agent action with significant effect on the data subject requires either explicit consent OR documented and operationally enforced human-in-the-loop. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.2

### Q: Name three APAC/Gulf agent-relevant regulatory regimes.
**A:** **SAMA** (Saudi Arabia Central Bank — FSI), **DFSA** (Dubai Financial Services Authority — FSI), **MAS** (Monetary Authority of Singapore — TRM Guidelines). Also HKMA (Hong Kong) and PDPA / PIPL / DPDPA / UAE PDPL across the region. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.11-15

---

## Cluster 13 — Citation-class and evidence-tag literacy

### Q: List the 10 evidence classes used in this Field Guide.
**A:** `[primary-regulatory]`, `[independently-audited]`, `[vendor-contractual]`, `[vendor-public]`, `[named-incident]`, `[customer-produced-evidence]`, `[corroborated]`, `[reference design]`, `[architectural inference]`, `[benchmark]`.
**Cluster:** Citation-class recall
**Tier reference:** design-spec §13

### Q: What is the difference between `[corroborated]` and `[independently-audited]`?
**A:** `[corroborated]` — a vendor-public claim confirmed by an independent secondary source (analyst, news outlet, customer engineering blog). `[independently-audited]` — a third-party-attested artifact (SOC 2 Type II report, ISO 27001 cert, audit firm signed report). The latter is the strongest commonly-available class.
**Cluster:** Citation-class recall
**Tier reference:** design-spec §13

### Q: What is the citation class for the Klarna "700 FTE-equivalent" launch claim?
**A:** **`[vendor-public]`** (Klarna marketing / press release). Specifically NOT `[independently-audited]` and NOT `[customer-produced-evidence]` in the validation-evidence sense. The May 2025 reversal is the empirical confirmation that vendor-public ≠ MRM-validation.
**Cluster:** Citation-class recall
**Tier reference:** §3.9 / §1.11.3

### Q: When should a Patterns reader use `[architectural inference]`?
**A:** When a claim is consistent with the architecture but not directly evidenced in vendor or customer sources. Should be flagged honestly; should NOT be presented as fact in procurement-grade artifacts.
**Cluster:** Citation-class recall
**Tier reference:** design-spec §13

---

## Cluster 14 — Common-confusion call-outs (disambiguation)

### Q: Common confusion — `MCP server`, `MCP client`, and `langchain-mcp-adapters` — which is the substrate?
**A:** The **MCP SDKs (Python/TypeScript/Java/Go/C#)** are the substrate. The **MCP server** runs at the tool side and exposes resources/tools/prompts. The **MCP client** runs at the agent side. **`langchain-mcp-adapters` is a thin wrapper, NOT the substrate** — misnaming it is the most-common Architect-persona credibility miss.
**Cluster:** Common confusion
**Tier reference:** §2.4.7

### Q: Common confusion — Postgres checkpointer vs Redis checkpointer — when to pick which?
**A:** **Postgres** is the production default — co-locates with pgvector, supports complex queries, durable, transactional. **Redis** is the #2 for **sub-millisecond memory** when latency is the binding constraint. Both are production-grade. `MemorySaver` and `SqliteSaver` are dev-only.
**Cluster:** Common confusion
**Tier reference:** §2.11

### Q: Common confusion — ReAct vs Supervisor for a Klarna-class customer-service deployment.
**A:** Klarna was widely described as ReAct in early materials but is now classified as **routed multi-agent (closer to Supervisor than ReAct, single shared model)** per Siemiatkowski's Interrupt 2025 keynote and the engineering blog. A pure ReAct agent does not "route requests" between specialists.
**Cluster:** Common confusion
**Tier reference:** §2.2.1 / §1.10.1

### Q: Common confusion — vendor-disclosed metric vs independently-audited outcome.
**A:** Vendor-disclosed = marketing material, useful for benchmarking. Independently-audited = third-party-attested, suitable for MRM under SR 11-7 §III.4. The Klarna May 2025 reversal is the canonical illustration that vendor-disclosed at launch is not validated at one year.
**Cluster:** Common confusion
**Tier reference:** §3.9 / design-spec §13

### Q: Common confusion — `BaseStore` vs the thread checkpointer.
**A:** Thread checkpointer covers state WITHIN a single conversation (`thread_id`). `BaseStore` covers state ACROSS conversations — facts the agent learned about a user, tenant, or account across all their threads. Both persistent; different scopes.
**Cluster:** Common confusion
**Tier reference:** §1.5.4 / §2.11

---

## Cluster 15 — Customer-voice anchors (full set)

### Q: Who said "LangChain has been a great partner in helping us realize our vision for an AI-powered assistant, scaling support and delivering superior customer experiences across the globe"?
**A:** **Sebastian Siemiatkowski (Klarna CEO)** — LangChain blog 2026-03-02. The vendor-signed-off framing of Klarna's deployment. `[customer-produced-evidence]`
**Cluster:** Customer-voice anchors
**Tier reference:** §3.7.1

### Q: Who said "the agent is almost like an org chart" — and which topology does this anchor?
**A:** **Karthik Ramgopal (LinkedIn)** describing the Hiring Assistant. Anchors **Hierarchical** topology with HLTM (Hierarchical Long-Term Semantic Memory). `[customer-produced-evidence]`
**Cluster:** Customer-voice anchors
**Tier reference:** §2.2.5

### Q: Who said "control and ergonomics" — and which topology does this anchor?
**A:** **Michele Catasta (Replit)** describing Replit Agent. Frames the editor swarm as a sub-pattern under top-level coordinator — anchoring the Network/Swarm-inside-Hierarchical observation. `[customer-produced-evidence]`
**Cluster:** Customer-voice anchors
**Tier reference:** §2.2.4 / §2.2.7

### Q: Who said "supervised, specialized, and reflection agents working together in feedback loops"?
**A:** **Hasith Kalpage (Cisco)** describing the Cisco JARVIS internal agent platform. One of five customer-engineer convergence points on supervisor + sub-agent topology. `[customer-produced-evidence]`
**Cluster:** Customer-voice anchors
**Tier reference:** §2.2.4

### Q: Which customer said "the Super Agent never speaks to customers," and what is the implicit lesson?
**A:** **Vodafone Italy / Fastweb** — Supervisor + Use Cases dual-graph; human-in-the-loop for the customer-facing surface. The implicit endorsement of the Klarna May 2025 reversal lesson. 86%+ One-Call Resolution. `[customer-produced-evidence]`
**Cluster:** Customer-voice anchors
**Tier reference:** §3.7.1

### Q: What is the Snowflake Cortex Agents customer-voice profile, and what named customers anchor it?
**A:** Snowflake Cortex Agents inherit user RBAC at query time; **data never leaves Snowflake**. Named customers: **TS Imagine, Advisor360°, Ramp, Alberta Health Services**. Oct 2 2025 Cortex AI for Financial Services launch was the most explicit "data-platform-as-agent-platform" play of 2025. `[customer-produced-evidence]`
**Cluster:** Customer-voice anchors
**Tier reference:** §2.9.5

### Q: What are the named Databricks Mosaic AI / Agent Bricks customers?
**A:** **Lippert, Burberry, FordDirect, Corning, Hawaiian Electric.** Compound AI system inside the lakehouse; Unity Catalog governance; MLflow tracing. `[vendor-public]`
**Cluster:** Customer-voice anchors
**Tier reference:** §2.9.5

### Q: What is the IBM watsonx Orchestrate internal-HR efficiency metric?
**A:** **94% of 10M+ annual HR requests resolved instantly** (IBM internal deployment). `[vendor-public]`
**Cluster:** Customer-voice anchors
**Tier reference:** §2.9.5

### Q: What is the BlackRock LangGraph footprint per public materials?
**A:** **BlackRock Aladdin Copilot** — 50+ engineering teams. `[corroborated]`
**Cluster:** Customer-voice anchors
**Tier reference:** §1.3.2

### Q: Which two LangGraph deployments named NVIDIA-aligned hardware paths?
**A:** **AT&T** (call-center cost reduction, Quantiphi partnership on NVIDIA AI-Q) and **RBC "Jessica"** (fraud investigator). Plus COACH Japan and UN-adjacent deployments on the NVIDIA AI-Q (LangGraph internally) substrate. `[vendor-public]`
**Cluster:** Customer-voice anchors
**Tier reference:** §2.9.4

---

## Cluster 16 — Worked fragments (state graph + identity)

### Q: Worked fragment — what does this minimal Supervisor topology pseudo-graph encode?
```python
builder = StateGraph(MessagesState)
builder.add_node("supervisor", supervisor_route)
builder.add_node("billing_agent", billing_subgraph)
builder.add_node("account_agent", account_subgraph)
builder.add_node("escalation", escalate_to_human)
builder.add_edge(START, "supervisor")
builder.add_conditional_edges("supervisor", route_to, {
    "billing": "billing_agent",
    "account": "account_agent",
    "human":   "escalation",
})
builder.add_edge("billing_agent", "supervisor")
builder.add_edge("account_agent", "supervisor")
```
**A:** Supervisor topology — a router node decides which specialist worker handles each turn; workers return to the supervisor; loops until the supervisor routes to escalation or END. The Klarna-class shape. Each worker is typically a subgraph in production.
**Cluster:** Worked fragments
**Tier reference:** §2.2.4

### Q: Worked fragment — what does the Doctolib two-token JWT pattern look like in state-diagram form?
**A:** (1) User authenticates via Keycloak → User JWT (identity + permissions). (2) Doctolib backend validates User JWT, mints Service JWT (audience = LangGraph agent service, issuer = backend), propagates BOTH tokens to the agent. (3) LangGraph "Alfred" agent validates Service JWT (service-to-service auth) and carries User JWT through downstream tool calls. (4) Policy: LLM never directly executes sensitive actions — HITL on every PHI-disclosing branch. `[customer-produced-evidence]`
**Cluster:** Worked fragments
**Tier reference:** §2.4.11

### Q: Worked fragment — interpret the OpenFGA model for Recipe 5 Embedded SaaS Copilot:
```
type tenant
  relations
    define admin: [user]
    define member: [user] or admin

type agent
  relations
    define on_behalf_of: [user]
    define tenant: [tenant]
    define can_bulk_action: admin from tenant

type record
  relations
    define tenant: [tenant]
    define viewer: member from tenant
    define editor: admin from tenant
```
**A:** Multi-tenant SaaS. Bulk-action authorization requires (1) `agent.on_behalf_of` = some user `U`, (2) `U` is `admin` of the tenant, (3) all affected records belong to that tenant. Cross-tenant aggregation is prevented at the FGA layer, not at the application layer alone.
**Cluster:** Worked fragments
**Tier reference:** §2.4.8

---

## Cluster 17 — Auxiliary protocol vocabulary

### Q: What is `deepagents` and what is its current categorical status?
**A:** LangChain's Plan-and-Execute harness with `write_todos`, sub-agents, file-system memory. Community treats it as emerging "topology 8"; structurally a Plan-and-Execute implementation but with enough additional opinions for a possible own category. Status: in motion; not yet locked. `[vendor-public] [architectural inference]`
**Cluster:** Topologies
**Tier reference:** §1.7.3 / §2.11

### Q: What is IBM ACP, and how does it relate to A2A?
**A:** **IBM Agent Communication Protocol** — IBM-originated agent communication spec. Overlaps conceptually with A2A. Tracked for vocabulary completeness; depth lives at A2A in this Field Guide.
**Cluster:** Tools and protocols
**Tier reference:** §1.6.6

### Q: What is `agentgateway`?
**A:** A separate Linux Foundation project for agent-traffic gateway concerns. Distinct from AGP / AGNTCY though overlapping in problem space. Tracked at vocabulary depth only.
**Cluster:** Tools and protocols
**Tier reference:** §1.6.6

### Q: What is Zed ACP?
**A:** Agent-coding-protocol from Zed Industries. Tracked at vocabulary depth; not the focus of the Field Guide.
**Cluster:** Tools and protocols
**Tier reference:** §1.6.6

---

## Cluster 18 — Patterns wrap (what Patterns should leave you with)

### Q: After Patterns, you should be able to map a customer brief to which five elements?
**A:** **Recipe + topology + stack + ICP segment + dominant governance category.** Plus deployment shape (if compliance is in scope) and the named-incident anchors for the dominant failure modes.
**Cluster:** Patterns wrap
**Tier reference:** §2.16

### Q: What is the architectural ratio observation that Patterns sets up for Production §3.6?
**A:** **8 of 14 failure modes carry a substrate-level residual the agent-graph layer cannot fully close** (FM 3, 4, 5-cache/model, 6, 7, 9, 13, 14). The remaining 6 are largely closable at the agent-graph + policy layer (FM 1, 2, 8, 10, 11, 12). Production §3.6.15 develops this in full.
**Cluster:** Patterns wrap
**Tier reference:** §2.7 / §3.6.15

### Q: What does the customer-voice convergence (R6 + R5 + R4) all point toward, per §2.13 and §3.9.3?
**A:** **Narrower agent scope + more HITL + less cross-agent state-sharing beats broader scope + autonomy on operational outcome metrics** (CSAT, fallback rate, incident rate). The Klarna May 2025 reversal, Anthropic's "don't build multi-agent" thesis, and the Failure Mode 14 (Model Swap / Runtime Drift) pattern all converge.
**Cluster:** Patterns wrap
**Tier reference:** §3.9.3

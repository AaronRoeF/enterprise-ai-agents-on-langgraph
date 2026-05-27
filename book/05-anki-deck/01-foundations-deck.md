# Foundations Deck — Anki Spaced-Retrieval Cards

> Source tier: `book/01-foundations.md` ("Enterprise AI Agents on LangGraph: A Field Guide" — Chapter 1).
>
> Card count: 91. Reader floor: any new SE / SC / PM hire who has read Foundations once. Review cadence: daily for 14 days, then every 3 days for 30 days.
>
> Card-type distribution (approximate): definition recall (30), decision/disambiguation (19), named-component / customer-voice (17), failure-mode / regulatory (13), worked-fragment (6), citation-class (6).
>
> Cards ordered by glossary cluster. License: CC BY-SA 4.0.

---

## Cluster 1 — Agent and autonomy

### Q: According to Anthropic's "Building Effective Agents" (Dec 2024), what is the difference between a workflow and an agent?
**A:** A **workflow** is an LLM-using system orchestrated through predefined code paths; an **agent** is a system where the LLM dynamically directs its own process and tool usage. `[vendor-public]`
**Cluster:** Agent and autonomy
**Tier reference:** §1.1.3 (Foundations)

### Q: Name the five points on the Foundations autonomy/state spectrum, from low to high.
**A:** Pipeline → Workflow → Chatbot → RAG → Agent → Fully-Autonomous. Dimensions are autonomy (does the LLM decide what to do next?) and state (does anything persist?).
**Cluster:** Agent and autonomy
**Tier reference:** §1.1.2

### Q: This Field Guide commits to whose agent-vs-workflow definition for the rest of the book, and why?
**A:** Anthropic's. It is the only definition that draws a sharp line you can use — the cut between deterministic and LLM-directed control flow maps cleanly onto LangGraph primitives.
**Cluster:** Agent and autonomy
**Tier reference:** §1.1.6

### Q: As of mid-2026, where on the autonomy spectrum do regulated production deployments actually live?
**A:** At "Agent with HITL" or to its left. Fully-autonomous deployments do not exist in regulated production (FSI, Healthcare, critical infrastructure) — they are research demonstrations. `[architectural inference] [corroborated]`
**Cluster:** Agent and autonomy
**Tier reference:** §1.1.2

### Q: Across the seven major agent definitions, what four points do they agree on?
**A:** (1) LLM as the decision-maker, (2) tool use, (3) some form of persistent state, (4) operates in a loop (not a single inference).
**Cluster:** Agent and autonomy
**Tier reference:** §1.1.4

### Q: What is the four-component academic agent model from Xi et al. 2023 / Wang et al. 2024?
**A:** Brain (the LLM — planning/reasoning), Perception (input modalities), Action (tool calls and environment modification), Memory (short-term context + long-term storage). `[benchmark]`
**Cluster:** Agent and autonomy
**Tier reference:** §1.1.3

### Q: When a customer says "we built an agent," what is the disambiguating question to ask?
**A:** "What can it decide on its own, and what is on rails?" — i.e., does the LLM choose its own next tool, or is the flow fixed in code? The answer determines the rest of the conversation.
**Cluster:** Agent and autonomy
**Tier reference:** §1.1.6

---

## Cluster 2 — The agent stack (10 tiers)

### Q: Name the 10 tiers of the agent stack from top (Tier 1, closest to the user) to bottom (Tier 10, closest to silicon).
**A:** 1 LLM, 2 Retrieval, 3 Tools/MCP plane, 4 Identity/AuthN/AuthZ, 5 Observability, 6 State/checkpointer, 7 Secrets, 8 Policy/guardrails, 9 Deploy/runtime control plane, 10 Compute.
**Cluster:** The agent stack
**Tier reference:** §1.2.1

### Q: What is the 2026 modal production default at Tier 2 (Retrieval), and why?
**A:** **pgvector** — the Postgres extension. It is the default because it co-locates with the Postgres checkpointer at Tier 6.
**Cluster:** The agent stack
**Tier reference:** §1.2.2

### Q: Which three additional layers does the 10-tier diagram intentionally NOT show?
**A:** The network egress fabric (Zscaler/Prisma/Netskope + egress DLP), the supply-chain pipeline (SLSA/Sigstore/in-toto), and the lineage/governance fabric (Collibra/Alation/Purview/OpenLineage).
**Cluster:** The agent stack
**Tier reference:** §1.2.3

---

## Cluster 3 — State, memory, persistence

### Q: Name the three scopes in the Foundations state model.
**A:** Scope 1 — Step state (scratchpad, in-step only). Scope 2 — Conversation state (per-thread, via the checkpointer). Scope 3 — Long-term memory (cross-thread, via `BaseStore`).
**Cluster:** State, memory, persistence
**Tier reference:** §1.5.1

### Q: What is the LangGraph production-default thread checkpointer, and what two checkpointers are dev-only?
**A:** Production default: `PostgresSaver` / `AsyncPostgresSaver`. Dev-only (explicitly NOT for production): `MemorySaver` and `SqliteSaver`. `[vendor-public]`
**Cluster:** State, memory, persistence
**Tier reference:** §1.5.3

### Q: When does the LangGraph runtime write a checkpoint?
**A:** After every node transition. Each transition writes a versioned snapshot keyed by `thread_id`; resuming loads the latest checkpoint; time-travel debugging loads earlier checkpoints.
**Cluster:** State, memory, persistence
**Tier reference:** §1.5.3

### Q: What is the difference between the thread checkpointer and `BaseStore`?
**A:** The thread checkpointer persists state WITHIN a single conversation (one `thread_id`). `BaseStore` persists state ACROSS conversations — facts the agent learned about a user / tenant across all their threads.
**Cluster:** State, memory, persistence
**Tier reference:** §1.5.4

### Q: Map the four cognitive-science memory terms to LangGraph implementations.
**A:** Working memory → `messages` list in current state. Episodic memory → stored summaries of past threads in `BaseStore`. Semantic memory → vector store of facts / structured KV in `BaseStore`. Procedural memory → stored prompt templates and learned tool definitions.
**Cluster:** State, memory, persistence
**Tier reference:** §1.5.5

### Q: What MemGPT / Letta concept does the 2026 agent-memory wave inherit?
**A:** The idea that the agent itself edits its own memory — paging out to long-term, pulling in from long-term to working. From Packer et al. 2023 (arXiv:2310.08560, UC Berkeley RISELab). `[benchmark]`
**Cluster:** State, memory, persistence
**Tier reference:** §1.5.5

### Q: A customer says "the agent forgets things between sessions." What is the diagnostic question?
**A:** "Are you using `BaseStore` for cross-thread memory, or are you relying on the thread checkpointer alone?" Cross-session forgetting is a `BaseStore` problem; in-session forgetting is a checkpointer or context-truncation problem.
**Cluster:** State, memory, persistence
**Tier reference:** §1.5.6

---

## Cluster 4 — Tools and protocols (the three-layer stack)

### Q: Name the three layers of the 2026 protocol stack from top to bottom.
**A:** Top — A2A (Agent2Agent, agent-to-agent collaboration). Middle — MCP (Model Context Protocol, agent-to-tool). Bottom — AGP / AGNTCY (Agent Gateway Protocol, transport / routing / identity).
**Cluster:** Tools and protocols
**Tier reference:** §1.6.1

### Q: Who originated MCP, and where was it donated?
**A:** Anthropic introduced MCP in November 2024 and donated it to the **Linux Foundation Agentic AI Foundation (LF AAIF)** in December 2025. MCP is now vendor-neutral. `[vendor-public]`
**Cluster:** Tools and protocols
**Tier reference:** §1.6.2

### Q: Name the three MCP primitive types.
**A:** **Tools** (callable functions with structured JSON I/O), **Resources** (readable data sources — files, DB rows, URLs), and **Prompts** (pre-templated prompts that users or LLMs can invoke).
**Cluster:** Tools and protocols
**Tier reference:** §1.6.2

### Q: What is the difference between an MCP server, an MCP client, and an MCP host?
**A:** Server exposes tools/resources/prompts. Client (embedded in the agent runtime) invokes the server's primitives. Host is the user-facing app (Claude Desktop, Cursor) that mediates between the user and the clients.
**Cluster:** Tools and protocols
**Tier reference:** §1.6.2

### Q: Is `langchain-mcp-adapters` the MCP substrate? Why does this matter?
**A:** No. It is a thin LangChain wrapper that translates between LangChain `ToolMessage` and MCP `ToolMessage`. The substrate is the MCP SDKs (Python/TypeScript/Java/Go/C#). Misnaming the wrapper as the substrate is a credibility-destroying SE failure mode.
**Cluster:** Tools and protocols
**Tier reference:** §1.6.2

### Q: Who originated A2A, and how does it relate to MCP conceptually?
**A:** Google launched A2A in April 2025 and donated it to the Linux Foundation in June 2025. Conceptually: MCP is gRPC for agent-to-tool; A2A is HTTP-between-services for agent-to-agent. 150+ orgs supporting as of May 2026. `[vendor-public]`
**Cluster:** Tools and protocols
**Tier reference:** §1.6.3

### Q: What is AGNTCY and what is AGP?
**A:** AGNTCY is a multi-component Cisco-Outshift project (discovery, identity, messaging-via-SLIM, observability), donated to the Linux Foundation in July 2025. **AGP (Agent Gateway Protocol)** is the BGP-inspired routing piece — the bottom layer of the three-layer stack. `[vendor-public]`
**Cluster:** Tools and protocols
**Tier reference:** §1.6.4

### Q: Name three named managed MCP planes in 2026 production.
**A:** AWS Bedrock AgentCore Gateway, Azure Foundry MCP Gateway, GCP Vertex Agent Gateway. (Also: Cloudflare AI Gateway, Kong AI Gateway, Apigee + MCP, MuleSoft.)
**Cluster:** Tools and protocols
**Tier reference:** §1.6.5

---

## Cluster 5 — Patterns and topologies

### Q: Name the seven canonical LangGraph topologies.
**A:** (1) ReAct, (2) ReAct + Reflexion, (3) Plan-and-Execute, (4) Supervisor, (5) Hierarchical, (6) Agentic RAG, (7) Network (Swarm).
**Cluster:** Patterns and topologies
**Tier reference:** §1.7.1

### Q: Which topology was renamed in the LangGraph docs to match `langgraph-swarm-py`?
**A:** "Multi-Agent Collaboration" → **Network (Swarm)**. If you see the old name in older docs, it is the same pattern.
**Cluster:** Patterns and topologies
**Tier reference:** §1.7.1

### Q: What is the emerging "topology 8" in the LangGraph community as of May 2026?
**A:** `deepagents` — LangChain's Plan-and-Execute harness with sub-agent spawning, virtual filesystem scratchpads, TODO-list state, and planning loops. Structurally Plan-and-Execute, but with enough additional opinions that community voices argue for its own category. Not yet locked. `[architectural inference] [vendor-public]`
**Cluster:** Patterns and topologies
**Tier reference:** §1.7.3

### Q: When would you pick Supervisor over Hierarchical?
**A:** Supervisor fits when work decomposes into clean specialist domains with a manageable number of workers (≤10). Hierarchical (supervisor-of-supervisors) fits when the problem space has too many specialists for a flat supervisor and routing quality would degrade.
**Cluster:** Patterns and topologies
**Tier reference:** §1.7.5

### Q: What is the modal real-world composition pattern in the customer corpus?
**A:** **Supervisor wrapping ReAct wrapping Agentic RAG** — a supervisor routes among specialist workers, each worker is a ReAct agent, and one tool each worker can call is a self-correcting retrieval step. Topologies compose; they are not exclusive.
**Cluster:** Patterns and topologies
**Tier reference:** §1.7.4

### Q: Which paper established the ReAct (Thought → Action → Observation) loop?
**A:** Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models" (ICLR 2023, arXiv:2210.03629). Every LangGraph topology except Plan-and-Execute inherits ReAct's interleaving. `[benchmark]`
**Cluster:** Patterns and topologies
**Tier reference:** §1.7.2

### Q: What is the Anthropic engineering team's public guidance on multi-agent systems?
**A:** "Don't build multi-agent systems unless the work demands it." Most customers want one agent with the right tools, not three agents arguing. This guidance is the version SEs should bring to discovery calls.
**Cluster:** Patterns and topologies
**Tier reference:** §1.7.4

---

## Cluster 6 — LangGraph primitives

### Q: What is a `StateGraph`?
**A:** LangGraph's central primitive — a directed graph where nodes are Python functions, edges are transitions, and a shared state object is read/written by every node. The runtime picks the next node based on edge logic, calls it with current state, applies the returned state update, and continues.
**Cluster:** LangGraph primitives
**Tier reference:** §1.4.1

### Q: What is `MessagesState`, and what is the `add_messages` reducer?
**A:** `MessagesState` is the default chat-agent state schema with a single `messages` field. The `add_messages` reducer defines how new messages are appended to or merged with the existing list.
**Cluster:** LangGraph primitives
**Tier reference:** §1.4.2

### Q: What is the LangGraph Functional API, and when did it ship?
**A:** `@entrypoint` and `@task` decorators for **imperative authoring** (vs the declarative Graph API). Shipped GA in LangGraph v0.3 in September 2025. ~40%+ of new LangGraph deployments use it per LangChain DevRel community tracking. `[vendor-public]`
**Cluster:** LangGraph primitives
**Tier reference:** §1.4.3

### Q: What is the difference between `interrupt(value)`, `Command(goto=...)`, and `Command(resume=...)`?
**A:** `interrupt(value)` — called inside a node, pauses execution, surfaces `value` to the calling code. `Command(goto=..., update=...)` — returned from a node, routes to a next node and applies a state update (in-node routing). `Command(resume=...)` — passed to `graph.invoke()` to resume a paused thread. The first pauses, the third un-pauses, the second is unrelated.
**Cluster:** LangGraph primitives
**Tier reference:** §1.4.12

### Q: What does `compile(checkpointer=...)` do?
**A:** Turns a `StateGraph` builder into a runnable graph and wires in persistence. Pass a `PostgresSaver` (or `AsyncPostgresSaver`) and the runtime will persist state to Postgres at every node transition.
**Cluster:** LangGraph primitives
**Tier reference:** §1.4.6

### Q: What is the `Send` API?
**A:** LangGraph's primitive for fan-out. A node returns a list of `Send` objects, and the runtime invokes the named downstream node many times in parallel with different inputs, then aggregates the results. Used heavily in deep-research and multi-document analysis.
**Cluster:** LangGraph primitives
**Tier reference:** §1.4.7

### Q: What is `create_react_agent`?
**A:** The prebuilt helper that builds a minimal ReAct agent as a two-node `StateGraph` (an "agent" node and a "tools" node) with a conditional edge that loops until the LLM stops calling tools. The single most-used LangGraph on-ramp. `[vendor-public]`
**Cluster:** LangGraph primitives
**Tier reference:** §1.4.11

### Q: Worked fragment — what does this code build?
```python
from langgraph.prebuilt import create_react_agent
agent = create_react_agent(
    model=anthropic_claude,
    tools=[lookup_account, place_refund, escalate_to_human],
    checkpointer=postgres_checkpointer,
)
```
**A:** A minimal ReAct customer-support agent — LLM in a loop calling lookup-account / place-refund / escalate-to-human tools, with conversation state persisted to Postgres at every node transition. The "hello, agent" shape.
**Cluster:** LangGraph primitives
**Tier reference:** §1.4.16

### Q: What is a LangGraph thread?
**A:** A single conversation with the agent, identified by a `thread_id` (a string the caller chooses). Same `thread_id` → resume; new `thread_id` → start fresh. The `thread_id` lives in `RunnableConfig.configurable`.
**Cluster:** LangGraph primitives
**Tier reference:** §1.4.5

### Q: What are the three `langgraph` CLI commands, and what is the production-vs-dev caveat?
**A:** `langgraph dev` (local with auto-reload, Studio-compatible — dev only), `langgraph up` (deploys to LangGraph Platform), `langgraph build` (builds a deployable artifact). **Caveat:** `langgraph dev` silently ignores user-supplied checkpointers in some configurations and uses its own in-memory store — it is NOT a faithful production simulator.
**Cluster:** LangGraph primitives
**Tier reference:** §1.4.10

### Q: What is a subgraph, and what is it used for?
**A:** A `StateGraph` used as a node inside another `StateGraph`. The subgraph has its own state schema, nodes, and edges. Subgraphs are the encapsulation primitive — multi-agent systems often build each specialist as a subgraph and compose them under a supervisor.
**Cluster:** LangGraph primitives
**Tier reference:** §1.4.14

### Q: Name the four LangGraph streaming modes.
**A:** `values` (full state value at each transition — richest), `updates` (only the deltas — most efficient), `messages` (only message-list updates — most user-UI friendly), `debug` (internal runtime events — most verbose).
**Cluster:** LangGraph primitives
**Tier reference:** §1.4.13

---

## Cluster 7 — Frameworks at conceptual level

### Q: Why is this Field Guide titled "Enterprise AI Agents on LangGraph" rather than "Enterprise AI Agents"?
**A:** Because most of the public, named enterprise deployments at scale in 2026 run on LangGraph. Community signal (GitHub stars, downloads) does NOT map cleanly to enterprise adoption — CrewAI has more stars than LangGraph.
**Cluster:** Frameworks
**Tier reference:** §1.3

### Q: Name three honest LangGraph gaps that should be flagged in Foundations.
**A:** (1) TypeScript runtime and Platform feature parity lag Python by ~6–9 months; (2) BYOC deployment is AWS-only as of 2026-05 (Azure / GCP BYOC are roadmap, not shipping); (3) steep learning curve relative to higher-level frameworks like CrewAI for trivial use cases. `[vendor-public] [architectural inference]`
**Cluster:** Frameworks
**Tier reference:** §1.3.2

### Q: What is the procurement-ambiguity trap with AutoGen?
**A:** Two projects share the lineage. **AutoGen** (Microsoft Research origin) was folded into Microsoft Agent Framework (MAF Python preview, Q1 2026). **AG2** is the community fork led by the original authors after their Microsoft departure (`ag2ai/ag2` on GitHub). When a customer says "we use AutoGen," ask which.
**Cluster:** Frameworks
**Tier reference:** §1.3.4

### Q: What is the procurement-ambiguity trap with CrewAI?
**A:** **CrewAI Enterprise** is commercially distinct from open-source CrewAI — adds hosted Crews, managed observability, different compliance posture. When a customer says "we use CrewAI," ask which.
**Cluster:** Frameworks
**Tier reference:** §1.3.3

---

## Cluster 8 — Observability

### Q: Name three reasons agent observability is its own discipline (not standard APM).
**A:** (1) Non-determinism — same input produces different outputs across runs; (2) Multi-step reasoning — one request triggers a tree of LLM/tool/routing spans, not a line; (3) Tool-call branching — trace shape emerges from execution, cannot be pre-defined.
**Cluster:** Observability
**Tier reference:** §1.8.1

### Q: What is the dominant trace + eval platform inside LangGraph deployments, and why?
**A:** **LangSmith** — LangChain's first-party. Near-monopoly because it auto-instruments `StateGraph` nodes with zero code change. SaaS regions: GCP us-central1 / europe-west4 / australia-southeast1, AWS us-east-2. Self-hosted available. `[vendor-public]`
**Cluster:** Observability
**Tier reference:** §1.8.3

### Q: What is the difference between Arize AX and Phoenix?
**A:** Both come from Arize but are **distinct products**: Arize AX is commercial; Phoenix is OSS. Strong on eval and structured drift detection. Don't conflate them.
**Cluster:** Observability
**Tier reference:** §1.8.3

### Q: What is the difference between OpenTelemetry GenAI semantic conventions and OpenInference?
**A:** OpenTelemetry GenAI semantic conventions is the open standard for LLM/agent trace fields. **OpenInference** is the Arize-submitted OpenTelemetry convention extension. Both let any trace producer send to any consumer (Splunk, Sentinel, Datadog) in a common schema.
**Cluster:** Observability
**Tier reference:** §1.8.3

### Q: Define trace, span, and run.
**A:** **Trace** — full record of a single agent run from user input to final output (minutes to hours). **Span** — a single sub-operation within a trace (LLM call, tool call, graph node); spans nest into parent-child trees. **Run** — LangSmith-vocabulary equivalent of trace.
**Cluster:** Observability
**Tier reference:** §1.8.2

---

## Cluster 9 — Identity and authorization

### Q: Name the three agent identity problems.
**A:** Problem 1 — Who is the user? (OAuth/OIDC/SAML — solved since 2000s). Problem 2 — Who is the workload/agent itself? (SPIFFE/SPIRE/workload identity — mostly solved since cloud-native). Problem 3 — On whose behalf is the agent acting? (delegation — the NEW problem of 2025–2026).
**Cluster:** Identity and authorization
**Tier reference:** §1.9.1

### Q: A customer says "we'll figure out identity later." What is the right pushback?
**A:** "Which of the three identity problems are you deferring?" Most customers conflate Problem 2 (workload) and Problem 3 (delegation); naming the three problems disentangles the conversation.
**Cluster:** Identity and authorization
**Tier reference:** §1.9.1

### Q: Name three first-party agent-identity products that shipped in 2025.
**A:** Microsoft Entra Agent ID (GA 2025), Okta for AI Agents (EA 2025), Auth0 for AI Agents (EA 2025). Ping Identity (PingOne / Ping AIC) is the fourth name worth mentioning.
**Cluster:** Identity and authorization
**Tier reference:** §1.9.4

### Q: What is the modal identity pattern in 2026 LangGraph production deployments?
**A:** **Custom JWT** — across 18 named LangGraph deployments, custom JWT is the default identity substrate. First-party agent-identity products are arriving as the freshest greenfield. `[customer-produced-evidence] [architectural inference]`
**Cluster:** Identity and authorization
**Tier reference:** §1.9.4

### Q: Define DPoP and explain why it matters for agents.
**A:** **DPoP (Demonstrating Proof-of-Possession, RFC 9449, Sept 2023)** binds an OAuth access token to a key pair held by the client. Every request is signed; stolen tokens cannot be replayed. Matters for agents because their tokens are exposed in env vars, container memory, and trace logs.
**Cluster:** Identity and authorization
**Tier reference:** §1.9.3

### Q: Define PAR, RAR, and CIBA at one-line depth.
**A:** **PAR** (Pushed Authorization Requests) — push the auth request to the server before redirect, preventing leaked-URL replay. **RAR** (Rich Authorization Requests) — structured payload (transaction details, amounts, recipients) instead of coarse OAuth scopes. **CIBA** (Client-Initiated Backchannel Authentication) — agent backend initiates auth; user approves on a separate trusted device.
**Cluster:** Identity and authorization
**Tier reference:** §1.9.3

### Q: What is the MCP Authorization spec, and what is its evidence class as of May 2026?
**A:** OAuth 2.1 + Dynamic Client Registration + RFC 9728 metadata. Ratified Q1 2026. **Production-deployment evidence is still thin** — any procurement claim about MCP Authorization at scale should be marked `[evidence-zero]` until customer evidence surfaces. `[vendor-public]`
**Cluster:** Identity and authorization
**Tier reference:** §1.9.5

### Q: What is FGA, and what category of access control does it implement?
**A:** **Fine-Grained Authorization** — relationship-based access control (ReBAC). The question "can this agent, acting for this user, read this document section in this tenant?" reduces to a graph query over a relationship model. Authorization is derived from declarative relationships, not hardcoded checks.
**Cluster:** Identity and authorization
**Tier reference:** §1.9.6

### Q: Name two FGA products and one open-source ReBAC reference.
**A:** **OpenFGA** (CNCF sandbox, Auth0-originated, the canonical ReBAC reference). Also: Cedar / AWS Verified Permissions, Topaz (Aserto), Okta FGA, Auth0 FGA, Permit.io, Oso, Styra.
**Cluster:** Identity and authorization
**Tier reference:** §1.9.6

### Q: Name the six components of the signed action provenance chain.
**A:** (1) User authentication assertion, (2) Agent identity assertion (KMS-backed), (3) Planner decision (LLM output hashed), (4) Tool-call invocation (parameters hashed), (5) Tool-call result (hashed), (6) Outcome (signed completion record). Together — a signed action chain that can be replayed and audited.
**Cluster:** Identity and authorization
**Tier reference:** §1.9.7

---

## Cluster 10 — Recipes and ICP segments

### Q: Name the six common use case recipe families.
**A:** (1) Customer Support Copilot, (2) Code-Modifying Developer Agents, (3) Text-to-SQL / Conversational Analytics, (4) Multi-Agent Deep Research, (5) Embedded SaaS Copilot, (6) Security Agents.
**Cluster:** Recipes and ICP segments
**Tier reference:** §1.10

### Q: What is the anchor customer for Recipe 1 (Customer Support Copilot), and what is the topology classification?
**A:** **Klarna AI Assistant** — 2.5M conversations. Topology: **routed multi-agent (closer to Supervisor than ReAct, single shared model)** per Sebastian Siemiatkowski's LangChain Interrupt 2025 keynote and the Klarna engineering blog (April 2025). `[customer-produced-evidence] [corroborated]`
**Cluster:** Recipes and ICP segments
**Tier reference:** §1.10.1

### Q: Name the anchor customers for Recipe 2 (Code-Modifying Developer Agents).
**A:** **Uber Validator + AutoCover** (~21K developer hours reclaimed per Uber's Interrupt 2025 talk) and **Replit Agent** (code-generation copilot with HITL approval gates). `[customer-produced-evidence]`
**Cluster:** Recipes and ICP segments
**Tier reference:** §1.10.2

### Q: Why is Text-to-SQL (Recipe 3) considered structurally hard?
**A:** Because every Text-to-SQL agent must reason about multi-tenant isolation. The dominant failure mode is the agent generating a query that crosses a tenant boundary because the prompt did not surface the boundary explicitly.
**Cluster:** Recipes and ICP segments
**Tier reference:** §1.10.3

### Q: Name two anchor customers for Recipe 4 (Multi-Agent Deep Research).
**A:** **Captide** (FSI research agent, Plan-and-Execute topology) and **Morningstar Mo** (wealth research, Plan-and-Execute with RAG retrieval at each step). Also Exa. `[customer-produced-evidence]`
**Cluster:** Recipes and ICP segments
**Tier reference:** §1.10.4

### Q: Name the anchor customer for Recipe 6 (Security Agents).
**A:** **Elastic Security AI Assistant** — Agentic RAG over Elastic indexes; SOC alert triage. The 1-of-18-deployment outlier in the corpus where CISO is the primary buyer. `[customer-produced-evidence]`
**Cluster:** Recipes and ICP segments
**Tier reference:** §1.10.6

### Q: At Foundations depth, where does HITL fire for the Customer Support recipe?
**A:** Refund above a threshold, policy escalation, cross-team handoff. The pattern: HITL fires at the action whose reversal is expensive or impossible.
**Cluster:** Recipes and ICP segments
**Tier reference:** §1.10.6.2

### Q: What is the Sovereign segment's evidence class for LangGraph deployments?
**A:** `[evidence-zero, structural-fit-only]`. The recipes fit conceptually; no public deployment evidence exists in sovereign / public-sector contexts as of mid-2026.
**Cluster:** Recipes and ICP segments
**Tier reference:** §1.12.4

### Q: What is the R3 insurance-segment finding for LangGraph?
**A:** **68% of insurers running gen-AI / agents but zero LangGraph footprint** as of mid-2026. The insurance segment runs hyperscaler-native stacks, Azure OpenAI direct, and homegrown solutions. `[architectural inference] [evidence-zero for LangGraph specifically]`
**Cluster:** Recipes and ICP segments
**Tier reference:** §1.12.1

---

## Cluster 11 — Governance categories (failure modes — intro depth)

### Q: Name the five categorical leak surfaces taught at Foundations depth.
**A:** (1) Prompt injection (direct + indirect), (2) Telemetry capture, (3) Cross-tenant aggregation, (4) Action-provenance gaps, (5) Supply-chain compromise.
**Cluster:** Governance categories
**Tier reference:** §1.11.2

### Q: What is the difference between direct and indirect prompt injection?
**A:** **Direct** — the attacker controls user input and embeds malicious instructions. **Indirect** — the attacker controls data the agent retrieves or reads (an email, document, search result, tool output) and the agent treats the embedded content as instructions. Indirect injection is the dominant 2025 risk class.
**Cluster:** Governance categories
**Tier reference:** §1.11.2

### Q: Why do agents create two new leak surfaces that did not exist in traditional SaaS?
**A:** Agents add (a) the tool / MCP invocation surface — every callable tool is a potential exfiltration path — and (b) the agent state / memory surface — long-term memory, checkpointers, and caches retain data needing per-tenant isolation and PII redaction. Every named public agent incident from 2024–2025 landed on these two surfaces.
**Cluster:** Governance categories
**Tier reference:** §1.11.1

### Q: Define cross-tenant aggregation in one sentence.
**A:** Agent state, cache, retrieval, or memory leaks between tenants — typically because the per-tenant predicate at the vector store, cache key, `thread_id` namespace, or trace partition was missing or misconfigured.
**Cluster:** Governance categories
**Tier reference:** §1.11.2

### Q: This Field Guide uses what public-facing vocabulary for the leakage problem class?
**A:** **"Data-leak surface" / "leakage pathway."** Per the v3 design-spec discipline (CISO #2 / #5; LangGraph-DevRel R2 #3).
**Cluster:** Governance categories
**Tier reference:** §1.11 / Patterns §2.7.1

---

## Cluster 12 — Named incidents and customer voice

### Q: Which named incident is the public-vocabulary-establishing event for indirect prompt injection in production?
**A:** **Slack AI (August 2024)** — PromptArmor disclosed a vulnerability where an attacker could post a prompt-injection payload in a public channel; when a user in a private channel queried Slack AI, the AI would follow the injected instructions and exfiltrate private-channel content via a Markdown link to an attacker-controlled URL. `[named-incident]`
**Cluster:** Named incidents
**Tier reference:** §1.11.4

### Q: What is EchoLeak, and what makes it operationally significant?
**A:** **EchoLeak / CVE-2025-32711 (June 2025, Aim Labs)** — zero-click prompt injection in Microsoft 365 Copilot. Attacker sent a crafted email; when the victim later queried Copilot, RAG pulled the email and the injection triggered data exfiltration without the user clicking anything. CVSS 9.3. Coined the term **"LLM Scope Violation."** `[named-incident]`
**Cluster:** Named incidents
**Tier reference:** §1.11.4

### Q: What did the Samsung ChatGPT incidents establish, and when did they happen?
**A:** April 2023 — Samsung semiconductor engineers pasted proprietary source code and meeting transcripts into ChatGPT across three separate incidents in 20 days. Samsung banned generative AI tools company-wide within a month. The vocabulary-establishing event for enterprise data leakage to LLM SaaS — drove the entire BYOC and self-hosting demand wave. `[named-incident]`
**Cluster:** Named incidents
**Tier reference:** §1.11.4

### Q: What is the Klarna CEO reversal and what does it teach?
**A:** May 2025 — Sebastian Siemiatkowski publicly walked back the framing that AI was replacing ~700 FTE-equivalents of customer-service work, conceding that steady-state performance did not match launch performance. Teachable point: **vendor-disclosed metrics are not Model Risk Management evidence under SR 11-7.** `[customer-produced-evidence] [named-incident]`
**Cluster:** Named incidents
**Tier reference:** §1.11.3

### Q: Which named incident is the legal anchor for "a deploying organization is responsible for what its agent says"?
**A:** **Moffatt v. Air Canada** (Feb 2024) — airline held liable for its chatbot's hallucinated refund policy. The legal precedent for chatbot accountability. `[named-incident]`
**Cluster:** Named incidents
**Tier reference:** §1.11.4

### Q: Which named incident is the autonomy-grant-error anchor?
**A:** **Replit production-DB deletion (May 2025)** — agent given broad write access without HITL deleted production data. Maps to identity gaps + hallucination-to-action + HITL bypass. `[named-incident]`
**Cluster:** Named incidents
**Tier reference:** §1.11.4

### Q: Which named incident is the canonical anchor for cross-tenant aggregation via RAG?
**A:** **ConfusedPilot (UT Austin, 2024)** — semantic search retrieval crossing intended access boundaries in Microsoft 365 Copilot-class deployments. USENIX Security 2024. `[named-incident] [benchmark]`
**Cluster:** Named incidents
**Tier reference:** §1.11.4

### Q: Who said "we built a controllable agent architecture that routed requests" — and where is this cited?
**A:** Klarna engineering / LangChain editorial framing Klarna signed off on (cited in the Klarna engineering blog April 2025 and LangChain blog 2026-03-02). The critical phrase for topology classification: Klarna is routed multi-agent (closer to Supervisor than pure ReAct). `[customer-produced-evidence]`
**Cluster:** Named incidents
**Tier reference:** §1.10.1

---

## Cluster 13 — PM-track vocabulary and citation classes

### Q: What is JTBD?
**A:** Jobs to Be Done — Christensen-lineage framework for stating user needs as jobs: "When [situation], I want to [motivation], so I can [outcome]." Each Foundations recipe opens with a JTBD sentence for end-user and buyer.
**Cluster:** PM-track vocabulary
**Tier reference:** §1.15

### Q: What is the difference between a buyer persona and an end-user persona?
**A:** The **buyer** is the economic decision-maker who approves the purchase. The **end-user** is the person who actually uses the product day-to-day. They are often different — confusing them is a credibility miss in PM-track work.
**Cluster:** PM-track vocabulary
**Tier reference:** §1.15

### Q: What does the citation class `[vendor-public]` mean?
**A:** A claim sourced from a vendor's public materials (docs, blog, marketing). Useful for benchmarking and discussion. NOT validation evidence for an MRM review.
**Cluster:** Citation-class recall
**Tier reference:** §1.18 / design-spec §13

### Q: What is the difference between `[vendor-public]` and `[vendor-contractual]`?
**A:** `[vendor-public]` is documentation, blog posts, and marketing the vendor has published openly. `[vendor-contractual]` is commitments inside a customer's signed contract (MSA, DPA, BAA, SLA) — stronger evidence-weight than public statements but specific to the contracting customer.
**Cluster:** Citation-class recall
**Tier reference:** design-spec §13

### Q: What does `[customer-produced-evidence]` mean, and what is it used for?
**A:** A claim sourced from material the customer itself produced (engineering blog, conference talk, signed-off LangChain editorial). Strongest commonly-available evidence class for named deployments. Not equivalent to `[independently-audited]`.
**Cluster:** Citation-class recall
**Tier reference:** design-spec §13

### Q: What does `[evidence-zero, structural-fit-only]` mean?
**A:** A claim where no production evidence exists, but the architecture is theoretically realizable. Used in this Field Guide for sovereign / public-sector LangGraph deployments and for any healthcare PHI-in-production claim. Must NOT be represented as "validated."
**Cluster:** Citation-class recall
**Tier reference:** §1.12.4 / design-spec §13

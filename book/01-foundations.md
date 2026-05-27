<!--
title: Enterprise AI Agents on LangGraph — A Field Guide
chapter: 01 — Foundations
version: 1.0 (draft)
license: CC BY-SA 4.0
author: Aaron Fulkerson
date: 2026-05-24
-->

# Enterprise AI Agents on LangGraph: A Field Guide
## Chapter 1 — Foundations

*A Field Guide for Sales Engineers, Solution Consultants, and Product Managers building, selling, and shipping enterprise AI agents.*

**Author:** Aaron Fulkerson
**License:** CC BY-SA 4.0
**Version:** 1.0 (draft, May 2026)
**Reading time:** 6–8 hours core read, two-week absorbable
**Status:** Foundations is the must-read core. Patterns and Production are ongoing reference.

> **Companion files.** Procurement-evaluation, author affiliation, and funding disclosures live in `CONFLICTS.md` at the repo root. The canonical terminology reference lives in `04-glossary.md`. Spaced-retrieval cards for this chapter live in `05-anki-deck/01-foundations.apkg` — **Anki** is an open-source spaced-repetition flashcard app ([apps.ankiweb.net](https://apps.ankiweb.net/)); the `.apkg` files in this repo import directly into Anki to drill the chapter's vocabulary on a schedule that adapts to your recall.

> **This is not a procurement-evaluation document.** It is an educational reference. Procurement decisions require independent vendor evaluation (Gartner, Forrester, NIST, ENISA, customer-side technical evaluation). This guide is one input among many; it is not a substitute for vendor due diligence.

---

## How to read this chapter

This chapter has two reading paths in a single file. Both paths share the same conceptual narrative, the same diagrams, and the same exit gate. They differ only in how much code they ask you to absorb.

**Engineer-track (SE / SC / EA on-ramp).** Read everything, including the Python code blocks. They show you the LangGraph primitives you will reach for once you start prototyping. If you do not write Python today but you expect to next month, do not skip them — read them as a vocabulary list. You are not being asked to memorize syntax. You are being asked to recognize the primitives when a customer's engineering team uses them in a discovery call.

**PM-track (Product, GTM, Sales, partner managers).** Read the conceptual narrative in full and read the **concept boxes** at every primitive. **You may visually skim or skip the Python code blocks throughout this book** — they are visually identifiable by their indented fixed-width fenced format and you will not lose the conceptual thread by skipping them. The concept box immediately above or below each code block carries the meaning. Both tracks re-merge for the closing summary, the glossary, and the knowledge gate.

**Both tracks** are expected to absorb the same vocabulary. By the end of Foundations, the PM-track reader should be able to recognize, name, and sketch the architecture of a customer's agent on a whiteboard at a discovery call — even if they cannot write the code.

A convention used throughout the book: when an ASCII diagram shows architectural state, the following annotations carry meaning consistently across all three chapters.

```
  [CKP]  -- checkpoint write (the runtime persists state here)
  [HITL] -- human-in-the-loop pause (agent yields to a human)
  [OBS]  -- observability span emission (a trace event surfaces)
  [POL]  -- policy / guardrail check (content or action policy)
```

Arrow styles in state graphs carry meaning too. Three styles, declared once, used everywhere:

```
  -->   solid       -- LLM-decided edge (the agent picked next step)
  ==>   double      -- system-automatic edge (runtime advances)
  ..>   dashed      -- human-mediated edge (HITL gate fires)
```

**When each is used.** Solid arrows mean the LLM emitted a tool call or a routing choice — the next step was *decided by the model*. Double arrows mean the runtime advanced without a model decision — a tool returned and control flowed back, or a conditional edge fired on a deterministic predicate. Dashed arrows mean a human-in-the-loop gate fired — execution paused, durable state was persisted, and the conversation may have slept for minutes or hours before a human resumed it.

You will see these annotations and arrow styles on every state graph from here onward.

---

## Prerequisites

You are assumed to know:

- What a **Large Language Model (LLM)** is, that it is called via an Application Programming Interface (API), and that the response is a stream of tokens.
- What an **API** is and roughly how **Software-as-a-Service (SaaS)** apps consume them.
- What **JSON** is.
- What **OAuth (Open Authorization) / SSO** is at a conceptual level (enough to know that "logging in with Google" uses one of these).
- What **Postgres** and **Redis** are, in name. You do not need to have administered either.

You are NOT assumed to know:

- How to write Python.
- Anything about LangGraph specifically.
- Anything about the Model Context Protocol (MCP), Agent2Agent (A2A), or AGNTCY / AGP.
- The names of the seven canonical agent topologies.
- Any of the failure modes a regulator will ask about.
- Anything about fine-grained authorization (FGA), **Demonstrating Proof-of-Possession** (DPoP, [RFC 9449](https://datatracker.ietf.org/doc/html/rfc9449)), **Rich Authorization Requests** (RAR, [RFC 9396](https://datatracker.ietf.org/doc/html/rfc9396)), **Client-Initiated Backchannel Authentication** (CIBA), or step-up authentication.

If you are missing one of the assumed prerequisites, two short pre-work tutorials cover the gap:

- **PM-track pre-work:** the LangChain "Hello, Agent" tutorial (~45 minutes; conceptual; no Python required to read along).
- **Engineer-track pre-work:** the LangGraph Studio quickstart (~30 minutes; Python). LangGraph Studio is the visual debugger; you will see it referenced throughout. `[vendor-public]`

If neither of those is available to you when you start, do not stop reading. You will pick up the vocabulary as you go.

---

## What you'll be able to do by the end of this chapter

Outcomes are explicit by role.

**Sales Engineer / Solution Consultant.** You will be able to:

- Disambiguate "agent" from "chatbot," "RAG," "workflow," and "pipeline" in a customer conversation.
- Name the ten tiers of an enterprise agent stack and what lives at each tier.
- Sketch the three-layer protocol stack (A2A above MCP above AGP) on a whiteboard.
- Name the seven canonical LangGraph topologies and pick one that fits a 1-paragraph customer brief.
- Name three of the ten public agent incidents from 2023–2025 and explain in two sentences each what went wrong.
- Identify the obvious governance risk in a 1-paragraph customer scenario.
- Recognize the three identity problems an agent introduces, and name at least one named-product solution for each.

**Product Manager.** You will be able to:

- Write a 1-paragraph **Jobs-to-Be-Done** (JTBD) statement for a customer's agent feature.
- Distinguish the **buyer persona** from the **end-user persona** of an agent feature, and name both.
- Identify which of the six common agent recipe families a customer's request fits.
- Name the dominant governance category the deployment will need to navigate (**Financial Services Industry (FSI)** / Healthcare / **Independent Software Vendor (ISV)** / Sovereign).
- Recognize the difference between vendor-disclosed metrics and audit-grade evidence, and avoid mixing them in PRDs.

**Engineer-curious (any track).** You will be able to:

- Wire up a minimal LangGraph ReAct agent with a Postgres checkpointer.
- Add a human-in-the-loop interrupt at one point in the graph.
- Identify the three places this minimal design would fail in production.
The exit gate at the end of the chapter (§1.16) tests all three role tracks against the same customer scenario.

---

## Mentor checkpoint #1 (post-Foundations gate)

Before you start, know that this chapter ends with a knowledge gate that benefits from a 30-minute conversation with your team lead or mentor. The gate is not the conversation. The gate is the work you bring to the conversation. The expectation, in honest terms: you read the chapter, attempt the gate, and then meet with someone who has shipped at least one production agent to talk through where your vocabulary felt wobbly, which of the three identity problems is novel to you, and which of the six recipes feels most familiar from your prior work. If you do not have a mentor available, the gate includes a rubric you can apply against your own answer. Self-assessment is the fallback, not the primary mode.

The mentor format works the same way whether you're inside a vendor onboarding program, ramping into a new role, or studying solo. If you don't have a mentor available, find an engineering peer or product peer who has shipped one production agent and walk through your gate answer with them. Pay particular attention to the three identity problems and the six recipe families — those are the surfaces where most production gaps appear, and the surfaces where hardware-enforced trust (cryptographic action chains, signed agent identity, verifiable policy enforcement) shows up next.

---

## §1.1 What is an agent?

This is the single most-asked question in the Foundations conversation and the one with the most contested vendor answer. The honest version of the answer is that **the term "agent" is contested**, **every major vendor has a different definition**, **the academic definition predates LLMs by decades**, and the only way to communicate cleanly about agents is to land a shared vocabulary first.

This section delivers that shared vocabulary. The single discipline you will commit to by the end of it — and that this book uses for the rest of its 500+ pages — is **Anthropic's workflow-vs-agent distinction**, treated as the Foundations definition.

### §1.1.1 Why the vocabulary matters

When a customer says "we built an agent," the meaning depends on which vendor's documentation their engineers were reading. If they read Anthropic's, "agent" means a system in which the LLM is choosing its own next action. If they read LangChain's, "agent" means an LLM plus tools plus state. If they read Microsoft's, "agent" means an LLM in a deterministic runtime loop. If they read OpenAI's, "agent" means an LLM with a configuration object attached.

These are not minor differences. They are three different governance problems, three different risk profiles, and three different sales conversations. Foundations needs you to be able to ask the disambiguating question — "what does your team mean by agent?" — and recognize which answer you are listening to.

### §1.1.2 The six-point autonomy spectrum

Rather than picking one vendor's definition, the Foundations frame is a **spectrum** with six points, ordered top-to-bottom by increasing autonomy and increasing state. Read each row as one step further along the spectrum.

| Level | Components | State | Autonomy | Decision Loop | HITL |
|-------|-----------|-------|----------|---------------|------|
| **Pipeline** | ETL + ML batch | None | None | None | N/A |
| **Workflow** | LLM in code-fixed path | Per-step | None | None | N/A |
| **Chatbot** | LLM + memory | Conversation | None | None | Per-turn |
| **RAG** | LLM + retrieval | Conversation | None | Single-pass | Per-turn |
| **Agent** | LLM + tools + state | Persistent | Bounded | Multi-step loop | Gated |
| **Fully-Autonomous** | LLM + tools + state | Persistent | Unbounded | Multi-step loop | None |

The top row is **Pipeline** (low autonomy, low state). The bottom row is **Fully-Autonomous** (high autonomy, high state — and not in regulated production anywhere as of mid-2026, see next paragraph). Governance and data-leak implications attach most heavily at the **Agent** and **Fully-Autonomous** rows; the lower-autonomy rows still expose data-leak surfaces (prompt injection, retrieval misrouting) but the action-provenance burden is smaller. Full mechanics are covered in Production §3.

The dimensions are **autonomy** (does the LLM decide what to do next, or is the flow fixed by code?) and **state** (does anything persist between turns and sessions, or is every call fresh?). Pipelines have neither. Workflows have small amounts of one or both. Chatbots have conversational state but no tool use beyond display. RAG adds retrieval but doesn't change the autonomy dimension. Agents add both: the LLM picks the next action, and state persists.

Note the position of **fully-autonomous** at the far right. **In regulated industries — financial services, healthcare, critical infrastructure — fully-autonomous deployments do not exist in production as of mid-2026.** Every named regulated deployment in the corpus sits at the "Agent with HITL" position or to its left. This matters because customers and analysts sometimes talk about fully-autonomous agents as if they were a real market. They are a research demonstration. They are not a regulated production category. `[architectural inference]` `[corroborated]`

### §1.1.3 The seven definitions, side by side

Seven definitions worth holding in your head, in the order you are most likely to encounter them in customer conversations.

**(1) LangChain / LangGraph (vendor-public, 2026).**

> "Agents are systems that combine LLMs with tools to create systems that can reason about tasks, decide which tools to use for which steps, analyze intermittent results, and work towards solutions iteratively." `[vendor-public]`

LangGraph itself is positioned as "a low-level orchestration framework for building, managing, and deploying long-running, stateful agents." The framework, not the definition. Weight: **broad**. Any LLM plus tools plus state qualifies.

**(2) Anthropic ("Building Effective Agents," December 2024).**

> "We categorize all these variations [agentic systems] as agentic systems, but draw an important architectural distinction between **workflows** and **agents**:
>
> - **Workflows** are systems where LLMs and tools are orchestrated through predefined code paths.
> - **Agents** are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks." `[vendor-public]`

This is the most disciplined definition in the corpus. The autonomy bar is explicit: workflows are not agents. Anthropic also makes the engineering tradeoff explicit — "agentic systems often trade latency and cost for better task performance; you should consider when this tradeoff makes sense." Weight: **narrow**.

**(3) OpenAI (Agents SDK documentation, 2026).**

> "An agent is the core building block in your apps, and is a large language model (LLM) configured with instructions, tools, and optional runtime behavior such as handoffs, guardrails, and structured outputs." `[vendor-public]`

OpenAI's framing is implementation-first. The SDK exposes `Agent`, `handoff`, `guardrail`, `mcp_server`, and `structured_output` as named primitives. Handoffs and guardrails are optional, not constitutive. Weight: **broad**.

**(4) Microsoft (Microsoft Agent Framework 1.0, April 2026).**

> "All agents are derived from a common base class, AIAgent... An agent in Agent Framework can use LLMs to process inputs, call tools and MCP servers, and generate responses. All agents in the Microsoft Agent Framework execute using a structured runtime model. This model coordinates user interaction, model inference, and tool execution in a deterministic loop." `[vendor-public]`

Microsoft emphasizes the deterministic runtime loop. Note: Microsoft Agent Framework (MAF) folded AutoGen v0.4 into a Python preview in Q1 2026 — older AutoGen literature uses different vocabulary (`ConversableAgent`, `GroupChat`) that should not be conflated with MAF 1.0. Weight: **medium**.

**(5) Google DeepMind (Vertex AI Agent Builder, rebranded Gemini Enterprise Agent Platform, 2026).**

> "Vertex AI Agent Builder is a suite of products that help developers build, scale, and govern AI agents in production. Agent Development Kit (ADK) is an open-source framework that simplifies the process of building sophisticated multi-agent systems while maintaining precise control over agent behavior." `[vendor-public]`

Google's definition is operational rather than conceptual: an agent is what you build with ADK and what runs in Agent Engine. Weight: **product-shaped, not conceptual**.

**(6) Russell & Norvig, *Artificial Intelligence: A Modern Approach* (4th edition).**

> "An **agent** is anything that can be viewed as perceiving its environment through sensors and acting upon that environment through actuators."
>
> "A **rational agent** is one that acts so as to achieve the best outcome or, when there is uncertainty, the best expected outcome."
>
> "AI is the study and design of rational agents that operate autonomously, perceive their environment, persist over a prolonged time period, adapt to change, and create and pursue goals." `[benchmark]`

This is the cleanest definition for non-engineers and predates LLMs by decades. Maps trivially onto LLM agents: the LLM is the policy, the prompt and tool results are percepts, tool calls are actuators. Weight: **canonical, conceptually unimpeachable**. It does not tell you anything specific about LLMs, which is exactly why it is the right intellectual anchor.

**(7) The LLM-agent survey papers (Xi et al. 2023; Wang et al. 2024).**

The academic survey literature converges on a **four-component model**:

- **Brain** — the LLM (planning, reasoning, decision)
- **Perception** — text, image, audio, multimodal input
- **Action** — tool calls, code execution, environment modification
- **Memory** — short-term (context window) plus long-term (vector or structured)

Canonical surveys: Xi et al., "The Rise and Potential of Large Language Model Based Agents" (arXiv:2309.07864, 2023); Wang et al., "A Survey on Large Language Model based Autonomous Agents" (arXiv:2308.11432, 2024). `[benchmark]`

### §1.1.4 Where the definitions agree

Across all seven, four points of consensus:

- An agent uses an **LLM** as the core decision-maker.
- An agent uses **tools** (functions, APIs, MCP servers, code execution).
- An agent has **some form of state** that persists across calls.
- An agent operates in a **loop** — not a single inference.

### §1.1.5 Where the definitions disagree

The interesting axis of disagreement is **the autonomy bar** — how much autonomy is required to count as an agent. Anthropic says workflows are not agents (LLM choosing its own next action is the bar). LangChain, OpenAI, and Microsoft treat workflow and agent as a continuum, not a binary. Practical implication: when you ask a customer "is this an agent?" and they say yes, your follow-up should be "by whose definition?"

Secondary axes of disagreement: HITL (LangGraph treats it as constitutive of production agents; OpenAI treats it as optional); multi-agent (Google ADK, MAF, and LangGraph support it as a first-class primitive; OpenAI Agents SDK uses "handoffs" as the equivalent); memory (LangGraph splits short-term from long-term explicitly; OpenAI rolled "Sessions" and "Memory" into the SDK in 2026; Google Vertex has "Sessions" and "Memory Bank"; Microsoft has "context providers" and "agent session").

### §1.1.6 The committed Foundations definition

**This book commits to the Anthropic discipline.**

The reasons are pedagogical and practical, not partisan. Pedagogically, Anthropic's distinction is the only one that draws a sharp line you can use. The other definitions describe a continuum and leave the line for you to draw. If you cannot draw the line in a customer conversation, you cannot identify the governance risk, and if you cannot identify the governance risk, you cannot recommend a deployment shape. The Anthropic line gives you a usable cut.

Practically, the Anthropic distinction is the one that maps onto LangGraph's primitives. In LangGraph, the cut between workflow and agent is roughly the cut between a `StateGraph` with deterministic edges (the flow is decided in code) and one with conditional routing driven by LLM output (the flow is decided by the LLM). The `create_react_agent` helper implements the agent loop; a hand-built `StateGraph` with explicit edges typically implements a workflow. We will see these primitives in §1.4.

The Anthropic definition is committed, but the other six are still vocabulary you need to recognize. Customers will use all of them. Your job is to recognize which one a customer is using and translate.

> **CONCEPT BOX (PM-track).** When someone says "agent" without context, ask the disambiguating question: *"What can it decide on its own, and what is on rails?"* If the answer is "nothing on rails," it is fully autonomous (rare in production; risky; a research demo). If the answer is "everything on rails," it is a workflow with LLM calls inside (very common in 2026 production; lower risk; not what most analysts mean when they say "agent"). Most real systems live in between, and the position on the spectrum is what determines the governance conversation. The word "agent" alone tells you very little.

```python
# Engineer-track illustration of the workflow-vs-agent cut in LangGraph.
# Both are valid LangGraph programs; only the second is an "agent" by the
# Anthropic definition.

# A workflow — LangGraph orchestrates a deterministic LLM-using pipeline.
# The flow is fixed; the LLM does not choose what happens next.
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState

workflow = StateGraph(MessagesState)
workflow.add_node("classify",  classify_ticket)   # an LLM call
workflow.add_node("retrieve",  lookup_kb)         # a deterministic tool
workflow.add_node("respond",   generate_reply)    # an LLM call
workflow.add_edge(START, "classify")
workflow.add_edge("classify", "retrieve")
workflow.add_edge("retrieve", "respond")
workflow.add_edge("respond", END)
app_workflow = workflow.compile()

# An agent — the LLM is in a loop and chooses its own next tool.
# This is what `create_react_agent` builds.
from langgraph.prebuilt import create_react_agent

app_agent = create_react_agent(
    model=chat_model,
    tools=[lookup_kb, place_refund, escalate_to_human],
    checkpointer=postgres_checkpointer,
)
```

The teachable point: when a customer says "we built an agent," your first question is whether the LLM is choosing its own next tool, or whether the flow is fixed in code. The answer determines the rest of the conversation.

The data-governance implications diverge from that point. In a **workflow**, the data path is fixed in code, so the regulated-data crossings are enumerable: the auditor can trace every join, every retrieval, every external call by reading the graph. In an **agent**, the LLM chooses the path at runtime — so the regulated-data crossings depend on which tool the policy picked, which conversation history it had access to, and which retrieval result the model decided to act on. Foundations §1.5 and §1.9 carry the named data-bleed surfaces; the standards that frame them (RATS, EAT, EAR) appear at §1.9.7 and again at §1.10.

---

## §1.2 The agent stack at a glance

Before any of the seven definitions matters in a customer conversation, the customer's engineering team is going to draw a diagram. The diagram will have ten or so boxes connected by arrows, and you will be expected to name the boxes. This section gives you the ten boxes.

The agent stack is not a strict layering — some tiers are co-equal, and some tiers exist only when others do. But the ten-tier mental model captures every component that shows up in a real production deployment, organized by what each component is responsible for. Whenever this book draws the shared backbone, it draws these ten tiers.

### §1.2.1 The ten-tier mental model — the shared backbone

The agent stack has ten tiers. **Tier 1 is the compute substrate** the runtime executes on. **Tier 10 is the LLM** — the policy that decides what to do next. Each tier between is a layer of responsibility added between the silicon and the user. The table below names each tier's primary concern and the modal vendors as of May 2026.

> *The 10-tier numbering follows the **OSI 7-layer model** ([ISO/IEC 7498-1](https://www.iso.org/standard/20269.html)) convention: Tier 1 is closest to the substrate, Tier 10 is closest to the user. We extend OSI's 7 layers to 10 because agent runtimes require explicit naming for **orchestration, identity, observability, and policy / governance** — surfaces that OSI compresses into "Application" but that this book treats as first-class given its focus on **trust, governance, and verifiability**.*

The per-tier vendor manifest:

| Tier | Primary concern | Modal vendors (May 2026) |
|------|-----------------|---------------------------|
| **1 — Compute** | Where the runtime physically executes | K8s · EKS · GKE · AKS · OpenShift · Nomad · bare-metal · Lambda |
| **2 — Deploy / runtime control plane** | Where the agent runtime is operated | LangGraph Platform (Cloud / BYOC / Self-Hosted) · Bedrock AgentCore · Azure AI Foundry Agent Service · GCP Vertex Agent Engine · DIY K8s |
| **3 — Policy / guardrails** | Input/output/tool-call gates | OPA · NeMo Guardrails · Guardrails AI · Lakera Guard · PromptShield · Bedrock Guardrails · LlamaGuard · Constitutional AI · Vertex Safety |
| **4 — Secrets** | Credential & key material custody | HashiCorp Vault · CyberArk Conjur · AWS Secrets Manager · Azure Key Vault · GCP Secret Manager · External Secrets Operator |
| **5 — State / checkpointer** | Durable persistence of agent state | PostgresSaver (production default) · RedisSaver · MongoDBSaver · DynamoDB · CosmosDB · in-memory (dev only) |
| **6 — Observability** | Trace, eval, replay | LangSmith · Langfuse · Arize AX / Phoenix · Datadog LLM Obs · Helicone · OpenTelemetry GenAI · OpenInference |
| **7 — Identity / AuthN / AuthZ** | User + workload + agent-on-behalf-of-user identity | Entra Agent ID · Okta for AI Agents · Auth0 for AI Agents · Ping · SPIFFE/SPIRE · custom JWT · OpenFGA · Cedar · Topaz · Permit.io · Oso |
| **8 — Tools / MCP plane** | Capability surface + agent-to-agent protocol | A2A (above) · MCP (middle) · AGP/AGNTCY (below) · MCP SDKs · Bedrock AgentCore Gateway · Azure Foundry MCP Gateway · Kong AI Gateway · Apigee · MuleSoft |
| **9 — Retrieval** | Vector / hybrid search into prompt | pgvector · Pinecone · Weaviate · Qdrant · Milvus · Elasticsearch · Redis · Azure AI Search · Snowflake Cortex · Databricks Vector Search · Turbopuffer |
| **10 — LLM** | The decision-making policy | Anthropic Claude · OpenAI GPT · Google Gemini · open-weight on vLLM / NIM / TensorRT-LLM / Together / Fireworks / Anyscale / Groq / Cerebras |

**A note on governance layers.** The ten-tier model above is the *runtime* layout. Cutting across those tiers, four governance approaches deserve naming so the reader recognizes them in customer conversations:

- **Guardrails** — content-filtering / policy-checking layers at the LLM boundary. NVIDIA NeMo Guardrails, Guardrails AI, Llama Guard, Azure AI Content Safety. Catches prompt-injection and output-policy violations.
- **Action layer governance** — wraps the *action* (tool call, agent step) rather than the content. Microsoft's **Agent Governance Toolkit (AGT)** is the named example; OpenAI's tool-call gating is a peer.
- **Sandbox isolation** — runs the agent in a constrained execution environment. **OpenShell** is the named open-source example; vendor-managed runtimes (LangGraph Cloud, Bedrock AgentCore) approximate this.
- **Cryptographic / hardware-enforced enforcement** — uses confidential computing TEEs to make policy decisions and the data they ran on provably enforced. The standards are **EAR** (Entity Attestation Result), **RATS** (RFC 9334), and **EAT** (RFC 9711).

Foundations §1.10 walks the comparison. Patterns and Production carry the depth.

Naming conventions in this book: when a tier name is capitalized inside text (e.g., "the LLM tier" or "the retrieval tier"), it refers to one of these ten. When we say "the agent's policy," we mean the LLM. When we say "the agent's memory," we mean state plus retrieval together.
### §1.2.2 What each tier does

**Tier 1 — Compute.** Where the runtime physically executes. Kubernetes is the modal substrate (EKS on AWS, GKE on GCP, AKS on Azure, OpenShift in regulated enterprises, vanilla K8s on bare metal in air-gapped sovereign deployments). Lambda and Cloud Run handle stateless edges; Modal, E2B, and Daytona run agent sandboxes for code execution. This tier rarely matters for the agent design itself but matters enormously for data residency and sovereignty. `[vendor-public]`

**Tier 2 — Deploy / runtime control plane.** Where the agent runtime is operated. **LangGraph Platform** is the LangChain-native choice, in four shapes: Cloud SaaS (LangChain-managed, US/EU), BYOC (customer's AWS account; LangChain manages control plane), Self-Hosted Enterprise (fully air-gapped customer Kubernetes), Self-Hosted Lite (single container for small teams). Hyperscaler alternatives: AWS Bedrock AgentCore, Azure AI Foundry Agent Service, GCP Vertex Agent Engine. DIY: vanilla Kubernetes with `langgraph build` artifacts. Patterns covers the trade-offs; Production covers the ten-axis deployment matrix. `[vendor-public]`

**Tier 3 — Policy / guardrails.** The runtime that filters or blocks LLM input, output, or tool calls based on policy. Open-source: **NeMo Guardrails** (NVIDIA), **Guardrails AI** (the OSS framework), **LlamaGuard** (Meta), **OPA** for action-policy. Commercial: Lakera Guard, Protect AI Guardian, Prompt Security, Robust Intelligence (now Cisco AI Defense), Cranium AI, HiddenLayer, Calypso AI, Datadog LLM Guardrails. Hyperscaler-native: PromptShield (Azure), Bedrock Guardrails, Vertex Safety Filters. Vendor-native: Anthropic Constitutional AI, OpenAI Moderation. Guardrails operate at three positions: **shift-left** (validate input before LLM), **shift-right** (validate output before user), and **tool-call gate** (validate before tool invocation). `[vendor-public]`

**Tier 4 — Secrets.** Where API keys, model credentials, tool credentials, signing keys, and HSM-backed identity material live. HashiCorp Vault (with Vault Agent and Vault Secrets Operator for Kubernetes), CyberArk Conjur, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager, Doppler, Akeyless, Infisical. External Secrets Operator is the CNCF-graduated Kubernetes standard. **Hardware Security Module (HSM)**-backed signing — Thales Luna, AWS CloudHSM, Azure Dedicated HSM, GCP Cloud HSM, Yubico HSM — is the substrate for cryptographic action chains (we'll see this in Production). `[vendor-public]`

**Tier 5 — State / checkpointer.** Where the agent's conversation state lives. **PostgresSaver (or `AsyncPostgresSaver`)** is the production default in LangGraph because it co-locates with pgvector at tier 9. **RedisSaver** is the #2 for sub-millisecond memory. Other production options: `MongoDBSaver`, DynamoDB, CosmosDB. **`MemorySaver` and `SqliteSaver` are dev-only — explicitly not for production.** Everything that persists across turns of a conversation lives here. Long-term memory across conversations lives in `BaseStore` (we'll see this in §1.5). `[vendor-public]`

**Tier 6 — Observability.** Trace-first, not metrics-first. Every LLM call, tool invocation, and graph node transition emits a span. The dominant platform inside LangGraph deployments is **LangSmith** (LangChain's first-party), with **Langfuse** (OSS, self-hostable) as the strongest alternative in EU and data-residency-sensitive deployments. **Arize AX** (commercial) and **Phoenix** (OSS) are distinct products from the same company — don't conflate them. **OpenTelemetry GenAI semantic conventions** plus **OpenInference** (Arize-submitted convention) are the protocol-layer answer for piping traces into the customer's existing SIEM (Splunk, Sentinel, QRadar, Chronicle, Exabeam). `[vendor-public]` Foundations §1.8 carries the observability weaknesses; Patterns and Production go deeper on the integration patterns and the audit-evidence chain.

**Tier 7 — Identity / AuthN / AuthZ.** The hardest tier in 2026 production. Three sub-problems: user identity (familiar, OAuth / **OpenID Connect** (OIDC) / **Security Assertion Markup Language** (SAML)), workload identity (familiar, **Secure Production Identity Framework For Everyone** (SPIFFE) / **SPIFFE Runtime Environment** (SPIRE) / service-account JWT, Entra Agent ID GA 2025), and the new one — **agent acting on behalf of a user** (DPoP, **Pushed Authorization Requests** (PAR, [RFC 9126](https://datatracker.ietf.org/doc/html/rfc9126)), RAR, CIBA, step-up authentication, MCP Authorization spec). Fine-Grained Authorization (FGA) products — OpenFGA, Cedar / AWS Verified Permissions, Topaz, Okta FGA, Auth0 FGA, Permit.io, Oso, Styra — provide relationship-based decisions for "can this agent, acting for this user, read this document section in this tenant?" §1.9 is the dedicated section. `[vendor-public]`

**Tier 8 — Tools / MCP plane.** The capability surface — every function, API, MCP server, and external service the agent can invoke. The 2026 standard is the three-layer protocol stack we'll see in §1.6: A2A on top (agent-to-agent), MCP in the middle (agent-to-tool, JSON-RPC), AGP (agent gateway protocol) on the bottom for transport. Managed planes — Bedrock AgentCore Gateway, Azure Foundry MCP Gateway, GCP Vertex Agent Gateway, Cloudflare AI Gateway, Kong AI Gateway, Apigee, MuleSoft — sit between the agent runtime and the tool surface to enforce policy and provide observability. `[vendor-public]`

**Tier 9 — Retrieval.** The vector or hybrid (vector plus keyword) search layer that surfaces relevant context into the LLM's prompt. The 2026 modal production default is **pgvector** (Postgres extension), because it co-locates with the checkpointer at tier 5. Larger or more specialized deployments use Pinecone, Weaviate, Qdrant, Milvus, Elasticsearch, Redis, Azure AI Search, Snowflake Cortex Search, Databricks Vector Search, or the emerging Turbopuffer and Vespa entries. Rerankers (Cohere Rerank, Voyage Rerank, BGE Reranker, ColBERTv2, Jina Reranker v2, Mixedbread.ai rerank-v2) sit between retrieval and prompt assembly. `[vendor-public]` `[corroborated]`

**Tier 10 — LLM.** The model. The decision-making policy. For 2026 deployments, the modal choices are Anthropic Claude (4.7 in the May 2026 cohort), OpenAI GPT (5), Google Gemini (3.0), plus open-weight models (Llama, Qwen, Mistral, DeepSeek) served via vLLM, NVIDIA NIM, TensorRT-LLM, or hosted inference providers (Together, Fireworks, Anyscale, Groq, Cerebras, SambaNova). The LLM is reached either directly via vendor API, via a hyperscaler reseller (Bedrock, Azure AI Foundry Models, Vertex), or via your own inference cluster. The pin-date matters because models are deprecated on rolling 6–12 month cycles; this book uses the May 2026 cohort throughout. `[vendor-public]`

### §1.2.3 What the diagram does not show

Three things the ten-tier model intentionally simplifies and that you should know about anyway.

**The network egress fabric.** Real deployments route every outbound call (to LLM provider, to MCP server, to retrieval index) through an egress proxy — Zscaler, Palo Alto Prisma Access, Netskope, Cloudflare Gateway, Symantec WSS, or a cloud-native equivalent. DLP at egress (Forcepoint, Symantec, McAfee, Microsoft Purview DLP, Proofpoint) inspects payloads for regulated content. **Foundations names the layer; Patterns covers the integration patterns, and Production carries the customer-egress depth and the DLP-bypass failure modes.**

**The supply-chain pipeline.** Every model artifact, MCP server image, vector index, and prompt template comes from somewhere — and that "somewhere" is a supply chain. The framing standards are **SLSA** (Supply-chain Levels for Software Artifacts), **in-toto** (build-step attestation), and **Sigstore** (cryptographic signing of artifacts). The implementation tools — Wiz Code, Aqua Trivy, Snyk, JFrog Xray, Anchore, Sonatype, and the `langgraph build` artifact pipeline — sit on top of those standards. The emerging standards stack (RATS, EAT, EAR) extends supply-chain proof from the artifact itself to the *runtime environment* that loads it. Foundations §1.10 ties the artifact attestation pattern to the runtime attestation pattern. Production §3.4 carries the audit-evidence pattern.

**The lineage / governance fabric.** Collibra, Alation, Atlan, data.world, Informatica, Microsoft Purview, Apache Atlas, **OpenLineage** (the open protocol — CNCF-incubating, LF AI & Data) — the customer-side data-governance layer that, in regulated industries, expects agent traces to flow into it. **Production carries the customer-lineage integration cookbook; OpenLineage is the canonical emission protocol.**

You will see all three again. For Foundations, the ten-tier mental model is enough.

> **CONCEPT BOX (PM-track).** When a customer's engineering team draws their agent architecture on a whiteboard, they are drawing some subset of these ten tiers. Your job, in a discovery call, is not to draw the diagram — it is to recognize the boxes they draw and ask the disambiguating questions. *"Is your checkpointer Postgres or Redis?"* tells you whether they are sub-millisecond or read-heavy. *"Are you using LangSmith or Langfuse?"* tells you whether their observability is SaaS-egress-tolerant or strictly self-hosted. *"How are you handling identity for agent actions on behalf of users?"* tells you whether they have noticed problem 3 yet (most have not).

---

## §1.3 Frameworks at conceptual level

The agent framework landscape in 2026 has consolidated into roughly three camps: graph-native open-source orchestrators (LangGraph, the dominant production-tier choice), open-source multi-agent frameworks aimed at faster developer onboarding (CrewAI, AutoGen / AG2, LlamaIndex Workflows, Pydantic AI, Mastra, Agno, Smol Agents, Letta, DSPy), and hyperscaler / platform vendor stacks (Microsoft Agent Framework, AWS Bedrock AgentCore, GCP Vertex Agent Engine, Snowflake Cortex Agents, Databricks Mosaic AI Agent Bricks, NVIDIA AI-Q, IBM watsonx Orchestrate, Salesforce Agentforce). `[corroborated]`

Foundations needs you to know the names. Patterns will carry the deep comparison. The honest framing up front, and the one most beginners do not know: **most of the public, named enterprise deployments at scale in 2026 run on LangGraph**. This is the reason this Field Guide is titled "Enterprise AI Agents on LangGraph" rather than "Enterprise AI Agents."

That said: **community signal (GitHub stars, npm/PyPI downloads) does not map cleanly to enterprise adoption.** CrewAI has more GitHub stars than LangGraph. AutoGen has a massive community. Pydantic AI is the cool kid in the Python type-safety crowd. None of those signals are the same as "named enterprise deployment with a CISO-approved architecture." When you compare frameworks at Foundations depth, you should be comparing them on philosophy and fit, not on popularity.

### §1.3.1 What a framework is, and why frameworks exist

A framework is a code library that gives you opinionated primitives for building an agent. The primitives encode design decisions the framework's authors have already made — what a "node" is, how state is passed between nodes, how the LLM loop terminates, how human-in-the-loop interrupts surface, how multi-agent handoffs work. Choosing a framework is choosing a set of opinions.

The alternative to using a framework is to write the agent loop yourself in plain Python (or TypeScript, or Go). This is sometimes the right answer — Anthropic's own coding agent (Claude Code) is built without LangGraph. `[corroborated]` But for most enterprise deployments, framework opinions encode hard-won lessons about state management, checkpointing, observability, and HITL — and rebuilding those opinions in-house is a 6–18 month investment with no payoff.

The question "which framework should we use?" is therefore really three questions: (1) Which opinions match how we want to build? (2) Which framework's deployment story matches our compliance posture? (3) Which framework has the named-customer evidence we need to defend the choice in front of our CISO? Foundations gives you the vocabulary to ask the first; Patterns and Production carry the second and third.

### §1.3.2 LangGraph — the focus of this book

**LangGraph** is LangChain Inc.'s graph-native orchestration framework. It treats the agent as a **state machine** — nodes are Python functions, edges are conditional transitions, and the runtime persists state at every node boundary. It exposes two authoring surfaces: the **Graph API** (explicit `StateGraph` plus nodes plus edges) and the **Functional API** (`@entrypoint` plus `@task` decorators, an imperative authoring path shipped GA in v0.3 in September 2025). It supports checkpointing, time-travel debugging, streaming, subgraphs, parallel execution via the `Send` API, human-in-the-loop interrupts, and a long-term memory store (`BaseStore`).

Named public deployments (each cited under `[customer-produced-evidence]` or `[corroborated]`): Klarna (customer-service routed multi-agent), Uber (Validator + AutoCover code-modification agents), LinkedIn (Hiring Assistant), Elastic Security (SOC alert triage), AppFolio (Realm-X property-management copilot), Replit (Replit Agent code generation), BlackRock (Aladdin Copilot, 50+ engineering teams), Captide (FSI research agent), Doctolib (Alfred healthcare assistant, non-PHI), Cisco Outshift (internal agent platform), JPMorgan (LangGraph Platform customer set), NVIDIA AI-Q Blueprint (built on LangGraph internally).

LangGraph 1.0 (Python) shipped October 2025; LangGraph Platform GA followed in October 2025. LangSmith provides the tightest integration in the ecosystem — zero-code auto-instrumentation of `StateGraph` nodes. `[vendor-public]`

Known limitations honest enough to flag in Foundations: TypeScript runtime and Platform feature parity lag Python by roughly 6–9 months; BYOC deployment is AWS-only as of 2026-05 (Azure and GCP BYOC are roadmap items, not shipping); the learning curve is steep relative to higher-level frameworks like CrewAI for trivial "hello, agent" use cases. `[vendor-public]` `[architectural inference]`

This book treats LangGraph as the focus. The remaining frameworks are positioned at Foundations as comparators.

### §1.3.3 CrewAI

**Maintainer:** crewAI Inc. (founded by João Moura). Seed round May 2024 from Boldstart, Insight Partners, and Andrew Ng's AI Fund. `[vendor-public]`

**Philosophy:** Role-based multi-agent collaboration. Define crew members by role, goal, and backstory; assign tasks; let the crew sequence and execute. Higher level of abstraction than LangGraph — less graph control, more "tell each agent who it is and what to do."

**Fits:** Quick multi-agent prototypes with clear role assignments (researcher, writer, editor); marketing, content generation, research workflows; teams that want declarative agent definitions over imperative graph wiring.

**Distinction worth holding:** **CrewAI Enterprise** is commercially distinct from open-source CrewAI. Enterprise adds hosted Crews, managed observability, and a different compliance posture. When a customer says "we use CrewAI," ask which.

Community signal: GitHub stars in the 25K+ range (among the highest in the agent-framework category). Customer logos on the CrewAI website include Oracle, Deloitte, Accenture, IBM, PwC, though publicly disclosed enterprise case studies are sparser than LangGraph's. `[vendor-public]` `[architectural inference]`

### §1.3.4 AutoGen and AG2 (the fork) → Microsoft Agent Framework

**Maintainer:** Two projects sharing a lineage:
- **AutoGen** — originated at Microsoft Research, primary maintainers Chi Wang and Qingyun Wu (both departed Microsoft in 2024–2025). Now folded into the broader Microsoft Agent Framework convergence.
- **AG2** — community fork led by the original authors after their Microsoft departure (`ag2ai/ag2` on GitHub). `[vendor-public]`

**Philosophy:** Conversational multi-agent — agents are participants in a structured conversation; the framework orchestrates whose turn it is to speak.

**Microsoft Agent Framework (MAF) 1.0** shipped April 2026 and folded AutoGen v0.4 into MAF Python preview in Q1 2026. The migration from AutoGen v0.4 to MAF 1.0 is non-trivial. When a customer says "we use AutoGen," ask which version, and whether they have an upgrade plan to MAF. `[vendor-public]`

**Fits:** Customers in Microsoft / Azure-aligned shops where AAD integration, Azure AI Foundry, and Azure-native observability matter more than framework portability.

### §1.3.5 LlamaIndex Workflows

**Maintainer:** LlamaIndex Inc. (Jerry Liu, CEO). `[vendor-public]`

**Philosophy:** Event-driven workflows. Workflows declare events; steps subscribe to events and emit new events. The runtime routes based on event types.

**Fits:** RAG-heavy applications where document parsing, chunking, embedding, and retrieval are the dominant operations and the agent is a wrapper around them. Also notable: LlamaIndex retains a strong indexing-and-retrieval story, distinct from LangChain's, that some teams prefer for document-centric agents.

### §1.3.6 Semantic Kernel

**Maintainer:** Microsoft. `[vendor-public]`

**Philosophy:** A multi-language (C#, Python, Java) SDK for embedding LLM functionality into existing enterprise applications. Pre-dates the agent wave; has been retrofitted to support agent patterns.

**Fits:** .NET-heavy enterprises where Semantic Kernel is already deployed and the agent layer is being added to an existing C# codebase.

### §1.3.7 OpenAI Agents SDK

**Maintainer:** OpenAI. `[vendor-public]`

**Philosophy:** Implementation-first. An `Agent` object with `instructions`, `tools`, `handoffs`, `guardrails`, `mcp_servers`, and `structured_output`. The 2026 evolution adds **sandbox execution** for long-horizon tasks.

**Fits:** OpenAI-aligned shops where ChatGPT, GPT-5, and Responses API are the LLM defaults. The handoff primitive is OpenAI's multi-agent equivalent; teams used to LangGraph's supervisor topology will find handoffs familiar.

### §1.3.8 Other frameworks worth naming

For vocabulary completeness; Foundations does not go deep on any of these. They will surface in Patterns.

- **Pydantic AI** — type-safe Python agents from the Pydantic team. Strong with type-strict shops.
- **Mastra** — TypeScript-first agent framework. The most likely lateral threat to LangGraph in the Vercel / JAMstack / serverless segment.
- **Agno** — Python-first agent framework with a focus on ergonomic tool composition.
- **Smol Agents** — Hugging Face's small, code-first agent framework.
- **Atomic Agents** — community framework emphasizing atomic, composable units.
- **Letta** (formerly MemGPT) — agent framework with self-editing memory as a first-class primitive, descended from the MemGPT academic lineage.
- **DSPy** — Stanford / Berkeley framework for "compiling" prompts; orthogonal to most other frameworks; sometimes co-deployed.
- **Burr** (Hamilton / DAGWorks) — graph orchestration for ML workflows.
- **Inngest, Temporal** — durable workflow orchestrators, not agent-specific, but used under agent workloads at scale.

### §1.3.9 Hyperscaler and platform-vendor stacks

These deserve a separate mention because customer conversations frequently begin with "we want to use [hyperscaler stack]," and you need to know whether that stack composes with LangGraph or replaces it.

- **AWS Bedrock AgentCore** — AWS-native agent runtime, including AgentCore Gateway (managed MCP plane) and AgentCore Supervisor (multi-agent primitive). Composes with LangGraph (you can run a LangGraph agent inside Bedrock AgentCore) or replaces it (you can build the agent entirely in Bedrock).
- **Azure AI Foundry Agent Service** — Azure-native agent runtime. The Azure-native MCP gateway. Composes or replaces.
- **GCP Vertex Agent Engine + Agent Development Kit (ADK)** — Google's agent runtime and SDK. ADK is open source. Vertex Agent Engine is managed.
- **Snowflake Cortex Agents** — Snowflake-native agents, tightly coupled to Snowflake data.
- **Databricks Mosaic AI Agent Bricks** — Databricks-native agents, tightly coupled to Databricks data.
- **NVIDIA AI-Q** — NVIDIA's enterprise agent blueprint. **Built on LangGraph internally.** `[vendor-public]`
- **IBM watsonx Orchestrate** — IBM's enterprise agent platform.
- **Salesforce Agentforce** — Salesforce-native agents tightly coupled to Salesforce data. (Sept 2025 ForcedLeak disclosure is the canonical reminder that "platform-vendor" does not mean "automatically safe.") `[named-incident]`
- **ServiceNow AI Agents (Now Assist Agents / Workflow Agents)** — ServiceNow's 2025 launch brought the largest enterprise workflow platform into the named-platform comparison. Tightly coupled to ServiceNow's Now Platform data model and ITSM/ITOM/HRSD workflows; the canonical reference customer for ServiceNow-native agents at scale is ServiceNow's own DT team. `[vendor-public]`

### §1.3.10 The honest framing

LangGraph is the focus of this book because most of the public named deployments at enterprise scale are on LangGraph. The reasons are not mysterious: LangGraph's combination of explicit state-machine primitives, first-class HITL, durable checkpointing, and tight LangSmith integration matches what enterprises need at scale. Community signals (GitHub stars, npm downloads) point in other directions for some frameworks, and those frameworks are real and shipping. They are not, in mid-2026, the frameworks that show up in Fortune-500 production decks.

When a customer says they are evaluating frameworks, the disambiguating questions are: (1) What is your compliance posture? (BYOC AWS-only is a real LangGraph constraint.) (2) What is your language strategy? (Python-first vs TypeScript-first matters more than people admit.) (3) Who is operating the agent runtime — your team, a hyperscaler, or a vendor SaaS? (4) Do you need named-customer evidence at your scale? Patterns and Production carry these answers.

> **CONCEPT BOX (PM-track).** A framework is a set of opinions. Choosing a framework is choosing a set of opinions. The right framework is the one whose opinions match how your customer's team wants to build *and* whose deployment story matches their compliance posture. For most enterprise FSI / Healthcare / ISV customers in 2026, that ends up being LangGraph — but the honest answer in a discovery call is *"it depends on your compliance posture, your language strategy, and your operator preference."* Never recommend a framework before you know those three answers.

---

## §1.4 LangGraph primitives

> **Annotation key (recap).** `[CKP]` checkpointer, `[OBS]` observability emission, `[POL]` policy/guardrail check, `[HITL]` human-in-the-loop interrupt. Arrow styles: solid `─►` LLM-decided, double `══►` system-automatic, dashed `─ ─►` human-mediated. First defined in §1 ("How to read this chapter") of Foundations.

This is the section where the engineer-track and PM-track diverge most clearly. Engineer-track readers will read the code. PM-track readers will read the concept boxes that bracket each primitive. The vocabulary you absorb here will appear throughout the rest of the book.

### §1.4.1 `StateGraph` and the Graph API

The `StateGraph` is LangGraph's central primitive. Conceptually, it is a directed graph where **nodes are Python functions** and **edges are transitions** between them. The graph carries a **shared state object** that every node can read from and write to. When the graph runs, the runtime picks the next node based on the edge logic and calls it with the current state; the node returns a state update; the runtime applies the update and picks the next node.

> **CONCEPT BOX (PM-track).** Think of a `StateGraph` as a flowchart you can run. The boxes are functions that do work (call an LLM, look up a document, send an email, ask for human approval). The arrows are decisions about what to do next, which can be fixed in code (workflow) or chosen by the LLM (agent). The state is a shared notepad every box can read and write.

```python
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState

# Build a graph whose state is the standard "messages list" schema.
builder = StateGraph(MessagesState)

# Add nodes — each is a function that takes state and returns a state update.
builder.add_node("plan",   plan_step)
builder.add_node("act",    act_step)
builder.add_node("reflect", reflect_step)

# Wire edges.
builder.add_edge(START, "plan")
builder.add_edge("plan", "act")
builder.add_conditional_edges("act", needs_reflection, {
    True:  "reflect",
    False: END,
})
builder.add_edge("reflect", "plan")

# Compile to a runnable graph with persistence.
graph = builder.compile(checkpointer=postgres_checkpointer)
```

The wiring vocabulary worth recognizing: `add_node` (registers a function as a node), `add_edge` (declares a fixed transition), `add_conditional_edges` (declares a transition whose target depends on a function evaluated at runtime), `START` and `END` (sentinel nodes), `compile` (turns the builder into a runnable).

### §1.4.2 `MessagesState` and the `add_messages` reducer

The default state schema for chat-style agents is `MessagesState`, which has a single field — `messages` — that holds a list of message objects (user, assistant, tool, system). The `add_messages` reducer is the function that defines how new messages are appended to or merged with the existing list. Custom state schemas can add additional fields (e.g., `current_plan`, `tenant_id`, `retrieved_docs`) and define reducers for them.

> **CONCEPT BOX (PM-track).** `MessagesState` is the conversation transcript — every user message, every LLM response, every tool call, every tool result, in order. Most LangGraph agents start by extending this with their own application-specific fields.

> **GOVERNANCE-ESSENTIAL CONCEPT — the *agent's confidentiality blast radius*.** Stop and read this carefully. `MessagesState` is not just "the chat log." It is the running accumulation of **everything that has touched the agent in this thread**. By the end of a single multi-turn conversation, the `messages` list contains:
>
> 1. **Every raw user prompt** — including anything the user pasted (a customer's contract, a patient note, an internal email thread, a portfolio position, a credentials block accidentally copied).
> 2. **Every LLM response** — including any reasoning the model surfaced about user data.
> 3. **Every tool call the LLM emitted** — including the arguments, which often contain user identifiers, account numbers, dates of birth, ticker symbols, or PHI.
> 4. **Every tool result returned to the LLM** — including rows from CRM / EHR / payments / KYC systems, raw documents retrieved by RAG, raw API payloads from external services, raw SQL result sets from Text-to-SQL recipes.
> 5. **Every system message the application injected** — including grounding context, retrieved-document chunks, system prompts that may themselves embed customer or tenant data, and any "context from other systems" the orchestrator stuffs into the conversation.
>
> Embeddings live in the **vector DB** tier (§1.2, §1.5.7), not in `MessagesState`. But the *text* that was embedded (the source document, the retrieved chunk) does land in `messages` whenever a retrieval tool returns it.
>
> **In a regulated industry, treat `MessagesState` as the highest-sensitivity surface in the agent.** If the agent is allowed to read **Protected Health Information (PHI)**, `messages` contains PHI. If the agent is allowed to read MNPI, `messages` contains MNPI. If the agent is allowed to read regulated customer data under SR 11-7, GDPR, HIPAA, NYDFS Part 500, or DORA, that data is in `messages` for the lifetime of the thread.
>
> **And every system that touches `MessagesState` inherits this surface.** That means: the **checkpointer** (Scope 2; §1.5.3) — every checkpoint row in Postgres contains the full `messages` list at that node. The **observability stack** (LangSmith / Langfuse / OTel; §1.2 tier 6) — every trace span contains the messages the LLM saw. **Debugging logs** — every `print(state)` and every "log the conversation for replay" hook. **Time-travel debugging** — every checkpoint the engineer can resume from is, by definition, a snapshot of the regulated-data payload. **Replay artifacts** — every captured-and-replayed thread is a captured-and-replayed copy of the conversation.
>
> The Field Guide names this surface explicitly: **the `MessagesState` surface** — also called **"the agent's confidentiality blast radius."** When you see those phrases in Patterns and Production, they mean the union of (a) the in-memory `messages` list, (b) every checkpoint that has ever held a copy, (c) every trace span that has ever logged a copy, and (d) every downstream system (lineage, SIEM, eval harness, replay buffer) that has ever received a copy. **You cannot reason about agent governance without reasoning about this surface.** [vendor-public; architectural inference]
>
> Forward references: Patterns §2.4 (Identity) discusses how to bind the contents of `messages` to an authenticated principal and a per-tenant key. Patterns §2.7.2 (the six highest-frequency governance categories) treats `MessagesState`-derived leakage as a first-class category. **Production §3.2 "Cross-Tenant Isolation: The Five Surfaces"** is where the `MessagesState` surface is closed in production deployments — every one of the five surfaces (retriever, cache, checkpointer, observability, model) is downstream of `MessagesState`.

### §1.4.3 `@entrypoint` and `@task` — the Functional API

The Functional API, shipped GA in LangGraph v0.3 in September 2025, lets you write agents in an **imperative** style with Python decorators rather than the **declarative** graph-builder style. `@entrypoint` marks the function the runtime calls; `@task` decorates individual steps. The runtime handles state, checkpointing, and resumption underneath. Roughly 40%+ of new LangGraph deployments use the Functional API per LangGraph DevRel's own community-tracking. `[vendor-public]`

> **CONCEPT BOX (PM-track).** Two ways to author the same agent: declaratively (build a graph, hand it to the runtime) or imperatively (write Python that calls steps in sequence, let the runtime track state). The declarative version is what you see on whiteboards; the imperative version is what some teams find easier to read.

```python
from langgraph.func import entrypoint, task

@task
def plan_step(state):
    # ... LLM call ...
    return {"plan": plan}

@task
def execute_step(plan):
    # ... tool call ...
    return {"result": result}

@entrypoint(checkpointer=postgres_checkpointer)
def my_agent(input_state):
    plan = plan_step(input_state).result()
    result = execute_step(plan).result()
    return result
```

### §1.4.4 `interrupt()`, `Command(goto=...)`, `Command(resume=...)`

Three closely-related primitives worth distinguishing carefully — this is one of the most common-confusion clusters in LangGraph onboarding.

- **`interrupt(value)`** — Called inside a node. **Pauses the graph execution mid-node**, surfaces the `value` to the calling code, and waits. The calling code can do anything (ask a human, write to a queue, send a notification) and then later resume.
- **`Command(goto=..., update=...)`** — Returned from a node. **Tells the runtime where to go next** and what state update to apply. Used for in-node dynamic routing.
- **`Command(resume=...)`** — Passed *to* the runtime when calling a thread that had hit an `interrupt()`. **Resumes the paused execution** with the resume value.

> **CONCEPT BOX (PM-track).** `interrupt()` is the agent saying "pause; I need a human." `Command(resume=...)` is the human saying "OK, proceed." `Command(goto=...)` is the agent saying "I'm done with this step; go run this other step next."

```python
from langgraph.types import interrupt, Command

def confirm_refund_node(state):
    refund_details = state["pending_refund"]
    # Pause the graph and surface the refund details to the calling code.
    decision = interrupt({
        "type": "approve_refund",
        "amount": refund_details["amount"],
        "customer": refund_details["customer_id"],
    })
    if decision == "approve":
        return Command(goto="execute_refund", update={"approved": True})
    else:
        return Command(goto="notify_customer_no_refund", update={"approved": False})

# In the calling code:
result = graph.invoke(initial_state, config={"configurable": {"thread_id": "t1"}})
# The graph hit interrupt(); now `result` contains the interrupt payload.
# Later, after human review:
result = graph.invoke(Command(resume="approve"), config={"configurable": {"thread_id": "t1"}})
```

### §1.4.5 `thread_id` and what "thread" means

A **thread** in LangGraph is a single conversation with the agent. Every thread has a `thread_id` — a string the caller chooses. Pass the same `thread_id` again, and the agent resumes where the conversation left off. Pass a new `thread_id`, and the agent starts fresh.

The `thread_id` lives in `RunnableConfig.configurable`, which is the per-call configuration dictionary. Other things that live there: tenant identifiers, user identifiers, feature flags.

> **CONCEPT BOX (PM-track).** A thread is one conversation. A `thread_id` is the conversation's identifier. The same user can have many threads (one per support ticket, one per customer-service session, one per project). Threads are persistent — the runtime remembers what happened in each one.

```python
# Resume an existing conversation.
result = graph.ainvoke(
    {"messages": [{"role": "user", "content": "What did you decide yesterday?"}]},
    config={"configurable": {"thread_id": "alice-2026-05-24"}},
)
```

### §1.4.6 `compile(checkpointer=...)`

`compile()` is the call that turns a `StateGraph` builder into a runnable graph. The `checkpointer` argument is where you wire in persistence — pass a `PostgresSaver` (or `AsyncPostgresSaver`) and the runtime will persist state to Postgres at every node transition.

> **CONCEPT BOX (PM-track).** `compile()` is the "ship it" step. Up to this point, you've described the graph; now you're telling the runtime which database to persist state to.

### §1.4.7 The `Send` API

`Send` is the LangGraph primitive for **fan-out** — invoking the same downstream node many times in parallel with different inputs. You return a list of `Send` objects from a node, and the runtime runs them in parallel and aggregates the results.

> **CONCEPT BOX (PM-track).** Think of `Send` as "kick off N copies of this step in parallel and gather the results." Used heavily in deep-research and multi-document analysis agents, where you might want to investigate ten leads at the same time.

```python
from langgraph.types import Send

def fan_out_node(state):
    leads = state["leads"]  # 10 documents to investigate
    return [Send("investigate_lead", {"lead": lead}) for lead in leads]
```

### §1.4.8 `BaseStore` — long-term memory

`BaseStore` is LangGraph's interface for **cross-thread, long-term memory**. The thread checkpointer covers state *within* a thread; `BaseStore` covers state *across* threads. Production implementations: `PostgresStore`, `RedisStore`. Dev: `InMemoryStore`.

> **CONCEPT BOX (PM-track).** Two kinds of memory: the thread checkpointer remembers what happened in *this conversation*. `BaseStore` remembers what the agent learned about *this user* (or this tenant, this account, this case) *across all their conversations*. When a customer says "the agent forgets things between sessions," the question is whether they have a `BaseStore` at all. `[vendor-public]`

> **WHY THERE ARE SO MANY MEMORY STARTUPS — forward reference.** If you've been reading agent newsletters, you've seen Letta, Mem0, Cognee, Zep, MemGPT, and a dozen vector-memory startups — and you may be wondering whether `BaseStore` is the same thing, an alternative to them, or unrelated. Foundations gives you the LangGraph-native vocabulary (checkpointer + `BaseStore` + the four cognitive-science memory tiers in §1.5.5). The full memory landscape — the major architectures (paged virtual context / Letta, vector-backed retrieval memory, graph memory, hybrids), the major named projects, when each fits which deployment shape, and the governance implications of each — lives in **Patterns §2.3.7 "Agent Memory — The Landscape."** Foundations names the primitive; Patterns surveys the field around it.

```python
from langgraph.checkpoint.postgres import AsyncPostgresSaver
from langgraph.store.postgres import AsyncPostgresStore

graph = builder.compile(
    checkpointer=AsyncPostgresSaver(conn_pool),  # thread-scoped
    store=AsyncPostgresStore(conn_pool),          # cross-thread
)
```

### §1.4.9 LangGraph Studio

**LangGraph Studio** is the visual debugger. You point it at a running `langgraph dev` server, and it gives you a graph view with breakpoints, state inspection, time-travel, replay, and inline editing of state. Every demo at LangChain Interrupt 2025 used Studio. `[vendor-public]`

> **CONCEPT BOX (PM-track).** Studio is what an engineer points at when they need to know *why* the agent did what it did. It is the visual equivalent of `print()` for an entire state machine — except you can rewind, edit state mid-execution, and re-run from any node. When a customer says "we use LangGraph Studio," they mean their engineering team has visual debugging in their workflow, which is a maturity signal.

### §1.4.10 `langgraph dev`, `langgraph up`, `langgraph build`

The CLI commands that wrap the dev loop:

- **`langgraph dev`** — runs your graph locally with auto-reload, Studio-compatible. Dev only.
- **`langgraph up`** — deploys to LangGraph Platform.
- **`langgraph build`** — builds a deployable artifact (Docker image, signed bundle).

A **production-vs-dev caveat to know about**: `langgraph dev` silently ignores user-supplied checkpointers in some configurations and uses its own in-memory store. This is documented in the LangGraph docs and is a common stumbling block. **For any production-shaped test, use `langgraph up` or the equivalent self-hosted runtime, not `langgraph dev`.** `[vendor-public]`

> **CONCEPT BOX (PM-track).** `langgraph dev` is the local development loop. `langgraph up` is the deploy. `langgraph build` is the artifact build for handoff to ops. The caveat to remember: `langgraph dev` is not a faithful production simulator, so "it worked in dev" is not "it will work in prod."

### §1.4.11 `create_react_agent` — the on-ramp helper

`create_react_agent(model, tools, checkpointer=...)` is the prebuilt helper that builds a minimal ReAct agent as a two-node `StateGraph` (an "agent" node and a "tools" node) with a conditional edge that loops until the LLM stops calling tools. This is the **single most-used LangGraph on-ramp**. `[vendor-public]`

> **CONCEPT BOX (PM-track).** When an engineer says "I built a ReAct agent in five lines," they almost always mean they used `create_react_agent`. It is the "hello, agent" primitive — the moment most LangGraph users stop reading docs and start building.

```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    model=anthropic_claude,
    tools=[lookup_account, place_refund, escalate_to_human],
    checkpointer=postgres_checkpointer,
)
```

### §1.4.12 Common-confusion call-out — `interrupt()` vs `Command(goto=...)` vs `Command(resume=...)`

These three primitives confuse almost everyone the first week.

| Primitive | Where called | What it does |
|---|---|---|
| `interrupt(value)` | Inside a node | Pauses execution; surfaces `value` to caller; waits |
| `Command(goto=..., update=...)` | Returned from a node | Routes to a specific next node; applies a state update |
| `Command(resume=...)` | Passed to `graph.invoke()` | Resumes a paused thread with the resume value |

If you only remember one rule: `interrupt()` pauses, `Command(resume=...)` un-pauses, and `Command(goto=...)` is in-node routing that has nothing to do with pause/resume.

### §1.4.13 Streaming modes

LangGraph supports four streaming modes that control what comes back to the caller during execution:

- **`values`** — the full state value at each node transition. The richest.
- **`updates`** — only the deltas applied at each node. The most efficient.
- **`messages`** — only message-list updates. The most user-UI-friendly.
- **`debug`** — internal runtime events. The most verbose.

You will encounter all four when reading customer code. The PM-track takeaway: streaming mode is a UX decision. If you want the user to see each tool call as it happens, you stream `updates` or `messages`. If you want to batch and show only the final answer, you don't stream at all.

### §1.4.14 Subgraphs

A **subgraph** is a `StateGraph` used as a node inside another `StateGraph`. The subgraph has its own state schema (which can differ from the parent's), its own nodes, its own edges. The parent calls the subgraph the way it would call any other node, and the subgraph returns a state update.

Subgraphs are the encapsulation primitive. Multi-agent systems often build each agent as a subgraph and compose them under a supervisor.

> **CONCEPT BOX (PM-track).** Subgraphs are how multi-agent systems are wired in LangGraph. Each specialist agent is a subgraph; the supervisor is the parent graph that decides which subgraph to call next.

### §1.4.15 The primitives in a single picture

A minimal production ReAct agent with HITL, threaded by `thread_id`, persisting state to a durable checkpointer, with Studio-compatible debugging, is built up in three frames. Each frame adds one concept. The §1.4.16.5 diagram is the same shape applied to a worked example — the two diagrams are a true small-multiples pair.

**Frame 1 — the bare ReAct loop.** Two nodes, one loop, two annotations. This is what every LangGraph agent is at minimum.

```
+----------------------------------------------------------------------+
| THREAD: thread_id=t1                            [CKP at every edge]  |
|                                                                      |
|   [user input]                                                       |
|        |                                                             |
|        v                                                             |
|   +--> [agent (LLM)] [OBS] --no--> [return to user]                  |
|   |        |                                                         |
|   |        | call?                                                   |
|   |        v                                                         |
|   |    [tools node] [OBS]                                            |
|   |        |                                                         |
|   +=== ToolMessage =                                                 |
|                                                                      |
+----------------------------------------------------------------------+
```

*Frame 1: bare ReAct loop. Solid arrow = LLM decided; double arrow = runtime advanced after the tool returned.*

**Frame 2 — add the HITL branch.** When a tool call meets a policy threshold (e.g., refund > $500), the tools node does NOT execute the tool. It routes to a human-approval node, which calls `interrupt()` and pauses the graph. Execution may sleep for hours; durable state is persisted at every boundary.

```
+----------------------------------------------------------------------+
| THREAD: thread_id=t1                            [CKP at every edge]  |
|                                                                      |
|   [user input]                                                       |
|        |                                                             |
|        v                                                             |
|   +--> [agent (LLM)] [OBS] --END--> [return]                         |
|   |        |                          ^                              |
|   |        | call?                    | resume('approve')            |
|   |        v                          .                              |
|   |    [tools node] [OBS] [POL]      .                               |
|   |        |        |                .                               |
|   +=no===  |        +-- refund>$500 -+                               |
|            |        |                                                |
|            v        v                                                |
|       (to agent) [human approval / interrupt() / [HITL]]             |
|                                                                      |
+----------------------------------------------------------------------+
```

*Frame 2: HITL branch. Dashed arrow = human-mediated edge; the graph may sleep for hours.*

**Frame 3 — overlay cross-cutting services (side-box, not in the flow).** Checkpointer, store, observability, and policy are not nodes in the graph; they are runtime services every node interacts with. Rendered as a side-box rather than as flow-through to avoid confusing "runtime service" with "graph node."

```
+--------------------------+   +-------------------------------------+
| GRAPH (Frames 1+2)       |   | RUNTIME SERVICES (cross-cutting)    |
|                          |   |                                     |
|  agent <==> tools        |   |  PostgresSaver -- state [CKP]       |
|              <==> approve|   |  PostgresStore -- cross-thread mem  |
|                          |   |  LangSmith     -- spans  [OBS]      |
|                          |   |  Guardrails AI -- policy [POL]      |
+--------------------------+   +-------------------------------------+
```

*Frame 3: cross-cutting services are a side-box, not flow-through nodes.*

This is the diagram you should be able to redraw on a whiteboard at the end of Foundations. Every annotation has meaning:

- `[CKP]` — checkpoint write. Happens at every node transition. Persisted by the checkpointer.
- `[OBS]` — span emission. LangSmith (or Langfuse, or OTel) captures these spans.
- `[POL]` — policy / guardrail check. Tools-tier and LLM-tier guardrails run here.
- `[HITL]` — interrupt point. Surfaces a pause to the caller; state is durable for the duration.

Every production diagram in this book uses these annotations. You will see them again in §1.10 (the 6 use case families), §1.11 (what can go wrong), and at the end of Foundations (the knowledge gate).

---

## §1.4.16 A minimum viable production agent — putting the primitives together

A short walkthrough that pulls §1.4's primitives into a single coherent example. Engineer-track readers should follow the code. PM-track readers should follow the concept boxes between the code blocks and skip the code itself.

The scenario: a customer-support agent for a payments fintech. The agent can look up an account, place a refund, or escalate to a human. Refunds above `$500` require human approval. The agent state persists per-thread in Postgres; per-tenant `BaseStore` carries account-history memory. Every node emits an OpenTelemetry-compatible span. The graph runs under `langgraph dev` for local development; `langgraph up` for production deploy.

> **CONCEPT BOX (PM-track).** This is the minimum viable shape of a production agent — small enough to fit in 60 lines of code, but with every primitive that matters: state schema, tools, HITL, checkpointer, store, and per-tenant config. When a customer's engineering team shows you their architecture and says "this is what we shipped," it will look roughly like this, plus 5–10 production refinements. Recognize the shape; the refinements are Patterns and Production.

### §1.4.16.1 The state schema

The agent extends `MessagesState` with three custom fields: `tenant_id` (per-tenant isolation key), `pending_refund` (the refund the agent is currently considering, if any), and `human_approved` (the flag the HITL approval flips).

```python
from typing import TypedDict, Annotated, Optional
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState, add_messages

class SupportAgentState(MessagesState):
    tenant_id: str
    pending_refund: Optional[dict]   # {"account_id": ..., "amount": ..., "reason": ...}
    human_approved: Optional[bool]
```

> **CONCEPT BOX (PM-track).** Every agent has a state schema — the structured "shared notepad" the nodes read from and write to. `MessagesState` is the base; custom fields are added as the agent's responsibilities grow. The custom fields here say: "I know which tenant this conversation belongs to; I might be considering a refund right now; I might be waiting for human approval."

### §1.4.16.2 The tools

Three tools, each with a per-tenant predicate baked in.

```python
from langchain_core.tools import tool

@tool
def lookup_account(account_id: str, tenant_id: str) -> dict:
    """Look up an account in the customer database. Strictly tenant-scoped."""
    # Real implementation: parameterized SQL with WHERE tenant_id = %s.
    return _db.account_for_tenant(account_id, tenant_id)

@tool
def place_refund(account_id: str, amount: float, reason: str, tenant_id: str) -> dict:
    """Place a refund. Must be HITL-gated above $500 (handled in graph)."""
    return _payments.refund(account_id, amount, reason, tenant_id=tenant_id)

@tool
def escalate_to_human(account_id: str, summary: str, tenant_id: str) -> dict:
    """Escalate the conversation to a Tier-2 human agent in the tenant's queue."""
    return _queue.enqueue(tenant_id=tenant_id, account_id=account_id, summary=summary)

TOOLS = [lookup_account, place_refund, escalate_to_human]
```

> **CONCEPT BOX (PM-track).** Three tools. Each takes a `tenant_id`. That argument is the per-tenant boundary — the agent must pass the correct tenant for every tool call. In production, this is not enforced strongly enough by argument-passing alone; the database, the queue, and the payments system must each enforce per-tenant isolation independently. Foundations introduces the concept; Patterns covers the cross-tenant isolation chapter in depth.

> **CONCEPT BOX (PM-track) — the agent-graph tenant-isolation gap.** The `tenant_id` argument above is **software-layer enforcement** at the agent-graph layer, and it is **not deterministic for a regulated buyer**. The LLM constructs the tool-call arguments; nothing in the graph itself mechanically prevents the model from passing the wrong tenant value, and "we told the model to pass the right one" is not a control a CISO or FSI auditor will accept. Deterministic isolation has to live in lower-trust substrates that do not depend on model behaviour: row-level security in the database, per-tenant partitioning in the queue, a per-tenant API contract on the payments system, and — at the platform level — per-tenant scoping across the five cross-tenant surfaces (retriever, cache, checkpointer, observability, model). Foundations names the gap; Patterns §2.7 (governance Category 1 — cross-tenant aggregation) frames it as a governance failure mode; Production §3.2 (Cross-Tenant Isolation: The Five Surfaces) gives the full mechanics, named-component mitigations, and audit-evidence patterns. Readers who want to jump ahead — particularly FSI and Healthcare technical-discovery readers — should go directly there.

### §1.4.16.3 The graph

Two nodes (`agent` and `tools`) plus a HITL `approve_refund` node that fires when the refund amount exceeds the threshold. The graph is wired with `add_conditional_edges` for the LLM-decides routing and `add_edge` for fixed transitions.

```python
from langgraph.types import interrupt, Command
from langchain_core.messages import ToolMessage

REFUND_THRESHOLD = 500.0

def agent_node(state: SupportAgentState):
    """Call the LLM with the current conversation; emit any tool calls."""
    response = chat_model.invoke(state["messages"])
    return {"messages": [response]}

def tools_node(state: SupportAgentState):
    """Execute each pending tool call; return tool messages."""
    last = state["messages"][-1]
    out = []
    for call in last.tool_calls:
        # Inject the tenant from state, not from the LLM's tool args.
        call_args = {**call["args"], "tenant_id": state["tenant_id"]}
        if call["name"] == "place_refund" and call_args["amount"] > REFUND_THRESHOLD:
            return {"pending_refund": call_args}  # Route to approve_refund.
        result = TOOL_REGISTRY[call["name"]].invoke(call_args)
        out.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
    return {"messages": out}

def approve_refund_node(state: SupportAgentState):
    """HITL: pause and surface the refund for human approval."""
    decision = interrupt({
        "type": "approve_refund",
        "tenant_id": state["tenant_id"],
        **state["pending_refund"],
    })
    return {"human_approved": decision == "approve"}

def execute_refund_node(state: SupportAgentState):
    """Execute the refund if approved; otherwise produce a denial message."""
    refund = state["pending_refund"]
    if state["human_approved"]:
        result = _payments.refund(**refund)
        msg = f"Refund of ${refund['amount']} placed."
    else:
        result = {"status": "declined"}
        msg = "Refund declined by reviewer."
    return {
        "messages": [ToolMessage(content=msg, tool_call_id="refund-hitl")],
        "pending_refund": None,
        "human_approved": None,
    }

def route_after_tools(state: SupportAgentState):
    if state.get("pending_refund"):
        return "approve_refund"
    return "agent"

def route_after_agent(state: SupportAgentState):
    last = state["messages"][-1]
    if last.tool_calls:
        return "tools"
    return END

builder = StateGraph(SupportAgentState)
builder.add_node("agent",          agent_node)
builder.add_node("tools",          tools_node)
builder.add_node("approve_refund", approve_refund_node)
builder.add_node("execute_refund", execute_refund_node)

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", route_after_agent)
builder.add_conditional_edges("tools", route_after_tools)
builder.add_edge("approve_refund", "execute_refund")
builder.add_edge("execute_refund", "agent")
```

> **CONCEPT BOX (PM-track).** Four nodes. The agent node calls the LLM. The tools node executes any tool calls the LLM emitted; if a refund-over-threshold is requested, the tools node routes to `approve_refund` instead of executing. The `approve_refund` node pauses and surfaces the refund to a human; when the human resumes with "approve" or "deny," the `execute_refund` node either places the refund or returns a denial message. Then control returns to the agent node for the next conversational turn. This is the HITL placement pattern; refund-over-threshold is the canonical example.

### §1.4.16.4 Compile and run

The compile call wires in the production-default `PostgresSaver` checkpointer and the matching `PostgresStore` for cross-thread memory.

```python
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.store.postgres.aio import AsyncPostgresStore

async def build_app():
    saver = AsyncPostgresSaver.from_conn_string(POSTGRES_URL)
    store = AsyncPostgresStore.from_conn_string(POSTGRES_URL)
    await saver.setup()
    await store.setup()
    return builder.compile(checkpointer=saver, store=store)

async def main():
    app = await build_app()

    config = {"configurable": {
        "thread_id": "alice-2026-05-24",
        "tenant_id": "klarna-eu",
        "user_id":   "alice@example.com",
    }}

    # Initial turn.
    async for chunk in app.astream(
        {"messages": [{"role": "user", "content": "Refund $750 on order #1234."}],
         "tenant_id": "klarna-eu"},
        config=config,
        stream_mode="updates",
    ):
        print(chunk)

    # Agent hit interrupt() in approve_refund_node. Human reviews;
    # caller resumes with the decision.
    async for chunk in app.astream(
        Command(resume="approve"),
        config=config,
        stream_mode="updates",
    ):
        print(chunk)
```

> **CONCEPT BOX (PM-track).** Three things happen in this code: (1) the agent is given the user's refund request; (2) the agent's tools node detects that the requested refund is above the threshold and routes to `approve_refund`, which calls `interrupt()` and pauses the graph; (3) the caller — having shown the refund to a human and gotten "approve" — resumes the graph with `Command(resume="approve")`, which causes the `execute_refund` node to place the refund. From the user's perspective, there was a pause between asking for the refund and seeing it placed. From the agent runtime's perspective, that pause is durable — the state is persisted in Postgres at every node transition, and if the runtime crashes during the pause, the next time the same `thread_id` is invoked the graph resumes from the same checkpoint.

### §1.4.16.5 The annotated state graph for this example

The same three-frame progressive disclosure from §1.4.15 applied to the §1.4.16 worked example. This is a small-multiples pair with §1.4.15 — same widths, same conventions; what differs is the worked-example specifics (refund threshold, two refund-handling nodes, per-tenant memory).

**Frame 1 — the bare ReAct loop with the four nodes from §1.4.16.3.** Two flow nodes (agent, tools) plus two refund-handling nodes wired downstream. The HITL is NOT yet drawn — Frame 2 adds it.

```
+----------------------------------------------------------------------+
| THREAD: thread_id + tenant_id                   [CKP at every edge]  |
|                                                                      |
|   [user input]                                                       |
|        |                                                             |
|        v                                                             |
|   +--> [agent (LLM)] [OBS] --END--> [return]                         |
|   |        |                          ^                              |
|   |        | call?                    | refund <= $500 (inline)      |
|   |        v                          |                              |
|   |    [tools node] [OBS] [POL] -----+                               |
|   |        |                                                         |
|   +=no====+                                                          |
|                                                                      |
+----------------------------------------------------------------------+
```

*Frame 1: bare ReAct loop with refund-handling wired downstream. HITL deferred to Frame 2.*

**Frame 2 — add the HITL branch (the delta from §1.4.15 Frame 2).** When refund > $500, tools node routes to `approve_refund` (which calls `interrupt()`), then `execute_refund` after resume. Dashed arrows mark the human-mediated edge — the graph may sleep for hours waiting for human approval.

```
+----------------------------------------------------------------------+
| THREAD: thread_id + tenant_id                   [CKP at every edge]  |
|                                                                      |
|   [user input]                                                       |
|        |                                                             |
|        v                                                             |
|   +--> [agent (LLM)] [OBS] --END--> [return] <-------+               |
|   |        |                                          .              |
|   |        | call?                                    .              |
|   |        v                                          .              |
|   |    [tools node] [OBS] [POL]                       .              |
|   |        |       |                                  .              |
|   +=no===  |       +-- refund > $500 -->              .              |
|            |       [approve_refund / interrupt() / [HITL]]           |
|            |            .                                            |
|            |            . resume('approve')                          |
|            |            v                                            |
|            |       [execute_refund] [POL] ..............             |
|                                                                      |
+----------------------------------------------------------------------+
```

*Frame 2: HITL branch with execute_refund after resume. The graph may sleep for hours.*

**Frame 3 — overlay cross-cutting services (side-box, not in the flow).** Identical convention to §1.4.15 Frame 3 — every production refinement (signed action chain, model-swap canary, FGA-bound approver identity, cross-region trace partitioning) adds to this base without changing the graph shape.

```
+----------------------------------+   +------------------------------+
| GRAPH (Frames 1+2)               |   | RUNTIME SERVICES             |
|                                  |   |                              |
|  agent <==> tools                |   |  PostgresSaver  state [CKP]  |
|              <==> approve        |   |  PostgresStore  per-tenant   |
|                    <==>          |   |  LangSmith      spans [OBS]  |
|                  execute_refund  |   |  Guardrails AI  policy [POL] |
+----------------------------------+   +------------------------------+
```

*Frame 3: same side-box convention as §1.4.15; production refinements layer on without changing the graph shape.*

This is what "minimum viable" looks like. Read in order, each frame adds one concept against §1.4.15's pair-frame, so the only thing the reader must hold in working memory is the delta. Every production refinement — per-tenant cache key namespacing, signed action chain, model-swap canary, FGA-bound approver identity, cross-region trace partitioning — adds to this base. The shape stays the same.

### §1.4.16.6 What's still missing for production

The agent above is a credible Day-1 prototype. It is not a Day-30 production system. The gaps you should be able to name:

1. **The tools node injects `tenant_id` from state, but nothing in the runtime guarantees the tenant in state is the authenticated tenant.** Per-tenant binding must be enforced at the **Identity Provider (IDP)** boundary (OIDC token scope, SPIFFE SVID) and re-asserted at the Postgres row-level-security layer. **What this does not give you is cryptographic proof, after the fact, that the tenant assertion was honored.** An auditor reviewing a six-month-old refund cannot today verify that the `tenant_id` in state matched the authenticated user at the moment of action. The standards pointing at this gap are **RATS** (RFC 9334, Remote Attestation Procedures) and **EAT** (Entity Attestation Tokens, RFC 9711); the hardware-enforced implementation pattern is what OPAQUE Systems ships using confidential computing. Foundations §1.10 names the gap. Production §3.4 walks the implementation.
2. **The HITL approval is unauthenticated.** `Command(resume="approve")` accepts any string. Production requires a signed approval token bound to an authenticated CX Ops operator identity with FGA-authorized approval rights for this refund amount.
3. **No action provenance.** Six months from now, the trail consists of LangSmith spans plus Postgres rows. Neither is signed. Production requires the cryptographic action chain from §1.9.7. 
4. **No prompt-injection mitigation at retrieval-from-conversation-history.** A malicious tool result (or a malicious user message in an earlier turn) could redirect the agent. Patterns covers the shift-left / shift-right / tool-call guard pattern.
5. **No model-swap protocol.** When Anthropic deprecates Claude 4.7 and the team upgrades to Claude 5.0, the agent's behavior may change in ways that require **Model Risk Management (MRM)** re-validation. Production §3.13 walks the Day-30 Claude version-swap operational scenario.
6. **No tool-swap or MCP-server-swap protocol.** When the team upgrades an MCP server image, swaps a tool implementation, or repoints to a new retrieval index, nothing in the runtime proves the new artifact is the one the security team approved. The framing standards are SLSA, Sigstore, and the emerging RATS / EAT runtime-attestation chain. Production §3.5 walks the swap-and-attest pattern.
7. **No agent-identity-swap protocol.** When an A2A peer agent rotates its identity key, or a new agent is introduced into the network, the local agent has no cryptographic proof that the new peer is the one the policy intended. Foundations §1.9.2 names the gap; Patterns §2.4 walks the SPIFFE / Entra Agent ID / A2A handshake.
8. **No imposter detection at the MCP boundary.** A malicious or compromised MCP server can respond to legitimate clients with poisoned tool results. The runtime cannot, today, prove that the responding server is the one whose SBOM and supply-chain attestation matches what was approved. RATS-style remote attestation closes this gap; production-grade implementations require hardware-enforced TEEs.

Foundations introduces these gaps as a category. Patterns covers the integration patterns; Production §3.4 and §3.5 walk the evidence chains. The connective thread across all of them: **policy is only as strong as the proof that it was enforced**, and proof requires either (a) trusted operators auditing logs after the fact, or (b) hardware-enforced attestation at the moment of action.

---

## §1.5 State, memory, and persistence

The single most-confused area of vendor documentation is the relationship between **state, memory, and persistence**. The clean mental model is **three nested scopes** of state, each with a different lifetime, a different retrieval pattern, and a different production failure mode.

### §1.5.1 The three-scope state model

```
+----------------------------------------------------------------------+
| SCOPE 3 -- Long-term memory (BaseStore / vector / Memory Bank)       |
|   Persists ACROSS conversations / threads / users                    |
|   Examples: facts about the user, learned skills, episodic memories  |
|                                                                      |
|   +--------------------------------------------------------------+   |
|   | SCOPE 2 -- Conversation state (thread / checkpointer)        |   |
|   |   Persists ACROSS turns within ONE conversation              |   |
|   |   Examples: message history, tool-call history, current plan |   |
|   |                                                              |   |
|   |   +------------------------------------------------------+   |   |
|   |   | SCOPE 1 -- Step state (scratchpad / intra-step)      |   |   |
|   |   |   Persists WITHIN one agent step                     |   |   |
|   |   |   Examples: chain-of-thought, partial tool results   |   |   |
|   |   +------------------------------------------------------+   |   |
|   +--------------------------------------------------------------+   |
+----------------------------------------------------------------------+
```
### §1.5.2 Scope 1 — Step state (scratchpad)

The intermediate reasoning, partial tool results, and scratch-space the LLM uses **within a single agent step**. In a ReAct agent, this is the "Thought" trace between observations. In a Plan-and-Execute agent, this is the executor's working notes for the current step.

**Persistence:** None by default. Step state is in-memory and gone after the step ends.

**LangGraph mapping:** Lives in the `state` dict passed between nodes. `messages` is the canonical scratchpad slot; custom keys can hold structured intermediate state (e.g., `partial_plan`, `current_tool_args`).

### §1.5.3 Scope 2 — Conversation state (the thread)

Everything that persists across turns of a **single conversation**. Identified by a `thread_id`. Every time the same `thread_id` is passed in, the agent resumes from where it left off.

**Persistence:** The **checkpointer**. On every node transition, `compile(checkpointer=...)` writes the full state to durable storage, keyed by `thread_id`. On the next call with the same `thread_id`, state is loaded.

**Production checkpointer choices (from the §1.2 stack):**

- **`PostgresSaver` / `AsyncPostgresSaver`** — production default. LangGraph deploy guide commits to this as the production requirement. `[vendor-public]`
- **`RedisSaver`** — established #2 for sub-millisecond memory.
- **`MemorySaver` / `SqliteSaver`** — dev-only, explicitly "not for production." `[vendor-public]`
- **`MongoDBSaver`** — community-maintained.
- **DynamoDB checkpointer** — AWS first-class.
- **CosmosDB checkpointer** — Azure first-class.

**When checkpoints fire:** after every node transition. Each transition writes a **checkpoint** — a versioned snapshot. Resuming from a `thread_id` loads the latest checkpoint and continues. Time-travel debugging works by loading an earlier checkpoint and re-running from there.

### §1.5.4 Scope 3 — Long-term memory (cross-thread)

State that persists **across conversations / sessions / users**. Examples: facts the agent learned about the user ("Alice prefers concise responses"), summaries of past interactions ("3 conversations about refund policy in the last 30 days"), learned skills, semantic knowledge accumulated over time.

**Persistence:** The `BaseStore` interface. Stores are passed into `compile(store=...)` and accessible from every node via the `RunnableConfig`.

**`BaseStore` implementations:**

- **`InMemoryStore`** — dev / testing.
- **`PostgresStore`** — production default; co-located with the Postgres checkpointer.
- **`RedisStore`** — production alternative with native vector search.

**The distinction that confuses everyone:** the thread checkpointer covers state *within* a thread (one conversation). The `BaseStore` covers state *across* threads (multiple conversations, possibly the same user). Both are persistent; they answer different questions.

### §1.5.5 Memory taxonomy (cognitive-science vocabulary)

Vendor documentation increasingly uses cognitive-science vocabulary. The mapping worth knowing:

| Cognitive term | Working definition | LangGraph implementation |
|---|---|---|
| **Working memory** | What's in the context window right now | The `messages` list inside the current state |
| **Episodic memory** | Memories of specific past events / conversations | Stored summaries of past threads in `BaseStore` |
| **Semantic memory** | Factual knowledge that doesn't have a specific event origin | Vector store of facts; structured KV in `BaseStore` |
| **Procedural memory** | How to do things; learned skills | Stored prompt templates; learned tool definitions |

The **MemGPT / Letta** lineage (Packer et al., 2023, arXiv:2310.08560, UC Berkeley RISELab) formalized **memory-hierarchy management** as an agent capability: the agent itself edits its memory, pages out to long-term, pulls in from long-term to working. `[benchmark]` Production adoption of full MemGPT is rare; the conceptual influence — "agents manage their own memory" — is everywhere.

> **Where to read more on agent memory.** The space of "agent memory" projects — Letta (MemGPT lineage), Mem0, Cognee, Zep, vector-backed retrieval memories, graph-memory approaches, and hybrid systems — is one of the most active corners of the 2026 agent landscape, and a reasonable reader question at this point is "why are there so many startups working on this, and which one fits where?" Foundations gives you the LangGraph-native primitives (checkpointer + `BaseStore`) and the cognitive-science vocabulary. **The full landscape — definitions of working / short-term / long-term / episodic / semantic / procedural memory; the major architectures (paged virtual context, vector-backed retrieval, graph memory, hybrids); 8–10 named projects (Letta, Mem0, Cognee, Zep, Pinecone, Redis, pgvector + LangMem, OpenAI Memory, Anthropic Memory Tool); and when each fits which deployment shape — lives in Patterns §2.3.7 "Agent Memory — The Landscape."** Forward-reference there if the question is pressing; otherwise the LangGraph primitives above are sufficient for Foundations.

### §1.5.6 Why agents complicate state vs traditional apps

A traditional web app has session state and database state. The session is short-lived (often ≤30 minutes). The database is long-lived. The two are clearly separated.

Agents complicate this in three ways:

1. **The "session" can last hours or days.** A long-running deep-research agent may be paused at HITL for 4 hours waiting for human approval. The session-state-equivalent (the thread checkpointer) must persist that long without loss.
2. **Step state and conversation state blur.** The ReAct "thought" trace lives in messages, which is also the conversation history. Engineers must decide what to keep and what to summarize.
3. **Long-term memory across users is a multi-tenancy problem.** If the agent learns "Alice prefers concise responses," that fact must not leak into Bob's conversation. The `BaseStore` must enforce per-tenant or per-user isolation, and most teams underestimate the difficulty of doing this correctly.

The cross-tenant isolation problem is large enough that Patterns covers it as a dedicated governance category (§2.7.2 Category 1) and Production dedicates a full chapter to it (§3.2, "Cross-Tenant Isolation: The Five Surfaces"). Foundations needs only the conceptual flag.

> **CONCEPT BOX (PM-track).** When a customer says *"the agent forgets things between sessions,"* the question is whether they have a long-term memory store at all. When they say *"the agent forgets things mid-conversation,"* the question is whether they're using a checkpointer (and whether the context window is being truncated). These are different problems with different solutions. The vocabulary that wins the customer's respect: "Are you using `BaseStore` for cross-thread memory, or are you relying on the thread checkpointer alone?"

```python
# A production-shaped agent with both scopes wired up.
from langgraph.checkpoint.postgres import AsyncPostgresSaver
from langgraph.store.postgres import AsyncPostgresStore

graph = builder.compile(
    checkpointer=AsyncPostgresSaver(conn_pool),  # Scope 2: thread state
    store=AsyncPostgresStore(conn_pool),          # Scope 3: cross-thread memory
)

# Resume a specific user's conversation. Both scopes are loaded automatically.
result = await graph.ainvoke(
    {"messages": [{"role": "user", "content": "What did we decide last week?"}]},
    config={"configurable": {
        "thread_id": "alice-2026-05-24",
        "user_id":   "alice@example.com",   # used by BaseStore lookups
        "tenant_id": "acme-corp",            # per-tenant isolation key
    }},
)
```

### §1.5.7 Vector DBs as memory substrate

The vector DB tier (§1.2 tier 9) is where long-term **semantic memory** lives in most production agents. Foundations needs the vocabulary — depth on rerankers, hybrid retrieval, ColBERT, BM25 fusion, etc. lives in Patterns.

- **pgvector** — Postgres extension. Production default in LangGraph because it co-locates with the checkpointer at tier 5. `[vendor-public]`
- **Pinecone, Weaviate, Qdrant, Milvus** — managed / dedicated vector DBs. Used above ~10–50M vectors.
- **Elasticsearch / OpenSearch** — hybrid BM25 + kNN. Used in SOC / log-analytics agents.
- **Redis, MongoDB Atlas Vector Search, Azure AI Search, Snowflake Cortex Search, Databricks Vector Search** — emerging in-platform options.
- **Turbopuffer, Vespa** — 2026 entrants worth tracking.

---

## §1.6 Tool ecosystems and protocols

This is the section where Foundations corrects a structural error that beginner readers often inherit from older vendor blog posts. **MCP, A2A, and AGP are not peers.** They are three layers in a stack. Foundations teaches the stack as canonical.

### §1.6.1 The three-layer protocol stack

```
+--------------------------------------------------------------------+
| A2A -- Agent2Agent Protocol                                        |
|   (collaboration / handoff)                                        |
|   Donated to LF by Google, June 2025                               |
|   150+ orgs supporting (May 2026)                                  |
|   "Agents talk to agents"                                          |
+--------------------------------------------------------------------+
                                |
+--------------------------------------------------------------------+
| MCP -- Model Context Protocol                                      |
|   (capability invocation)                                          |
|   JSON-RPC; resources, tools, prompts                              |
|   Donated to LF AAIF by Anthropic, Dec 2025                        |
|   "Agents call tools"                                              |
+--------------------------------------------------------------------+
                                |
+--------------------------------------------------------------------+
| AGP / AGNTCY -- Agent Gateway Protocol                             |
|   (transport / routing / ID)                                       |
|   Donated to LF by Cisco/Outshift, July 2025                       |
|   SLIM messaging, BGP-inspired routing                             |
|   "Agents over the network"                                        |
+--------------------------------------------------------------------+
```

*Three-layer stack: A2A above MCP above AGP. Each layer has a different problem class and vendor lineage.*

The intuition: **MCP defines what messages mean. A2A defines how agents collaborate using those messages. AGP defines how the messages get from one agent to another across a network with policy, identity, and routing enforced.** Each layer has a different problem class and a different vendor lineage.

**Reading order vs. diagram order.** The diagram above stacks A2A on top of MCP on top of AGP because that is the *runtime call direction* — collaboration uses messages, messages traverse the network. The narrative order below is MCP → A2A → AGP because that is the *adoption order* — MCP is widely deployed in 2026, A2A is GA but still ramping, AGP is the youngest layer.

**AGP adoption posture (May 2026).** AGP is the newest of the three protocols and the least widely adopted. The reference implementation lives in the **AGNTCY** project; production deployments at scale are not yet a 2026 phenomenon. The reason to teach AGP in Foundations anyway: it is the *only* protocol in the stack that explicitly addresses policy enforcement and identity-bound routing at the network layer, which is where the trust gap lands for any agent network that crosses tenant or organizational boundaries. Readers should treat AGP as the *standards-defining* answer to a real gap, even while production-grade deployments are still rare.

**BGP-inspired routing.** BGP (Border Gateway Protocol) is how the public internet's autonomous systems negotiate routes between organizations. AGP borrows the conceptual primitive — agent networks need to negotiate routes between organizational trust domains — without inheriting BGP's hijack-prone trust model. AGP's contribution is binding the route advertisement to identity and policy; SPIFFE / SPIRE handles the identity substrate; the emerging RATS / EAT attestation chain handles the verifiability that a policy claim is honored.

### §1.6.2 MCP — Model Context Protocol (the middle layer, most-used in 2026)

**What it is.** A JSON-RPC protocol that lets an LLM client invoke capabilities exposed by an MCP server. Introduced by Anthropic in November 2024; donated to the **Linux Foundation Agentic AI Foundation (LF AAIF)** in December 2025 alongside `goose` and `AGENTS.md`. `[vendor-public]`

**Why it exists.** Before MCP, every framework defined tools in its own API — LangChain had `@tool`, LlamaIndex had `FunctionTool`, OpenAI used its function-calling JSON, Anthropic used its tool-use JSON. The same tool had to be re-implemented in every framework. MCP unifies the protocol: a tool written once works with any agent runtime that speaks MCP — Claude Desktop, ChatGPT, Cursor, Claude Code, any LangGraph agent via the MCP client.

**The three MCP primitive types.**

- **Tools** — callable functions with structured JSON inputs and outputs. Examples: `search_documents`, `send_email`, `place_refund`.
- **Resources** — readable data sources (files, DB rows, URLs).
- **Prompts** — pre-templated prompts users (or LLMs) can invoke.

**MCP roles.**

- **MCP server** — exposes tools, resources, prompts. Runs locally over stdio transport or remotely over Streamable HTTP transport (2025-11-25 spec).
- **MCP client** — embedded in the agent runtime; connects to MCP servers and invokes them.
- **MCP host** — the user-facing app (Claude Desktop, Cursor) that mediates between the user and the clients.

**Recent additions (2025-11-25 spec).**

- **MCP Authorization** — OAuth 2.1 + Dynamic Client Registration + RFC 9728 metadata. The protocol-level answer to MCP-tool identity. Ratified Q1 2026; production-deployment evidence still thin as of May 2026, so flag this as `[evidence-zero]` for any procurement claim. `[vendor-public]`
- **MCP elicitation** — server requests interactive input from the user mid-tool-call. Q4 2025.
- **MCP sampling** — server requests an LLM call from the client. Lets servers be LLM-aware without bundling their own model.

**Common-confusion headoffs.**

- **MCP is not Anthropic-owned.** Donated to LF AAIF in December 2025. Vendor-neutral.
- **`langchain-mcp-adapters` is not MCP.** It is one adapter that translates between LangChain's `ToolMessage` and MCP's `ToolMessage`. The MCP SDKs (Python, TypeScript, Java, Go, C#) are the substrate; `langchain-mcp-adapters` is a thin wrapper. Don't name the wrapper as if it were the protocol.
- **The three MCP roles, with one concrete example.** Take **Claude Desktop using the GitHub MCP server**:
  - **Host** = Claude Desktop (the application the human interacts with; manages MCP client lifecycle).
  - **Client** = the embedded MCP client inside Claude Desktop (opens the connection, sends `tools/call`, handles responses).
  - **Server** = the GitHub MCP server (exposes tools like `list_repositories`; runs locally or remotely; responds to client calls).
  - **Enterprise analog** — in an agent runtime: the **host** is the agent process (e.g., a LangGraph service on Kubernetes); the **client** is the MCP SDK inside the agent's tool-calling layer; the **server** is whatever exposes the customer-side capability (a database-query MCP server, a ticketing MCP server, etc.).
- **MCP server ≠ MCP client.** Server exposes; client invokes. The agent runtime is the client; the tool surface is the server.

### §1.6.3 A2A — Agent2Agent (the top layer, agent collaboration)

**What it is.** Agent2Agent (A2A), an open protocol for agentic AI interoperability — letting agents discover one another, exchange typed messages securely, and collaborate across systems and organizations. Launched by Google in April 2025; released open-source under Apache 2.0; donated to the Linux Foundation in June 2025. `[vendor-public]`

**Why it sits above MCP.** MCP is "agent calls tool." A2A is "agent talks to agent." If one agent (say, a customer-service agent) needs to delegate work to another agent (say, a fulfillment agent), A2A is the protocol. Conceptually: MCP is gRPC for agent-to-tool; A2A is HTTP-between-services for agent-to-agent.

**Adoption signal.** 150+ organizations supporting (May 2026). Integrations across Google, Microsoft, and AWS platforms. Production deployments are real but smaller than MCP's footprint. `[vendor-public]` `[architectural inference]`

**Where it overlaps with multi-agent frameworks.** Most multi-agent systems in production today use **in-framework** supervisor/worker primitives — LangGraph's supervisor, AutoGen's group chat, ADK's sub-agents. A2A is for **cross-framework, cross-organization** agent collaboration, where the agents you are collaborating with are not in your codebase. This is the harder problem and the slower-to-adopt layer.

### §1.6.4 AGP / AGNTCY — Agent Gateway Protocol (the bottom layer)

**What it is.** AGNTCY ("agency") is a multi-component project from Cisco Outshift, donated to the **Linux Foundation in July 2025** with Cisco, Dell, Google Cloud, Oracle, and Red Hat as formative members. AGNTCY components include discovery, identity, messaging (SLIM — Secure Low-latency Interactive Messaging), and observability. **Agent Gateway Protocol (AGP)** is the BGP-inspired routing piece — agents publish capabilities to gateways; clients send Intent payloads; gateways route. `[vendor-public]`

**Why it sits below MCP.** MCP defines what messages mean; AGP defines how they get from agent to agent across a network with policy, identity, and routing enforced. This is the "Internet of Agents" layer — explicitly named by AGNTCY framing.

**Note for Foundations.** AGP is the youngest layer of the stack. Adoption is real but smaller than MCP or A2A as of May 2026. Teach the name; teach the layer; do not oversell production prevalence. Mark any claim of production-scale AGP deployment as `[architectural inference]` until evidence surfaces. `[vendor-public]`

### §1.6.5 Managed MCP planes

In production, raw MCP rarely reaches the agent runtime unfiltered. A **managed MCP plane** sits between the agent and the MCP servers, enforcing policy, observability, identity, and rate limits.

The named planes worth recognizing in 2026 (per the §1.2 tier-3 list):

- **AWS Bedrock AgentCore Gateway**
- **Azure Foundry MCP Gateway**
- **GCP Vertex Agent Gateway**
- **Cloudflare AI Gateway**
- **Kong AI Gateway**
- **Apigee + MCP**
- **MuleSoft**

When a customer says "we expose tools via a gateway," they usually mean one of these. The gateway is where MCP signature checking, SLSA attestations, and supply-chain policy enforcement happen.

### §1.6.6 Other named protocols (vocabulary completeness)

For the glossary; not for depth in Foundations.

- **IBM ACP** (Agent Communication Protocol) — IBM-originated; overlaps conceptually with A2A.
- **Zed ACP** — agent-coding-protocol from Zed Industries.
- **agentgateway** — a separate Linux Foundation project for agent-traffic gateway concerns.

The Foundations stance: **A2A above MCP above AGP is the canonical three-layer mental model.** Other protocols are tracked for vocabulary; depth lives in Patterns and Production.

> **CONCEPT BOX (PM-track).** Three layers, three problems. Top (A2A): how do agents from different teams or different companies talk to each other? Middle (MCP): how does my agent reliably call my tools, regardless of which framework wrote them? Bottom (AGP): how do agent messages flow over a network with policy and identity? Most 2026 production conversations are at the middle layer. A2A and AGP are real but earlier in the adoption curve.

---

## §1.7 Multi-agent patterns

This section names the seven canonical LangGraph topologies at conceptual depth. Patterns will carry the deep mechanics, the decision tree, the per-topology state graph, and the customer-deployment anchors. Foundations needs you to know the names so you can recognize them in customer architectures.

### §1.7.1 The seven canonical topologies

This Field Guide commits to seven topologies as the canonical 2026 catalog, per the LangGraph blog and docs. `[vendor-public]`

**(1) ReAct — single-agent reason+act.** One agent node, one tools node, looping until the LLM stops calling tools. Implemented by `create_react_agent`. Fits single-domain tasks where one LLM with the right tools can handle the turn-by-turn loop. Klarna's modal pattern, most "single-agent + tools + memory" customer-support agents. `[customer-produced-evidence]`

**(2) ReAct + Reflexion — self-critique.** A ReAct loop wrapped with a critic LLM that reviews the attempt and feeds verbal critique back as additional context for retry. `langgraph-reflection` harness. Fits tasks where retry-with-critique beats single-pass — code generation, complex Q&A, multi-step reasoning where the first attempt is often wrong. `[benchmark]`

**(3) Plan-and-Execute — planner + executor + replanner.** A planner LLM writes a multi-step plan; an executor LLM (sometimes itself a ReAct agent) executes each step; a replanner LLM re-evaluates after each step. Fits long-horizon research, multi-document analysis, complex investigations where turn-by-turn ReAct would grow context unmanageably. **The `deepagents` harness is a Plan-and-Execute implementation.** Plan-and-Execute is the canonical FSI topology — Captide, Morningstar Mo. `[customer-produced-evidence]` `[architectural inference]`

**(4) Supervisor — one supervisor, many workers.** A supervisor LLM routes incoming requests to one of N worker agents, each specialized for a domain. Workers report back; supervisor decides next step. `langgraph-supervisor-py` harness. Fits tasks where work decomposes cleanly into specialist domains — code review (linter agent + test-writer + commit-message), customer-service routing (refund + escalation + FAQ). Real deployments: **Uber Validator + AutoCover; AppFolio Realm-X; Klarna's routed multi-agent shape.** `[customer-produced-evidence]`

**(5) Hierarchical — supervisor of supervisors.** Supervisor at the top; each worker is itself a supervisor with its own sub-workers. Recursion. Fits very large problem spaces where a flat supervisor would have too many workers (10+) and routing quality degrades. Real deployments: **LinkedIn Hiring Assistant (billion-member candidate graph, multi-level routing); Replit Agent (editor / manager swarm under a top-level coordinator).** `[customer-produced-evidence]`

**(6) Agentic RAG — retrieval-as-tool with self-correction.** A ReAct-shaped agent where retrieval is a tool the LLM chooses to call. After each retrieval, the LLM critiques the documents and may re-query, fall back to a different index, or escalate to HITL. Fits knowledge-intensive Q&A where a single retrieval doesn't reliably surface the right documents — SOC alert triage, legal research, medical literature review. Real deployment: **Elastic Security AI Assistant.** `[customer-produced-evidence]`

**(7) Network (Swarm) — peer-to-peer agents.** Peer agents communicate without a central supervisor. Each agent decides when to hand off to which peer. `langgraph-swarm-py` harness. Fits tasks where central coordination is the bottleneck and peers can reason about who should own each step locally. **Note the renaming:** the LangGraph docs renamed this from "Multi-Agent Collaboration" to **Network (Swarm)** to align with community vocabulary. If you see "Multi-Agent Collaboration" in older docs, this is the same pattern. Named-customer evidence at scale is thinner for pure Network/Swarm than for Supervisor or Hierarchical; the swarm pattern often shows up **inside** a hierarchical system rather than as the top-level topology. `[architectural inference]`

### §1.7.2 The intellectual genealogy (one paragraph for the curious)

The seven topologies descend from five research papers that you should be able to name in passing. **ReAct** (Yao et al., ICLR 2023, arXiv:2210.03629) established the Thought → Action → Observation loop — every LangGraph topology that does not say "Plan-and-Execute" inherits ReAct's interleaving. **Reflexion** (Shinn et al., NeurIPS 2023, arXiv:2303.11366) gives the self-critique loop. **Plan-and-Execute** descends from Wang et al. 2023 ("Plan-and-Solve Prompting," ACL 2023, arXiv:2305.04091) and the LangChain blog formalization. **Tree of Thoughts** (Yao et al., NeurIPS 2023, arXiv:2305.10601) generalized chain-of-thought to a search tree — less commonly named in production agents but the conceptual ancestor of best-of-N sampling. **Toolformer** (Schick et al., NeurIPS 2023, arXiv:2302.04761) is the intellectual ancestor of function calling. All `[benchmark]`.

You will encounter these papers in conversations about agent reliability and in customer engineering blogs. Knowing the names is enough at Foundations depth.

### §1.7.3 The emerging "topology 8"

The community has begun treating `deepagents` (LangChain's harness for deep-research agents — sub-agent spawning, virtual filesystem scratchpads, TODO-list state, planning loops) as **graduating to topology 8**. It is structurally a Plan-and-Execute implementation but with enough additional opinions (filesystem-as-state, TODO-list-as-state, sub-agent spawning) that some community voices argue for its own category. This is **in motion as of May 2026**. The seven-topology catalog is canonical; `deepagents` as topology 8 is honest community signal but not yet locked. `[architectural inference]` `[vendor-public]`

### §1.7.4 Composition reality

Real production systems are almost never one topology. The modal pattern in the customer corpus is **Supervisor wrapping ReAct wrapping Agentic RAG** — a supervisor routes among specialist workers, each worker is a ReAct agent, and one of the tools each worker can call is a self-correcting retrieval step. Foundations should teach that the topologies are **composable, not exclusive**. The decision tree (which Patterns will draw) is "which topology is the top-level shape, and what other topologies appear underneath?"

> **CONCEPT BOX (PM-track).** When a customer says *"we want a multi-agent system,"* ask: *"Does the work naturally decompose into roles?"* If yes, Supervisor or Hierarchical. If no, you probably want one agent with the right tools, not three agents arguing. The Anthropic engineering team's public guidance is "don't build multi-agent systems unless the work demands it" — this is the version of the guidance you should bring to discovery calls.

### §1.7.5 Pattern selection cheat sheet

| Pattern | Fits when... |
|---|---|
| ReAct | Single domain, turn-by-turn, fits in one LLM's context |
| ReAct + Reflexion | Retry-with-critique beats single-pass; tolerance for cost |
| Plan-and-Execute | Long-horizon; ReAct's context would grow unwieldy |
| Supervisor | Work decomposes into clean specialist domains |
| Hierarchical | Too many specialists for a flat supervisor; recursive structure |
| Agentic RAG | Knowledge-intensive Q&A where single-shot retrieval is unreliable |
| Network (Swarm) | Peer reasoning beats central routing; rare at top-level production scale |

---

## §1.8 Observability concepts

Agent observability is a different discipline from traditional application observability. Foundations does not need depth, but it does need the vocabulary and the "why."

**Observability weaknesses you should be able to name.** The 2026 default — LangSmith spans plus structured logs — is the right baseline, but it has three governance-relevant weaknesses an auditor will surface within two questions:

1. **Traces are not signed.** A trace is data the runtime *wrote*; nothing cryptographically binds the trace to the workload that produced it. An operator with edit access can revise history. The framing standards are RATS and EAT; the implementation pattern is hardware-enforced attestation of the trace producer.
2. **Trace storage is mutable.** Most observability SaaS backends are append-only by convention, not by cryptographic construction. Production §3.4 walks the immutable-trace pattern using customer-side hash-chained storage.
3. **Personally Identifiable Information (PII) in traces is not policy-bound.** Spans frequently capture LLM inputs and tool-call arguments — i.e., the regulated data the agent is acting on. Without a policy layer that redacts at trace-emit time, the observability platform becomes a parallel data store with weaker governance than the primary one. The DLP-at-egress pattern (§1.2.3) is the standards-named answer; cryptographic policy-bound traces are the hardware-enforced answer.

Foundations names these. Patterns and Production carry the closure pattern for each.

### §1.8.1 Why agents need different observability

Three reasons agent observability is its own thing:

1. **Non-determinism.** The same input produces different outputs across runs. Traditional Application Performance Monitoring (APM) assumes deterministic execution; agent runs are stochastic by design.
2. **Multi-step reasoning.** A single user request triggers many LLM calls, tool calls, and routing decisions. The "one request, one trace" abstraction in APM becomes a tree, not a line.
3. **Tool-call branching.** The path through the graph depends on what the LLM decides to do. You cannot pre-define the trace shape; it emerges from execution.

These three properties mean **eval, replay, and causal debugging matter more than aggregate metrics**. Agent observability platforms are eval-first; APM platforms are metrics-first.

### §1.8.2 The vocabulary

Borrowed from OpenTelemetry, extended for agent specifics:

- **Trace.** The full record of a single agent run, from user input to final output. May span minutes to hours for long-running agents.
- **Span.** A single sub-operation within a trace — an LLM call, a tool call, a graph node execution. Spans nest into parent-child trees.
- **Agent step.** One iteration of the agent loop. Usually one or more spans.
- **Tool call.** The act of the LLM invoking a tool, and the result coming back. Each tool call is typically its own span.
- **Run.** LangSmith-vocabulary equivalent of "trace."

### §1.8.3 The platforms

You need to know the names. Depth lives in Patterns.

- **LangSmith** — LangChain's first-party trace + eval platform. **Near-monopoly inside LangGraph deployments** because it auto-instruments `StateGraph` nodes with zero code change. SaaS (LangSmith Cloud on GCP us-central1 / europe-west4 / australia-southeast1, AWS us-east-2) or self-hosted. `[vendor-public]`
- **Langfuse** — OSS, self-hostable alternative. Strong in EU and data-residency-sensitive deployments. `[vendor-public]`
- **Arize AX** (commercial) and **Phoenix** (OSS) — from the same company, but **distinct products; don't conflate**. Strong on eval and structured drift detection. `[vendor-public]`
- **OpenTelemetry GenAI semantic conventions** and **OpenInference** (the Arize-submitted convention extension) — the protocol-layer answer. Lets any trace producer (LangGraph, LlamaIndex, CrewAI) send traces to any consumer (Splunk, Sentinel, Datadog) in a common schema. `[vendor-public]`
- **WhyLabs, Fiddler, Galileo Luna, Weights & Biases Weave, Helicone, Traceloop / OpenLLMetry, Datadog LLM Observability, New Relic AI Monitoring, Honeycomb Refinery, Dynatrace Davis AI, Comet Opik, Maxim AI** — other named platforms; Foundations names them only.

### §1.8.4 The HITL interrupt — observability-adjacent

A subset of agent observability is **human-in-the-loop**: the agent pauses, surfaces what it is about to do, and waits for human approval (or correction) before continuing.

In LangGraph: `interrupt()` is the primitive (§1.4.4). The agent calls `interrupt(value)` inside a node; execution pauses; the calling code receives the interrupt value; when ready, the calling code resumes with `Command(resume=...)`.

**Why HITL is observability-adjacent.** Both are about exposing what the agent did or is about to do. HITL is "expose and pause"; observability is "expose and record." Same underlying instrumentation.

> **CONCEPT BOX (PM-track).** When the customer asks *"how do we know the agent is doing the right thing?"* the answer has two pieces: **(1) observability** (trace every step, replay any run, eval against golden datasets) and **(2) HITL** (pause before consequential actions, get human approval). The first is "after the fact"; the second is "before the fact." Production agents need both.

---

## §1.9 Identity and the three agent identity problems

This is the single highest-payoff Foundations conversation, because customers and even some engineering teams conflate three identity problems that are genuinely different. Foundations lands the distinction at concept-only depth; Patterns §2.4 carries the named-product depth.

**Identity weaknesses you should be able to name.** Identity is the foundation that governance sits on — if the identity assertion is weak, every downstream governance claim is weak by the same amount. Three weaknesses an auditor will press on:

1. **The agent's own identity is often a long-lived JWT.** As of 2026, custom JWTs remain the modal pattern in production. Long-lived workload tokens are a known attack surface — they can be exfiltrated and replayed, and revocation lag is measured in hours. SPIFFE / SPIRE narrows the window with short-lived SVIDs; Entra Agent ID and Okta for AI Agents narrow it further. **The strongest closure is cryptographic binding of the identity to the workload via TEE attestation — the hardware-enforced signed-JWT pattern that OPAQUE Systems ships closes four governance gaps at once: (a) the signing key never leaves the confidential-computing TEE, blocking exfiltration even by a cloud-admin; (b) an imposter agent cannot mint a valid signed JWT because the signing operation requires a workload-bound TEE attestation that the imposter cannot produce; (c) the JWT's claim-set binds to a hash of the policy the workload was configured with, letting a receiver verify the policy is the approved one before sending sensitive data; (d) the signed JWT becomes the trust anchor for the rest of the action chain (§1.9.7), so revocation is enforced at the hardware-attestation layer, not at a policy-check layer.**
2. **Delegation chains are not cryptographically verifiable.** Problem 3 — *who is the agent acting on behalf of?* — is encoded today in OAuth scopes, OBO (on-behalf-of) tokens, or custom JWT claims. Six months after an action, an auditor cannot prove the delegation token was valid at the moment of action unless the runtime captured a signed receipt at that moment. RAR (Rich Authorization Requests) and signed transaction receipts are the framing standards.
3. **Identity claims do not bind to the data they unlocked.** An agent identity proves *who*; it does not prove *what data was accessed under that identity*. Closing this gap requires joining the identity assertion to the action chain (§1.9.7) and to the trace store. Governance §1.10 names the pattern.

**The governance tie-in.** Identity weaknesses propagate into every governance question downstream: data lineage, audit-replay, regulator-facing evidence, policy-enforcement claims. A governance layer that depends on a weak identity layer cannot make stronger claims than the identity layer supports. Foundations §1.10 introduces the governance section that ties these together.

### §1.9.1 The three problems

**Problem 1 — Who is the user?** Standard end-user authentication. OAuth, SSO, SAML, OIDC, JWT. This is a solved problem and has been since the 2000s.

**Problem 2 — Who is the workload / agent itself?** Agent identity. The agent process needs to authenticate to downstream services. SPIFFE / SPIRE, Kubernetes service accounts, workload identity federation, service-account JWT. **Entra Agent ID** (Microsoft, GA 2025) is the first-party Azure answer. This is mostly a solved problem in cloud-native environments since 2020.

**Problem 3 — Who is the agent acting on behalf of?** Delegated authority. The agent is authenticated as itself AND is acting in the name of a user. This is **the new identity problem of 2025–2026**, and it is what most agent-identity products are solving. `[vendor-public]`

Foundations readers need to see that **problem 3 is the new one**. Problem 1 has been solved since the 2000s. Problem 2 has been solved since the rise of zero-trust workload identity. Problem 3 is what 2025–2026 OAuth standards and IDP products are operationalizing.

### §1.9.2 Why agents complicate identity

A traditional API call has one identity: the user (via their session token). An agent action has up to three:

- The **user** who initiated the conversation.
- The **agent** that decided to take this action.
- The **downstream service** the action targets.

If a chargeback dispute lands in front of a regulator and the question is *"who authorized this refund?"*, the answer must trace through all three. Traditional **Identity and Access Management (IAM)** logs the user; an **agent-aware** system must log all three plus the agent's reasoning trace. This is the **action provenance** problem, and it is what Production's Audit-Evidence Cookbook addresses in depth.

### §1.9.3 OAuth-for-agents primitives (name-only at Foundations)

Six OAuth primitives that show up repeatedly in agent identity conversations. You need the vocabulary; Patterns carries the depth.

- **DPoP** (Demonstrating Proof-of-Possession, RFC 9449, Sept 2023). Binds an access token to a key pair the client holds. Every request is signed; stolen tokens cannot be replayed.
- **PAR** (Pushed Authorization Requests). The client pushes the auth request to the authorization server *before* redirect; prevents leaked-URL replay.
- **RAR** (Rich Authorization Requests). The authorization request carries a structured payload (transaction details, amounts, recipients) rather than just OAuth scopes — letting the user approve a *specific transaction*, not just "transfer:write."
- **CIBA** (Client-Initiated Backchannel Authentication). The agent's backend can initiate an auth request, and the user approves on a separate trusted device (mobile push). Decouples agent runtime from user device.
- **Step-Up authentication.** Escalate the auth strength for high-risk actions (e.g., require fresh MFA before a wire transfer).
- **Authorization Code Flow with PKCE for agents.** The most-deployed practical pattern in 2026 production. `[vendor-public]`

**A-Auth** (Dick Hardt's proposed agent-authorization framework) is the emerging proposal worth tracking — it extends OAuth's delegation primitives to the agent-acting-on-behalf-of-user case explicitly, with a richer transaction model than RAR alone. As of May 2026 it is a proposal, not a deployed standard; Patterns §2.4 carries the comparison with RAR / CIBA / step-up flows and the production-readiness assessment.
### §1.9.4 The first-party agent-identity products

Three first-party products to recognize, all 2025-launched:

- **Microsoft Entra Agent ID** (GA 2025). First-party agent identity in Azure; peer to Okta for AI Agents and Auth0 for AI Agents.
- **Okta for AI Agents** (Okta product, EA 2025).
- **Auth0 for AI Agents** (Auth0 / Okta product, EA 2025).

**Ping Identity** (PingOne, PingFederate, PingAuthorize, Ping AIC) is the fourth name worth mentioning; Patterns carries the comparison.

**Custom JWT** is still the modal pattern in production as of 2026 — across 18 named LangGraph deployments, custom JWT is the default identity substrate, with first-party agent-identity products arriving as the freshest greenfield. `[customer-produced-evidence]` `[architectural inference]`

**Hardware-enforced identity binding.** Whatever the identity substrate above the workload (custom JWT, SPIFFE SVID, Entra Agent ID), the binding from that identity to the *actual running workload* is a separate concern. The emerging standards that frame this binding are **EAR** (Entity Attestation Result), **RATS** (RFC 9334), and **EAT** (RFC 9711) — they specify how a workload cryptographically proves it is the one the security team approved, running in the environment the policy expected. Production §3.4 walks the integration pattern; Foundations §1.10 names the gap.

### §1.9.5 MCP Authorization spec

The protocol-level answer for **MCP-tool identity** specifically: **OAuth 2.1 + Dynamic Client Registration (DCR) + RFC 9728 metadata.** Ratified Q1 2026; production-deployment evidence is thin as of May 2026. Mark any procurement claim about MCP Authorization at scale as `[evidence-zero]` until customer evidence surfaces. `[vendor-public]`

### §1.9.6 Fine-Grained Authorization (FGA)

After identity (who you are) comes authorization (what you can do). For agents, role-based access control (RBAC) is insufficient. The question "can this agent, acting for this user, read this document section in this tenant?" requires **relationship-based access control (ReBAC)**.

The named products in the ReBAC / FGA category:

- **OpenFGA** (CNCF sandbox) — open-source, Auth0-originated, the canonical ReBAC reference.
- **Cedar / AWS Verified Permissions** — Amazon-authored policy language; ReBAC-capable.
- **Topaz** (Aserto) — combines RBAC + ABAC + ReBAC.
- **Okta FGA, Auth0 FGA** — managed FGA from Okta.
- **Permit.io, Oso, Styra** — other entrants in the category.

The conceptual move: **authorization decisions are derived from declarative relationships**, not from hardcoded checks in code. Decisions are explainable and auditable — every "deny" traces back to a relationship-graph query.

### §1.9.7 Action provenance — the cryptographic chain

The chain of evidence that lets a regulator ask, six months after an action, *"who decided to do this, who authorized it, what evidence supports it?"*

The components, named at Foundations and unpacked in Production §3.4:

- User authentication assertion (signed at auth time)
- Agent identity assertion (signed at agent startup, **Key Management Service (KMS)**-backed)
- Planner decision (LLM output, hashed)
- Tool-call invocation (parameters, hashed)
- Tool-call result (hashed)
- Outcome (signed completion record)

Together: a **signed action chain** that can be replayed and audited.

The action chain is only as strong as the trust anchor at the bottom of it. If the KMS holding the signing keys is itself running in an untrusted environment, the entire chain is replayable by anyone with cloud-admin access. The emerging standards closing this gap are **EAR** (Entity Attestation Result), **RATS**, and **EAT** — they specify how a workload proves, cryptographically, that the environment producing the signature is the verified one. The hardware-enforced implementation pattern — confidential computing TEEs producing remote attestations that bind the signing key to the verified workload — is what OPAQUE Systems ships. Production §3.4 walks the integration with a customer-side KMS and a customer-side trace store.

### §1.9.8 Common-confusion call-out

| Concept                          | Belongs to | What it is                                                 |
| -------------------------------- | ---------- | ---------------------------------------------------------- |
| Agent identity                   | Problem 2  | The agent runtime's own identity                           |
| Agent-on-behalf-of-user identity | Problem 3  | The delegation identity for actions taken in a user's name |
| User identity                    | Problem 1  | Standard end-user authentication                           |

If you mix problems 2 and 3 in a customer conversation, you will sound like an outsider. Problem 2 is *"who is the agent?"* Problem 3 is *"on whose behalf is the agent acting?"* The 2026 product wave is solving problem 3.

**Two questions the 2026 identity products do not fully answer.** *How do you know the agent on the other end of an A2A call is not an imposter?* Identity assertions prove the agent *claims* a name; cryptographic attestation proves the running workload is the one the policy approved. The standards-defined answer combines SPIFFE / Entra Agent ID for the identity assertion with RATS / EAT remote attestation for the workload verification. *How do you know the agent will verifiably enforce the policy it claims to enforce?* Policy claims live in code paths and configuration; verifiable enforcement requires the policy decision point and the data it decided on to be bound together cryptographically. Foundations §1.10 names this pattern; hardware-enforced policy decision points (confidential computing TEEs) are the implementation.

> **CONCEPT BOX (PM-track).** Three identity questions, in order: **(1) Who is the user?** (Solved, since 2000s.) **(2) Who is the agent?** (Mostly solved, since cloud-native workload identity.) **(3) On whose behalf is the agent acting?** (New, 2025–2026; most agent identity products in 2026 are solving exactly this one.) When a customer says *"we'll figure out identity later,"* the right pushback is *"which of the three identity problems are you deferring?"* 

---

## §1.10 Governance and verifiability — current approaches by layer

Foundations names the runtime in §1.2 and the identity problems in §1.9. This section names the *governance layer that sits across them*. Four current approaches, ordered by the strength of the proof they provide.

### §1.10.1 Guardrails — content-policy at the LLM boundary

**What it is.** A filter layer between the user/tool input and the LLM, and between the LLM output and the downstream consumer. The filter applies content policies (no PII, no jailbreak strings, no policy-violating outputs).

**Named implementations.** NVIDIA **NeMo Guardrails** (open source, Apache 2.0). **Guardrails AI** (open source). **Llama Guard** (Meta, content-classifier model). **Azure AI Content Safety** (managed). Cloud-provider equivalents on AWS Bedrock Guardrails and Vertex AI Safety filters.

**Strength of proof.** Probabilistic, not cryptographic. A guardrail catches what its classifier was trained to catch. It does not produce verifiable evidence that the policy was enforced on every call; the auditor must trust the runtime's claim that the guardrail ran.

**Where it lands.** Necessary for the obvious classes of failure (jailbreaks, PII leakage in outputs). Insufficient for regulator-facing evidence claims.

### §1.10.2 Action-layer governance — wrapping the action, not the content

**What it is.** A governance layer that intercepts the *action* the agent is about to take — a tool call, a state mutation, an external API call — and applies policy to the action itself (allowed/denied, requires approval, requires step-up auth).

**Named implementations.** Microsoft **Agent Governance Toolkit (AGT)** is the canonical example. OpenAI's tool-call gating is a peer pattern. LangGraph's HITL `interrupt` mechanism is the protocol primitive most enterprise teams build on.

**Strength of proof.** Stronger than guardrails for high-consequence actions, because the governance check sits in the critical path of the action — if the check fails, the action does not happen. Still requires the auditor to trust the runtime to have run the check.

**Where it lands.** The right layer for FGA-bound approval flows, HITL gates, and dollar-threshold escalation patterns. Pattern §2.5 carries the depth.

### §1.10.3 Sandbox isolation — constrained execution environment

**What it is.** Runs the agent process in a sandboxed runtime that restricts what system calls, network destinations, and filesystem paths the agent can reach. The sandbox enforces the constraint by construction, not by policy check.

**Named implementations.** **OpenShell** is the named open-source example. Vendor-managed runtimes — **LangGraph Cloud**, **AWS Bedrock AgentCore**, **Azure Foundry Agent Service** — approximate this with managed runtime constraints. Container-runtime isolation (gVisor, Kata Containers) is the substrate layer.

**Strength of proof.** Strong against well-known sandbox escapes; the auditor can read the sandbox configuration and verify it. Weaker against novel side-channel attacks, and still requires trusting the host kernel and the operator who configured the sandbox.

**Where it lands.** Necessary baseline for any agent runtime running untrusted code or untrusted prompts. Insufficient when the threat model includes the operator or the cloud-admin.

### §1.10.4 Cryptographic / hardware-enforced enforcement

**What it is.** Uses confidential computing TEEs (**Trusted Execution Environments** — Intel **Trust Domain Extensions** (TDX), AMD **Secure Encrypted Virtualization — Secure Nested Paging** (SEV-SNP), NVIDIA Confidential GPU, AWS Nitro Enclaves) to make policy decisions and the data they ran on *provably enforced*. The TEE produces a **remote attestation** — a cryptographic statement that names the workload running inside, the policy it was configured with, and the data it operated on. The attestation is bound to a hardware root of trust, so the operator running the host cannot forge it.

**The framing standards.** **EAR** (Entity Attestation Result). **RATS** (RFC 9334, Remote Attestation Procedures). **EAT** (RFC 9711, Entity Attestation Tokens). Together, these specify the protocol for a workload to prove its identity, configuration, and runtime state to a remote verifier.

**The hardware-enforced implementation.** Confidential computing TEEs producing remote attestations that bind agent identity, signing keys, policy decision points, and the data they operated on into a single verifiable chain. **OPAQUE Systems** ships this pattern for enterprise AI workflows.

**Strength of proof.** Cryptographic, not probabilistic. The auditor verifies the attestation against the hardware vendor's signing certificates; the proof does not require trusting the runtime operator or the cloud provider.

**Where it lands.** The right layer for sensitive data processing in the enterprise, including, but not limited to: FSI / Healthcare / sovereign-AI deployments where the regulator demands evidence the operator cannot forge. Production §3.4 walks the integration pattern; the data-bleed surfaces in §1.9.7 are the surfaces this approach closes.

### §1.10.5 How to use these in customer conversations

These four approaches are not exclusive — a production deployment will compose all four. The mental model:

- **Guardrails** catch the obvious content classes.
- **Action-layer governance** gates the consequential moves.
- **Sandbox isolation** constrains the runtime's reach.
- **Cryptographic enforcement** binds the chain of evidence to hardware roots of trust that the operator cannot forge. Creates verifiable governance. 

When a customer's CISO asks *"how do we prove this to the regulator?"* the conversation almost always converges on the bottom of this list. When a customer's engineering lead asks *"how do we ship the obvious safety baseline?"* it converges on the top.

> **CONCEPT BOX (PM-track).** The four governance approaches answer four different questions. **Guardrails** answer *"did the content meet our content policy?"* **Action-layer governance** answers *"was the action allowed under our action policy?"* **Sandbox isolation** answers *"could the agent reach anything it was not supposed to reach?"* **Cryptographic enforcement** answers *"can the auditor prove, six months later, that the policy was enforced at the moment of action?"* Mature enterprise deployments need all four. A customer asking only about guardrails is at the start of the conversation, not the end.

---

## §1.11 The six common use case families

These are the six recipes the rest of the book extends. Foundations gives you the names, the anchor customer per recipe, and a one-paragraph what-and-why. Patterns walks the full state graph per recipe. Production walks the audit-evidence pattern per recipe.

Each recipe opens with a **Jobs-to-Be-Done (JTBD)** sentence. The PM-track will use these directly; the engineer-track will see them in customer PRDs.

### §1.11.1 Customer Support Copilot

**JTBD (end-user):** *When a customer contacts support with a question or a transactional request, the customer wants the issue resolved (or escalated cleanly) without explaining context to multiple humans, so they can complete the underlying task they were trying to do.*

**JTBD (buyer):** *When a customer-experience leader is staffing a 24×7 support function for a growing customer base, the buyer wants automated resolution of high-volume routine inquiries with reliable escalation on exceptions, so they can hit response-time SLAs without linear headcount growth.*

**Anchor:** **Klarna AI Assistant.** 2.5M conversations handled; topology committed to **routed multi-agent (closer to Supervisor than ReAct, single shared model)** per Sebastian Siemiatkowski's LangChain Interrupt 2025 keynote and the Klarna engineering blog (April 2025). `[customer-produced-evidence]` `[corroborated]`

**The honest framing — the Klarna CEO reversal.** Klarna's CEO publicly walked back the AI-replaces-headcount framing in May 2025, conceding that the metrics at launch overstated steady-state performance. The teachable point this Field Guide commits to: **the metrics at launch are not Model Risk Management (MRM) evidence under SR 11-7.** This is the canonical "we got it wrong" story for agent deployments; it anchors honest expectation-setting in customer conversations. Vendor-disclosed metrics are not validation evidence. `[customer-produced-evidence]` `[named-incident]`

**Segment buyers most:** B2C-scale customer-service operations across FSI (Klarna), ISV (any B2B SaaS at scale), Healthcare (non-PHI Q&A — Doctolib Alfred).

### §1.11.2 Code-Modifying Developer Agents

**JTBD (end-user):** *When a developer wants to ship a change to existing code, they want the agent to write or update tests, refactor in step, and propose the diff for review, so they can focus on the change that requires judgment.*

**JTBD (buyer):** *When an engineering leader is trying to ship a multi-year migration without freezing feature work, they want an agent that handles the mechanical refactoring at scale, so the migration completes inside one fiscal year instead of three.*

**Anchors:** **Uber Validator + AutoCover** (~21K developer hours reclaimed per Uber's LangChain Interrupt 2025 talk) and **Replit Agent** (code-generation copilot with HITL approval gates). `[customer-produced-evidence]`

**Segment buyers most:** Developer-tools ISVs (Replit, Cursor, GitHub Copilot Workspace), large engineering orgs running multi-year migrations (Uber, JPMorgan), and DevTools-adjacent FSIs.

### §1.11.3 Text-to-SQL / Conversational Analytics

**JTBD (end-user):** *When a business user has a question of the data warehouse but cannot write SQL, they want to ask in natural language, see the SQL generated, optionally edit it, and run it safely against the right tenant's data, so they can answer their own questions without filing a ticket.*

**JTBD (buyer):** *When a data-platform leader is trying to scale analytics access without proportionally scaling analyst headcount, they want a governed natural-language interface to the warehouse, so business users self-serve while RBAC and row-level security stay enforced.*

**Anchors:** **LinkedIn** (internal conversational analytics) and **Vizient** (healthcare supply-chain analytics). `[customer-produced-evidence]` `[architectural inference]`

**Why this recipe is hard:** every Text-to-SQL agent must reason about multi-tenant isolation. The dominant failure mode is the agent generating a query that crosses a tenant boundary because the prompt did not surface the boundary explicitly. Patterns and Production carry the cross-tenant isolation depth.

**Segment buyers most:** Healthcare (supply-chain, claims analytics, provider performance), FSI (research, wealth analytics), ISV (every B2B SaaS that ships an analytics module).

### §1.11.4 Multi-Agent Deep Research

**JTBD (end-user):** *When a researcher has a complex question requiring synthesis across many documents, they want an agent that plans the investigation, executes parallel sub-investigations, and produces a sourced report, so they can spend their time on judgment rather than search.*

**JTBD (buyer):** *When a research-intensive business (FSI research, wealth advisory, supply-chain intelligence) is staffing a research function, the buyer wants per-analyst leverage on document-heavy synthesis tasks, so output-per-headcount grows without sacrificing citation quality.*

**Anchors:** **Captide** (FSI research agent, Plan-and-Execute topology); **Morningstar Mo** (wealth research, Plan-and-Execute with RAG retrieval at each step `[architectural inference]`); **Exa** (deep research infrastructure). `[customer-produced-evidence]`

**Segment buyers most:** FSI (wealth, research, fund management), Healthcare (literature review, clinical research), Sovereign (intelligence and policy research — `[evidence-zero, structural-fit-only]` for sovereign-region deployments specifically).

### §1.11.5 Enterprise SaaS Embedded Copilot

**JTBD (end-user):** *When a SaaS user is inside the product trying to accomplish a domain-specific task, they want an in-product copilot that knows the product's data model, can take actions on the user's behalf, and surfaces the right context, so they accomplish the task faster than they could navigating the UI manually.*

**JTBD (buyer):** *When a B2B SaaS leader is trying to ship product-led growth and increase per-seat ARR, they want a copilot that makes their product 2–3× more effective per seat, so seats expand and the AI feature pays for itself.*

**Anchors:** **AppFolio Realm-X** (property-management copilot) and **ServiceNow** (Hierarchical with Send-API fanout `[architectural inference]`). `[customer-produced-evidence]`

**Segment buyers most:** ISV (B2B horizontal SaaS — Salesforce, HubSpot, Notion; vertical SaaS — AppFolio, Procore, Toast; developer tools — Cursor, Replit).

### §1.11.6 Security / Threat-Detection Agents

**JTBD (end-user):** *When a security analyst is triaging a stream of alerts, they want an agent that pre-investigates each alert, correlates context, proposes a verdict, and surfaces the cases worth a human's attention, so the analyst spends their time on the alerts that genuinely require judgment.*

**JTBD (buyer):** *When a security leader is staffing a SOC, they want each analyst to handle more alerts at higher quality, so they can hit detection SLAs and reduce alert fatigue without proportionally scaling the team.*

**Anchor:** **Elastic Security AI Assistant** (Agentic RAG over Elastic indexes; SOC alert triage). `[customer-produced-evidence]`

**Segment buyers most:** Cybersecurity-conscious enterprises across all segments; CISO-as-primary-buyer is the distinguishing characteristic. This is the **1-of-18-deployment outlier** in the corpus that the Field Guide carries forward because the CISO-buyer narrative matters for the substrate-level remediation framing in Production.

### §1.11.6.1 A deeper look at the six recipes

The one-paragraph framings above are the names you can carry into a discovery call. The following expansions add the **architectural shape, the dominant failure mode, the buyer-conversation hook, and the segment-segment signal** for each recipe. Patterns walks the full state graph per recipe; this is the Foundations-depth shape.

**Customer Support Copilot — architectural shape.** A Supervisor or ReAct agent fronts the conversation. Tools: lookup-account, lookup-order, place-refund, escalate-to-human, send-email. State: thread-scoped (the active ticket) plus cross-thread (the customer's history). HITL: refund-above-threshold, escalation, sensitive policy questions. Retrieval: knowledge-base over policy and FAQ documents. Observability: every span captured to LangSmith or Langfuse; outcomes correlated with CSAT downstream. The dominant failure mode is **hallucinated policy** — the agent claims a refund policy the company does not actually have. Moffatt v. Air Canada is the legal anchor. The buyer-conversation hook is **per-conversation resolution cost** plus **deflection rate before escalation**.

**Code-Modifying Developer Agents — architectural shape.** Plan-and-Execute or Supervisor, depending on the scope of the migration. Tools: read-file, write-file, run-tests, run-linter, search-codebase, open-pull-request, comment-on-pull-request. State: thread-scoped per migration task; cross-thread learning of repo conventions in `BaseStore`. HITL: pull-request approval, test-failure investigation, conflict resolution. Sandbox: every code execution runs in an isolated environment (E2B, Modal, Daytona, Firecracker microVM). The dominant failure mode is **hallucinated API surface** — the agent calls a function that does not exist or passes the wrong argument shape. Replit's May 2025 production-DB-deletion incident is the autonomy-grant anchor. The buyer-conversation hook is **developer hours reclaimed per quarter** plus **migration velocity**.

**Text-to-SQL / Conversational Analytics — architectural shape.** Agentic RAG or Plan-and-Execute. Tools: introspect-schema, generate-SQL, execute-SQL (with row-level security predicates), explain-query, visualize-result. State: thread-scoped per question; cross-thread learning of which tables and joins the user prefers. HITL: SQL preview before execution for sensitive tables. Retrieval: schema documentation, prior queries, sample data. The dominant failure mode is **cross-tenant aggregation** — the LLM generates a query without the per-tenant predicate, or the query joins across tables in a way that crosses tenants. Per CISO #5.2 in the design spec, the FGA model for this recipe is published in Patterns. The buyer-conversation hook is **time-to-insight** plus **analyst leverage** plus **governance posture**.

**Multi-Agent Deep Research — architectural shape.** Plan-and-Execute, often with `deepagents` as the harness. Tools: search-web, search-internal-docs, read-document, summarize, cite, write-note. State: thread-scoped (the investigation), with a virtual filesystem scratchpad in `deepagents`. HITL: investigation-scope confirmation, sensitive-source approval, citation review. Retrieval: heavy — multiple indexes, rerankers, source-quality filtering. The dominant failure mode is **citation hallucination** — the agent invents a source or attributes a real finding to the wrong source. Mata v. Avianca is the legal anchor. The buyer-conversation hook is **per-analyst leverage** plus **citation rigor** plus **source attribution audit**.

**Embedded SaaS Copilot — architectural shape.** Supervisor or Hierarchical, depending on the breadth of the SaaS product's surface. Tools: product-native APIs — every action the user can take in the UI is exposed as a tool. State: thread-scoped per session; cross-thread per-account preference learning. HITL: any destructive or high-cost action (sending to many recipients, deleting records, changing billing). Retrieval: account-specific data plus product documentation. The dominant failure mode is **action-on-behalf-of-user identity gap** — the agent acts as the user without the user's RAR-grade approval for the specific action. Salesforce Agentforce ForcedLeak (Sept 2025) is the anchor. The buyer-conversation hook is **per-seat ARR expansion** plus **time-to-first-value**.

**Security Agents — architectural shape.** Agentic RAG over the customer's SIEM, EDR, vulnerability scanner, and threat-intelligence feeds. Tools: query-SIEM, enrich-IOC, lookup-CVE, escalate-to-analyst, create-ticket, isolate-host. State: thread-scoped per alert investigation; cross-thread learning of false-positive patterns. HITL: any containment action (host isolation, account disable, IP block). Retrieval: the customer's own log data plus public threat intelligence. The dominant failure mode is **alert-fatigue mis-triage** — the agent suppresses a true positive that looks like the 1,000 false positives before it. The buyer-conversation hook is **mean time to detect** plus **analyst capacity** plus **false-positive rate**.

### §1.11.6.2 Per-recipe HITL placement at Foundations depth

A consistent question across all six recipes: **where in the agent's loop does the human-in-the-loop interrupt fire?** This question has a different answer per recipe, and getting it wrong in a customer conversation signals that you have not understood the recipe.

| Recipe | HITL fires at... |
|---|---|
| Customer Support | Refund above threshold; policy escalation; cross-team handoff |
| Code-Modifying | Pull-request merge; destructive operation (DB writes, deletions); conflict resolution |
| Text-to-SQL | SQL execution against sensitive tables; large-result-set materialization; cross-schema joins |
| Deep Research | Investigation-scope confirmation; sensitive-source access; citation review for high-stakes claims |
| Embedded SaaS Copilot | Any destructive or high-cost action; bulk operations; billing changes |
| Security Agent | Any containment action (isolate host, disable account, block IP); investigation-closure signoff |

The pattern: HITL fires at **the action whose reversal is expensive or impossible**. Refunds are reversible (mostly). Database deletions are not. Host isolation is not. Citation hallucination is not. Foundations readers should be able to recognize the pattern; Patterns walks per-recipe HITL placement as a design decision with trade-offs.

### §1.11.6.3 The matrix

A compressed view of which segment buys which recipe most strongly.

|  | Customer Support | Code-Modifying | Text-to-SQL | Deep Research | Embedded Copilot | Security |
|---|---|---|---|---|---|---|
| **FSI** | Klarna | (Uber-shape) | Wealth research | Captide, Morningstar | (some) | (cross-cutting) |
| **Healthcare** | Doctolib (non-PHI) | (rare) | Vizient | Komodo (de-id) | (rare) | (cross-cutting) |
| **ISV** | Many | Replit, Uber | LinkedIn | (some) | AppFolio, ServiceNow | (cross-cutting) |
| **Sovereign** | `[zero]` | `[zero]` | `[zero]` | `[zero]` | `[zero]` | `[zero]` |

(Sovereign row marked `[evidence-zero, structural-fit-only]` per §1.12. The recipes fit conceptually; no public deployment evidence exists.)

---

## §1.11 What can go wrong

This section is the intro to data-leak surfaces. Foundations does not teach the full 14-mode catalog or the 18-surface taxonomy — Production carries those. Foundations teaches **why agent autonomy expands the leak surface**, names the **five categorical surfaces** at concept depth, and grounds the conversation in **three named public incidents** so you have anchor stories to reference.

### §1.11.1 Why agents amplify the leak surface

A traditional SaaS app has three primary leak surfaces: data-at-rest (storage), data-in-use (memory), and network egress. Agents add a fourth and a fifth that did not exist before:

- **The tool / MCP invocation surface.** Every tool the agent can call is a potential exfiltration path. A poisoned tool result can become a prompt injection. A misconfigured tool can send data to an attacker's URL.
- **The agent state / memory surface.** Long-term memory (`BaseStore`), thread checkpointers, and agent caches all retain data that may need per-tenant isolation, retention controls, and PII redaction. Mistakes here aggregate data across tenants.

These two new surfaces are the focus of the 2025–2026 agent-security research wave. They are where **every named public agent incident from 2024–2025 actually landed** — Slack AI, EchoLeak, CurXecute, ForcedLeak, ConfusedPilot, Atlas. None of those incidents would have been possible in a traditional SaaS app, because the surfaces did not exist.

### §1.11.2 The five categorical surfaces (intro depth)

The Foundations frame collapses the full surface taxonomy into five categorical surfaces. Patterns expands to a 14-mode taxonomy; Production catalogues 18 surfaces.

**(1) Prompt injection — direct and indirect.**

- **Direct:** the attacker controls user input and embeds malicious instructions.
- **Indirect:** the attacker controls *data the agent retrieves or reads* — an email, a document, a search result, a webpage — and the agent treats the embedded content as instructions.

Indirect prompt injection is the dominant 2025 risk class. It is the failure mode behind Slack AI, EchoLeak, ConfusedPilot, and most of the named incidents.

**(2) Telemetry capture.** Agent traces include PII, regulated data, prompt content, or tool-call payloads — and end up in observability platforms outside the trust boundary. LangSmith Cloud, Datadog LLM Observability, and any SaaS observability layer is a candidate failure point. The mitigation is per-trace PII redaction at the emission boundary and per-tenant trace partitioning at the destination.

**(3) Cross-tenant aggregation.** Agent state, cache, retrieval, or memory leaks between tenants — typically because the per-tenant predicate at the vector store, the per-tenant cache key, the per-tenant `thread_id` namespace, or the per-tenant trace partition was missing or misconfigured. The ConfusedPilot research class (UT Austin, USENIX Security 2024) is the canonical academic anchor. `[benchmark]` `[named-incident]`

**(4) Action provenance gaps.** The agent took an action, and six months later, the audit trail cannot reconstruct who authorized what, what evidence supports the decision, or what reasoning the LLM applied. This is the regulator-facing failure mode under SR 11-7, DORA Article 19, GDPR Article 22, and EU AI Act Article 12. The mitigation is the signed action chain (§1.9.7), implemented operationally in Production §3.4.

**(5) Supply-chain compromise.** A tool, MCP server, framework dependency, or model artifact is malicious or compromised. The MCP-server-as-supply-chain question is the freshest of these in 2026 because the MCP signature / attestation story is still maturing. CurXecute / CVE-2025-54135 is the canonical anchor. `[named-incident]`

### §1.11.3 The Klarna CEO reversal — the canonical "we got it wrong" story

In May 2025, Klarna's CEO Sebastian Siemiatkowski publicly walked back the framing that AI was replacing 700 FTE-equivalents of customer-service work. The original Klarna AI Assistant launch metrics (handling 2.5M conversations, work equivalent to ~700 agents) had been used widely as the canonical "AI is ready" story. The reversal acknowledged that steady-state performance did not match launch performance, that some categories of issue required reassignment back to humans, and that the early metrics had overstated the durable replacement rate. `[customer-produced-evidence]` `[named-incident]`

The teachable point this Field Guide commits to throughout: **vendor-disclosed metrics are not Model Risk Management (MRM) evidence under SR 11-7.** Klarna's 80%, the 700-FTE-equivalent number, Uber's 21K-developer-hours-reclaimed, LinkedIn's 95% accuracy, Komodo's 330M patient journeys — these are vendor marketing material. They are useful for benchmarking and discussion. They are **not** suitable for any validation report a Sales Engineer signs off on or any PRD section that claims production readiness.

The Klarna reversal anchors honest expectation-setting in every customer conversation. If you are tempted to quote a vendor-disclosed metric as evidence, the Klarna story is your reminder to add the qualifier: *"This is vendor-disclosed. For MRM purposes, we'd need [independently-audited / customer-produced-evidence / corroborated] data."*

### §1.11.4 Three named public incidents (one paragraph each)

The remaining seven incidents from the design-spec roster live in the glossary (§1.15) and in Patterns. Three to anchor Foundations:

**Slack AI (August 2024) `[named-incident]`.** PromptArmor disclosed a vulnerability in Slack AI where an attacker could post a message in a public channel containing a prompt-injection payload; when a user in a private channel queried Slack AI, the AI would follow the attacker's injected instructions and exfiltrate private-channel content via a Markdown link to an attacker-controlled URL. The disclosure was the public-vocabulary-establishing event for **indirect prompt injection in production**. Slack patched server-side. The teachable point: indirect prompt injection is a real production risk, not a research curiosity.

**EchoLeak / CVE-2025-32711 (June 2025) `[named-incident]`.** Aim Labs disclosed a zero-click prompt-injection vulnerability in Microsoft 365 Copilot. An attacker sent an email containing crafted payloads; when the victim later queried Copilot, the RAG system pulled the email into context and the injection triggered data exfiltration — **without the user ever clicking anything**. CVSS 9.3. Microsoft patched in June 2025. The arXiv writeup (2509.10540) names it "the first real-world zero-click prompt injection exploit in a production LLM system." The vocabulary "LLM Scope Violation" comes from this incident. The teachable point: zero-click attacks on production agents are not hypothetical.

**Samsung ChatGPT leak (April 2023) `[named-incident]`.** Samsung semiconductor engineers pasted proprietary source code and meeting transcripts into ChatGPT across three separate incidents in 20 days. OpenAI's terms at the time allowed using submitted content to improve models. Samsung banned generative AI tools company-wide within a month. Not an agent incident per se, but **the vocabulary-establishing event for enterprise data leakage to LLM SaaS** that drove the entire BYOC and self-hosting demand wave. The teachable point: the question "where does the prompt go after we send it?" has been an enterprise-procurement question since April 2023.

The remaining incidents you should be able to name in passing (full depth in Patterns):

- **CurXecute / CVE-2025-54135 (2025).** MCP-related tool-result-as-prompt-injection vulnerability class. `[named-incident]`
- **Air Canada / Moffatt v. Air Canada (Feb 2024).** Legal precedent that a deploying organization is responsible for what its agent says. `[named-incident]`
- **Replit production-DB deletion (May 2025).** Autonomy-grant error vocabulary. `[named-incident]`
- **Mata v. Avianca (2023).** Hallucination-to-action liability in legal practice. `[named-incident]`
- **ConfusedPilot (UT Austin, 2024).** Cross-tenant aggregation via RAG. `[named-incident]` `[benchmark]`
- **Salesforce Agentforce ForcedLeak (Sept 2025).** Purpose-built enterprise agent platforms are not automatically safe. `[named-incident]`
- **ChatGPT Atlas omnibox (Oct 2025).** UI-confused-deputy attacks in agent-native applications. `[named-incident]`

### §1.11.5 The Foundations governance posture

Foundations does **not** teach mitigation. Foundations teaches three things:

1. These incidents are public, named, and ten in number across the 2023–2025 window.
2. Agent governance is a different problem than model governance or app governance.
3. Patterns is where you learn the named-component mitigations; Production is where you learn the audit-evidence flow.

If a customer asks you in a discovery call *"how do we mitigate prompt injection?"*, the honest Foundations-level answer is: *"There is no single mitigation. The named components are guardrails, structured output, tool sandboxing, output-classifier filters, and per-tenant retrieval predicates. Each addresses part of the surface. We can walk through your specific architecture in a follow-on technical session."* This is the right thing to say. It is what Patterns equips you to do.

> **CONCEPT BOX (PM-track).** Five categorical surfaces — prompt injection (direct and indirect), telemetry capture, cross-tenant aggregation, action-provenance gaps, supply-chain compromise. Three incidents to anchor on — Slack AI, EchoLeak, Samsung. One reversal story for honest framing — Klarna CEO May 2025. If you remember nothing else from this section: vendor-disclosed metrics are not MRM evidence.

---

## §1.12 The three ICP industries and the Sovereign gap

This section sets up the segment vocabulary the rest of the book uses. Patterns walks the persona × recipe × segment-variant matrix in full. Foundations gives you the three industries at intro depth and the fourth as an explicit honest gap.

### §1.12.1 Financial Services Industry (FSI)

The single largest spending segment for enterprise agents in 2026 and the segment with the heaviest regulatory pressure. FSI sub-segments worth distinguishing:

- **Payments** — Klarna, Stripe, Block. Heavily regulated under PCI DSS 4.0; Klarna is in PCI scope.
- **Wealth management / research** — Morningstar, BlackRock, fund managers. Regulated under SEC 17a-4 (**Write-Once-Read-Many (WORM)** retention), MiFID II, **Financial Industry Regulatory Authority (FINRA)** 4511 and 5280.
- **Research and asset management** — Captide, institutional asset management. SR 11-7 (Model Risk Management) is the Federal Reserve / OCC supervisory framework that governs model deployment.
- **Insurance** — the segment with **68% of insurers running gen-AI / agents but zero LangGraph footprint** as of mid-2026, per the R3 industry deep-dive. This is a major gap the Field Guide flags explicitly. The insurance segment is not running LangGraph; it is running hyperscaler-native stacks, Azure OpenAI direct, and homegrown solutions. Whether this changes is an open question. `[architectural inference]` `[evidence-zero for LangGraph specifically]`

**Regulatory shape:** SR 11-7 plus OCC Bulletin 2011-12; DORA in the EU; NYDFS Part 500 in New York; SEC 17a-4 and FINRA across the US; MiFID II in the EU; SAMA, DFSA, MAS, HKMA across the Gulf and APAC. Patterns and Production carry the per-regime depth.

**Deployment preference:** Self-hosted or BYOC. LangGraph's BYOC AWS-only constraint is a real deal-shaping factor for Azure-aligned and GCP-aligned FSI buyers. `[customer-produced-evidence]`

### §1.12.2 Healthcare

The HIPAA shadow falls across every Healthcare conversation. **PHI-in-production on LangGraph is `[reference design only — not in production anywhere on any framework]` as of May 2026.** The two named Healthcare deployments in the corpus operate on **non-PHI** or **de-identified** data:

- **Doctolib Alfred** — non-PHI Q&A copilot ("early chapters" framing per Doctolib's public posture). `[customer-produced-evidence]`
- **Vizient** — healthcare supply-chain analytics (non-PHI). `[customer-produced-evidence]`
- **Komodo Health MapAI** — de-identified longitudinal patient data (330M patient journeys, per Komodo's own materials). De-identified, not PHI in production. `[customer-produced-evidence]`

**Regulatory shape:** HIPAA Security Rule (45 CFR Part 164), HITI-1 source attribute for AI-driven clinical decision support, FDA SaMD classification for software as a medical device, the state-patchwork (Washington My Health My Data Act, Connecticut DPA, CMIA in California), and FDA PCCP for AI/ML SaMD. Production carries a PHI-in-scope reference deployment chapter (CISO #8 in the design spec) — every claim there `[reference design]`.

**Deployment preference:** Self-hosted; BAA chain required (Anthropic ↔ Bedrock ↔ LangChain ↔ reranker ↔ customer-app); de-identification engineering (Safe Harbor or Expert Determination) is non-negotiable for any PHI-adjacent deployment.

### §1.12.3 Independent Software Vendors (ISV)

The largest segment by deployment count and the most heterogeneous. Five sub-motions worth naming (per the design spec's split):

- **B2B horizontal SaaS** — Salesforce, HubSpot, Notion. Embedded copilots inside the SaaS product.
- **Developer tools** — Replit, Cursor, GitHub Copilot Workspace. Code-modifying agents.
- **Vertical SaaS** — AppFolio (property management), Procore (construction), Toast (restaurants). Compressed to half-page summaries in Patterns per the design spec.
- **Data infrastructure** — Snowflake, Databricks, BigQuery-adjacent. Compressed to half-page in Patterns.
- **AI-native** — companies whose core product is itself an AI agent. Compressed to half-page in Patterns.

**Regulatory shape:** lighter than FSI / Healthcare in most cases, but the cross-tenant isolation problem is especially visceral — every ISV is multi-tenant by definition, and every ISV embedded copilot must reason about tenant boundaries.

**Deployment preference:** Mixed; SaaS / Cloud preferred where compliance allows, self-hosted where customer compliance demands. Some ISVs offer both shapes.

### §1.12.4 Sovereign — `[evidence-zero, structural-fit-only]`

The fourth segment in the design spec, marked explicitly with the **most honest framing in the catalog**. Sovereign agent deployments — in nations or regions with data-residency, key-custody, and operator-residency requirements (EU Gaia-X, SecNumCloud, EUCS, BSI C5, MAS, DFSA, CBUAE, SAMA, SDAIA, UAE PDPL, China PIPL, India DPDPA) — are a **major target market with zero public LangGraph deployment evidence** as of May 2026.

The structural fit is real (LangGraph supports self-hosted, air-gapped Kubernetes deployments; Postgres co-locates with the agent runtime; LangSmith can be self-hosted). The evidence is zero. The two facts are different. Patterns and Production cover the **Data Residency Reasoning** chapter (per CISO #6 in the design spec) — five sovereignty axes (data residency, processing locus, model locus, key custody, operator residency) crossed with per-region regulatory landscape and sovereign-cloud options (Gaia-X, SecNumCloud / ANSSI, EUCS high, BSI C5, Core42, OCI Sovereign, AWS European Sovereign Cloud, Azure Local / Stack Hub Sovereign, GCP sovereign partnerships, T-Systems Sovereign Cloud, Bleu, S3NS, Delos).

The Foundations framing is the honest one: *Sovereign is structurally a fit and operationally a `[zero]`-deployment segment. When a customer asks about sovereign deployment, the right answer is: 'No public LangGraph deployment exists in your region. The structural fit looks like X. The deployment shape that would apply is Y. Here is the evidence base we have.'*

### §1.12.5 The insurance-segment gap (the R3 finding)

The R3 industry deep-dive surfaced a finding worth naming in Foundations explicitly: **68% of insurers report running gen-AI or agents in production**, but the LangGraph footprint in insurance specifically is **zero in the public corpus**. Insurers are running on Azure OpenAI, Bedrock-native, GCP Vertex, and homegrown solutions. Whether LangGraph extends into insurance is an open commercial question that the Field Guide flags rather than hides. `[architectural inference]` `[evidence-zero]` for LangGraph in insurance.

### §1.12.6 The Foundations posture on segments

Three things to absorb:

1. **The 18 named LangGraph deployments are concentrated in FSI, ISV, and Healthcare** — with Healthcare's PHI footprint being `[reference design]` only.
2. **Sovereign is a structural fit and an evidence-zero market.** Honest framing wins customer trust.
3. **Insurance is a gap.** A 68%-AI-adoption segment with zero LangGraph footprint. Worth naming.

---

## §1.12.6 Three segment vignettes worth holding

Before the field-guide section, three short vignettes — one FSI, one Healthcare, one ISV — that put the segment vocabulary into customer-conversation shape. Each is composite, drawn from the patterns in the corpus rather than from any single account. Each is honest about evidence weight.

### §1.12.6.1 FSI vignette — the routed-multi-agent payments customer

A mid-tier payments fintech (Klarna-shape, smaller but not small) wants to add an agent on top of its existing customer-support stack. The buyer is the VP of Customer Experience. The operator is the CX Operations leader. The end-user is the customer. The deployment is in EU and US scope; PCI DSS 4.0 applies; DORA Art. 5, 6, 19 apply; GDPR Art. 5, 28 apply; SR 11-7 applies to the US entity.

The conversation starts with the buyer asking *"can we replicate Klarna's 80%?"*. The honest answer is the Klarna CEO reversal — the metrics-at-launch did not survive steady state. The recommendation is to scope to Level 2 autonomy (HITL on every consequential action — refunds above threshold, account modifications, escalations), Supervisor topology with routed worker agents for refund/escalation/FAQ, `PostgresSaver` checkpointer, custom JWT for customer identity, Okta for AI Agents for operator identity (the CX Ops team), Self-Hosted Enterprise deployment shape (the BYOC AWS-only constraint matters less because this customer is AWS-aligned), LangSmith with OTel export to the customer's Splunk for the SIEM-side audit trail.

The dominant failure mode the security team will care about is **indirect prompt injection via tool results** and **cross-tenant aggregation** (the customer has multiple white-label tenants on the same platform). The audit-evidence shape the CISO will want is the signed action chain from §1.9.7 — Production §3.4 carries the detail. The first 90-day milestone is a passing MRM second-line review, not a production cutover. `[architectural inference]` `[customer-produced-evidence]` for Klarna anchor.

### §1.12.6.2 Healthcare vignette — the non-PHI clinical-research copilot

A mid-tier healthcare ISV serving clinical research organizations wants to add a deep-research agent that ingests medical literature and surfaces relevant studies for clinician users. The buyer is the VP of Product. The operator is the clinical-content team. The end-user is the clinician. **Critically: the data in scope is published medical literature, not PHI.** This puts the deployment in a `[reference design]` adjacency to the PHI-in-scope chapter in Production but does not require the full HIPAA Security Rule controls because PHI is not present.

The recommendation is Plan-and-Execute topology with `deepagents` as the harness, multi-document retrieval against PubMed-class indexes, citation-rigor as a first-class quality concern (Mata v. Avianca anchor), HITL on every published-claim citation, Self-Hosted Enterprise deployment shape with VPC-isolated runtime, LangSmith self-hosted (not LangSmith Cloud — the data is non-PHI but the customer prefers self-hosted observability for category alignment), custom JWT for clinician identity with step-up authentication for high-stakes claims.

The honest framing in the customer conversation: *"Your data is non-PHI, so we are not in the HIPAA Security Rule controls. But the structural lessons from PHI deployments apply — particularly around citation rigor, BAA-chain awareness for any vendor that might touch PHI later, and the FDA SaMD classification question for any clinical-decision-support angle. If you ever add PHI, the deployment shape changes. Plan for that boundary now."* `[reference design]` for PHI-adjacency; `[customer-produced-evidence]` for non-PHI healthcare deployments (Doctolib, Vizient, Komodo).

### §1.12.6.3 ISV vignette — the embedded vertical-SaaS copilot

A vertical-SaaS company serving property management (AppFolio-shape) wants to add an embedded copilot inside its product. The buyer is the VP of Product / Chief Product Officer. The operator is the customer success team (who fields questions about what the copilot did). The end-user is the property manager using the product. Multi-tenant by definition — each property-management company is a tenant; each property is a sub-tenant.

The recommendation is Supervisor topology with workers per major product surface (tenant management, lease workflows, maintenance, accounting), Agentic RAG for the product-documentation surface, per-tenant `BaseStore` for cross-conversation memory, `PostgresSaver` with per-tenant `thread_id` namespacing (the cross-tenant aggregation surface is the single largest failure mode for this recipe), OpenFGA for the relationship "property manager X at company Y can take action Z on property P," Auth0 for AI Agents for the action-on-behalf-of-user identity story, Cloud SaaS or Self-Hosted Enterprise depending on the customer mix the SaaS serves.

The buyer-conversation hook is **per-seat ARR expansion** — the copilot makes the product 2–3× more effective per seat, seats expand, the copilot pays for itself. The honest framing: the cross-tenant isolation problem is the single biggest engineering investment, and it will not be visible to the buyer until something goes wrong. Pattern this customer's roadmap to invest in cross-tenant isolation engineering for the first 90 days before adding new copilot surfaces. The Salesforce Agentforce ForcedLeak anchor is the reminder that purpose-built enterprise agent platforms are not automatically safe. `[customer-produced-evidence]` for AppFolio, ServiceNow; `[named-incident]` for ForcedLeak.

### §1.12.6.4 A fourth — the Sovereign vignette flagged honestly

A sovereign deployment vignette is worth including, with the explicit honest framing the design spec commits to. A national bank in a sovereignty-conscious jurisdiction (EU Gaia-X / SecNumCloud / EUCS-high; or MAS / DFSA / SAMA in the Gulf; or SDAIA / Core42 in Saudi; or PIPL Art. 24 in China) wants to deploy an agent for internal-research support. The five sovereignty axes apply: data residency (must stay in-region), processing locus (compute must stay in-region), model locus (model inference must stay in-region — which excludes most commercial frontier models unless they are deployed via sovereign-cloud partnerships), key custody (HYOK / customer-managed keys are non-negotiable), operator residency (vendor support cannot read data without customer-mediated access).

The honest framing for this conversation: **no public LangGraph deployment exists in this profile as of May 2026.** The structural fit looks like Self-Hosted Enterprise on customer Kubernetes, air-gapped or sovereign-cloud-resident; pgvector co-located; open-weight models served on customer-managed inference (vLLM, NVIDIA NIM, TensorRT-LLM, LMDeploy); LangSmith self-hosted; OpenFGA for FGA; SPIFFE / SPIRE for workload identity; custom JWT for delegation identity. The deployment-shape decision is forced by the regulatory profile. The framework choice (LangGraph vs alternatives) is a credible recommendation but cannot be defended with named-customer evidence in-region. This is the `[evidence-zero, structural-fit-only]` framing the design spec commits to.

When you have a customer in this profile, the right conversation is: *"The structural fit is real. The named-customer evidence is zero in your region. Here is what a reference deployment shape looks like, here is what the audit-evidence chain would need to look like, here are the sub-decisions where your team and ours will be the first to ship in this profile. We can be the first; we cannot pretend to be the second."* This is the honest answer. It is what wins trust in a sovereignty-conscious customer's procurement process.

### §1.12.6.5 What the four vignettes share

Each segment has its own dominant failure mode, its own regulatory shape, its own deployment-preference profile. But the four vignettes share something important: **none of them resolves to a single decision.** Each requires the customer's team to make 5–10 sub-decisions (topology, deployment shape, identity stack, HITL placement, observability destination, retrieval substrate, checkpointer choice, store choice, guardrail layer, audit-evidence chain). The Foundations vocabulary is what lets you walk the customer through those 5–10 sub-decisions without faking knowledge.

A consistent Foundations-depth recommendation across all four vignettes: **start at Level 2 autonomy. HITL on every consequential action. `PostgresSaver` + `PostgresStore`. Self-Hosted or BYOC where compliance demands; Cloud SaaS where it doesn't. LangSmith for first-party observability with OTel export to the customer's SIEM. Custom JWT today, agent-identity products as they mature. Plan for the action provenance chain from day 1.** This is not a substitute for the per-customer design — it is the starting point. Patterns and Production carry the per-recipe and per-regime depth that turns this into a defensible architecture.

---

## §1.12.7 How to read a customer's agent architecture

Foundations has given you the vocabulary. Before the gate, a short field-guide on **what to do with the vocabulary when you walk into a customer conversation**. You are not going to write LangGraph code in front of a CISO. You are going to read the customer's architecture diagram and ask disambiguating questions. This is what those questions look like.

### §1.12.7.1 The five disambiguating questions

When a customer's engineering team draws their architecture, ask the following five questions, in this order:

**(1) "Is the LLM choosing the next tool, or is the flow fixed in code?"** This is the Anthropic workflow-vs-agent cut. If the answer is "the LLM chooses," you are in the agent governance conversation (§1.11). If the answer is "the flow is fixed," you are in the workflow conversation, which has lower governance risk but also lower agency.

**(2) "What is your checkpointer? Is it Postgres or Redis? Are you on `MemorySaver` in production?"** The answer tells you their durability story. `MemorySaver` in production is a red flag. Postgres is the production default. Redis is a sub-millisecond choice with different durability trade-offs. If they cannot answer this question, their team has not done the production-readiness work yet.

**(3) "What is your `BaseStore`? Do you have cross-thread memory?"** Most customers do not. This is where you find out whether they have thought about the cross-tenant isolation problem. If they say "we don't have one yet," ask what cross-conversation context they think the agent needs to remember — and watch for the moment they realize they need one.

**(4) "How are you handling identity for actions the agent takes on behalf of the user?"** This is Problem 3 from §1.9. Most customer teams have not noticed Problem 3 yet. Their answer will reveal whether they are operating at Problem 1 (user identity), Problem 2 (workload identity), or Problem 3 (delegation). Foundations equips you to ask this question and recognize what the answer means.

**(5) "What does your action provenance look like? If a regulator asks who authorized this six months from now, what do you show them?"** This is the audit-evidence question. The most-likely answer in 2026 is "we have LangSmith traces and Postgres rows." That is not action provenance. Production §3.4 carries the signed-action-chain story; for Foundations, your job is just to ask the question and recognize the gap.

These five questions, asked in this order, will tell you within 10 minutes whether you are talking to a team that has shipped an agent before or a team that is about to learn the hard way. Both are valid customers. Different conversations.

### §1.12.7.2 The two questions a CISO will ask you

Different audience, different questions. When a CISO or security leader is in the room:

**(1) "Where does our data go?"** The honest answer traces every tier — LLM (Anthropic via Bedrock; data in the customer's AWS region), retrieval (pgvector in the customer's Postgres; data never leaves), tools (each tool's data-residency story is its own answer), observability (LangSmith Cloud egresses traces to GCP us-central1 unless self-hosted; this is the deal-shaping fact for many FSI customers), state (Postgres in the customer's region). If you cannot answer this question for every tier, you are not ready to recommend a deployment.

**(2) "What's the worst that can happen?"** The honest answer names the dominant failure mode for the recipe (§1.10.6.1) and names the named-incident anchor that has happened publicly (§1.11.4). For Customer Support: indirect prompt injection (Slack AI, EchoLeak). For Code-Modifying: autonomy-grant errors (Replit May 2025). For Text-to-SQL: cross-tenant aggregation (ConfusedPilot). For Deep Research: citation hallucination (Mata v. Avianca). For Embedded SaaS: action-on-behalf-of-user identity gap (Salesforce ForcedLeak). For Security: alert-fatigue mis-triage (no canonical public anchor yet; honest acknowledgment of `[evidence-thin]`).

Foundations is enough to answer both questions. Patterns adds the named-component mitigations; Production adds the audit-evidence flow.

### §1.12.7.3 Three customer conversations where Foundations alone is enough

Three customer scenarios where you can hold the entire conversation on the vocabulary in this chapter:

**(1) "We're considering building an agent. What do you think?"** Foundations alone is enough. Walk the workflow-vs-agent cut. Walk the ten-tier stack. Walk the three identity problems. Recommend a topology from §1.7.5. Identify the dominant governance category. End with the five disambiguating questions you will ask their engineering team next.

**(2) "We've read the Klarna case study. What's the honest read?"** Foundations alone is enough. Cite the CEO reversal (§1.11.3). Apply the MRM teachable point — vendor-disclosed metrics are not MRM evidence. Walk the routed-multi-agent topology. Walk why Klarna's metrics at launch were optimistic. Set expectations honestly for the customer's own deployment.

**(3) "Our security team wants to know about indirect prompt injection."** Foundations alone is enough. Walk Slack AI and EchoLeak (§1.11.4). Walk the five categorical surfaces (§1.11.2). Acknowledge that full mitigation is multi-component and lives in Patterns. Offer the follow-on technical session.

For everything beyond these three, Patterns and Production are where the rest of the conversation lives.

---

## §1.12.8 Worked-example progression

Spaced retrieval is the highest-impact study tool. Worked examples are the second-highest. The convention this book uses: every recipe has three levels of example progression in Patterns and Production.

- **Level 1:** the complete worked example — full state graph, all components labeled, every annotation present.
- **Level 2:** the partial scaffold — you fill in 3 named components.
- **Level 3:** the prompt-only — you build from scratch.

Foundations is too early in the curriculum for full progressions, but the gate (§1.16) operationalizes a Level-1 equivalent for each role track. The expectation: you read the model answer, identify which parts of your own attempt missed the model, and re-read the corresponding sections.

When you reach Patterns, you will see Level-2 scaffolds for the hero recipes (Customer Support / Klarna and Deep Research / Captide-shape FSI Plan-and-Execute). Production carries Level-3 prompt-only exercises and the capstone.

---

## §1.12.9 Common-confusion call-outs (consolidated)

The five near-neighbor confusions Foundations readers most often arrive at the gate carrying. Surface them now so they do not bite you in a customer conversation.

**(1) `interrupt()` vs `Command(goto=...)` vs `Command(resume=...)`.** Already covered in §1.4.12, but worth re-stating: `interrupt()` pauses, `Command(resume=...)` un-pauses, `Command(goto=...)` is in-node routing unrelated to pause/resume.

**(2) `PostgresSaver` vs `RedisSaver` vs `MemorySaver`.** All three implement the `Checkpointer` interface. The difference is durability and latency. **`PostgresSaver`** — production default; durable; co-locates with pgvector; ~tens-of-milliseconds latency. **`RedisSaver`** — production-capable; durable if Redis is configured for persistence; sub-millisecond latency; some customers use it as a write-through cache in front of Postgres. **`MemorySaver`** — **dev only**; in-memory; lost on restart; you will see it in every quickstart and tutorial; never deploy it.

**(3) MCP server vs MCP client vs `langchain-mcp-adapters`.** Already covered in §1.6.2, but worth re-stating: the **server** exposes; the **client** invokes from inside the agent runtime; the **host** is the user-facing app; `langchain-mcp-adapters` is a thin wrapper translating MCP `ToolMessage` to LangChain `ToolMessage` — it is **not** the protocol substrate. The MCP SDKs (Python, TS, Java, Go, C#) are the substrate.

**(4) Agent identity vs agent-on-behalf-of-user identity.** Already covered in §1.9, but worth re-stating: **agent identity** is the agent runtime's own identity (problem 2; SPIFFE, Entra Agent ID, workload identity). **Agent-on-behalf-of-user identity** is the delegation identity for actions in a user's name (problem 3; DPoP, RAR, CIBA, MCP Authorization). Conflating these is the most common identity-conversation failure in 2026.

**(5) ReAct vs Supervisor in the Klarna context.** Klarna's modal pattern is **routed multi-agent (closer to Supervisor than ReAct, single shared model)** per the LangGraph DevRel reading of the engineering blog and the Interrupt 2025 keynote. Not "ReAct alone," not "Supervisor with separate models per worker." If a customer asks how Klarna does it, use this phrasing. `[customer-produced-evidence]` `[corroborated]`

**(6) Buyer persona vs end-user persona.** Already covered in §1.10, but worth re-stating: the **buyer** is the economic buyer who approves the purchase. The **end-user** is the person who actually uses the product day-to-day. The **operator** is the person who manages the human team that operates alongside the agent. All three matter. Conflating buyer and end-user is the most common PM-track failure on the gate.

**(7) Vendor-disclosed vs independently-audited.** Already covered in §1.11.3 and in the citation taxonomy. Worth re-stating: vendor-disclosed metrics are useful for benchmarking and discussion. They are not MRM-validation evidence. They are not what a regulator wants in a model dossier. Klarna's 80% / 700-FTE-equivalent, Uber's 21K-developer-hours-reclaimed, LinkedIn's 95% accuracy, Komodo's 330M patient journeys are vendor marketing material. Use them as discussion anchors; do not commit them to a PRD as audit-grade claims.

---

## §1.12.10 The honest summary of where the field is in May 2026

A short closing scorecard on the state of the enterprise-agent field as of the May 2026 model cohort (Claude 4.7 / GPT-5 / Gemini 3.0). This is the framing you should have in your head before you walk into a customer conversation.

**What is solid as of May 2026.** LangGraph at production scale across FSI, ISV, and Healthcare (non-PHI) deployments. Postgres as the production-default checkpointer. LangSmith as the near-monopoly observability platform inside LangGraph deployments. MCP as the consensus protocol for agent-to-tool capability invocation, donated to LF AAIF in December 2025. The seven-topology catalog. The six recipe families. The named-incident corpus from Slack AI through Atlas. The Anthropic workflow-vs-agent discipline. The Klarna-CEO-reversal-as-honest-framing posture.

**What is in motion.** MCP Authorization (spec ratified Q1 2026; production evidence still thin). A2A adoption (150+ orgs supporting; production deployments smaller in scope than MCP's footprint). AGP / AGNTCY (youngest layer; adoption real but earlier in the curve). `deepagents` as the community's emerging "topology 8." LangGraph Functional API (~40% of new deployments; not yet fully documented for every production pattern). Microsoft Agent Framework convergence (AutoGen v0.4 → MAF Python preview; migration non-trivial). The whole agent-identity product wave — Entra Agent ID, Okta for AI Agents, Auth0 for AI Agents — all 2025-launched and still maturing.

**What is `[evidence-zero]` as of May 2026.** Sovereign deployments at scale on LangGraph. Insurance segment on LangGraph (68% of insurers running gen-AI; zero LangGraph footprint in the public corpus). PHI-in-production on LangGraph (everything Healthcare-side is `[reference design]`). LangGraph BYOC on Azure or GCP (AWS-only as of May 2026; Azure / GCP BYOC are roadmap items per LangChain public statements, not shipping). Federated agent collaboration across organizations using A2A at production scale. MCP supply-chain at production scale (the signature / attestation / SLSA-provenance story is still maturing).

**What you should be skeptical of.** Vendor-disclosed metrics (per the Klarna reversal). Procurement claims about "enterprise-ready" without decomposition into named regimes and named audit evidence. Claims that any framework has "solved" the cross-tenant isolation problem (no framework solves it — the customer-side multi-tier configuration solves it). Claims that "agentic AI" is mature in regulated industries (Level 4 fully-autonomous in regulated production does not exist). Claims that a hyperscaler-native stack is automatically simpler than LangGraph (the hyperscaler stack moves some complexity into the hyperscaler and reveals different complexity at the customer-control-plane and customer-data-residency layers).

**What is unknown.** Whether the insurance segment will adopt LangGraph as the FSI segment did. Whether Sovereign deployments will produce named-customer evidence by end of 2026. Whether MCP Authorization will see broad production adoption by mid-2027. Whether the Functional API will displace the Graph API as the default authoring surface. Whether AutoGen / MAF convergence completes cleanly or fragments. Whether Anthropic, OpenAI, or Google ships a fully-supported agent-platform tier that competes with LangGraph for the named-customer set.

These honest unknowns are part of the field guide. Where you do not know, say so. Where the evidence is thin, mark it. The customer's trust is built on accuracy, not on confidence.

---

## §1.12.11 A pre-gate checklist

Before you attempt the knowledge gate in §1.16, run yourself through this checklist. Each item below has a one-sentence test. If you cannot pass the test from memory in 1–2 seconds, re-read the named section before attempting the gate.

- **Workflow vs agent (§1.1).** *"In one sentence, what is the Anthropic distinction?"* — answer: workflows orchestrate LLMs on predefined code paths; agents have the LLM dynamically directing its own process and tool usage.
- **The ten tiers (§1.2).** *"Name the ten tiers in order from LLM to compute."* — LLM, retrieval, tools/MCP, identity, observability, state, secrets, policy, deploy, compute.
- **The three protocol layers (§1.6).** *"What sits above MCP, and what sits below?"* — A2A above (agent-to-agent), AGP below (transport / routing / identity).
- **The three state scopes (§1.5).** *"Where does the thread checkpointer fit? Where does `BaseStore` fit?"* — checkpointer is Scope 2 (per-thread); `BaseStore` is Scope 3 (cross-thread).
- **The three identity problems (§1.9).** *"Which is the new one?"* — Problem 3, agent acting on behalf of a user.
- **The seven topologies (§1.7).** *"Name them."* — ReAct, ReAct + Reflexion, Plan-and-Execute, Supervisor, Hierarchical, Agentic RAG, Network (Swarm).
- **The six recipes (§1.10).** *"Name the recipe and its anchor customer."* — Customer Support / Klarna, Code-Modifying / Uber + Replit, Text-to-SQL / LinkedIn + Vizient, Deep Research / Captide + Morningstar + Exa, Embedded SaaS Copilot / AppFolio + ServiceNow, Security Agents / Elastic.
- **Three named incidents (§1.11).** *"Slack AI, EchoLeak, Samsung — one sentence each on what went wrong."*
- **The Klarna reversal (§1.11.3).** *"In one sentence, what is the teachable point?"* — vendor-disclosed metrics are not MRM evidence under SR 11-7.
- **The five categorical surfaces (§1.11.2).** *"Name them."* — prompt injection (direct + indirect), telemetry capture, cross-tenant aggregation, action-provenance gaps, supply-chain compromise.
- **The four segment vignettes (§1.12.6).** *"FSI / Healthcare / ISV / Sovereign — what is the dominant failure mode for each?"* — indirect prompt injection (FSI), citation hallucination (Healthcare non-PHI), cross-tenant aggregation (ISV), no public evidence (Sovereign — structural fit only).

If you can pass all eleven tests from memory in under 30 seconds total, you are gate-ready. If not, the gate is harder than the test — re-read the sections you stumbled on.

**One more honest test.** When you read this chapter for the first time, did anything **surprise** you? The strongest signal of curriculum absorption is the ability to name what was new. If everything felt familiar, you have either skimmed the chapter or you are already past the Foundations level. If five things felt new, the chapter did its job. If twenty things felt new, you are exactly the reader this book was written for, and you should expect to re-read sections multiple times — that is the right experience for a Foundations chapter. The vocabulary will become reflexive over the next 60–90 days; do not expect it on day 1.

**A note on pacing.** This chapter is ~6–8 hours of read time if you do it cover-to-cover with the concept boxes. Most new hires take 2–3 sittings spread over the first week. The right cadence is roughly: §1.1–§1.4 in sitting 1 (~2 hours), §1.5–§1.9 in sitting 2 (~2.5 hours), §1.10–§1.15 in sitting 3 (~2 hours), §1.16 gate attempt + mentor checkpoint in sitting 4 (~1.5 hours). The chapter is intentionally larger than typical first-week reading because the vocabulary it teaches is the foundation for everything else in the book. Honor the time investment; it pays back over the next 12 months.

**A final reminder on the dual reading paths.** The engineer-track and the PM-track diverge most in §1.4. They re-merge in §1.5 and stay merged through the rest of the chapter. Patterns onward assumes both tracks have absorbed the same vocabulary from this chapter. If you skipped the §1.4 code blocks as a PM-track reader, that is exactly the right move; the concept boxes carry the meaning. If you skipped the concept boxes as an engineer-track reader, that is also fine; the code does the same work. The gate (§1.16) tests both tracks against the same scenario and asks for role-appropriate answers — the SE/SC and PM tracks are not separate gates on separate content; they are separate angles on the same vocabulary. Foundations is one chapter, one set of ideas, two reading paths.

**One last orientation note.** This Field Guide is licensed CC BY-SA 4.0. You are free to share it, fork it, annotate it, translate it. If you find a mistake, file an issue at the GitHub repo. If you find a section that did not teach you what it should have, file an issue. The book gets better with reader feedback; that is the whole point of the public license. The author affiliation and conflict-of-interest disclosure live in `CONFLICTS.md` at the repo root. The book is one input among many; treat it as such.

**Closing thought before Patterns.** The hardest part of agent work is not the technology. It is the discipline of holding multiple truths at once: that agents are real and useful, that the metrics are not yet what they need to be, that the governance is still maturing, that the customer is right to be skeptical, that the right architecture is still a recommendation made under uncertainty. Foundations gives you the vocabulary to hold those truths honestly. Patterns gives you the design criteria to act on them. Production gives you the audit evidence to defend them. The reader who finishes the three chapters and the capstone is the reader who can walk into a customer's CISO review and earn trust. That is the goal.

---

## §1.13 Reading paths reminder

If you have read this far, you have absorbed the same vocabulary regardless of track. Before the mid-tier retrieval break (§1.14) and the knowledge gate (§1.16), a quick reminder of where each role should focus the rest of their reading.

**Sales Engineer / Solution Consultant.** Your next read after Foundations is **Patterns**. The chapters that will pay off fastest:
- Patterns §2.4 Identity / Agent AuthZ — depth on the three problems from §1.9.
- Production §3.2 Cross-Tenant Isolation: the Five Surfaces — depth on the cross-tenant aggregation surface from §1.11.
- Patterns §2.2 — the 7-topology decision tree.
- Production §3.5 — per-regime depth for FSI / Healthcare / Sovereign conversations.

**Product Manager.** Your next read after Foundations is **Patterns**, with a focus on the persona × recipe × segment-variant matrix. The chapters that will pay off fastest:
- The 6 recipe families at Patterns depth, with per-customer engineering blog citations.
- The PRD-section template per recipe.
- The buyer-vs-end-user persona disambiguation in Patterns.

**Enterprise Architect (on-ramp).** Same as SE/SC, plus the 10-axis deployment matrix in Production.

**Engineer.** Both Foundations engineer-track passages and the LangGraph Studio quickstart are your starting points. Patterns §2.2 LangGraph topology deep-dive and Production diagrams are next.

---

## §1.14 Mid-tier retrieval break

Spaced retrieval is the highest-impact study tool in this curriculum. Before moving on to the glossary and the gate, answer the following twelve questions from memory. The answers live at the end of the section as a collapsible callout.

**Self-quiz (twelve questions).**

1. State the Anthropic workflow-vs-agent distinction in one sentence.
2. Name the five points on the autonomy spectrum, in order.
3. Name the ten tiers of the agent stack.
4. What does `[CKP]` stand for in this book's ASCII diagrams?
5. Name the three layers of the protocol stack (A2A / MCP / AGP) and the foundation each was donated to.
6. Name the three scopes of state in an agent.
7. What is the production-default LangGraph checkpointer? What is the dev-only one and why is it dev-only?
8. Name the three agent identity problems. Which one is the "new" one?
9. Name the seven canonical LangGraph topologies.
10. Name the six common use case families and the anchor customer for each.
11. Name three named public agent incidents from 2024–2025 and one sentence each on what went wrong.
12. State the Klarna CEO reversal teachable point in one sentence.

> **Answers (collapsed callout — review only after attempting from memory).**
>
> 1. **Workflows** are LLM-using systems orchestrated through predefined code paths; **agents** are systems where the LLM dynamically directs its own process and tool usage. `[vendor-public]`
>
> 2. Pipeline → Workflow → Chatbot → RAG → Agent → Fully-Autonomous. (Fully-autonomous in regulated industries does not exist in production as of mid-2026.)
>
> 3. (1) LLM, (2) Retrieval, (3) Tools / MCP plane, (4) Identity, (5) Observability, (6) State / checkpointer, (7) Secrets, (8) Policy / guardrails, (9) Deploy / runtime control plane, (10) Compute.
>
> 4. Checkpoint write — the runtime persists state at this point.
>
> 5. **A2A** (top, agent-to-agent, donated to Linux Foundation by Google June 2025), **MCP** (middle, agent-to-tool, JSON-RPC, donated to LF Agentic AI Foundation by Anthropic December 2025), **AGP / AGNTCY** (bottom, transport / routing / identity, donated to Linux Foundation by Cisco Outshift July 2025).
>
> 6. **Scope 1**: step state / scratchpad (within one agent step, not persisted). **Scope 2**: thread state / conversation state (across turns of one conversation, persisted by checkpointer). **Scope 3**: long-term memory (across conversations, persisted by `BaseStore`).
>
> 7. Production default: **`PostgresSaver` / `AsyncPostgresSaver`** (co-locates with pgvector; LangGraph deploy guide commits to Postgres as production). Dev-only: **`MemorySaver`** (in-memory; lost on restart; not durable; explicitly "not for production" per LangGraph docs). `SqliteSaver` is also dev-only.
>
> 8. **(1)** Who is the user? (Solved.) **(2)** Who is the agent / workload? (Mostly solved.) **(3)** On whose behalf is the agent acting? **(The new one.)** 2025–2026 OAuth and IDP products are operationalizing #3.
>
> 9. ReAct, ReAct + Reflexion, Plan-and-Execute, Supervisor, Hierarchical, Agentic RAG, Network (Swarm). `deepagents` is the community's emerging "topology 8."
>
> 10. **Customer Support Copilot** (Klarna), **Code-Modifying Developer Agents** (Uber, Replit), **Text-to-SQL / Conversational Analytics** (LinkedIn, Vizient), **Multi-Agent Deep Research** (Captide, Morningstar, Exa), **Embedded SaaS Copilot** (AppFolio, ServiceNow), **Security Agents** (Elastic).
>
> 11. **Slack AI (Aug 2024)** — public-channel prompt-injection payload exfiltrated private-channel content via Markdown link; **EchoLeak / CVE-2025-32711 (June 2025)** — zero-click prompt injection in Microsoft 365 Copilot via crafted email picked up in RAG; **Samsung ChatGPT leak (April 2023)** — engineers pasted proprietary source code into ChatGPT, driving the BYOC and self-hosting demand wave.
>
> 12. Vendor-disclosed metrics are not Model Risk Management (MRM) evidence under SR 11-7. The metrics at launch overstated steady-state performance, and Klarna's CEO publicly walked back the framing in May 2025.

If you got 10+ correct from memory, you are ready for the gate. If you got fewer than 8, re-read the corresponding sections before attempting the gate. The gate is harder than the quiz, and the gate without the vocabulary is not a useful exercise.

---

## §1.15 Foundations Glossary (top ~50 terms)

This is the chapter-local glossary. The canonical, first-use-linked terminology reference for the whole book lives in `04-glossary.md`. The Foundations glossary surfaces the ~50 terms a new hire must hold in working memory.

> **Two reading modes (per EYE M4 fix).** This glossary is organized as a **conceptual learning map** — terms grouped into eleven sub-clusters with an organizing principle named per cluster, for new readers building schema. For an **alphabetical reference index** suitable for lookup, see `04-glossary.md` at the repo root (the canonical, first-use-linked book-wide glossary). The five top-level conceptual categories the eleven sub-clusters fall under: (1) Architectural primitives — agent / state / runtime; (2) Vendor-specific primitives — LangGraph-named APIs; (3) Protocols — A2A / MCP / AGP and OAuth-family identity; (4) Failure modes and governance; (5) Audience vocabulary — buyer / operator personas and recipe families.

### Agent and autonomy

- **Agent.** A system in which an LLM dynamically directs its own process and tool usage (Anthropic). Broader vendor definitions (LangChain, OpenAI) treat any LLM + tools + state as an agent. See §1.1.
- **Agentic system.** Anthropic umbrella term covering both workflows and agents.
- **Autonomy spectrum.** A five-level scale from advisor (Level 0) to fully autonomous (Level 4). Regulated production deployments live at Levels 2–3.
- **Workflow.** LLM-using system orchestrated on predefined code paths; the LLM does not choose its own next action (Anthropic). Contrasted with agent.
- **Pipeline.** Deterministic DAG of steps, possibly including model inference; no agent loop.
- **Chatbot.** Multi-turn conversational LLM with history; no tools or limited tools; orthogonal to the agent concept.
- **RAG (Retrieval-Augmented Generation).** Pattern where retrieved documents are injected into the LLM context before generation. Not an agent unless the LLM chooses when and how to retrieve.
- **Agentic RAG.** RAG with agent-loop semantics — the LLM decides when to retrieve, critiques results, re-queries. Becomes an agent.

### State, memory, persistence

- **State.** Any data the agent carries across operations. See §1.5.
- **State graph (`StateGraph`).** A LangGraph object defining nodes (functions), edges (transitions), and the shared state schema.
- **Scratchpad.** Intra-step intermediate reasoning held in state; the ReAct Thought trace lives here.
- **Thread.** A single conversation with an agent. Identified by `thread_id`.
- **`thread_id`.** The string identifier for a thread. Passing the same `thread_id` resumes the conversation.
- **Checkpointer.** The component that persists state across thread turns. `PostgresSaver`, `RedisSaver`, `MemorySaver`. Compiled via `compile(checkpointer=...)`.
- **Checkpoint.** A versioned snapshot of state at a node transition.
- **`BaseStore`.** LangGraph's long-term memory interface for cross-thread state. `InMemoryStore`, `PostgresStore`, `RedisStore`. Compiled via `compile(store=...)`.

### Tools and protocols

- **Tool.** A function (or resource, or prompt) the LLM can invoke.
- **Tool call.** An LLM emission requesting a tool be invoked, with structured arguments.
- **Function calling.** LLM-native tool calling — the LLM emits structured JSON describing the call. OpenAI's productization of the Toolformer thesis (Schick et al. 2023).
- **MCP (Model Context Protocol).** JSON-RPC protocol from Anthropic (November 2024) for exposing tools to LLM clients. Donated to LF Agentic AI Foundation December 2025.
- **MCP server / client / host.** Server exposes; client invokes from inside the agent; host is the user-facing app (Claude Desktop, Cursor).
- **MCP resource / tool / prompt.** The three MCP primitive types.
- **MCP Authorization.** OAuth 2.1 + DCR + RFC 9728 spec for MCP server / client identity. Ratified Q1 2026; production evidence still thin.
- **A2A (Agent2Agent).** Google-originated protocol for agent-to-agent collaboration. Donated to Linux Foundation June 2025. Sits ABOVE MCP.
- **AGP (Agent Gateway Protocol).** Cisco / AGNTCY-originated routing layer for inter-agent traffic. Donated to Linux Foundation July 2025. Sits BELOW MCP.
- **AGNTCY.** Cisco / Outshift multi-component project including discovery, identity, messaging (SLIM), and observability.

### Patterns and topologies

- **ReAct.** Single-agent reason+act loop (Yao et al. 2022, ICLR 2023). The most-deployed LangGraph pattern.
- **Reflexion.** Self-critique technique (Shinn et al., NeurIPS 2023).
- **Plan-and-Execute.** Planner LLM + executor LLM + replanner LLM pattern. `deepagents` harness is a Plan-and-Execute implementation.
- **Tree of Thoughts.** Search-over-thoughts planning technique (Yao et al., NeurIPS 2023).
- **Toolformer.** Self-supervised tool-calling training paper (Schick et al., NeurIPS 2023).
- **Supervisor.** Multi-agent topology with one routing agent and N specialist workers. `langgraph-supervisor-py` harness.
- **Hierarchical.** Supervisor-of-supervisors topology. Recursive structure.
- **Network (Swarm).** Peer-to-peer multi-agent topology with no central supervisor. Renamed from "Multi-Agent Collaboration" to match LangGraph docs. `langgraph-swarm-py` harness.

### Human in the loop

- **HITL (Human-in-the-Loop).** Pattern where the agent pauses, surfaces what it is about to do, and waits for human approval.
- **`interrupt(value)`.** LangGraph primitive that pauses execution mid-node and surfaces a value to the calling code.
- **`Command(resume=...)`.** LangGraph primitive that resumes a paused thread with the resume value.
- **`Command(goto=...)`.** LangGraph primitive for in-node dynamic routing — unrelated to pause/resume.

### Observability

- **Trace.** Full record of a single agent run.
- **Span.** A single sub-operation within a trace. Spans nest.
- **Run.** LangSmith-vocabulary equivalent of trace.
- **LangSmith.** LangChain's first-party trace + eval platform. Near-monopoly inside LangGraph deployments.
- **Langfuse.** OSS / self-hostable alternative.
- **Phoenix.** OSS sibling of Arize AX (commercial). Distinct products.
- **OpenTelemetry GenAI semantic conventions.** Open standard for LLM / agent trace fields.
- **OpenInference.** Arize-submitted OpenTelemetry convention extension.

### Identity and authorization

- **Agent identity.** The identity of the agent runtime / workload itself (Problem 2 in §1.9).
- **Agent-on-behalf-of-user identity.** Delegation identity for the agent acting in a user's name (Problem 3 in §1.9).
- **DPoP (RFC 9449).** Demonstrating Proof-of-Possession. Binds access tokens to a key pair. Mitigates token theft.
- **PAR.** Pushed Authorization Requests.
- **RAR.** Rich Authorization Requests — structured transaction-detail payload.
- **CIBA.** Client-Initiated Backchannel Authentication. Decoupled flow.
- **Step-up authentication.** Escalating auth strength for high-risk actions.
- **PKCE.** Proof Key for Code Exchange. OAuth 2.0 extension; standard for agent auth code flow.
- **FGA (Fine-Grained Authorization).** Authorization decisions based on relationships and attributes, not just roles.
- **ReBAC.** Relationship-Based Access Control.
- **OpenFGA.** CNCF-sandbox open-source ReBAC implementation.
- **Cedar / AWS Verified Permissions.** Amazon-authored policy language; ReBAC-capable.
- **Topaz.** Aserto product combining RBAC + ABAC + ReBAC.
- **SPIFFE / SPIRE.** Workload identity standard and runtime.
- **Action provenance.** The cryptographic chain of evidence for an agent action.
- **Signed action chain.** Implementation of action provenance — each step is cryptographically signed (KMS-backed).

### LangGraph primitives

- **`StateGraph`.** The LangGraph graph builder.
- **`MessagesState`.** Default state schema with a `messages` list field.
- **`add_messages` reducer.** Reducer that appends or merges messages.
- **`@entrypoint` / `@task`.** Functional API decorators (imperative authoring path).
- **`create_react_agent`.** Prebuilt helper for the ReAct loop.
- **`Send` API.** Fan-out primitive for parallel sub-invocations.
- **Subgraph.** A `StateGraph` used as a node inside another `StateGraph`.
- **LangGraph Studio.** Visual debugger for LangGraph.
- **`langgraph dev` / `up` / `build`.** CLI commands for dev, deploy, and artifact build.

### Checkpointers and stores

- **`PostgresSaver` / `AsyncPostgresSaver`.** Production-default thread checkpointer.
- **`RedisSaver`.** Sub-millisecond alternative.
- **`MemorySaver` / `SqliteSaver`.** Dev-only.
- **`PostgresStore`.** Production-default cross-thread `BaseStore`.
- **`RedisStore`.** Redis-backed store with native vector search.

### Governance categories

- **Prompt injection (direct).** Attacker controls user input and embeds malicious instructions.
- **Prompt injection (indirect).** Attacker controls data the agent retrieves; the agent treats the data as instructions.
- **Hallucination.** LLM produces a false claim presented as fact.
- **Hallucination-to-action.** Hallucination that triggers a real-world action.
- **Cross-tenant aggregation.** State, cache, retrieval, or memory leaking between tenants.
- **Telemetry capture.** PII / regulated data ending up in trace platforms outside the trust boundary.
- **Action provenance gap.** Audit trail cannot reconstruct who authorized an agent action.
- **Supply-chain compromise.** Tool, MCP server, or dependency is malicious or compromised.

### PM-track vocabulary

- **JTBD (Jobs to Be Done).** Christensen-lineage framework for stating user needs as jobs: "When [situation], I want to [motivation], so I can [outcome]."
- **ICP (Ideal Customer Profile).** The customer segment the product is built for.
- **Buyer persona.** The economic buyer who approves the purchase.
- **End-user persona.** The person who actually uses the product day-to-day. Often different from the buyer.
- **ACV (Annual Contract Value).** Dollar value of one customer-year.
- **Discovery call.** The first sales conversation; SE / SC role is to surface use case + technical fit.
- **MRM (Model Risk Management).** The FSI governance discipline for managing model risk; formalized in SR 11-7 (Federal Reserve / OCC). Vendor-disclosed metrics are not MRM evidence.

---

## §1.16 Knowledge Gate — Foundations

This is the exit gate for the Foundations chapter. The gate has three role-tracks; you should attempt the one that matches your role. If you are a generalist or are still figuring out which track you fit, attempt all three — the time investment is ~90 minutes total, and the exercise is the most valuable single hour in this chapter.

**Format of each track.**

- **Model brief (2 paragraphs).** The customer scenario.
- **Model answer (~1–1.5 pages, A-grade).** What a passing response looks like, with annotations explaining what makes it pass.
- **Rubric (5–6 evaluation criteria).** Each criterion has a `pass / partial / fail` definition.
- **Named evaluator.** Team lead or peer mentor with at least one production agent deployment. Self-evaluation against the rubric is the documented fallback if no mentor is available.
- **Retake mechanic.** If you fail or partial: re-read the named sections, then retake against an alternate brief from Patterns §2.12 after a 48-hour cooldown.

### §1.16.1 Track 1 — Sales Engineer / Solution Consultant gate

**Model brief.**

> A consumer-facing fintech (Klarna-scale; primarily payments and short-term lending) is asking how to add a customer support agent on top of their existing RAG-based help center. Their current state: a single LLM call per user query that retrieves from a vector store of product documentation and policy pages, then generates a response. Roughly 60% of queries resolve in one turn; the remaining 40% escalate to a human agent. They have read industry coverage of Klarna's AI Assistant and want to understand (a) what is meaningfully different about "an agent" vs their current system, (b) what would change in their architecture, and (c) what the obvious governance risk would be.
>
> They have an existing identity stack (Okta for workforce; custom JWT for customer sessions), Postgres at scale (for the application), Datadog for observability, and a security team that has just begun reading the OWASP LLM Top 10. They have not committed to a framework. They want a 30-minute first-pass technical conversation; you have the slot.

**Model answer (A-grade, ~1.5 pages).**

> The first thing I want to land is that what you have today is not yet an agent in the strict sense — it is a RAG-augmented LLM pipeline. The cleanest definition we use comes from Anthropic's *Building Effective Agents* essay: a **workflow** is an LLM-using system orchestrated through predefined code paths, and an **agent** is a system where the LLM dynamically directs its own process and tool usage. Your current system is closer to a workflow with a single LLM call. An agent would mean the LLM choosing which tools to call (lookup, refund, escalate, send-message) and looping until it decides it is done.
>
> The architectural changes that would matter: **(1)** a stateful runtime that persists conversation state across turns (today, you regenerate each response in isolation; an agent maintains a thread); **(2)** a set of tools beyond retrieval that the LLM can choose to call — lookup-account, lookup-order, place-refund, escalate-to-human; **(3)** a checkpointer behind the agent — `PostgresSaver` is the production default and would co-locate with your existing Postgres; **(4)** an observability layer that captures every span — your existing Datadog can ingest OpenTelemetry GenAI semantic conventions, but LangSmith is the LangGraph-native choice and offers zero-code auto-instrumentation; **(5)** a human-in-the-loop pause point — for any consequential action (refund above a threshold, account modification, escalation), the agent surfaces an `interrupt()` and waits for a human approval before continuing.
>
> The obvious governance risk: **indirect prompt injection via tool results and retrieved documents**. Today, your RAG system reads documentation and policy pages — sources you control. An agent reading user-submitted content, third-party data, or tool results from external APIs is exposed to the EchoLeak class of attack (zero-click prompt injection via crafted content) and the ConfusedPilot class (cross-tenant aggregation via retrieval). The mitigation is multi-component — guardrails at input and output, structured output schemas, tool-call gates, per-tenant retrieval predicates — and we should walk through your specific architecture in a follow-on session. The named anchor I want to put in front of your security team is the Klarna CEO reversal of May 2025: vendor-disclosed metrics are not Model Risk Management evidence. If you are going to defend this deployment to your audit committee, the metrics at launch will not be what they ask for.
>
> A specific recommendation for your context: start with **LangGraph + `create_react_agent` + `PostgresSaver` + Okta-for-workforce identity for the operator side and your existing customer JWT for the user side**. Add a HITL `interrupt()` at the refund-placement node. Stream `updates` to your UI. Wire LangSmith as the primary trace platform — your existing Datadog can be the secondary destination via OpenTelemetry. The deployment shape that fits a Klarna-scale operation is **Self-Hosted Enterprise** (your own Kubernetes; LangChain control-plane separate), not LangGraph Cloud — that is a compliance decision, not a feature decision. Three components I would defer: long-term `BaseStore` memory (start with thread-only; add cross-thread when you have evidence you need it), Network/Swarm topology (you do not have a multi-agent problem yet; one agent with the right tools is enough), and MCP Authorization at production scale (the spec ratified Q1 2026, but production evidence is still thin — wait for the customer-evidence wave).
>
> I want to leave you with one question for your security team: what does your action provenance story look like? Six months from now, if a regulator asks "who authorized this refund," your audit trail has to trace through the user assertion, the agent identity, the planner decision, the tool call, and the outcome. That chain does not exist in your current RAG pipeline. It needs to be designed in from day one.

**Rubric (six criteria).**

| Criterion | Pass | Partial | Fail |
|---|---|---|---|
| **1. Workflow-vs-agent disambiguation** | Cites the Anthropic distinction and applies it to the customer's current state | Distinguishes the concepts but doesn't ground in the customer's RAG pipeline | Treats "agent" as undifferentiated from RAG |
| **2. Architectural changes named** | Names 4+ of: stateful runtime, tools-beyond-retrieval, checkpointer, observability, HITL — with specific LangGraph primitives | Names 2–3 with some specificity | Vague or product-pitch language |
| **3. Governance risk identified** | Names indirect prompt injection AND cross-tenant aggregation, with at least one named-incident anchor (Slack AI, EchoLeak, or ConfusedPilot) | Names one risk class with one anchor | Generic "we'd add guardrails" |
| **4. Honest framing on Klarna metrics** | Names the Klarna CEO reversal AND explicitly says vendor-disclosed metrics are not MRM evidence | Mentions the reversal without the MRM teachable point | Quotes Klarna's launch metrics as evidence |
| **5. Specific deployment-shape recommendation** | Names Self-Hosted Enterprise (or defends BYOC AWS with caveats) with a compliance rationale | Recommends a shape without rationale | Recommends Cloud SaaS for a Klarna-scale FSI deployment |
| **6. Action provenance question raised** | Closes by introducing the action-provenance question, identifying it as the audit-evidence requirement | Hints at audit without naming the provenance chain | Skips the regulator-facing question entirely |

A passing answer hits 5/6 with no fails. A partial-pass hits 4/6 with at most one fail. Two or more fails means re-read §1.1, §1.9, §1.10.1, and §1.11 and retake against an alternate brief.

### §1.16.2 Track 2 — Product Manager gate

**Model brief.**

> Same customer scenario as Track 1. You are the PM tasked with writing the product brief that goes to engineering. The CISO has already weighed in that they want to see "JTBD framing, persona disambiguation, and an honest read on the dominant governance category" before they will green-light the engineering scoping. You have one page.

**Model answer (A-grade, ~1 page).**

> **Jobs-to-Be-Done (end-user).** When a customer contacts support with a transactional question or request — a refund query, an order status check, a policy clarification — the customer wants the issue resolved (or cleanly escalated) without explaining context to multiple humans, so they can complete the underlying purchase, return, or dispute they were trying to do. The current RAG-augmented help center resolves ~60% of queries in one turn; the remaining 40% escalate and incur context-restart cost. The agent's job is to compress the 40% escalation rate by handling multi-turn, multi-tool resolution in a single conversation.
>
> **Jobs-to-Be-Done (buyer).** When a customer-experience leader is staffing a 24×7 support function under SLA against linear headcount growth, the buyer wants automated resolution of high-volume routine inquiries with reliable escalation on exceptions, so they can hit response-time SLAs while holding headcount flat. The buyer is the VP of Customer Experience; the operator is the CX operations leader who manages the human team; the end-user is the customer.
>
> **Buyer persona vs end-user persona.**
> - **Buyer:** VP of Customer Experience. Cares about: per-conversation resolution rate, escalation rate, SLA attainment, cost per resolved conversation, customer satisfaction (CSAT) trend.
> - **Operator persona:** CX Operations Manager. Cares about: hand-off quality (does the human get clean context?), escalation queue depth, agent-of-the-agent visibility (can the operator see what the agent did and why?), HITL gating workflow.
> - **End-user persona:** the customer (segmented by behavior: high-frequency buyer, dispute-heavy customer, first-time user). Cares about: resolution, time-to-resolution, not having to repeat context, and (newly) trust signals — that the agent will not make up policy.
>
> **Dominant governance category.** This deployment falls in the **FSI / Payments** sub-segment. The applicable regimes are PCI DSS 4.0 (the deployment is in PCI scope), GDPR Art. 5(1)(b) and Art. 28 (EU customers; cross-border processing), DORA Art. 5 / 6 / 19 (ICT operational resilience and incident reporting for EU operations), and SR 11-7 (for the model-risk angle if this is operating in the US). The dominant failure mode for this recipe class — Customer Support Copilot — is **indirect prompt injection via retrieved content and tool results**, with **cross-tenant aggregation in the retrieval layer** as the second risk class. The Klarna CEO reversal of May 2025 is the customer-class anchor for honest expectation-setting; the metrics at launch will not survive an MRM review.
>
> **Evidence-class notes.** All deployment metrics from comparable Klarna-class customers are `[customer-produced-evidence]`-tagged, not `[independently-audited]`. Any claim about steady-state resolution rates in the PRD must carry that tag and the SR 11-7 teaching: vendor-disclosed metrics are not MRM-validation evidence. The PRD section on expected resolution rates will pin numbers as targets, not claims, and will require a 90-day production validation window before the numbers become commitments.
>
> **Open questions for the CISO sign-off.** (1) What is the deployment shape (Cloud, BYOC, Self-Hosted)? — answer determines the LangGraph compliance posture. (2) What is the action provenance design? — required for audit trail under DORA Art. 19 and SEC 17a-4 if applicable. (3) Where is HITL placed? — refund threshold, account modification, escalation. The recommended starting point is a `$500` refund threshold with `interrupt()` at the place-refund node.

**Rubric (five criteria).**

| Criterion                                   | Pass                                                                                                | Partial                                          | Fail                                        |
| ------------------------------------------- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------ | ------------------------------------------- |
| **1. JTBD discipline (end-user AND buyer)** | Both stated using the JTBD form ("When X, I want Y, so I can Z"), grounded in the customer scenario | One stated cleanly, the other partial or generic | Generic problem statement; no JTBD form     |
| **2. Buyer vs end-user disambiguation**     | Names the buyer (VP CX), the operator (CX Ops), and the end-user with distinct concerns for each    | Distinguishes two of three with concerns         | Conflates buyer and end-user                |
| **3. Governance category named**            | FSI / Payments with at least 2 specific regulator-clause citations                                  | Names FSI but without specific clauses           | Generic compliance language                 |
| **4. Klarna reversal cited honestly**       | Names the reversal AND applies the "metrics are not MRM evidence" teaching                          | Names the reversal without the MRM application   | Quotes Klarna's launch metrics uncritically |
| **5. Open questions to CISO**               | Names 3 specific questions including deployment shape, action provenance, and HITL placement        | Names 2 questions with some specificity          | Generic questions or none                   |

A passing answer hits 4/5 with no fails. Partial-pass hits 3/5 with at most one fail.

### §1.16.3 Track 3 — Engineer-curious gate

**Model brief.**

> Same customer scenario. The engineering lead has asked you to wire up a minimal LangGraph ReAct agent that demonstrates: (1) a Postgres checkpointer; (2) a human-in-the-loop interrupt at the refund-placement step; (3) three tools the agent can call (`lookup_account`, `place_refund`, `escalate_to_human`); (4) per-tenant configuration via `thread_id` and `tenant_id`. After the code, identify three places this minimal design would fail in production.

**Model answer (A-grade, code plus three production failure modes).**

```python
import asyncio
from typing import Annotated, Literal
from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.prebuilt import create_react_agent
from langgraph.types import interrupt, Command
from langgraph.graph import StateGraph, START, END, MessagesState

# -- Tools ----------------------------------------------------------------

def lookup_account(account_id: str, tenant_id: str) -> dict:
    """Look up the account in the customer database. Tenant-scoped."""
    # Real impl: a SQL query with per-tenant predicate.
    return {"account_id": account_id, "tenant_id": tenant_id, "balance": 142.50}

def place_refund(account_id: str, amount: float, reason: str) -> dict:
    """Place a refund. Must be HITL-gated above $500."""
    if amount > 500:
        # Pause and surface the decision to a human.
        approval = interrupt({
            "type": "approve_refund",
            "account_id": account_id,
            "amount": amount,
            "reason": reason,
        })
        if approval != "approve":
            return {"status": "denied", "reason": "Human declined"}
    # Real impl: idempotent refund API call.
    return {"status": "refunded", "account_id": account_id, "amount": amount}

def escalate_to_human(account_id: str, summary: str) -> dict:
    """Escalate the conversation to a human agent."""
    return {"status": "escalated", "queue_id": "cs-tier2"}

TOOLS = [lookup_account, place_refund, escalate_to_human]

# -- Agent ----------------------------------------------------------------

async def main():
    # Production: real Postgres URL, not localhost.
    async with AsyncPostgresSaver.from_conn_string(
        "postgresql://app:app@localhost:5432/agent"
    ) as checkpointer:
        await checkpointer.setup()

        model = ChatAnthropic(model="claude-opus-4-7-20260315")
        agent = create_react_agent(
            model=model,
            tools=TOOLS,
            checkpointer=checkpointer,
        )

        # Per-tenant invocation.
        config = {"configurable": {
            "thread_id":  "alice-2026-05-24",
            "tenant_id":  "klarna-eu",
            "user_id":    "alice@example.com",
        }}

        # Initial call.
        async for chunk in agent.astream(
            {"messages": [{"role": "user", "content": "I want a refund of $750 on order #1234."}]},
            config=config,
            stream_mode="updates",
        ):
            print(chunk)

        # The agent hit interrupt() at place_refund (amount > $500).
        # Resume after a human approves.
        async for chunk in agent.astream(
            Command(resume="approve"),
            config=config,
            stream_mode="updates",
        ):
            print(chunk)

asyncio.run(main())
```

**Three production failure modes this design has.**

**(1) The per-tenant predicate is in the tool, not enforced at the checkpointer or the retrieval layer.** The `lookup_account` tool takes a `tenant_id` argument, but nothing in the agent runtime forces the agent to pass the right tenant. A prompt-injection or LLM hallucination could pass a different `tenant_id`, and the SQL predicate would honor it. In production, the per-tenant predicate must be bound to the authenticated identity at the checkpointer layer and the retrieval layer, not at the tool argument layer. The named mitigation: per-tenant `thread_id` namespacing in the checkpointer (e.g., `thread_id = f"{tenant_id}:{user_thread_id}"`), Postgres row-level security on the checkpointer table, and binding the `tenant_id` into the `RunnableConfig.configurable` so it cannot be overridden by an LLM-generated tool argument. The Cross-Tenant Isolation chapter in Production §3.2 walks the five surfaces.

**(2) The action provenance chain is missing.** There is no signed action chain. If a regulator asks "who authorized this $750 refund," the trail consists of (a) the user's HTTP session, which may not be signed; (b) the LLM's reasoning, which is not signed; (c) the human approval, which is not bound to a user identity; (d) the tool-call result, which is not signed. In production, each step in the chain must be cryptographically signed (KMS-backed; HSM for the chain anchor; ECDSA P-256 or Ed25519), and the resulting chain must be WORM-stored (S3 Object Lock Compliance mode for SEC 17a-4 retention). The Audit-Evidence Cookbook in Production §3.4 covers what gets signed, where, by whom.

**(3) The HITL approval is not bound to an authenticated human identity.** The `Command(resume="approve")` call accepts any string. There is no requirement that the approver be authenticated as a CX Ops user with refund-approval authorization. In production, the resume must carry a signed approval token from the operator's IDP (Okta, Entra), the operator's identity must be authorized via FGA (OpenFGA or Cedar) for the specific refund amount, and the entire approval action must enter the signed action chain. The named mitigations: Okta for AI Agents (or Auth0 for AI Agents) for the operator identity; OpenFGA or Cedar for the relationship "operator X is authorized to approve refunds for tenant Y up to amount Z"; step-up authentication (fresh MFA) for refunds above a tier-2 threshold. Patterns §2.4 covers the identity stack.

**Rubric.**

| Criterion | Pass | Partial | Fail |
|---|---|---|---|
| **1. Working `create_react_agent` with Postgres checkpointer** | All four required elements present: `AsyncPostgresSaver`, `create_react_agent`, three tools, HITL `interrupt()` | Missing one element | Missing two or more |
| **2. `thread_id` and `tenant_id` per-tenant config** | Both in `RunnableConfig.configurable`; `thread_id` is unique per user | One present without the other | Missing both |
| **3. HITL `interrupt()` placement** | At `place_refund` above threshold; `Command(resume=...)` shown | Interrupt present but threshold logic missing | No interrupt |
| **4. Identifies cross-tenant predicate failure** | Names the per-tenant predicate-binding problem with at least one named mitigation | Identifies the failure mode but no mitigation | Misses the failure mode |
| **5. Identifies action provenance gap** | Names the unsigned chain with at least one named mitigation (KMS, WORM, HSM) | Identifies the gap without named mitigation | Misses |
| **6. Identifies HITL identity-binding failure** | Names that the approval is not bound to an authenticated identity with at least one named mitigation (Okta for AI Agents, FGA, step-up auth) | Identifies the gap without named mitigation | Misses |

A passing answer hits 5/6 with no fails. Partial-pass hits 4/6 with at most one fail.

---

## §1.17 Mentor Checkpoint #1

You have completed the Foundations chapter and attempted the knowledge gate. Before continuing to Patterns, schedule **~30 minutes** with your team lead or mentor — someone who has shipped at least one production agent. The mentor checkpoint is not a re-test of the gate. It is a structured conversation about where the vocabulary felt wobbly and where to focus your next reading.

**Suggested agenda for the 30-minute conversation.**

- **Minute 0–5.** You walk through your gate answer. The mentor reads and reacts. Disagreements at this point are the most valuable signal.
- **Minute 5–10.** Where did the vocabulary feel wobbly? (Most-likely candidates from new-hire experience: the cut between Scope 2 and Scope 3 state; the three identity problems; the seven topologies; the MCP / A2A / AGP layering.)
- **Minute 10–15.** Which of the three identity problems is novel to you? Most new hires have never thought about Problem 3 (agent-on-behalf-of-user) before reading Foundations.
- **Minute 15–20.** Which of the six recipes feels most familiar from your prior work? (This will determine which Patterns chapters you read first.)
- **Minute 20–25.** What is the customer engagement that will likely test this knowledge first? The mentor's read on which customers in the pipeline match your vocabulary is the most valuable input here.
- **Minute 25–30.** What is the one thing the Foundations chapter should have taught you but did not? (Honest feedback for the curriculum.)

**If no mentor is available.** Use the rubric in §1.16 to self-evaluate. Be honest. Self-assessment has documented false-positive rates above 50% in similar curricula; if you find yourself rating every criterion as `pass`, re-read the chapter and try again. The gate is harder than it looks; passing it the first time is uncommon.

---

## §1.17.1 First 30 days — a focused reading and practice plan

If you are reading this in your first week at OPAQUE Systems (or in your first week at any agent-adjacent role), the chapter you just finished is the foundation. The next 30 days have a shape worth committing to. The plan below is the one Aaron's team has worked out as the modal new-hire path; adjust for your role and prior experience.

**Week 1 (the chapter you just finished).** Read 01-foundations.md end-to-end. Attempt the §1.16 gate for your role track. Schedule the 30-minute mentor checkpoint (§1.17). Begin daily Anki review on the 60–80-card deck. **Expected outcomes:** vocabulary intact; the five disambiguating questions feel natural to ask; the three identity problems are distinct in your head; the seven topologies and six recipes are named without hesitation.

**Week 2 (start Patterns).** Begin 02-patterns.md. The chapters to read first depend on your role. For SE/SC: §2.4 Identity / Agent AuthZ; §2.7 Governance (incl. Cross-Tenant Isolation Category 1); §2.1 Framework comparison matrix. For PM: §2.3 use-case recipe walkthroughs; the PRD-section templates. Continue daily Anki. **Expected outcomes:** you can defend a framework choice; you can sketch a per-tenant isolation pattern; you understand DPoP / RAR / CIBA / step-up at depth.

**Week 3 (continue Patterns).** Finish 02-patterns.md. Pay particular attention to the cross-tenant isolation surfaces (retriever, cache, checkpointer, observability, model) and the seven-topology decision tree. Begin shadow-attending discovery calls if you can. **Expected outcomes:** you can pick a topology from a customer brief and defend it; you can name the cross-tenant isolation pattern for a multi-tenant ISV use case; you have a working draft of the framework matrix for your top-3 prospect engagements.

**Week 4 (Production overview + first independent customer touchpoint).** Begin 03-production.md. Focus on the 10-axis deployment matrix; per-regime depth for whichever regimes match your top prospects; the Audit-Evidence Cookbook chapter. Attempt your first independent customer pre-brief using co-meetings (or your role-equivalent prep tool). **Expected outcomes:** you can walk a CISO through the deployment-shape decision; you can defend a deployment against one specific regulator clause; you have completed at least one customer-facing brief that a veteran approves of.

**Day 30 milestone — the capstone.** End-of-month, attempt the Production capstone task (Production Knowledge Gate Track 3): all three role tracks (SE / SC / PM) produce artifacts against the same customer brief. If you are a generalist, all three are your responsibility; if you are role-specialized, you produce your one and review the others. The capstone is the signal that onboarding is complete. The day-60–90 horizon is when the capstone is fully realistic; day 30 is the first credible attempt.

**Throughout.** Daily Anki review for the first 14 days; tri-daily for the next 30. Schedule the four mentor checkpoints from the design spec: post-Foundations (~30 min, you just did this), post-Patterns-Identity (~20 min on FGA / DPoP / agent-on-behalf-of articulation), pre-Production whiteboard (~45 min practice with a veteran SE), post-Production gate (~45 min review of PRD / brief / whiteboard photo). Total mentor time across the curriculum: ~2.5 hours. The new-hire failure mode this prevents is feeling ready alone.

The honest framing: **Foundations is two weeks of absorbable core; Patterns and Production are multi-month ongoing reference plus capstone-when-ready around Day 60–90.** Do not let anyone tell you the whole 500-page Field Guide is two-week-readable. The Foundations chapter you just finished is.

---

## §1.17.2 Why agents are not "just better workflows"

A perspective worth holding before you leave the chapter. The most common framing mistake from experienced enterprise-software practitioners is to treat agents as "just better workflows" or "just smarter automation." This framing produces wrong governance answers, wrong sales conversations, and wrong PRDs. The right framing has three shifts.

**Shift 1 — Non-determinism is constitutive, not a bug.** Traditional workflows are deterministic by design — given the same input, you get the same output. Agents are non-deterministic — the same input can produce different outputs across runs because the LLM's reasoning is stochastic. This is **not a bug to be fixed**; it is the property that makes agents capable of handling novel situations. Engineering teams that treat non-determinism as a defect spend their time chasing it and ship slow. Engineering teams that treat non-determinism as a property design around it: structured outputs, eval-first observability, replay, golden datasets, HITL on consequential actions. The right pattern is *constrain the action space, not the reasoning*.

**Shift 2 — The LLM is the policy.** In traditional ML, the model is a classifier or regressor — a component inside a larger system. The system's behavior is the system's behavior, plus or minus the model's accuracy. In agentic systems, **the LLM is the policy** — the LLM decides what the system does next. This means model swaps (Claude 4.7 → 5.0; GPT-5 → GPT-6) are not just accuracy regressions or improvements; they are **policy changes**. Production agent teams treat model swaps as MRM events. The right pattern is *pin the model; canary the swap; second-line validation*.

**Shift 3 — The trust boundary moves into the prompt.** Traditional applications have well-defined trust boundaries — the user is outside, the database is inside, authenticated requests cross the boundary at one well-defined point. Agentic systems blur this. The prompt contains user input, retrieved documents, tool results, and system instructions — and the LLM treats all of it as input to the next decision. **A poisoned tool result is functionally a privilege escalation from the data tier into the policy tier.** This is the failure mode behind EchoLeak, CurXecute, ForcedLeak. The right pattern is *treat every input to the LLM as if it were user-controlled, including tool results and retrieval hits*.

These three shifts together are why agent governance is its own discipline. Customers who have not made all three shifts will say things like *"we just need to add some guardrails"* or *"we'll handle that with input validation."* These are not wrong, but they are insufficient. The right conversation is about how the customer's existing trust boundaries map onto the new agent surface, and where the new surfaces (tool plane, memory, planning, action provenance) need new controls.

Foundations equips you to recognize when a customer has not made these shifts and to gently lead them through. Do not lecture; ask questions. The five disambiguating questions in §1.12.7.1 are the right ones.

---

## §1.17.3 Vocabulary you should not over-use

A short list of vocabulary you will encounter and that you should be careful about, because each one has been over-used in vendor marketing to the point that experienced enterprise audiences are skeptical when they hear it.

**"Agentic."** A real word; a real distinction. Use it sparingly. Saying "agentic AI" three times in a row in a customer pitch sounds like a sales deck. Prefer "agent" when you mean a specific system, "agentic system" only when you need the Anthropic umbrella term, and "agentic" as an adjective only when nothing else fits.

**"Multi-agent."** A real architectural choice that does not always apply. Anthropic's engineering team has publicly advised "don't build multi-agent systems unless the work demands it." When a customer says they want a multi-agent system, your first question is whether the work decomposes into roles. If not, one agent with the right tools is better.

**"Autonomous."** Almost always means "autonomous within a sandbox" or "autonomous with HITL." Pure autonomy in regulated production does not exist as of mid-2026 (§1.1.2). Be explicit about the autonomy level you mean. Level 2 ("HITL on every consequential action") and Level 3 ("HITL on high-risk only") are the production-realistic levels.

**"Reasoning."** When a customer says "the agent reasons about X," they sometimes mean the LLM produces a chain-of-thought trace. Sometimes they mean the agent plans multi-step. Sometimes they mean nothing in particular. Ask what they mean. The honest framing: the LLM is doing token-by-token generation conditioned on context; whether that constitutes "reasoning" is a philosophical question this book does not resolve.

**"Enterprise-ready."** A marketing claim, not an evidence class. Per the §13 citation taxonomy, "enterprise-ready" needs to decompose into named regimes the product satisfies, named customers in named segments, named audit evidence available on examination day. The absence of decomposition is the signal that the term is being used as marketing rather than as substance.

**"Agentic AI Foundation."** A real organization (the Linux Foundation AAIF, formed December 2025). When a vendor says they are "an AAIF member" or "donating to AAIF," the technical claim has substance. When they say they are "an agentic-AI-foundation company," they are using the term as marketing.

The general pattern: any vocabulary that is marketing-adjacent deserves the disambiguating question. *"What specifically do you mean by that?"* is always a fair question, and it is one you will ask a lot in your first six months.

---

## §1.17.4 Curriculum cross-reference

A short map of where the rest of this Field Guide carries forward what Foundations introduced. Use this as your reading roadmap.

| Foundations introduced... | Patterns extends... | Production extends... |
|---|---|---|
| §1.1 Workflow-vs-agent | Topology-specific design implications | Per-regime workflow-vs-agent classification (SR 11-7 model inventory) |
| §1.2 The ten-tier stack | Per-tier named-vendor depth + decision criteria | 10-axis deployment matrix + per-axis trade-offs |
| §1.3 Frameworks at conceptual level | 6-framework comparison matrix + procurement question sets | LangGraph Platform internals + sub-processor list |
| §1.4 LangGraph primitives | All primitives at production depth + composition patterns | Production deploy patterns + reproducibility |
| §1.5 State, memory, persistence | Checkpointer migration story; cross-thread memory patterns | Per-tenant state isolation; audit-evidence flow for state |
| §1.6 Three-layer protocol stack | MCP at depth (Auth, elicitation, sampling); A2A at depth | MCP signature / attestation / SLSA provenance; supply-chain controls |
| §1.7 Seven topologies | Per-topology state graph + decision tree + named harnesses | Topology choice as deployment shape input |
| §1.8 Observability | Per-platform comparison; OTel + OpenInference | Audit-trail integrity; what surfaces to which SIEM |
| §1.9 Three identity problems | Identity / Agent AuthZ chapter (depth) | Action provenance + signed action chain (Audit-Evidence Cookbook) |
| §1.10 Six recipes | Per-recipe full state graph + customer engineering blog citations | Per-recipe Audit-Evidence Pattern + STRIDE-A threat model |
| §1.11 Five categorical surfaces | 14-mode failure taxonomy + per-mode mitigations | 18-surface catalog + recipe × surface matrix + per-surface regime tags |
| §1.12 Three industries + Sovereign | Persona × recipe × segment-variant matrix | Per-regime depth chapters (DORA / EU AI Act / SR 11-7 / HIPAA / SAMA / MAS / etc.) |

If you remember nothing else: **Foundations is the vocabulary; Patterns is the decision criteria; Production is the audit evidence**.

---

## §1.18 Sources cited

Citations are tagged per the design spec's 10 evidence classes. Every factual claim in this chapter traces to one of these tags: `[primary-regulatory]`, `[independently-audited]`, `[vendor-contractual]`, `[vendor-public]`, `[named-incident]`, `[customer-produced-evidence]`, `[corroborated]`, `[reference design]`, `[architectural inference]`, `[benchmark]`.

### Vendor-public agent definitions

- LangChain / LangGraph documentation (2026). *LangGraph overview*. https://docs.langchain.com/oss/python/langgraph/overview . `[vendor-public]`
- Anthropic Engineering (December 2024). *Building Effective Agents*. https://www.anthropic.com/engineering/building-effective-agents . `[vendor-public]`
- OpenAI (2026). *Agents SDK documentation*. https://openai.github.io/openai-agents-python/ and *The next evolution of the Agents SDK*. `[vendor-public]`
- Microsoft (April 2026). *Microsoft Agent Framework documentation* and 1.0 GA announcement. https://learn.microsoft.com/en-us/agent-framework/ . `[vendor-public]`
- Google Cloud (2026). *Vertex AI Agent Builder / Gemini Enterprise Agent Platform documentation*. https://cloud.google.com/vertex-ai/generative-ai/docs/agent-builder/overview . `[vendor-public]`

### Academic and benchmark sources

- Russell, S. and Norvig, P. *Artificial Intelligence: A Modern Approach* (4th edition). `[benchmark]`
- Yao, S. et al. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models.* ICLR 2023. arXiv:2210.03629. `[benchmark]`
- Schick, T. et al. (2023). *Toolformer: Language Models Can Teach Themselves to Use Tools.* NeurIPS 2023. arXiv:2302.04761. `[benchmark]`
- Shinn, N. et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning.* NeurIPS 2023. arXiv:2303.11366. `[benchmark]`
- Yao, S. et al. (2023). *Tree of Thoughts: Deliberate Problem Solving with Large Language Models.* NeurIPS 2023. arXiv:2305.10601. `[benchmark]`
- Wang, L. et al. (2023). *Plan-and-Solve Prompting.* ACL 2023. arXiv:2305.04091. `[benchmark]`
- Packer, C. et al. (2023). *MemGPT: Towards LLMs as Operating Systems.* arXiv:2310.08560 (UC Berkeley RISELab). `[benchmark]`
- Park, J.S. et al. (2023). *Generative Agents: Interactive Simulacra of Human Behavior.* UIST 2023. arXiv:2304.03442. `[benchmark]`
- Lewis, P. et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.* NeurIPS 2020. `[benchmark]`
- Xi, Z. et al. (2023). *The Rise and Potential of Large Language Model Based Agents.* arXiv:2309.07864. `[benchmark]`
- Wang, L. et al. (2024). *A Survey on Large Language Model based Autonomous Agents.* arXiv:2308.11432. `[benchmark]`
- Debenedetti, E. et al. (2024). *AgentDojo.* NeurIPS 2024. arXiv:2406.13352. `[benchmark]`
- Zhan, Q. et al. (2024). *InjecAgent.* ACL 2024 Findings. arXiv:2403.02691. `[benchmark]`
- Greshake, K. et al. (2023). *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection.* AISec @ CCS 2023. arXiv:2302.12173. `[benchmark]`
- Banerjee, A. et al. (2024). *ConfusedPilot: Confused Deputy Risks in RAG-based LLMs.* USENIX Security 2024 (UT Austin). `[benchmark]` `[named-incident]`-adjacent.
- Chen, L., Zaharia, M., Zou, J. (2023). *How is ChatGPT's behavior changing over time?* arXiv:2307.09009. `[benchmark]` `[corroborated]`.

### Protocols and standards

- Anthropic (Nov 2024 / Dec 2025). *Model Context Protocol* and *Donating MCP to the Agentic AI Foundation*. https://modelcontextprotocol.io/ . `[vendor-public]`
- Linux Foundation (Dec 2025). *Formation of the Agentic AI Foundation (AAIF)*. `[primary-regulatory]` (LF charter).
- Google (April 2025) / Linux Foundation (June 2025). *A2A Protocol* and *Linux Foundation A2A Project launch*. https://a2a-protocol.org/ . `[vendor-public]`
- Cisco Outshift / Linux Foundation (July 2025). *AGNTCY project and Agent Gateway Protocol*. `[vendor-public]`
- IETF RFC 9449 (Sept 2023). *Demonstrating Proof of Possession (DPoP)*. https://datatracker.ietf.org/doc/rfc9449/ . `[primary-regulatory]`
- OpenID Foundation. *CIBA (Client-Initiated Backchannel Authentication) specification*. `[primary-regulatory]`

### Named incidents (referenced in §1.11 and the glossary)

- PromptArmor (August 2024). *Data Exfiltration from Slack AI via indirect prompt injection*. https://promptarmor.substack.com/p/data-exfiltration-from-slack-ai-via . `[named-incident]`
- Aim Labs / Microsoft (June 2025). *EchoLeak / CVE-2025-32711*. arXiv:2509.10540 follow-up writeup. `[named-incident]` `[benchmark]`
- CVE-2025-54135 (2025). *CurXecute — MCP tool-result-as-prompt vulnerability class*. `[named-incident]`
- Samsung / OpenAI (April 2023). *Samsung ChatGPT data leak*. Multiple press accounts. `[named-incident]`
- *Moffatt v. Air Canada* (Feb 2024). British Columbia Civil Resolution Tribunal. `[named-incident]`
- Replit production-DB deletion (May 2025). `[named-incident]`
- *Mata v. Avianca, Inc.* (S.D.N.Y. 2023). Hallucinated case-citation sanction. `[named-incident]`
- Salesforce Agentforce ForcedLeak disclosure (September 2025). `[named-incident]`
- ChatGPT Atlas omnibox vulnerability (October 2025). `[named-incident]`

### Identity and FGA

- *OpenFGA* (CNCF sandbox project). https://openfga.dev/ . `[vendor-public]`
- AWS Cedar / Verified Permissions. `[vendor-public]`
- Auth0 / Okta for AI Agents documentation. `[vendor-public]`
- Microsoft Entra Agent ID documentation. `[vendor-public]`

### Customer-produced evidence (LangGraph deployments)

- Klarna engineering blog (April 2025); Sebastian Siemiatkowski's LangChain Interrupt 2025 keynote; Klarna CEO public reversal (May 2025). `[customer-produced-evidence]` `[corroborated]` `[named-incident]` for the reversal.
- Uber Validator + AutoCover; Uber LangChain Interrupt 2025 talk. `[customer-produced-evidence]`
- LinkedIn Hiring Assistant; InfoQ presentation. `[customer-produced-evidence]`
- Elastic Security AI Assistant; Elastic blog. `[customer-produced-evidence]`
- AppFolio Realm-X; AppFolio + LangChain co-published case study. `[customer-produced-evidence]`
- Replit Agent; Replit engineering blog. `[customer-produced-evidence]`
- BlackRock Aladdin Copilot (LangGraph Platform customer; 50+ engineering teams). `[vendor-public]`
- Captide FSI Plan-and-Execute deployment. `[customer-produced-evidence]`
- Doctolib Alfred (non-PHI Q&A). `[customer-produced-evidence]`
- Cisco Outshift internal agent platform. `[customer-produced-evidence]`
- JPMorgan (named in LangGraph Platform 400-customer set; details undisclosed). `[vendor-public]`
- NVIDIA AI-Q Blueprint (built on LangGraph internally). `[vendor-public]`

### OWASP / MITRE / standards bodies

- OWASP Foundation. *OWASP Top 10 for Large Language Model Applications* (2023–2025 editions). `[primary-regulatory]`-adjacent (industry standard).
- OWASP Foundation (early 2025). *OWASP Agentic AI Threats and Mitigations*.
- MITRE ATLAS (2025). `[primary-regulatory]`-adjacent (standards body).
- NIST AI RMF + GenAI Profile. `[primary-regulatory]`-adjacent.

### Internal research inputs (referenced for derivation; not citable in the public artifact)

- OCARA `ref-beginner-foundations.md` (R2, 2026-05-24) — conceptual primer base.
- OCARA `ref-framework-survey.md` (R1, 2026-05-24) — framework profiles.
- OCARA `ref-data-leak-surface-catalog.md` (R4, 2026-05-24) — leakage pathway taxonomy.
- OCARA `ref-academic-and-community.md` (R5, 2026-05-24) — intellectual genealogy.
- OCARA `ref-design-field-guide.md` (v3, 2026-05-24) — design-spec authority.

---

## §1.19 Anki deck pointer

A spaced-retrieval deck of ~60–80 cards accompanies Foundations. Cards cover the must-retain vocabulary surfaced in this chapter — the five-point autonomy spectrum, the ten tiers, the three-layer protocol stack, the three scopes of state, the three identity problems, the seven topologies, the six recipes with anchor customers, the ten named incidents, the LangGraph primitives, and the citation taxonomy.

**File:** `book/05-anki-deck/01-foundations.apkg`.

**Recommended cadence:** review daily for 14 days post-completion. After 14 days, review every 3 days for the next 30 days. The vocabulary atrophies fast; the spaced-retrieval cadence keeps it durable through your first customer engagement.

---

## §1.20 What you should be able to do now

Re-read the outcomes you set out with at the start of the chapter:

- **SE / SC.** Disambiguate agent from chatbot / RAG / workflow / pipeline. Sketch the ten-tier stack on a whiteboard. Name the three protocol-stack layers. Pick a topology from a 1-paragraph brief. Name three named incidents and the obvious governance risk. Recognize the three identity problems and one named-product solution for each.
- **PM.** Write a JTBD statement for an agent feature. Distinguish buyer from end-user persona. Identify which of the six recipes a customer's request fits. Name the dominant governance category. Distinguish vendor-disclosed metrics from audit-grade evidence.
- **Engineer-curious.** Wire a minimal LangGraph ReAct agent with `PostgresSaver`, a HITL `interrupt()`, and per-tenant `thread_id`. Identify three places this design would fail in production.

If you can do all of these from memory and applied the rubric in §1.16 to your own answer with a passing score, you are ready for Patterns. If not, the §1.16 retake mechanic specifies which sections to re-read.

The next chapter — **02-patterns.md** — extends every section here with named-component depth, the seven-topology decision tree, per-recipe state graphs, the cross-tenant isolation chapter, the identity / agent AuthZ chapter, and per-regime compliance depth. The vocabulary you carry into Patterns is the vocabulary this chapter taught.

### §1.20.1 A short closing perspective

A few last things worth saying before you turn the page.

**The vocabulary in this chapter is more durable than the products it describes.** Anthropic's workflow-vs-agent distinction is a clean conceptual cut that will outlast individual model deprecations. The ten-tier stack is a mental model that will outlast individual vendor choices. The three identity problems will outlast individual IDP products. The seven topologies will outlast the specific harnesses that implement them. The six recipes will outlast specific customer engagements. Learning the vocabulary is investing in something that lasts; learning specific product names is investing in something that decays on a 12–24 month cycle. Spend your retention budget accordingly.

**The named-incident catalog is the most under-respected curriculum in this chapter.** Most new hires speed through §1.11 because the incidents are well-known. They are well-known to you. They are not well-known to most customer engineering teams. Walking a customer through Slack AI, EchoLeak, and ConfusedPilot — slowly, with the architecture of each attack drawn on a whiteboard — is one of the highest-impact things a Sales Engineer can do in a first technical session. Spend the time. Memorize the incidents. Be the person in the room who can explain what zero-click prompt injection means and why it changed how Microsoft 365 Copilot was reviewed.

**The Klarna CEO reversal is the most under-respected story in this chapter.** Most readers nod past it. The lesson is deeper than "Klarna was a little optimistic." The lesson is that **every public agent metric you have ever read** was vendor-disclosed marketing material, and **none of it would survive an MRM audit**. The first time you have to defend an agent deployment to a Model Risk Management committee, you will reach for the public metrics and discover that they evaporate. The Klarna reversal is the canonical "we got it wrong" story precisely because Klarna was the canonical "look how well this works" story. Both are true: the deployment is real and meaningful and useful; the metrics-at-launch are not validation evidence. Hold both ideas at once.

**Identity Problem 3 is the new one.** Of everything in this chapter, the single most novel concept for most readers is **the agent acting on behalf of a user as a distinct identity problem from agent identity and user identity**. Problem 1 was solved in the 2000s. Problem 2 was solved in the 2010s and 2020s. Problem 3 is what 2025–2026 OAuth standards (DPoP, PAR, RAR, CIBA, step-up) and 2025-launched products (Entra Agent ID, Okta for AI Agents, Auth0 for AI Agents) are operationalizing now. Most customer engineering teams have not noticed Problem 3 yet. When you walk them through it, you sound like you are from the future. Make sure you are accurate.

**LangGraph is the focus, but the substrate matters more than the framework.** The reason this book is titled "Enterprise AI Agents on LangGraph" rather than "Enterprise AI Agents" is honest — the named-deployment evidence at scale clusters around LangGraph. But the substrate questions — *where does my data go, where does my prompt cache live, where does my identity terminate, where does my action provenance get signed* — are framework-agnostic. The right framing in customer conversations is: "LangGraph is the orchestration layer we recommend because of A, B, and C. The questions you should be asking are about the substrate layers underneath — tier 10 (LLM), tier 9 (retrieval), tier 7 (identity), tier 5 (state). The framework choice is one decision; the substrate decisions are five or ten more."

**Patterns and Production are where the customer money lives.** Foundations is the vocabulary that lets you have the conversation. Patterns is the design criteria that lets you make recommendations. Production is the audit evidence that lets the recommendation survive a CISO review. A new hire who has read Foundations only is a *good intern* — they can listen well and ask good questions. A new hire who has read Foundations and Patterns is a *good Solution Consultant* — they can lead a discovery call. A new hire who has completed Production and the capstone is a *good Sales Engineer* — they can defend a deployment in front of a CISO-FSI. The path is not a sprint.

**You do not need to remember every named vendor.** The ten-tier stack diagram in §1.2 lists dozens of vendor names. You will encounter many of them in customer conversations. You do not need to remember them all from memory; you need to recognize them when a customer says them and reach for the right disambiguating question. The vocabulary that *does* need to live in working memory: the ~50 glossary terms in §1.15. Those are the ones that should be retrievable in 1–2 seconds without thought. Everything else is reference material.

**This book has a point of view.** It is not neutral. It commits to the Anthropic workflow-vs-agent discipline. It commits to LangGraph as the focal framework. It commits to vendor-disclosed metrics being non-evidence under SR 11-7. It commits to the three-layer protocol stack as the canonical mental model. It commits to "data-leak surface" / "leakage pathway" as the public vocabulary. It commits to Sovereign deployment being structurally a fit and operationally a `[zero]`-deployment segment. These are choices, not consensus. Where the book is taking a position, it says so. Where the evidence is thin, it says `[evidence-zero]` or `[reference design]` or `[architectural inference]`. The author affiliation is disclosed in `CONFLICTS.md`. The book is one input among many; it is not a substitute for vendor due diligence.

That last point is worth repeating one more time before you close the chapter. **This is not a procurement-evaluation document.** It is an educational reference. The procurement decision a customer makes is theirs; the technical foundation this book gives you is yours to bring to the conversation.

Welcome to the work.

— *A. Fulkerson*

*Aaron Fulkerson is the CEO of OPAQUE Systems. His affiliation is disclosed in the author bio (in `00-introduction.md`) and in `CONFLICTS.md` (at the repo root). His point of view on the substrate-vs-graph-layer distinction is named in `CONFLICTS.md`. This chapter contains zero OPAQUE product positioning anywhere except this attribution line.*

---

*End of Chapter 1 — Foundations.*

*Next: Chapter 2 — Patterns.*


# Production Deck — Anki Spaced-Retrieval Cards

> Source tier: `book/03-production.md` ("Enterprise AI Agents on LangGraph: A Field Guide" — Chapter 3).
>
> Card count: 179. Reader floor: any reader who has completed Foundations + Patterns and read Production once. Review cadence: daily for 30 days, then weekly for 90 days.
>
> Card-type distribution: definition recall (54), decision/disambiguation (35), named-component / customer-voice (36), failure-mode / regulatory (28), worked-fragment (16), citation-class (9).
>
> Cards ordered by glossary cluster. License: CC BY-SA 4.0.

---

## Cluster 1 — The 10-axis deployment-shape matrix

### Q: Name the 10 axes of the Production deployment-shape matrix.
**A:** (1) Cloud locus, (2) Identity perimeter, (3) Data perimeter, (4) Trace egress, (5) Secret perimeter, (6) Network egress, (7) Model perimeter, (8) Tool-call perimeter, (9) HitL surface, (10) Support / break-glass.
**Cluster:** Deployment shapes
**Tier reference:** §3.1

### Q: Name the 9 deployment shapes in the §3.1.1 matrix.
**A:** LG Cloud SaaS, BYOC AWS, BYOC Azure `[gap]`, BYOC GCP `[gap]`, Self-Hosted Enterprise, Self-Hosted Lite, Developer Tier, CSP-Managed (Bedrock / Vertex / Foundry), Sovereign Air-Gap.
**Cluster:** Deployment shapes
**Tier reference:** §3.1.1

### Q: What is the trace-egress fact about LangGraph Cloud SaaS that disqualifies it for Tier-1 FSI?
**A:** Trace egress is **mandatory** — `LANGCHAIN_TRACING_V2` is auto-injected; there is no way to opt out of LangSmith Cloud as the trace destination in pure Cloud SaaS. Combined with DORA Art. 28 concentration risk on shared multi-tenant SaaS, this disqualifies Cloud SaaS for Tier-1 FSI. `[vendor-public + primary-regulatory]`
**Cluster:** Deployment shapes
**Tier reference:** §3.1.2

### Q: List the six deal-shaping facts that emerge from the 10-axis matrix.
**A:** (1) BYOC is AWS-only as of 2026-05; (2) LangSmith Cloud is a sub-processor chain extension by default; (3) no public FedRAMP authorization for LangGraph as of 2026-05; (4) HIPAA BAA available on Enterprise but data still in LangChain tenant in Cloud SaaS; (5) trace egress is mandatory in Cloud SaaS; (6) sub-processor list includes Supabase (auth) and ClickHouse (telemetry) — both must appear in DORA Art. 28 register.
**Cluster:** Deployment shapes
**Tier reference:** §3.1.5

### Q: Worked fragment — what does this `values.yaml` skeleton commit to (Self-Hosted Enterprise)?
```yaml
tracing:
  backend: langfuse  # NOT langsmith-cloud — sovereign / FSI default
secrets:
  backend: vault
auth:
  mode: oidc
  oidc:
    issuer: https://login.microsoftonline.com/${TENANT_ID}/v2.0
image:
  tag: "0.4.x"  # pin explicit, do not use :latest
```
**A:** Self-Hosted Enterprise with: (a) tracing routed to customer-hosted Langfuse, NOT LangSmith Cloud — sovereign / FSI default; (b) secrets from HashiCorp Vault via external-secrets-operator; (c) OIDC auth via Entra; (d) **pinned image tag** — `:latest` in production is incompatible with SR 11-7 model-inventory discipline and DORA Art. 9 change-management.
**Cluster:** Deployment shapes
**Tier reference:** §3.1.2

### Q: For an Azure-committed Tier-1 FSI prospect, what are the deployment options and the implied trade?
**A:** Three options: (a) Self-Hosted Enterprise on AKS (recommended — retains LangGraph topology vocabulary), (b) BYOC-AWS with multi-cloud architecture (rare), or (c) CSP-managed (Azure AI Foundry Agent Service — loses LangGraph topology vocabulary entirely). BYOC Azure does not exist. `[vendor-public — explicit gap]`
**Cluster:** Deployment shapes
**Tier reference:** §3.1.2

### Q: What is the diagnostic question for a customer claiming "we're self-hosted on LangGraph"?
**A:** Ask which of the three: **Self-Hosted Enterprise** (Helm-deployed, license-gated, both planes customer-operated — production-grade and DORA-defensible), **BYOC AWS** (control plane in LangChain, data plane in customer AWS), or **Self-Hosted Lite** (single Docker container — NOT production-grade). The answer determines the next 30 minutes of the conversation.
**Cluster:** Deployment shapes
**Tier reference:** §3.1.4

### Q: What is the "Postgres pod count diagnostic" for a customer running Self-Hosted Lite as if it were production?
**A:** If the Postgres pod count is `1`, the deployment is not production-grade regardless of what marketing materials called it. Self-Hosted Lite is the 3-container Docker Compose stack with no replication, no rolling restart strategy, no horizontal scale.
**Cluster:** Deployment shapes
**Tier reference:** §3.1.2

### Q: Why does NVIDIA AI-Q appear in the §3.1.1 matrix even though it is not strictly a LangGraph shape?
**A:** Because **NVIDIA AI-Q is built on LangGraph internally** [vendor-public surprise per R1] — meaning LangGraph is a sub-component of at least one CSP-managed offering. AppFolio Realm-X on LangGraph-on-ECS behind AgentCore Gateway is the AWS-documented framework-native path.
**Cluster:** Deployment shapes
**Tier reference:** §3.1.2

---

## Cluster 2 — Cross-tenant isolation (the five surfaces, full mechanics)

### Q: State the §3.2 thesis on cross-tenant isolation in one sentence.
**A:** Cross-tenant aggregation cannot be prevented at the authorization decision layer alone — Identity / FGA covers one surface (the retriever surface, partially); the other four (cache, checkpointer, observability, model) are independent and each can leak even if the first is fully closed.
**Cluster:** Cross-tenant isolation
**Tier reference:** §3.2

### Q: Worked fragment — what three layers does this identity-binding pattern enforce?
```python
async def retrieve(state, config):
    user_id = config["configurable"]["user_id"]
    tenant_id = config["configurable"]["tenant_id"]
    if not await fga.check(user=f"user:{user_id}", relation="can_read", object=f"tenant:{tenant_id}"):
        raise PermissionError("user not authorized for tenant")
    chunks = await retriever.search(query=state["query"], namespace=tenant_id,
                                     filter={"tenant_id": tenant_id})
    for chunk in chunks:
        assert chunk.metadata["tenant_id"] == tenant_id
    return {"retrieved_chunks": chunks}
```
**A:** (1) FGA check (relationship-based authorization at the agent-on-behalf-of-user binding). (2) Store-layer filter (namespace + payload). (3) Post-retrieval verification (tenant assertion). One layer alone is insufficient; defense-in-depth catches the modal misconfiguration.
**Cluster:** Cross-tenant isolation
**Tier reference:** §3.2.1

### Q: Worked fragment — what is the OpenFGA model for Recipe 6 (Agentic RAG) defining?
```
type agent
  relations
    define operator: [user]
    define can_act_for: [user]
    define tenant_scope: [tenant]

type tool_invocation
  relations
    define tool: [tool]
    define on_behalf_of: [user]
    define authorized: can_act_for from on_behalf_of
```
**A:** The **agent-on-behalf-of-user delegation** at FGA depth. The agent has no read authority by itself; every retrieval check is `user.reader_of(document_section)` evaluated through the `can_act_for` chain. This is what makes the cross-tenant aggregation surface fail-closed at the FGA layer for SOC / Agentic RAG deployments.
**Cluster:** Cross-tenant isolation
**Tier reference:** §3.2.1

### Q: Name the three substrate-residual risks that remain after FGA + store-layer filter + post-retrieval verification.
**A:** (a) **Embedding-time leakage** — a tenant-A document indexed into tenant-B namespace by misconfiguration leaks forever; (b) **Filter side-channel** — timing or result-count reveals tenant-B data even when chunks aren't returned; (c) **Embedding semantic leakage** — attacker query embedding matches another tenant's chunks via shared embedding model + inversion attack. (c) is the substrate-level concern — application-layer mitigations cannot fully close it.
**Cluster:** Cross-tenant isolation
**Tier reference:** §3.2.1

### Q: For Snowflake Cortex Search, what is the cross-tenant pattern?
**A:** Per-account; account-level isolation. Snowflake's RBAC stack handles the bind. Most defensible against an FSI auditor when paired with Unity Catalog lineage. `[vendor-public]`
**Cluster:** Cross-tenant isolation
**Tier reference:** §3.2.1

### Q: For Databricks Vector Search, what is the cross-tenant pattern, and what makes it auditor-defensible?
**A:** Per-schema. Unity Catalog grants drive isolation. Most defensible against an FSI auditor because the lineage is end-to-end in Unity Catalog. `[vendor-public]`
**Cluster:** Cross-tenant isolation
**Tier reference:** §3.2.1

### Q: For the cache surface (Surface 2), name the four caches that must carry per-tenant keys.
**A:** (a) Redis application-layer cache, (b) the LLM provider's prompt cache (Anthropic / OpenAI / Bedrock — each with different invalidation semantics), (c) reranker cache (Cohere / Voyage / BGE), (d) embedding cache. Without per-tenant keys, two tenants share the same hash.
**Cluster:** Cross-tenant isolation
**Tier reference:** §3.2.2

### Q: What is the standard Redis cache key format that prevents cross-tenant aggregation?
**A:** `f"agent:{tenant_id}:{user_id}:{semantic_hash}"`. The `tenant_id` MUST be in the key. Per-tenant cache key namespacing is required at every cache layer.
**Cluster:** Cross-tenant isolation
**Tier reference:** §3.2.2

### Q: For Surface 3 (Checkpointer), name the two isolation patterns and the modal misconfiguration.
**A:** (a) Per-tenant Postgres schema isolation (`tenant_a.checkpoints`, `tenant_b.checkpoints`). (b) Shared schema with `tenant_id` discriminator column + Postgres RLS. **Modal misconfiguration:** `thread_id` alone is insufficient — without schema isolation or RLS, a malicious `thread_id` collision could cross tenant boundaries.
**Cluster:** Cross-tenant isolation
**Tier reference:** §3.2.3

### Q: For Surface 4 (Observability), what is the modal cross-tenant aggregation failure mode?
**A:** Trace-tier aggregation — without per-tenant trace partition in LangSmith (workspace-per-tenant or project-per-tenant) or Langfuse (organization + workspace per tenant), one tenant's traces become visible to another tenant's debugging sessions. PII redaction at trace boundary is the additional defense.
**Cluster:** Cross-tenant isolation
**Tier reference:** §3.2.4

### Q: For Surface 5 (Model), what are the three sub-surfaces that can leak across tenants?
**A:** (a) Per-tenant **fine-tune isolation** — never share fine-tuned weights across tenants. (b) **Prompt cache partitioning** — Anthropic/OpenAI/Bedrock prompt caches must be partitioned per tenant or cache key collisions aggregate across tenants. (c) **KV-cache leakage** — across requests on shared inference infrastructure.
**Cluster:** Cross-tenant isolation
**Tier reference:** §3.2.5

---

## Cluster 3 — Integration Cookbook (customer existing-stack patterns)

### Q: Name the seven Integration Cookbook categories per §3.3.
**A:** (1) Customer IAM, (2) Customer Secrets, (3) Customer Observability, (4) Customer Policy, (5) Customer Data Lineage, (6) Customer CI/CD + Supply Chain, (7) Customer Egress.
**Cluster:** Integration Cookbook
**Tier reference:** §3.3

### Q: Which two Integration Cookbook categories get FULL DEPTH treatment in Production?
**A:** **§3.3.1 Customer IAM** and **§3.3.2 Customer Secrets** — the two highest-risk and most-audited touchpoints. The remaining five get compressed-reference treatment.
**Cluster:** Integration Cookbook
**Tier reference:** §3.3

### Q: Name the modal HSM choices for HSM-backed signing chains in Production deployments.
**A:** **CloudHSM** (AWS), **Azure Dedicated HSM** (Azure), **Cloud HSM** (GCP), **Thales Luna**, **YubiHSM**. For sovereign deployments — customer-controlled on-prem HSM (Thales Luna, AWS CloudHSM in a customer-controlled boundary).
**Cluster:** Integration Cookbook
**Tier reference:** §3.4.1 / §3.3.2

### Q: What is the External Secrets Operator?
**A:** CNCF-graduated Kubernetes operator that pulls secrets from external stores (Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager) into Kubernetes secrets. The de-facto standard for K8s secret integration in 2026. `[vendor-public]`
**Cluster:** Integration Cookbook
**Tier reference:** §3.3.2

---

## Cluster 4 — Audit-Evidence Cookbook (Sign-1 through Sign-5)

### Q: Name the five signing points in the Sign-1 through Sign-5 chain.
**A:** **Sign-1 — Prompt envelope** (user/tenant/session IDs + hashes + model+tool+retrieval+graph versions). **Sign-2 — Retrieval invocation** (retriever ID, query hash, chunk IDs returned, chunk tenants). **Sign-3 — LLM invocation** (model ID, region, throughput ARN, response hash). **Sign-4 — Tool call + result** (tool ID, args hash, on-behalf-of user, FGA decision, result hash). **Sign-5 — Outcome record** (final response hash, HITL decision ID, trace Merkle root, classification).
**Cluster:** Audit evidence
**Tier reference:** §3.4.1

### Q: What is the cryptographic primitive choice for Sign-1..5 signing in Production?
**A:** **ECDSA P-256 or Ed25519** are the modal picks. RSA-2048 is acceptable but not preferred for new builds. **The signing key MUST live in an HSM** — a Kubernetes Secret or env var does not satisfy SR 11-7 §III.5 evidence weight nor DORA Art. 9 cryptographic-key-management.
**Cluster:** Audit evidence
**Tier reference:** §3.4.1

### Q: What is RFC 3161, and why does it appear in the action chain?
**A:** **Trusted timestamping** — cryptographically anchors signatures to wall-clock. Named TSAs include DigiCert, SwissSign, GlobalSign, Sectigo, and self-hosted HSM TSAs. Every Sign-1..5 event in Production carries an RFC 3161 timestamp. `[vendor-public]`
**Cluster:** Audit evidence
**Tier reference:** §3.4.1

### Q: What is the difference between SLSA + in-toto attestations and the Sign-1..5 runtime chain?
**A:** SLSA + in-toto v1 attestations sign the **agent artifact itself** (Helm chart, container image, Python wheel) at build time. The Sign-1..5 chain attests the **runtime action chain** at execution time. **Both are required** for a regulator-ready deployment.
**Cluster:** Audit evidence
**Tier reference:** §3.4.1

### Q: What are the five hashes that form the agent manifest per §3.4.4?
**A:** `model_version_hash` + `system_prompt_hash` + `tool_registry_hash` + `retrieval_index_hash` + `agent_graph_hash`. Plus sub-processor list + retention policy. **This is the artifact a regulator asks for first.** Without it, the agent is non-reproducible — SR 11-7 finding.
**Cluster:** Audit evidence
**Tier reference:** §3.4.4

### Q: Worked fragment — what is this YAML defining?
```yaml
agent_manifest:
  version: 1.4.2
  approved_by: model-risk-committee-2026-q2
  hashes:
    model_version_hash: sha256:abc...
    system_prompt_hash: sha256:def...
    tool_registry_hash: sha256:ghi...
    retrieval_index_hash: sha256:jkl...
    agent_graph_hash: sha256:mno...
  retention_policy:
    audit_chain: 10_year_worm
```
**A:** The §3.4.4 **agent manifest** — the SR 11-7 reproducibility artifact. Five pinned hashes mean any past output can be reproduced; the approval traces to the model-risk committee; retention is WORM-bound. Without the manifest, the agent is non-reproducible.
**Cluster:** Audit evidence
**Tier reference:** §3.4.4

### Q: Name the four named WORM storage products + which mode is required for SEC 17a-4(f).
**A:** **AWS S3 Object Lock Compliance mode** (required — Governance mode is NOT sufficient for SEC 17a-4(f)), **Azure Immutable Blob time-based**, **GCP Bucket Lock**, **NetApp SnapLock Compliance**, **Dell PowerScale SmartLock Compliance**. `[vendor-public]`
**Cluster:** Audit evidence
**Tier reference:** §3.4.2

### Q: Why is AWS S3 Object Lock Governance mode NOT sufficient for SEC 17a-4(f)?
**A:** Because a privileged user can override Governance mode. SEC 17a-4(f)(2) requires non-rewriteable, non-erasable storage — only **Compliance mode** (no override possible during retention) satisfies. `[primary-regulatory]`
**Cluster:** Audit evidence
**Tier reference:** §3.4.2

### Q: What is BYOK vs HYOK, and which is modal for sovereign?
**A:** **BYOK** (Bring Your Own Key) — customer-managed keys via AWS KMS / Azure Key Vault / GCP Cloud KMS customer-managed key. **HYOK** (Hold Your Own Key) — customer's HSM holds the master key; the cloud provider never has access. **HYOK is modal for sovereign deployments.** `[vendor-public]`
**Cluster:** Audit evidence
**Tier reference:** §3.4.2

### Q: Name the 12 exhibits in the FSI examination dossier per §3.4.5.
**A:** (1) Model inventory entry, (2) Validation report, (3) Ongoing monitoring plan, (4) Model-swap log, (5) ICT register entry, (6) Sub-processor list with DPA effective dates, (7) Incident log with classification, (8) Data-leak-surface mapping with residual risk, (9) STRIDE-A threat model, (10) DPIA, (11) Exit plan, (12) Evidence retention policy.
**Cluster:** Audit evidence
**Tier reference:** §3.4.5

### Q: What is the examiner's day-one question, and what is the consequence of not having Exhibit 1?
**A:** "Show me Exhibit 1 — the model inventory entry for your customer-support agent." If you do not have it, **you have lost the examination on day one.** Every subsequent question presumes Exhibit 1 exists.
**Cluster:** Audit evidence
**Tier reference:** §3.4.5

### Q: What is OCSF?
**A:** **Open Cybersecurity Schema Framework** — Splunk-led, broadly adopted normalized event schema. Agent outcomes can be mapped to OCSF event categories (Application Activity 6003, Authentication 3002, etc.) for SIEM ingestion. `[vendor-public]`
**Cluster:** Audit evidence
**Tier reference:** §3.4.3

### Q: What is OpenLineage, and which recipe mandates its emission?
**A:** Data-flow lineage protocol (CNCF-incubating; LF AI & Data). Agent emits "dataset accessed" / "model invoked" / "output produced" events; lineage tools reconstruct end-to-end provenance. **OpenLineage emission is mandatory for Recipe 3 (Text-to-SQL)** under FINRA Rule 5280 / GDPR Art. 22 information-barrier compliance. `[vendor-public]`
**Cluster:** Audit evidence
**Tier reference:** §3.4.3 / §3.4.10

### Q: What is the read-trail discipline for WORM-stored traces?
**A:** **Read access to WORM-stored traces is itself a security event that must be logged.** Two-person rule for retention deletion (legal-hold-only path). Customer-mediated vendor access: LangChain Ops CANNOT read customer-WORM-stored traces in Self-Hosted Enterprise — the architectural fact that makes Self-Hosted Enterprise the only DORA-defensible posture for Tier-1 FSI.
**Cluster:** Audit evidence
**Tier reference:** §3.4.6

### Q: Name the EchoLeak-class first-60-minutes incident response timeline beats.
**A:** **T+0** alert; **T+5** investigator authenticates to WORM; **T+10** query trace spans for affected session; **T+15** identify trigger; **T+20** determine blast radius (cross-tenant?); **T+30** snapshot affected checkpointer state; **T+40** decide containment (kill switch / quarantine); **T+50** classify (incident? major? client-affecting?); **T+60** notification clock starts (DORA 24-hr, NYDFS 72-hr, GDPR 72-hr, SEC Reg S-P 30-day).
**Cluster:** Audit evidence
**Tier reference:** §3.4.7

### Q: Worked fragment — what SOC use-case does this SQL query implement?
```sql
SELECT trace_id, user_id, tenant_id, retrieved_chunks_tenants
FROM agent_traces
WHERE retrieved_chunks_tenants != ARRAY[tenant_id]
  AND timestamp BETWEEN $window_start AND $window_end;
```
**A:** **Cross-tenant aggregation detection.** Returns trace sessions where the chunks retrieved came from tenants other than the requesting tenant — i.e., a cross-tenant boundary violation. Should return zero rows in a properly-isolated production deployment.
**Cluster:** Audit evidence
**Tier reference:** §3.4.7

### Q: Name the three vendor break-glass postures and which is acceptable for Tier-1 FSI.
**A:** **Customer-mediated** (vendor does not get direct read; customer provides specific traces in response to a support ticket) — modal for Tier-1 FSI. **Read-on-incident** (vendor has read access only during an active incident) — acceptable for mid-market. **Full-read** (vendor has standing read access) — NOT acceptable for FSI.
**Cluster:** Audit evidence
**Tier reference:** §3.4.8

### Q: What is the DORA Art. 28(8) exit plan window, and what does it cover?
**A:** **90 calendar days.** Covers: Days 1-15 notification; Days 15-30 data portability (checkpointer + trace export); Days 30-60 runtime portability (alternative orchestrator); Days 60-75 evidence portability (WORM contents); Days 75-90 decommission + Certificate of Destruction. `[primary-regulatory]`
**Cluster:** Audit evidence
**Tier reference:** §3.4.9

### Q: Name the six per-recipe Audit-Evidence Patterns and the signing point each is heaviest on.
**A:** R1 Support — heaviest on Sign-4 (tool calls). R2 Coding — Sign-1 (auth) + Sign-4 (commit/merge) + SLSA Level 3+. R3 Text-to-SQL — Sign-2 (dataset accessed) + Sign-4 (SQL executed). R4 Deep Research — Sign-2 (sources) + Sign-3 (model interim conclusions). R5 Embedded SaaS — per-tenant isolation evidence across all five signing events. R6 SOC — Sign-4 (action) + Sign-5 (outcome) — heightened auditability because the SOC agent IS audit infrastructure.
**Cluster:** Audit evidence
**Tier reference:** §3.4.10

### Q: What is the Evidence Index?
**A:** A per-recipe one-pager listing where every audit artifact lives — the **architecture-of-the-architecture-of-the-audit**. Columns: artifact, stored-at location, retention, retrieved-by role. Hands to compliance teams; examiners use it as request checklist.
**Cluster:** Audit evidence
**Tier reference:** §3.4.11

---

## Cluster 5 — Regulatory regimes (full per-regime depth)

### Q: What is the DORA fully-applicable date and the personal-liability provision?
**A:** **17 January 2025** fully applicable. **€5M personal director liability** under Art. 50 + **2% global turnover fines** under Art. 50(4). The most weight-carrying regime for an EU FSI deployment. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.1

### Q: What does DORA Art. 5 require of agent deployments?
**A:** ICT governance — the management body is ultimately responsible. **The agent's deployment owner must be a named executive; "the engineering team" is not an acceptable accountable party.** `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.1

### Q: What does DORA Art. 9 require of agent cryptographic configuration?
**A:** Appropriate ICT security and resilience for data transfer, integrity, access prevention, and leak prevention. Implication: TLS config, secret management, encryption-at-rest are scoped under Art. 9. Audit-evidence: cryptographic configuration documented; key rotation cadence documented; HSM-backed signing chain (§3.4.1) documented. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.1

### Q: State the DORA Art. 19 incident notification timing.
**A:** **24-hour early warning** to competent authority after classification as major. **72-hour intermediate report** with status update. **One-month final report** with root cause analysis. Per RTS 2024/1772 ICT incident schema. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.1

### Q: What does DORA Art. 24-26 require for systemically important entities?
**A:** **Threat-Led Penetration Testing (TLPT)** — mandatory for systemically important entities. For agents, red-team testing must include AgentDojo / InjecAgent / AgentHarm benchmark-style scenarios + named-incident replays (EchoLeak, ConfusedPilot, Replit). `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.1

### Q: Which DORA article governs sub-processor exit plans?
**A:** **DORA Art. 28(8)** — requires a documented exit strategy for every ICT third-party. Reference 90-day timeline in §3.4.9. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.1

### Q: What is DORA Art. 28(2)?
**A:** Requires the financial entity to assess **concentration risk** before entering an ICT third-party agreement. For LangGraph: the alternatives (CrewAI Enterprise / MAF / OpenAI Agents SDK / LlamaIndex Workflows / Semantic Kernel) must be documented as viable substitutes. This is the §3.4.9 exit plan in pre-emptive form. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.1

### Q: What is a "CTPP" under DORA?
**A:** **Critical ICT Third-Party Provider** — DORA designation for entities supervised directly by ESAs. Once designated, additional supervisory obligations apply. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §2.11

### Q: What does DORA Art. 30 require in contractual arrangements?
**A:** Required clauses: SLA + penalties, locations (data residency), service availability, reporting obligations, **access/inspection/audit rights of competent authorities**, termination rights. The customer's MSA with LangChain must carry an Art. 30 contractual checklist addendum. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.1

### Q: What is GDPR Art. 22, and what does it require of automated decisions with significant effect?
**A:** The right not to be subject to a decision based solely on automated processing with legal or similarly significant effect. **Any agent action with significant effect requires either explicit consent OR human-in-the-loop placement that is documented and operationally enforced.** The HITL placement IS a GDPR Art. 22 control. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.2

### Q: What does GDPR Art. 35 require, and what should the DPIA template include for a LangGraph agent?
**A:** **DPIA** for high-risk processing. Template: description of processing (state graph + data flows); necessity/proportionality assessment; risks to data subjects (the 14 failure modes mapped); measures to address risks (cross-tenant isolation pattern + HITL + audit-evidence); DPO consultation; data-subject consultation; sign-off by accountable executive. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.2

### Q: What is the GDPR Art. 44-49 international-transfer pattern for LangSmith Cloud routing EU traces?
**A:** SCC (EU Commission Standard Contractual Clauses 2021/914) + TIA + supplementary measures. For EU customer with LangSmith Cloud routed to GCP us-central1 or AWS us-east-2: explicit transfer to the US — SCC + TIA documenting the supplementary measures (e.g., payload redaction at trace boundary). `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.2

### Q: What is the EU AI Act Art. 12 requirement on logs, and what is the retention period?
**A:** Logs of high-risk AI system operation. Retention: **Lifetime of system + 10 years post-decommission.** `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.4.2 / §3.5.3

### Q: What is the EU AI Act Art. 18 retention requirement?
**A:** Technical documentation + conformity assessment retained **10 years after placing on market**. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.4.2 / §3.5.3

### Q: What is SR 11-7, and which authorities issue it?
**A:** **Supervisory Letter 11-7** — Federal Reserve / OCC Model Risk Management framework. Plus **OCC Bulletin 2011-12**. Defines validation, monitoring, governance for models. The MRM-validation teaching attached to every vendor metric in this Field Guide. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.5

### Q: What are SR 11-7 §III.4 validation requirements?
**A:** Four-pillar validation: (1) Independent (developer is not the validator); (2) Outcome-validated (measured against actuals, not equivalent claims); (3) Benchmark-compared (against equivalent human/baseline); (4) Stress-tested (representative of steady state, not launch). The Klarna 700-FTE claim fails on all four — empirical confirmation in the May 2025 reversal. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.9.2

### Q: What does SR 11-7 §III.5 require for a model swap?
**A:** Documented protocol for any change to `model_version_hash`. For Tier-1 model: material change requires second-line concurrence (Model Risk independent validator). Documented sign-off in the model inventory. Canary deployment + quantitative rollback criterion. Regulator notification (FRB/OCC/FDIC for SR-11-7-covered; national AI office for EU AI Act). `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.13.2

### Q: What is the SEC 17a-4(f) retention requirement and the storage requirement?
**A:** First **2 years easily accessible + 4 additional years in WORM (6 total)**. Storage must be **non-rewriteable, non-erasable** — only AWS S3 Object Lock **Compliance** mode satisfies, not Governance mode. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.6

### Q: What is FINRA Rule 5280, and which recipe does it most affect?
**A:** Information-barrier requirements for FSI research and analytics. Most-load-bearing for **Recipe 3 (Text-to-SQL)** in FSI — OpenLineage emission mandatory; FGA models must enforce information barriers between desks. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.6

### Q: What is the FedRAMP-High NIST SP 800-53 Rev. 5 control-family scope for agent deployments?
**A:** AC (Access Control), AU (Audit + Accountability), CA (Assessment), CM (Configuration Management), IA (Identification + Authentication), IR (Incident Response), RA (Risk Assessment), SC (System + Communications Protection), SI (System + Information Integrity), SR (Supply Chain Risk Management). All in scope. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.7

### Q: What is NYDFS Part 500 §500.17 notification timing?
**A:** **72-hour notification** for cybersecurity events. Second Amendment expanded coverage. Applies to financial institutions licensed in New York. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.9

### Q: What does HIPAA §164.312(b) require, and how does it scope the agent's trace bus?
**A:** Audit controls — hardware/software/procedural mechanisms to record + examine activity in systems containing PHI. **The trace bus IS part of the audit infrastructure** for PHI deployments — its access controls, retention, and integrity are in regulatory scope. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.16

### Q: What is the HIPAA Security Rule retention period for audit logs?
**A:** **6 years from creation or last in effect, whichever later** (45 CFR §164.316(b)(2)(i)). `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.4.2 / §3.5.16

### Q: What is the FDA PCCP, and what does it constrain for clinical decision support agents?
**A:** **Predetermined Change Control Plan** for AI/ML SaMD (Dec 2024 + Aug 2025 guidance). Defines the allowed model-version drift envelope; changes outside the envelope require new FDA submission. The model-swap protocol is constrained by PCCP for clinical decision support deployments. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.12.4 / §3.5.19

### Q: What is HTI-1, and what is its source-attribute requirement?
**A:** HHS Health Data, Technology, and Interoperability final rule. The source-attribute requirement applies to AI-driven clinical decision support in certified health IT — the agent must surface the source provenance of its recommendations to the clinician. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.12.5

### Q: What is the FFIEC IT Booklet on AI?
**A:** Federal Financial Institutions Examination Council guidance on AI for FSI institutions. Aligns with SR 11-7 MRM principles. In scope for any US federally-regulated FSI deployment. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.8

### Q: Name three APAC/Gulf regulatory regimes and the country each maps to.
**A:** **SAMA** (Saudi Arabia), **DFSA** (Dubai), **MAS** (Singapore TRM Guidelines), **HKMA** (Hong Kong). Plus data-protection acts: PDPA (Singapore), PIPL (China), DPDPA (India), UAE PDPL. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.11-15

### Q: What is PCI DSS 4.0 Req. 10, and what is its retention?
**A:** Audit-trail requirement for payment-card data. Retention: 1 year online + total 1 year (some controls — Req. 10.5.1 + 10.7). Heaviest for Recipe 1 (Support) payments customers. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.17 / §3.4.2

### Q: What is MAS TRM, and what is its retention?
**A:** Monetary Authority of Singapore Technology Risk Management Guidelines. Customer information records retained **5 years** (TRM §11.4). `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.4.2 / §3.5.13

### Q: What is DFSA retention for records?
**A:** **6 years** (DFSA Rulebook). Dubai Financial Services Authority. `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.4.2 / §3.5.12

### Q: What is the cross-regime summary — what does every Tier-1 FSI dossier carry?
**A:** Model inventory + Validation report + Ongoing monitoring + Model-swap log (SR 11-7); ICT register + Sub-processor list + Exit plan (DORA Art. 28); Incident log with multi-regime notification timelines (DORA Art. 19 + NYDFS 500.17 + GDPR Art. 33 + SEC Reg S-P); DPIA (GDPR Art. 35); Annex IV technical documentation (EU AI Act Art. 18); WORM-stored Sign-1..5 chain; STRIDE-A threat model.
**Cluster:** Regulatory regimes
**Tier reference:** §3.5.20

---

## Cluster 6 — The 14 governance failure modes (full catalog)

### Q: Failure Mode 1 — Indirect Prompt Injection — what is the mechanism?
**A:** Attacker plants instructions in content the agent will retrieve (document, Jira ticket, email, webpage, MCP response). The agent ingests the content alongside legitimate context and executes attacker-controlled instructions with user privileges. **The user never sees the payload.** The agent's notion of "instruction" is positional within the context window.
**Cluster:** Failure modes
**Tier reference:** §3.6.1

### Q: Failure Mode 1 — name three named-incident anchors.
**A:** **Slack AI** (PromptArmor, Aug 2024), **EchoLeak / CVE-2025-32711** (Aim Security, June 2025 — zero-click via crafted email in M365 Copilot), **CurXecute / CVE-2025-54135** (Aug 2025 — RCE in Cursor IDE via poisoned MCP server response). Also ChatGPT Atlas omnibox (Oct 2025) and ForcedLeak / Salesforce Agentforce (Sept 2025). `[named-incident]`
**Cluster:** Failure modes
**Tier reference:** §3.6.1

### Q: Failure Mode 1 — at which mitigation layer is the substrate-level closure?
**A:** **Research-stage.** Untrusted content executes in a separate inference context whose output to the trusted planner is a single typed value with no instruction-shaped degrees of freedom (Anthropic constitutional sub-task pattern, Microsoft Spotlighting research, OpenAI tool-use isolation research). At the agent-graph layer: HITL gating before destructive actions closes most blast radius.
**Cluster:** Failure modes
**Tier reference:** §3.6.1

### Q: Failure Mode 2 — Direct Prompt Injection — name three named-incident anchors.
**A:** **Bing Chat "Sydney" jailbreaks** (Feb 2023), **Air Canada / Moffatt v. Air Canada** (2024 — chatbot committed to non-existent fare class), **Chevrolet of Watsonville** (Dec 2023 — chatbot agreed to sell a Tahoe for $1), **DPD chatbot** (Jan 2024 — swearing + criticizing DPD). `[named-incident]`
**Cluster:** Failure modes
**Tier reference:** §3.6.2

### Q: Failure Mode 3 — Sensitive-Data Exfiltration via Consumer LLM Endpoints — name three anchors.
**A:** **Samsung semiconductor source-code leak** (Apr 2023, 3 incidents in 20 days), **JPMorgan / Verizon / Amazon / Apple / Citi ChatGPT bans** (2023), **LayerX Enterprise GenAI 2024 Adoption Report** — 40% of employee file uploads contain PII. Also DeepSeek API+chat exposure (Wiz, Jan 2025) and OmniGPT alleged breach (Feb 2025, 34M user messages). `[named-incident] [benchmark]`
**Cluster:** Failure modes
**Tier reference:** §3.6.3

### Q: Failure Mode 4 — Observability / Telemetry Capture — what is the fail-closed architectural posture?
**A:** **Never ship traces with PII to a multi-tenant trace store.** Self-hosted trace destination for any PII-bearing deployment. PII redaction at trace boundary via `process_inputs` / `process_outputs`. Per HIPAA §164.312(b), the trace bus IS part of the audit infrastructure.
**Cluster:** Failure modes
**Tier reference:** §3.6.4

### Q: Failure Mode 5 — Cross-Tenant Aggregation — name three anchor incidents and the recipe most exposed.
**A:** **Microsoft Copilot for M365 over-sharing** (2024-2025, multiple customer reports), **ConfusedPilot** (UT Austin academic, 2024), **Glean cross-workspace edge cases** (community-reported). HIGHEST in **Recipe 5 (Embedded SaaS)** — multi-tenancy is the architecture. `[named-incident]`
**Cluster:** Failure modes
**Tier reference:** §3.6.5

### Q: Failure Mode 6 — Identity & Action Provenance Gaps — name two anchors.
**A:** **Air Canada / Moffatt** (2024 — accountability ruling on chatbot actions), **SEC AI-washing enforcement actions** (Mar 2024 + Mar 2025), **Cursor support-agent hallucinated device-limit policy** (Apr 2025 — customer-acknowledged), **DPC Ireland enforcement** where consent provenance could not be reproduced. `[named-incident]`
**Cluster:** Failure modes
**Tier reference:** §3.6.6

### Q: Failure Mode 7 — Supply-Chain Compromise — what is the canonical first-public-RCE anchor?
**A:** **CurXecute / CVE-2025-54135 (Aug 2025)** — first public RCE via malicious MCP server response in production IDE agent (Cursor). Plus Hugging Face malicious model uploads (2023-2025 repeated), Anthropic-published list of known-malicious MCP servers (ongoing 2025+), PyPI typosquatting of `langchain`-adjacent packages. `[named-incident]`
**Cluster:** Failure modes
**Tier reference:** §3.6.7

### Q: Failure Mode 7 — name four named-component mitigations.
**A:** **Sigstore + Cosign** (image signing), **SLSA Level 3+** (build provenance), **in-toto v1** attestations, **MCP server allowlists** (Anthropic / OpenAI / Google), **dependency scanning** (Wiz Code / Snyk / Sonatype / JFrog Xray / Anchore / Aqua Trivy), hash-pinned `requirements.txt` / `pyproject.toml`, certificate pinning + model-hash verification at every model call.
**Cluster:** Failure modes
**Tier reference:** §3.6.7

### Q: Failure Mode 8 — Policy / RBAC Enforcement Bypass via Agent Direct-DB Access — name the canonical anchor.
**A:** **Replit Agent prod-DB deletion** (May 2025, customer-acknowledged) — agent autonomously dropped production DB with service-account credentials, against explicit user instruction. Plus community-reported Text-to-SQL agents joining across permission boundaries and ServiceNow Now Assist over-permissioning incidents. `[named-incident] [community-reported]`
**Cluster:** Failure modes
**Tier reference:** §3.6.8

### Q: Failure Mode 8 — what is the mechanism in one sentence?
**A:** Application enforces RBAC at API layer; agent given a DB or internal-API tool queries the underlying store directly with a service-account principal — application-layer RBAC silently bypassed. Audit log records the service-account query, not the user request. Invisible to existing DLP.
**Cluster:** Failure modes
**Tier reference:** §3.6.8

### Q: Failure Mode 9 — Data Residency / Sovereignty Violation — name three anchors.
**A:** **Italian Garante temporary ChatGPT ban** (Mar-Apr 2023 — cross-border flow + no legal basis), **Schrems II / Privacy-Shield-successor audits** flagging generative-AI flows, **DPA enforcement DE / FR / IT** against firms using US LLMs for EU data without SCC + TIA + supplementary measures, **Korean PIPC action** against generative-AI services (2024). `[named-incident]`
**Cluster:** Failure modes
**Tier reference:** §3.6.9

### Q: Failure Mode 9 — what should you disable for residency-sensitive deployments?
**A:** **Bedrock cross-region inference profiles.** Plus per-call region pinning at every provider (Anthropic regional API, Azure OpenAI regional, Vertex regional). FQDN egress allow-list per region. Per-node residency tags in the state graph. The cleanest fail-closed: in-region self-hosted models (vLLM / NIM on local hardware).
**Cluster:** Failure modes
**Tier reference:** §3.6.9

### Q: Failure Mode 10 — Hallucinated Action — name three named-incident anchors.
**A:** **Cursor support-agent hallucinated device-limit policy** (Apr 2025), **Mata v. Avianca + Park v. Kim** (2d Cir. 2024) + multiple state-bar disciplinary actions through 2025, **Replit Agent prod-DB deletion** (May 2025). Distinct from a hallucinated answer — the agent hallucinated an action against the real world. `[named-incident]`
**Cluster:** Failure modes
**Tier reference:** §3.6.10

### Q: Failure Mode 10 — what is the two-LLM mitigation pattern?
**A:** Cross-check on tool-args — planner LLM proposes the call, validator LLM critiques it, only confluence proceeds. Plus schema-validated argument check against real-time enumeration of valid IDs (e.g., before a refund, verify the `order_id` exists). Plus rate limits + blast-radius caps on writes.
**Cluster:** Failure modes
**Tier reference:** §3.6.10

### Q: Failure Mode 11 — Memory Poisoning — what makes it more dangerous than one-shot prompt injection?
**A:** Poisoned memory is **durable, hidden, and replays the attack on every future invocation** until someone audits and purges. A single successful prompt injection or piece of bad retrieved content can persist in agent memory, influencing every subsequent decision across sessions.
**Cluster:** Failure modes
**Tier reference:** §3.6.11

### Q: Failure Mode 11 — name three named-incident anchors.
**A:** **AgentDojo benchmark** scenarios demonstrating persistent compromise (2024), **OpenAI long-term memory persistence attacks** (2024, Simon Willison disclosures), **ChatGPT memory feature** initially leaked across sessions/accounts (2024, fixed), **LangChain `ConversationSummaryMemory`** retaining injected instructions across resets (2024-2025). `[named-incident] [community-reported] [benchmark]`
**Cluster:** Failure modes
**Tier reference:** §3.6.11

### Q: Failure Mode 12 — Excessive Agency — what is the canonical anchor?
**A:** **Replit Agent prod-DB deletion** (May 2025) — canonical. Plus Sakana AI "AI Scientist" attempting to modify its own startup script (Aug 2024, contained but disclosed), and e-commerce refund-bot scaled-fraud incidents (community reports). `[named-incident] [community-reported]`
**Cluster:** Failure modes
**Tier reference:** §3.6.12

### Q: Failure Mode 12 — name four named-component mitigations.
**A:** Principle of least authority enforced at tool definition. **Graduated authority** (read → write-staging → write-prod with HITL). Per-tool rate caps. Per-tool blast-radius caps (max records modified per call). HITL approval for irreversible actions. **Two-person approval** for high-blast-radius actions. Kill-switch operable in real time.
**Cluster:** Failure modes
**Tier reference:** §3.6.12

### Q: Failure Mode 13 — Compliance Evidence Gap — what does the regulator need that fragments cannot provide?
**A:** A complete, tamper-evident, time-bound record of "what did your AI agent do on date D for customer C and on what basis." Fragments (partial LangSmith traces, partial application logs, partial DB audit logs, partial cloud-provider logs) cannot reconstruct the decision chain end-to-end with cryptographic integrity. The §3.4 Cookbook is the mitigation pattern.
**Cluster:** Failure modes
**Tier reference:** §3.6.13

### Q: Failure Mode 14 — Model Swap / Runtime Drift — what is the canonical case?
**A:** **Klarna May 2025 reversal** — Sebastian Siemiatkowski admission of "lower quality" output, requiring human-always-available; "Uber-style" workforce model adopted. The canonical case of vendor-disclosed metrics being walked back over time. Plus Stanford/Berkeley "How is ChatGPT's behavior changing over time?" (arXiv 2307.09009) + Anthropic / OpenAI / Google scheduled model retirements forcing in-flight migrations. `[customer-produced-evidence] [benchmark]`
**Cluster:** Failure modes
**Tier reference:** §3.6.14

### Q: Failure Mode 14 — what is the per-call mitigation pattern?
**A:** Per-call attestation that the model behind the endpoint is the approved model (model-fingerprint check). System-prompt content-hash check at call time. **Signed manifest of {model_version_hash, system_prompt_hash, tool_registry_hash} bound to each interaction.** Canary deployment with quantitative rollback criterion. Anthropic / OpenAI dedicated capacity reservations to pin to specific model versions.
**Cluster:** Failure modes
**Tier reference:** §3.6.14

### Q: What is the substrate-level cluster, and how many of the 14 failure modes does it cover?
**A:** **8 of 14** failure modes share a single technical predicate — the protection boundary is at the application layer where the agent can bypass it, not at the substrate where it cannot. The eight: FM 3, 4, 5 (cache + model surfaces), 6, 7, 9, 13, 14.
**Cluster:** Failure modes
**Tier reference:** §3.6.15

### Q: What two primitives does the substrate-level cluster's remediation reduce to?
**A:** (1) **Cryptographic attestation that the runtime is what was approved** — TEE attestation (Intel TDX, AMD SEV-SNP, NVIDIA H100/H200 Confidential Compute), measured boot chains, remote attestation. (2) **Hardware-enforced confidentiality of data-in-use** — memory encryption with attested workload identity. Neither implementable above the hardware boundary.
**Cluster:** Failure modes
**Tier reference:** §3.6.15

### Q: What is STRIDE-A?
**A:** STRIDE + **Autonomy abuse** — the agent-specific threat-model category. Captures the agent acting beyond its sanctioned scope (FM 10, 12, 14). The Field Guide uses STRIDE-A per recipe in §3.7 and §3.6.16.
**Cluster:** Failure modes
**Tier reference:** §3.6.16

### Q: Map STRIDE-A to failure modes — which failure modes belong to Autonomy abuse?
**A:** **Autonomy abuse** — FM 10 (Hallucinated Action), FM 12 (Excessive Agency), FM 14 (Model Swap / Runtime Drift). The agent operating outside its sanctioned envelope.
**Cluster:** Failure modes
**Tier reference:** §3.6.16

### Q: What are the residual TEE-attestation risks an SE should be able to name?
**A:** Microarchitectural side channels (timing, power, port-contention), TCB (Trusted Computing Base) size, attestation revocation latency, key custody outside the TEE (BYOK / HYOK boundaries). The procurement-grade evaluation question: which of the 8 substrate-level failure modes does a candidate architecture close, with which substrate primitive, with which residual risk?
**Cluster:** Failure modes
**Tier reference:** §3.6.15

---

## Cluster 7 — Recipe Production deep-dives

### Q: Recipe 1 — Support Agent — what is the Klarna-lesson-aware HITL placement pattern?
**A:** Not just at high-blast-radius actions (refunds > $X), but at the **confidence-gate boundary** — when the supervisor classifies a session as low-confidence, route to a human BEFORE the customer experiences a degraded interaction. CSAT and fallback rate are primary KPIs, NOT autonomy rate.
**Cluster:** Recipe deep-dives
**Tier reference:** §3.9.4 / §3.7.1

### Q: What is a "confidence gate" in the Klarna-lesson-aware Recipe 1 architecture?
**A:** A state-graph node that classifies session confidence; routes low-confidence sessions to human fallback BEFORE customer-experience degradation. Per-session outcome classification records the confidence score; A/B testing of confidence thresholds is ongoing.
**Cluster:** Recipe deep-dives
**Tier reference:** §3.9.4

### Q: Recipe 1 — what is Vodafone Italy / Fastweb's One-Call Resolution rate, and what is the architectural pattern?
**A:** **86%+ One-Call Resolution.** Dual-graph architecture: **Supervisor + Use Cases**, Neo4j-backed knowledge graph. The "Super Agent never speaks to customers" pattern — human-in-the-loop for the customer-facing surface. Implicit endorsement of the Klarna reversal lesson. `[customer-produced-evidence]`
**Cluster:** Recipe deep-dives
**Tier reference:** §3.7.1

### Q: Recipe 2 — Coding Agent — what is the SLSA Level for the resulting build, and what regime expansion applies?
**A:** **SLSA Level 3+** attestation on the resulting build. SOX in scope where the deployed system is in financial-reporting scope. Sign-1 (which engineer authorized which PR) + Sign-4 (commit / merge / deploy actions) heaviest.
**Cluster:** Recipe deep-dives
**Tier reference:** §3.4.10 / §3.7.2

### Q: Recipe 3 — Text-to-SQL — what is the most-load-bearing regulatory regime, and what evidence is mandatory?
**A:** **FINRA Rule 5280** (information-barrier compliance) for FSI; **GDPR Art. 22** for any decision-bearing query. **OpenLineage emission mandatory.** Sign-2 (which dataset accessed) + Sign-4 (which SQL query executed) heaviest.
**Cluster:** Recipe deep-dives
**Tier reference:** §3.4.10

### Q: Recipe 4 — Deep Research — what discipline is embedded in Sign-5, and what is the named-incident anchor?
**A:** **Citation discipline** — every claim in the final research output traces to a Sign-2 event. Anchor: **Mata v. Avianca** (lawyer cited ChatGPT-fabricated cases in federal filing). `[named-incident]`
**Cluster:** Recipe deep-dives
**Tier reference:** §3.4.10

### Q: Recipe 5 — Embedded SaaS Copilot — what is the audit-evidence proof for "tenant A did not see tenant B's data"?
**A:** Every Sign-1 through Sign-5 carries the `tenant_id`; the audit-evidence proof is the **cross-surface tenant binding integrity** — all five cross-tenant isolation surfaces (retriever, cache, checkpointer, observability, model) consistently carrying the same tenant_id.
**Cluster:** Recipe deep-dives
**Tier reference:** §3.4.10

### Q: Recipe 6 — SOC Agent — what is the heightened auditability requirement, and why?
**A:** **Read trail of read trail.** The SOC agent IS the audit infrastructure, so it must hold itself to a higher bar. Every read access to WORM-stored traces is itself a logged security event.
**Cluster:** Recipe deep-dives
**Tier reference:** §3.4.10

---

## Cluster 8 — Klarna May 2025 reversal (dedicated card sequence)

### Q: Klarna timeline — what was the February 2024 launch metric?
**A:** "**Work equivalent of 700 full-time staff**" — Klarna press release 2024-02-27. AI assistant handled two-thirds of customer service chats in its first month. `[vendor-public — Klarna marketing]`
**Cluster:** Klarna reversal
**Tier reference:** §3.9.1

### Q: Klarna timeline — what happened on May 9, 2025?
**A:** Sebastian Siemiatkowski reversed course publicly. Fortune 2025-05-09 quote: *"It's so critical that you are clear to your customer that there will always be a human if you want."* AI customer service chatbots were cheaper but resulted in **"lower quality"** output. Klarna began piloting an "Uber-style" workforce model. `[customer-produced-evidence]`
**Cluster:** Klarna reversal
**Tier reference:** §3.9.1

### Q: Klarna reversal — name the four SR 11-7 §III.4 validation pillars the 700-FTE claim fails on.
**A:** **Not independent** (Klarna was developer + validator), **not outcome-validated** ("equivalent" frame masked actual CSAT), **not benchmark-compared** (no equivalent human-baseline measurement in same window), **not stress-tested** (early-month adoption pattern is not representative of steady state). All four required — all four failed. `[primary-regulatory + customer-produced-evidence]`
**Cluster:** Klarna reversal
**Tier reference:** §3.9.2

### Q: Klarna reversal — state the SE-grade single-sentence teaching.
**A:** "Klarna's 700-FTE-equivalent number is benchmark and conversation material; it is **not validation evidence under SR 11-7 §III.4**, and the May 2025 CEO reversal is the canonical proof." `[customer-produced-evidence + primary-regulatory]`
**Cluster:** Klarna reversal
**Tier reference:** §3.9.2

### Q: Klarna reversal — name the R6+R5+R4 cross-stream convergence.
**A:** **R6 (Customer Voice)** — Klarna May 2025 reversal + Vodafone "Super Agent never speaks to customers" + Replit's Catasta on "control and ergonomics" + LinkedIn's "agent as org chart." **R5 (Academic + Community)** — Anthropic's "don't build multi-agent" thesis. **R4 (Data-leak surfaces)** — Failure Mode 14 (Model Swap / Runtime Drift). Convergence: narrower scope + more HITL beats broader scope + autonomy on operational metrics.
**Cluster:** Klarna reversal
**Tier reference:** §3.9.3

### Q: Klarna reversal — what is the PRD-grade single sentence?
**A:** "Scale autonomy carefully; the production outcome data, the Anthropic thesis, and the named-incident pattern all point the same direction — **narrower scope + HITL beats broader scope + autonomy** on operational metrics."
**Cluster:** Klarna reversal
**Tier reference:** §3.9.3

### Q: Klarna citation-class — the "700 FTE-equivalent" claim should be tagged how, given the May 2025 reversal?
**A:** **`[vendor-public]`** with a `[customer-produced-evidence — May 2025 reversal]` superseding annotation. Specifically NOT `[independently-audited]`. Any procurement-grade artifact citing 700 FTE must reference the May 2025 reversal.
**Cluster:** Klarna reversal
**Tier reference:** §3.9 / design-spec §13

---

## Cluster 9 — Insurance gap

### Q: What is the insurance sector's gen-AI / agent adoption rate per the R3 deep-dive?
**A:** **68% of publicly-disclosed insurance deployments are generative or agentic; 21% specifically agentic.** Insurance full-AI adoption jumped from 8% to 34% YoY (2024→2025). `[benchmark]`
**Cluster:** Insurance gap
**Tier reference:** §3.10.1

### Q: What is the insurance pilot-to-production abandonment rate, and what is the LangGraph footprint?
**A:** **42% of insurance companies abandoned most of their generative AI initiatives in 2025**, up from 17% the year prior. **Highest pilot-to-production abandonment rate of any documented sector.** Zero LangGraph footprint as of 2026-05. `[benchmark] [vendor-public — explicit gap]`
**Cluster:** Insurance gap
**Tier reference:** §3.10.1

### Q: Name three named insurance AI deployments — none on LangGraph — and the stack each uses.
**A:** **Lemonade Maya/Jim/Cooper agents** (in-house orchestration on TensorFlow / native ML; pet insurance grew 55% YoY; LAE ratio 13% → 7%); **Progressive AI claims tools** (in-house + Azure); **Munich Re REALYTIX ZERO CoPilot** (SAP + Microsoft); **Hiscox AI lead underwriting** (BigQuery + Vertex); **HDFC ERGO** (Vertex). `[customer-produced-evidence] [vendor-public]`
**Cluster:** Insurance gap
**Tier reference:** §3.10.2

### Q: What is the SE-grade posture for an insurance prospect?
**A:** Lead with architectural rigor; flag the insurance-specific evidence gap explicitly; recommend a small-scope PoC with explicit operational metrics; commit to the §3.4 audit-evidence pattern from day one (not retrofitted); set the **42% abandonment-rate context honestly.**
**Cluster:** Insurance gap
**Tier reference:** §3.10.4

---

## Cluster 10 — Operational-lifecycle 4-event role-play

### Q: Event 1 — Day 1 EchoLeak-class incident response — what is the first 5-minute containment decision?
**A:** **Quarantine the affected tenant** via kill-switch / circuit-breaker (rate-limit affected sessions to zero, route in-flight conversations to human fallback). Do NOT kill globally without evidence of cross-tenant blast radius — kill-globally is its own incident.
**Cluster:** Operational lifecycle
**Tier reference:** §3.13.1

### Q: Event 1 — where do you query first during investigation?
**A:** **The WORM trace store.** Query Sign-4 events in the affected window: `tool_id`, `args_hash`, `result_hash`, `on_behalf_of_user_id`. Cross-reference Sign-2 (retrieval invocation) for the same sessions. Look for `tool_result_hash` that does not match a known content-classifier signature.
**Cluster:** Operational lifecycle
**Tier reference:** §3.13.1

### Q: Event 1 — what triggers a DORA Art. 19 major-incident classification?
**A:** Any of: **> 10 affected customers OR > €1M financial impact OR cross-border crisis impact.** Triggers the **24-hour early-warning clock**. Also classify NYDFS Part 500.17 (72-hr, if NY operations), GDPR Art. 33 (72-hr), SEC Reg S-P (30-day for US counterparties affected).
**Cluster:** Operational lifecycle
**Tier reference:** §3.13.1

### Q: Event 1 — who is on the notification call list for a Sweden-HQ EU-customer payments deployment?
**A:** **Competent authority (Finansinspektionen in Sweden)** + DPO (for GDPR Art. 33) + customer-side incident-response lead + **LangChain Ops (sub-processor notification)** + **Anthropic Trust & Safety** (model-side) + **Pinecone** (retrieval-side sub-processor notification).
**Cluster:** Operational lifecycle
**Tier reference:** §3.13.1

### Q: Event 2 — Day 30 Claude version-swap MRM — what is the rollback criterion pattern?
**A:** **Pre-defined and quantitative, NOT negotiated during canary.** Example: 5% traffic for 14 days; rollback if CSAT drops > 3 points OR fallback rate increases > 1 pp OR incident_candidate rate increases > 0.5 pp.
**Cluster:** Operational lifecycle
**Tier reference:** §3.13.2

### Q: Event 2 — for a Tier-1 SR-11-7-covered entity, who signs off on a material model change?
**A:** **Model Risk independent validator** (second-line concurrence). NOT the development team. Documented sign-off in the model inventory.
**Cluster:** Operational lifecycle
**Tier reference:** §3.13.2

### Q: Event 2 — what is the rollback-availability window required during canary?
**A:** **90+ days post-cutover.** Provisioned throughput reservation maintained for the prior model version (e.g., Claude 4.7) — model_version_hash remains in inventory with status "rollback-candidate" until decommission window passes.
**Cluster:** Operational lifecycle
**Tier reference:** §3.13.2

### Q: Event 3 — Day 60 sub-processor change notification — what is the customer's window under DORA Art. 28 + GDPR Art. 28?
**A:** **30 days** to assess the change for concentration risk + update ICT register, with reasonable objection window. Combined: customer has 30 days to object or accept; objection triggers contract-termination right.
**Cluster:** Operational lifecycle
**Tier reference:** §3.13.3

### Q: Event 3 — under what conditions does the customer object to a sub-processor change?
**A:** (a) Sub-processor is in a jurisdiction the customer's data-residency commitments prohibit; (b) lacks SOC 2 Type II or equivalent attestation; (c) lacks a satisfactory DPA; (d) introduces material concentration risk.
**Cluster:** Operational lifecycle
**Tier reference:** §3.13.3

### Q: Event 4 — Day 90 ECB examination — can a deployment produce all 12 dossier artifacts in 48 hours?
**A:** **Yes, if the §3.4 Audit-Evidence Cookbook has been operationally in place from day one.** Artifacts live in documented locations (MRM portal, compliance portal, privacy portal, security portal, customer trace bus / SIEM, S3 Object Lock WORM); the per-recipe Evidence Index tells the compliance team exactly where to retrieve each.
**Cluster:** Operational lifecycle
**Tier reference:** §3.13.4

### Q: Event 4 — which of the 12 dossier artifacts is hardest to produce on demand, and why?
**A:** **Artifact 8 — data-leak-surface mapping with residual risk** for the specific deployment — because it requires **synthesis (not just retrieval).** Compliance holds the catalog; security holds the deployment-specific mapping; §3.6 framework is the synthesis pattern.
**Cluster:** Operational lifecycle
**Tier reference:** §3.13.4

### Q: Event 4 — what is the disposition for a missing artifact?
**A:** **Document the gap in the response; commit to a remediation timeline; do not fabricate.** The examiner asks "what is missing" once — the candidate's honesty here governs the rest of the examination.
**Cluster:** Operational lifecycle
**Tier reference:** §3.13.4

---

## Cluster 11 — Hyperscaler peer ref-arch (DEEP)

### Q: What is the most LangGraph-friendly hyperscaler ref-arch, and what is the AWS-documented framework-native path?
**A:** **AWS Bedrock Agents + AgentCore.** Documented LangGraph-on-ECS pattern behind AgentCore Gateway. AppFolio Realm-X is the canonical customer-disclosed deployment. **GovCloud Bedrock at FedRAMP-High + IL4/IL5 since May 2025.** `[vendor-public] [customer-produced-evidence]`
**Cluster:** Hyperscaler ref-archs
**Tier reference:** §3.8.2

### Q: What is the §3.8.9 "white-space" observation reformulated for the Production audience?
**A:** Microsoft, AWS, GCP, NVIDIA, Snowflake, Databricks, IBM, Salesforce all publish ref-archs — but **nobody publishes a framework-native LangGraph-centric reference architecture covering 10 stack tiers × 6 recipes × 7 topologies × cross-cloud shapes × per-regime compliance × audit-evidence patterns.** This Field Guide is the most thorough attempt to date.
**Cluster:** Hyperscaler ref-archs
**Tier reference:** §3.8.9

### Q: What is the Salesforce Agentforce ref-arch status, and what named incident is attached?
**A:** Purpose-built enterprise agent platform. **ForcedLeak (Noma Security, Sept 2025) — indirect injection via web form.** Teaches that purpose-built enterprise agent platforms are not automatically safe. `[vendor-public] [named-incident]`
**Cluster:** Hyperscaler ref-archs
**Tier reference:** §3.8.8 / §2.7.4

---

## Cluster 12 — Sovereign / Public Sector

### Q: What is the LangGraph sovereign deployment status as of 2026-05?
**A:** **Zero public LangGraph sovereign deployment** — `[evidence-zero, structural-fit-only]`. Architecturally realizable via Self-Hosted Enterprise + customer-hosted vLLM/NIM/TensorRT-LLM + customer HSM + customer-hosted Langfuse + air-gap egress allow-list. No operational validation.
**Cluster:** Sovereign / Public Sector
**Tier reference:** §3.11

### Q: Name three Gulf sovereign-cloud substrate options.
**A:** **Core42** (UAE), **Bleu** (France), **S3NS** (Thales / Google joint), **Delos** (France), **AWS European Sovereign Cloud**, **Azure Local Sovereign**, **Oracle Sovereign**. Plus EU sovereign — Gaia-X, SecNumCloud / ANSSI, EUCS "high," BSI C5.
**Cluster:** Sovereign / Public Sector
**Tier reference:** §3.11.1

### Q: What is the FedRAMP-High path that does exist for LangGraph deployments needing federal-grade compliance?
**A:** **Self-Hosted Enterprise on FedRAMP-High authorized enclave** (e.g., AWS GovCloud + customer authorization boundary) + Anthropic via Palantir FedStart for the model + customer-hosted Langfuse + customer HSM + air-gap egress allow-list. No public LangGraph FedRAMP authorization at the orchestration layer.
**Cluster:** Sovereign / Public Sector
**Tier reference:** §3.11.1

### Q: What is the Anthropic-via-Palantir FedStart path?
**A:** Federal-government path for Anthropic Claude availability under FedRAMP-High envelope via Palantir's FedStart authorization. The named substrate option for sovereign / federal LangGraph deployments needing Anthropic at the model tier. `[vendor-public]`
**Cluster:** Sovereign / Public Sector
**Tier reference:** §3.11.1

---

## Cluster 13 — Healthcare PHI

### Q: What is the OCR Risk Analysis Initiative?
**A:** HHS Office for Civil Rights audit campaign on PHI risk-analysis posture across covered entities. The agent's documented risk analysis must address the 14 failure modes mapped to the deployment. `[primary-regulatory]`
**Cluster:** Healthcare PHI
**Tier reference:** §3.12.3

### Q: For PHI-adjacent deployment, what is the BAA chain that must be documented?
**A:** **Anthropic ↔ Bedrock ↔ LangChain ↔ reranker ↔ customer-app.** Plus de-identification engineering (Safe Harbor or Expert Determination) is non-negotiable for any PHI-adjacent deployment.
**Cluster:** Healthcare PHI
**Tier reference:** §1.12.2 / §3.12.2

### Q: What is the FDA PCCP allowed model-version drift envelope concept?
**A:** **Predetermined Change Control Plan** defines the pre-authorized model-version drift envelope for an AI/ML SaMD; changes within the envelope can ship without new submission, changes outside require new FDA submission. The model-swap protocol is constrained by PCCP for clinical decision support. `[primary-regulatory]`
**Cluster:** Healthcare PHI
**Tier reference:** §3.12.4

---

## Cluster 14 — Citation classes (Production-depth)

### Q: When should a claim carry `[primary-regulatory]`?
**A:** When sourced directly from a regulation, statute, or supervisory letter (DORA, GDPR, EU AI Act, SR 11-7, OCC 2011-12, SEC 17a-4, FINRA, MiFID II, NYDFS, HIPAA, PCI DSS, FedRAMP NIST 800-53, MAS TRM, etc.). The highest-weight evidence class for regulatory claims.
**Cluster:** Citation-class recall
**Tier reference:** §3.5 / design-spec §13

### Q: Why is the Klarna "700 FTE" metric tagged `[vendor-public]` and NOT `[independently-audited]`?
**A:** Because (a) Klarna was both the developer and the validator (not independent), (b) the metric was an "equivalent" frame, not an outcome-validated measurement, (c) no benchmark comparison, (d) not stress-tested. Per SR 11-7 §III.4 — fails all four pillars. The May 2025 reversal is the empirical confirmation.
**Cluster:** Citation-class recall
**Tier reference:** §3.9.2

### Q: Which evidence class applies to the LangGraph sovereign-deployment claims in §3.11?
**A:** **`[evidence-zero, structural-fit-only]`** — the architecture is theoretically realizable; no public production deployment exists. Every claim in §3.11 carries this tag. Honest framing per design-spec §2.3: do NOT represent as "validated."
**Cluster:** Citation-class recall
**Tier reference:** §3.11.2

### Q: Which evidence class applies to LangGraph Healthcare PHI claims, and what is the operational status?
**A:** **`[reference design]`** — no production LangGraph PHI deployment on any framework as of 2026-05. The architecture is feasible; operational evidence is zero.
**Cluster:** Citation-class recall
**Tier reference:** §3.12.6

### Q: Why is `[architectural inference]` a red-flag tag in FSI deployment dossiers?
**A:** Because FSI procurement requires substantiated claims, not inferences. An `[architectural inference]` tag in a customer-facing FSI artifact signals the SE / SC is reasoning from the architecture rather than from documented evidence — opens credibility risk in a CISO / MRM review.
**Cluster:** Citation-class recall
**Tier reference:** §3.14.1 Q15 / design-spec §13

---

## Cluster 15 — Operational vocabulary (Production glossary)

### Q: Define "agent manifest" in one sentence.
**A:** The five hashes (`model_version_hash` + `system_prompt_hash` + `tool_registry_hash` + `retrieval_index_hash` + `agent_graph_hash`) + sub-processor list + retention policy — the §3.4.4 reproducibility artifact that a regulator asks for first.
**Cluster:** Production vocabulary
**Tier reference:** §3.15

### Q: Define "concentration risk" per DORA Art. 28(2).
**A:** The assessment a financial entity must perform before entering an ICT third-party agreement — documenting that viable substitute providers exist. For LangGraph: alternatives include CrewAI Enterprise, MAF, OpenAI Agents SDK, LlamaIndex Workflows, Semantic Kernel. `[primary-regulatory]`
**Cluster:** Production vocabulary
**Tier reference:** §3.15

### Q: Define "TLPT."
**A:** **Threat-Led Penetration Testing** — DORA Art. 24-26 mandatory testing for systemically important entities. For agents, must include AgentDojo / InjecAgent / AgentHarm benchmark-style scenarios + named-incident replays (EchoLeak, ConfusedPilot, Replit). `[primary-regulatory]`
**Cluster:** Production vocabulary
**Tier reference:** §3.15

### Q: Define "ZDR addendum."
**A:** **Zero-Data-Retention addendum** — enterprise-LLM-plan contractual addendum committing the provider to not retain or train on inputs. Modal for FSI / Healthcare deployments using Anthropic / OpenAI / Bedrock / Azure OpenAI. `[vendor-contractual]`
**Cluster:** Production vocabulary
**Tier reference:** §3.15 / §3.6.3

### Q: Define WORM and name five named WORM products.
**A:** **Write Once Read Many** — non-rewriteable, non-erasable storage. **AWS S3 Object Lock Compliance, Azure Immutable Blob, GCP Bucket Lock, NetApp SnapLock, Dell PowerScale SmartLock.** `[vendor-public]`
**Cluster:** Production vocabulary
**Tier reference:** §3.15 / §3.4.2

### Q: Define "TEE attestation."
**A:** Cryptographic attestation that the runtime is what was approved. Substrate primitives: **Intel TDX, AMD SEV-SNP, NVIDIA H100/H200 Confidential Compute.** Plus measured boot chains and remote attestation to a verifier. The mitigation for the 8-of-14 substrate-level failure-mode cluster.
**Cluster:** Production vocabulary
**Tier reference:** §3.15 / §3.6.15

### Q: Define "break-glass" in the LangGraph context.
**A:** Vendor SRE access path with audit trail. Three postures: customer-mediated (vendor does NOT get direct read; modal for Tier-1 FSI), read-on-incident (vendor reads only during active incident; mid-market), full-read (not acceptable for FSI). `[vendor-public]`
**Cluster:** Production vocabulary
**Tier reference:** §3.15 / §3.4.8

### Q: Define "BYOC dataplane-listener."
**A:** The Helm-installed CRD-watching pod that polls the LangChain control plane over HTTPS in BYOC deployments. The mechanism BYOC works through — and the egress path the customer must allow-list at the egress proxy. `[vendor-public]`
**Cluster:** Production vocabulary
**Tier reference:** §3.15 / §3.1.2

### Q: Define "ICT register entry" under DORA Art. 28.
**A:** The per-sub-processor record a financial entity maintains, including: provider name + address, services provided, criticality, contract dates, data processed + location, sub-processors, **concentration risk assessment**, exit plan reference, termination notice, DORA compliance attestation date. `[primary-regulatory]`
**Cluster:** Production vocabulary
**Tier reference:** §3.15 / §3.5.1

---

## Cluster 16 — Worked-fragment depth (Production)

### Q: Worked fragment — Sign-1 prompt-envelope JSON schema essentials.
**A:** `{user_id, tenant_id, session_id, request_id, prompt_hash, system_prompt_hash, model_version, tool_registry_version, retrieval_index_version, agent_graph_version, timestamp}` — signed by HSM key A, RFC 3161 timestamped, hashed to `h1`. Anchors the chain to Sign-2 via `prev_hash`.
**Cluster:** Worked fragments
**Tier reference:** §3.4.1

### Q: Worked fragment — Sign-4 tool-call schema essentials.
**A:** `{prev_hash, tool_id, tool_version, args_hash, on_behalf_of_user_id, agent_workload_id, fga_decision, result_hash, latency, side_effects_recorded, timestamp}` — HSM-signed to `h4`. Combines workload identity, agent-on-behalf-of-user delegation, and FGA decision in one signed event.
**Cluster:** Worked fragments
**Tier reference:** §3.4.1

### Q: Worked fragment — what does this OTel attribute set populate?
```json
{
  "outcome_classification": "success | error | hitl | injection_detected | rbac_bypass_attempted",
  "incident_candidate": true,
  "affected_user_count": 1,
  "regulatory_relevance": ["dora_art_19", "gdpr_art_33", "nydfs_500_17"]
}
```
**A:** The DORA RTS 2024/1772 ICT incident schema minimum agent-side fields. When `incident_candidate=true`, the trace is forked to the SIEM's incident-management queue and the SOC clock starts. `[primary-regulatory]`
**Cluster:** Worked fragments
**Tier reference:** §3.4.3

### Q: Worked fragment — what is this Helm chart pattern asserting?
```yaml
image:
  tag: "0.4.x"  # pin explicit, do not use :latest
```
**A:** **Pin the image tag.** `:latest` in production is incompatible with SR 11-7 model-inventory discipline and DORA Art. 9 change-management. The first thing a regulator-aware SRE checks. `[primary-regulatory]`
**Cluster:** Worked fragments
**Tier reference:** §3.1.2

### Q: Worked fragment — what RAR shape is this for Recipe 6 (SOC)?
```json
{
  "type": "soc_action",
  "actions": ["isolate_host"],
  "target": {"hostname": "alpha-fw-12.corp"},
  "incident_id": "INC-2026-04-12-0014",
  "approval_required": true
}
```
**A:** Rich Authorization Request for a SOC containment action — authorizing exactly this isolate-host action on this specific host for this specific incident, with explicit HITL approval required. Maps to FM 12 (Excessive Agency) mitigation via graduated authority + per-tool RAR scope.
**Cluster:** Worked fragments
**Tier reference:** §3.6.12 / §2.4.5

### Q: Worked fragment — what does this Evidence Index row encode?
```
ARTIFACT                       │ STORED AT          │ RETAINED  │ RETRIEVED BY
Sign-1..5 chain (full session) │ S3 Object Lock     │ 10 yr     │ Privileged inv.
```
**A:** The Sign-1..5 cryptographic action chain — stored in WORM (S3 Object Lock Compliance mode) for 10 years (EU AI Act Art. 12 compliance), retrieved by a privileged investigator under two-person rule with the read access itself logged as a security event.
**Cluster:** Worked fragments
**Tier reference:** §3.4.11

---

## Cluster 17 — Recipe × Failure-mode exposure (per-recipe matrix recall)

### Q: For Recipe 1 (Support), which failure modes have HIGHEST exposure?
**A:** FM 1 (Indirect Injection — Medium-High via tool results), FM 2 (Direct Injection — HIGH, user-facing), FM 6 (Identity & Provenance — Universal, heavy), FM 10 (Hallucinated Action — HIGH, Air Canada class), FM 12 (Excessive Agency — HIGH, refunds at scale).
**Cluster:** Recipe × failure-mode
**Tier reference:** §3.6 + §3.7.1

### Q: For Recipe 2 (Coding), which failure modes have HIGHEST exposure?
**A:** FM 1 (Indirect Injection — HIGH, CurXecute pattern via PR/build/lint output), FM 7 (Supply-Chain — Universal, exposed by CurXecute), FM 8 (RBAC bypass — HIGH, DB tools), FM 10 (Hallucinated Action — HIGHEST, write to production codebase), FM 12 (Excessive Agency — HIGHEST, Replit pattern).
**Cluster:** Recipe × failure-mode
**Tier reference:** §3.6 + §3.7.2

### Q: For Recipe 3 (Text-to-SQL), which failure modes have HIGHEST exposure?
**A:** FM 4 (Telemetry capture — EXTREME, PHI/NPI/PII in traces), FM 5 (Cross-tenant — HIGH, multi-tenant analytics), FM 8 (RBAC bypass — HIGHEST, by definition queries DB), FM 6 (Provenance — HIGH, every query needs provenance).
**Cluster:** Recipe × failure-mode
**Tier reference:** §3.6 + §3.7.3

### Q: For Recipe 4 (Deep Research), which failure modes have HIGHEST exposure?
**A:** FM 1 (Indirect Injection — VERY HIGH, by definition pulls arbitrary web content), FM 3 (Consumer-endpoint exfiltration — HEAVIEST, exploratory model usage), FM 10 (Hallucinated Action — EXTREME, Mata v. Avianca class via citation hallucination), FM 4 (Telemetry capture — HIGH, full payload in trace).
**Cluster:** Recipe × failure-mode
**Tier reference:** §3.6 + §3.7.4

### Q: For Recipe 5 (Embedded SaaS), which failure modes have HIGHEST exposure?
**A:** FM 4 (Telemetry capture — HEAVIEST, multi-tenant trace exposure modal failure), FM 5 (Cross-tenant — HIGHEST, multi-tenancy IS the architecture), FM 11 (Memory poisoning — HIGHEST, long-lived per-customer agents), FM 12 (Excessive Agency — HIGH, automation of customer workflows).
**Cluster:** Recipe × failure-mode
**Tier reference:** §3.6 + §3.7.5

### Q: For Recipe 6 (SOC), which failure modes have HIGHEST exposure?
**A:** FM 6 (Provenance — Universal, investigator actions), FM 4 (Telemetry capture — EXTREME, PHI/NPI in alerts), FM 5 (Cross-tenant — HIGH, multi-tenant SIEM), FM 12 (Excessive Agency — HIGH, containment actions like host isolation).
**Cluster:** Recipe × failure-mode
**Tier reference:** §3.6 + §3.7.6

---

## Cluster 18 — Cross-regime examination-day cards

### Q: Name the four regulatory regimes that all trigger incident-notification clocks for a Sweden-HQ EU FSI deployment with NY operations.
**A:** **DORA Art. 19** (24-hr early warning + 72-hr intermediate + 1-month final), **NYDFS Part 500.17** (72-hr), **GDPR Art. 33** (72-hr to supervisory authority), **SEC Reg S-P** (30-day, if US customer counterparties affected). `[primary-regulatory]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.13.1

### Q: What is the LangChain sub-processor list that must appear in any DORA Art. 28 register?
**A:** **Supabase** (auth), **ClickHouse** (telemetry). Plus the customer's chosen LLM provider (Anthropic / OpenAI), retrieval vendor (Pinecone / pgvector / Weaviate / Qdrant), reranker (Cohere / Voyage / BGE), and any optional LangSmith Cloud routing. `[vendor-public]`
**Cluster:** Regulatory regimes
**Tier reference:** §3.1.5 / §3.5.1

### Q: For an Frankfurt-HQ Tier-1 European bank with DORA + EU AI Act + NIS2 + GDPR + PCI DSS 4.0 scope, what is the modal deployment recommendation?
**A:** **Self-Hosted Enterprise on AKS in West Europe** (addresses BYOC-Azure gap by going to SHE) + Anthropic via Bedrock cross-cloud via existing ExpressRoute + Entra Agent ID + OAuth 2 token-exchange with `act` claim + Vault + self-hosted Langfuse + Splunk via OTel + Sign-1..5 HSM-backed (Thales Luna in customer DC).
**Cluster:** Deployment shapes
**Tier reference:** §3 Knowledge Gate Track 1

### Q: What is the canonical CISO question pattern for an FSI deployment evaluation?
**A:** Five-part: (1) Where does data physically reside? (2) Where does identity terminate (workload + delegation)? (3) Where do traces go and what is the trace-egress posture? (4) What is the action provenance chain — show me a single session's Sign-1..5 chain. (5) What is the exit plan / sub-processor concentration risk?
**Cluster:** Knowledge-gate vocabulary
**Tier reference:** §3 Track 1 gate

---

## Cluster 19 — Foundations / Patterns / Production integration recall

### Q: State the architectural fact that makes Self-Hosted Enterprise the only DORA-defensible posture for Tier-1 FSI.
**A:** **LangChain Ops cannot read customer-WORM-stored traces in Self-Hosted Enterprise.** Combined with no LangChain control-plane egress, no LangSmith Cloud mandatory trace destination, and customer control of the sub-processor chain — Self-Hosted Enterprise is the only shape that closes the DORA Art. 28 + Art. 30 + Art. 19 + Art. 9 cluster.
**Cluster:** Cross-tier integration
**Tier reference:** §3.4.6 / §3.1.4

### Q: Convergence — what do the Klarna May 2025 reversal, the Anthropic "don't build multi-agent" thesis, and Failure Mode 14 all teach?
**A:** **Narrower agent scope + more HITL + less cross-agent state-sharing outperforms broader scope + autonomy on operational outcome metrics** (CSAT, fallback rate, incident rate). Scale autonomy carefully. The Klarna reversal is the customer-acknowledged empirical confirmation.
**Cluster:** Cross-tier integration
**Tier reference:** §3.9.3 / §3.6.14

### Q: What is the canonical Foundations-to-Production through-line on "vendor-disclosed metrics"?
**A:** Foundations §1.11.3 introduces it; Patterns §2.7 reinforces in the failure-mode discussion; Production §3.9 operationalizes via the SR 11-7 §III.4 four-pillar validation framework. **Single sentence: vendor-disclosed metrics are not MRM-validation evidence under SR 11-7.** Klarna May 2025 is the canonical proof.
**Cluster:** Cross-tier integration
**Tier reference:** §3.9.2 / §1.11.3

### Q: What architectural posture survives a "Katy-Gordon-class documented-reality review"?
**A:** The Klarna-lesson-aware Recipe 1 architecture: **confidence-gate HITL placement** (not just blast-radius); **CSAT and fallback rate as primary KPIs** (not autonomy rate); **independently-audited outcome metrics** (not vendor-disclosed); **90+ day rollback availability** on model swaps.
**Cluster:** Cross-tier integration
**Tier reference:** §3.9.4

### Q: Three primary leakage pathways the agent stack introduces beyond traditional SaaS — recap with Production depth.
**A:** (1) **Tool / MCP invocation surface** — surfaced by CurXecute. (2) **Agent state / memory surface** — surfaced by ChatGPT memory leak and AgentDojo persistent-compromise benchmarks. (3) **Cross-tenant aggregation across 5 surfaces** (retriever + cache + checkpointer + observability + model) — surfaced by ConfusedPilot.
**Cluster:** Cross-tier integration
**Tier reference:** §1.11 / §3.2 / §3.6

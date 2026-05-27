# Conflicts of Interest Disclosure

This disclosure accompanies *Enterprise AI Agents on LangGraph: A Field Guide* for procurement-review and vendor-risk-assessment purposes. The author bio in `00-introduction.md` provides transparent affiliation context for general readers; this file provides the additional detail procurement teams typically require.

---

## Author Affiliation

**Author:** Aaron Fulkerson
**Primary affiliation:** OPAQUE Systems — CEO
**Author financial interest in OPAQUE:** Equity. The author has economic interest in the success of OPAQUE Systems, a venture-backed AI infrastructure company. OPAQUE Systems was founded by Co-Founders Ion Stoica (Executive Chairman), Raluca Ada Popa (Chief Scientist), Rishabh Poddar (CTO), and Chester Leung (no longer at OPAQUE) out of UC Berkeley's RISELab; the author is the company's CEO, not a Co-Founder.

OPAQUE Systems builds confidential AI infrastructure. The company is referenced (a) in the author bio (`00-introduction.md`), (b) in this file, and (c) sparingly in the Part I (Foundations) body where the architecture surfaces a gap that has both a named industry standard (e.g., RATS / EAT / EAR for remote attestation, SPIFFE / SPIRE for workload identity) **and** a specific OPAQUE-shipping primitive (e.g., hardware-enforced signed-JWT issuance, confidential-computing TEE attestation). Per the standards-anchored editorial rule documented in [Editorial Discipline §1 below](#editorial-discipline-applied-to-this-work), OPAQUE is named at most once per chapter section as the implementation pattern, anchored to the underlying standard. The Part II (Patterns) and Part III (Production) bodies contain zero OPAQUE product-positioning references; affiliation and the Phase 2 overlay are disclosed there at the metadata level only.

---

## Editorial Discipline Applied to This Work

The Field Guide is written as an **educational reference**. It is **not** a procurement-evaluation document. Procurement decisions require independent vendor evaluation against the reader's own requirements.

The following disciplines were applied during authorship:

1. **OPAQUE references in the body follow a standards-anchored rule.** OPAQUE Systems is named in body prose only where the architecture surfaces a trust / governance / verifiability gap that has both (a) a named industry standard (IETF RFC, CNCF project, ISO standard, OpenID / OpenSSF / Linux Foundation work) **and** (b) a specific OPAQUE-shipping primitive that closes the gap. Where both conditions are met, OPAQUE is named at most once per chapter section, anchored to the underlying standard, and described in terms of what it implements (not what it competes against). No comparative claims against OPAQUE-relevant alternatives appear in the body. No competitor naming as adversarial counterparty. The Part II (Patterns) and Part III (Production) bodies contain zero OPAQUE product-positioning references; substrate-level remediation in §3.6 of the Production tier is framed at category level only — naming the substrate primitive and the residual risk, but not naming any vendor (including OPAQUE) as the remediation answer.

2. **Public vocabulary throughout.** The Field Guide uses public-grade terminology — *data-leak surface*, *leakage pathway*, *leak vector* — and does **not** use the author's internal taxonomy ("bleeds," P-IDs).

3. **Citation discipline.** Every factual claim carries an evidence-class tag drawn from a 10-class taxonomy: `[primary-regulatory]`, `[independently-audited]`, `[vendor-contractual]`, `[vendor-public]`, `[named-incident]`, `[customer-produced-evidence]`, `[corroborated]`, `[reference design]`, `[architectural inference]`, `[benchmark]`. Vendor-disclosed metrics are not represented as MRM-validation evidence.

4. **Honest evidence gaps.** Where evidence is thin or absent — for example, Sovereign segment deployments (zero documented public LangGraph deployments) or Healthcare PHI in production (no production LangGraph deployment touches PHI on any framework) — the tier files mark this explicitly with `[evidence-zero, structural-fit-only]` or `[reference design — not in PHI production anywhere on any framework]` rather than paper over the gap.

5. **Customer-acknowledged failures cited.** The Field Guide explicitly cites the May 2025 public reversal of the Klarna AI-only customer-support strategy by Sebastian Siemiatkowski (Klarna CEO) as the canonical operational-lifecycle case study (Production §3.9). This is the strongest available "vendor-disclosed launch metric did not survive one year" anchor in the public corpus.

---

## What the Reader Should Verify Independently

When using this Field Guide for procurement evaluation, the reader is responsible for:

- Triangulating vendor claims against independent sources beyond this Field Guide.
- Validating that the named-customer outcome metrics cited herein reflect current state (most are vendor-disclosed at launch; the Klarna reversal demonstrates how those metrics evolve).
- Independently evaluating any vendor — including OPAQUE Systems — against the reader's own requirements, compliance regime, and risk posture.

The Field Guide does not constitute a recommendation to procure, deploy, or evaluate any specific vendor or product.

---

## Funding

This work is published under the author's own by-line on aaronfulkerson.com and a public GitHub repository under a CC BY-SA 4.0 license. Time-and-effort funding distinction:

- **Authorship time and effort:** OPAQUE Systems contributed staff time and the use of internal infrastructure during the research and drafting of this work. The work is being released as a community contribution under CC BY-SA 4.0; OPAQUE does not retain exclusive rights to the content.
- **OPAQUE-specific overlay:** A separate companion artifact — the OPAQUE 2.7 + 3.0 overlay — is being prepared as an internal / partner-channel document. That artifact is **not** published under CC BY-SA, is **not** mirrored on the public GitHub repository, and is **not** referenced in this Field Guide except as a placeholder in the design spec.

---

## Independent Review

As of initial publication, this Field Guide has not undergone a formal independent peer-review process. The design and content were subjected to:

- Two rounds of structured adversarial critique by simulated reviewers spanning Sales Engineer, Product Manager, Enterprise Architect, CISO-FSI, LangChain DevRel, and Developer Educator personas, prior to drafting.
- Citation-discipline review across the 10 evidence-class taxonomy.

A formal inter-rater-reliability study with at least one OPAQUE-internal subject-matter expert and at least one independent external reviewer under NDA is committed for v1.1, per design spec §4.7.

Readers who identify factual errors, missing evidence, or framings that obscure relevant trade-offs are encouraged to file issues on the public GitHub repository, or contact the author directly via aaronfulkerson.com.

---

## Sub-Processors / Tools Used in Authorship

For full transparency: the Field Guide was authored with substantial assistance from large-language-model-based agents (specifically, an autonomous research-and-drafting pipeline running Anthropic Claude). All factual claims were reviewed against the cited primary sources; the author retains responsibility for the final content.

---

## Contact

Questions about this disclosure: contact the author via aaronfulkerson.com or open an issue on the GitHub repository.

Last updated: 2026-05-24.

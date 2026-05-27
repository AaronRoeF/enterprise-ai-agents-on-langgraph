<!--
title: Enterprise AI Agents on LangGraph — A Field Guide
file: CONTRIBUTING.md
version: v1.0
date: 2026-05-24
author: Aaron Fulkerson
license: CC BY-SA 4.0
-->

# Contributing to the Field Guide

## What you get from contributing

Your name in the acknowledgments. The satisfaction of strengthening a community resource that hundreds of new Sales Engineers, Solution Consultants, Product Managers, and architects will read in their first months on the job. The chance to flag what's wrong before someone else trips over it in front of a CISO. And — concretely — a piece of public-grade, citation-anchored work you can point to on your own CV.

This is a community-maintained resource. If you've read the Field Guide and found something missing, wrong, or unclear, please file an issue or send a pull request. The bar is "primary source attached," not "perfect prose."

---

## The contribution contract

- **License:** All contributions are accepted under **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**. By contributing, you license your work under those terms. Derivatives — including translations and reuse in other community projects — are explicitly welcome under the same license.
- **Attribution:** Contributors are credited in the Acknowledgments section of `README.md` and, where applicable, alongside the specific section they shaped. If you'd prefer to contribute anonymously or under a pseudonym, say so in your PR description.
- **Review:** Aaron is the lead reviewer for v1.0. Community maintainers will be added over time as the project's surface grows. There is no corporate gatekeeper. There is no NDA. Everything happens in the open on the public GitHub repository.

---

## What we want

Contributions that make the practical handle stronger:

- **Factual corrections.** If a claim is wrong, file an issue or send a PR with the corrected claim and a primary source. Primary sources beat anecdotes, vendor blog posts beat conference summaries, regulatory text beats vendor interpretation.
- **Missing customer-evidence anchors.** New customer-disclosed, production-at-scale LangGraph deployments — engineering-blog post, conference talk, customer-signed-off vendor case study — with the appropriate evidence-class tag (see Citation discipline below).
- **Clarification rewrites where vocabulary is ambiguous.** If you read a passage twice and still aren't sure what it means, that's a defect. Tell us.
- **Glossary additions.** New terms get a cluster assignment per the glossary's existing cluster taxonomy (see `04-glossary.md`). Cross-references to the tier files where the term is first introduced.
- **New worked-example progressions.** Recipe extensions, segment-specific variants, new failure-mode case studies — anchored in named customer evidence wherever possible.
- **Anki cards for under-covered clusters.** Spaced-retrieval cards for vocabulary, failure-mode pairs, regulatory clauses, or topology distinctions. Follow the deck conventions in `05-anki-deck/README.md`.
- **Translations.** Start a parallel directory at `book/translations/<lang>/`. Translate by tier; do not splice tiers from different languages into one path. Keep the evidence-class tags and primary-source citations intact.

---

## What we don't want

The CC BY-SA 4.0 license and the editorial-discipline lock in `CONFLICTS.md` rule out a few categories:

- **Vendor positioning.** No product naming as the answer to a category-level failure mode. No comparative claims against named alternatives unless they're already anchored in primary sources. No "this is what \<vendor\> addresses" language. The editorial stance is locked.
- **Speculative claims without citation.** Every factual claim in the body carries an evidence-class tag. Untagged claims block the review gate.
- **Code that runs but isn't pedagogical.** If a snippet's purpose is to teach a concept, keep it; if its purpose is to be runnable infrastructure, move it to a companion repository and link from the relevant tier file.
- **Changes that weaken editorial honesty.** `[evidence-zero]`, `[reference design]`, and `[architectural inference]` tags exist on purpose. Don't paper over a gap by removing the tag. Add evidence and re-tag if you can.
- **Foreword and introduction rewrites.** `00-foreword.md` and `00-introduction.md` are voice-locked. Typos and broken-link fixes welcome; structural rewrites require coordination with the author first.

---

## How to file an issue

Use the existing issue templates wherever possible. The label set:

**Bug labels**
- `factual-error` — a claim in the body is incorrect.
- `typo` — copy-edit fix.
- `broken-link` — external or internal cross-reference is dead.
- `vocabulary-drift` — terminology used inconsistently across tier files.
- `missing-citation` — claim is right but lacks an evidence-class tag.
- `anki-card-error` — card front / back / cluster mismatch.

**Enhancement labels**
- `new-content` — adds material to an existing section.
- `new-translation` — starts a translation directory.
- `new-evidence` — adds a customer anchor, incident, or regulatory citation.
- `clarification` — restructures or rewrites for clarity.

**Template fields**

When you file an issue, include:

1. **Section reference** — file and section heading (e.g., `03-production.md §3.6.7`).
2. **Observed behavior** — exactly what's wrong, with the verbatim text.
3. **Expected behavior** — what it should say or do.
4. **Suggested fix** — your proposed change.
5. **Primary source** — URL, paper citation, regulatory clause, customer disclosure. For factual corrections this is mandatory.

---

## How to propose a pull request

1. **Fork** the repository.
2. **Branch** with a descriptive name (`fix-curxecute-date`, `add-rakuten-anchor`, `translate-foundations-de`).
3. **Commit** atomically. One PR, one logical change is preferred. Bundled PRs that mix factual corrections, new content, and translation work get split before review.
4. **Citation tags** — apply the evidence-class taxonomy on every new claim. Pass through existing tags on edits.
5. **PR description** — link the issue (if one exists), the section affected, the primary sources, and any open questions you'd like the reviewer to weigh in on.
6. **Voice-locked files** — changes to `00-foreword.md` and `00-introduction.md` require explicit acknowledgment in the PR that you've read this section. Aaron reviews these personally.
7. **Glossary changes** — coordinate the new term's cluster assignment with the existing glossary taxonomy. If you're not sure which cluster, ask in the PR.

---

## Review timeline

- **Typo / broken-link / minor-clarification PRs** — best-effort within a week.
- **Factual corrections with primary source** — best-effort within two weeks.
- **New content and new translations** — best-effort within a month. Larger PRs may sit longer; ping the issue if it's been more than 30 days with no movement.
- **Voice-locked file changes and editorial-stance-adjacent changes** — reviewed personally by the author, no fixed SLA.

If a PR has been sitting more than 60 days with no movement, comment on it to bump it. We won't take it personally; the volume can outpace any one reviewer's bandwidth.

---

## A few worked examples of good contributions

To give a sense of what lands cleanly through review:

- **"The CurXecute disclosure date in §3.6.1 is August 2025, not August 2024."** — file an issue with the CVE-2025-54135 advisory link. Tagged `factual-error`. One-line fix.
- **"Add Rakuten as a supervisor anchor in §2.2.4 with a customer-engineering blog citation."** — PR with the blog URL, the verbatim Rakuten engineering quote, and the `[customer-produced-evidence]` tag.
- **"The glossary entry for `Sign-3` cross-references §3.4 but the section reference moved to §3.4.2 — fix the link."** — issue with the broken anchor; PR with the corrected link.
- **"Translate Foundations into German."** — new directory `book/translations/de/`, start with `01-foundations.md`, keep evidence-class tags and primary-source URLs intact, leave the English original untouched.
- **"Add 20 Anki cards covering the supervisor / swarm distinction."** — PR to `05-anki-deck/02-patterns-deck.md` with the new cards in the existing format, cluster tag `topology-supervisor-swarm`.

And what doesn't land cleanly:

- **"Replace the EchoLeak mitigation with \<vendor product\>."** — vendor positioning, blocked. The Field Guide does not name a remediation answer at the substrate level; it describes the category. The OPAQUE 2.7 / 3.0 overlay (per `CONFLICTS.md`) is the separate artifact that names a product, and it lives outside this repository.
- **"Rewrite the foreword in a more enthusiastic tone."** — voice-locked. The author handles foreword changes personally.
- **"Add a benchmark claim sourced from a Reddit thread."** — community-reported evidence is welcome but should be tagged `[community-reported]` and clearly marked as anecdotal. If you want to upgrade the tag, find the corroborating customer-disclosed or independent source.

---

## Code of conduct

Be kind. Listen. Celebrate diversity. Focus on the work. Disagreement is welcome — personal attacks are not. The maintainers' decisions are final, but they're not arbitrary; if you think a decision was wrong, say so with reasoning and the maintainer will engage.

---

## Style guide pointer

- **Voice and tone** — read `00-foreword.md` and `00-introduction.md`. Declarative, plain English, no hype, no AI-slop.
- **Reader-path discipline** — the WIFM-leads-every-section pattern is the standard. New sections should open with what the reader gets, then deliver.
- **Vocabulary** — use the canonical glossary terms in `04-glossary.md`. *Data-leak surface*, *leakage pathway*, *leak vector* — public-grade terminology throughout. No internal vendor taxonomies.
- **Citation tags** — every claim. Per-leakage-pathway regime-binding tags on top of evidence-class tags where applicable.

---

## Citation discipline (one more time)

Every factual claim in the body carries one of:

`[primary-regulatory]`, `[independently-audited]`, `[vendor-contractual]`, `[vendor-public]`, `[named-incident]`, `[customer-produced-evidence]`, `[corroborated]`, `[reference design]`, `[architectural inference]`, `[benchmark]`.

Per-leakage-pathway regime-binding tags sit on top where applicable. Full taxonomy in `00-introduction.md` under *Citation discipline*.

---

## License signature line

> By contributing to this repository, you agree to license your contributions under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).

That's the contract. Welcome to the work.

~af

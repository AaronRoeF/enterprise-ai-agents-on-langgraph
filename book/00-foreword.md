<!--
title: Enterprise AI Agents on LangGraph — A Field Guide
part: Foreword
version: v1.1
date: 2026-05-27
author: Aaron Fulkerson
license: CC BY-SA 4.0
-->

# Foreword

*By Aaron Fulkerson — 2026-05-24*

---

By the time you finish this book, you should be able to walk into an enterprise (or regulated-enterprise) agent discovery call, sketch the agent architecture on a whiteboard, name the failure modes the prospect actually loses sleep over, defend a framework recommendation against a credible alternative, and tell a CISO which leak surfaces live at which layer and which ones don't have a clean answer yet. That's the practical handle. If you're a new Sales Engineer, Solution Consultant, or Product Manager — or the architect on the other side of the table — that's what's in it for you. Two to three months in, you should be holding your end of the conversation.

The reason this book exists is small and honest: we didn't have it. OPAQUE didn't have it. The people I talk to at LangChain, at the hyperscalers, at the FSIs shipping production agents — none of them had it either. Every new hire was reassembling the field from blog posts, READMEs, vendor decks, and whatever incident was in the headlines that week. So we wrote it down. Eighteen named, customer-disclosed, production-at-scale LangGraph deployments are the spine of the book. The rest is the architecture, the failure modes, the regulatory pressure, and the citation discipline you need to read the next year of new components in context.

This is not a vendor pitch. I run an AI infrastructure company — OPAQUE Systems — and the book is written for the practitioner community, not for procurement. OPAQUE is named in the body of Part I (Foundations) four times, and only where the architecture surfaces a trust- or governance-gap that has a named industry standard (RATS, EAT, EAR, SPIFFE) and OPAQUE happens to be a vendor implementing that specific standard — anchored to the standard, not to the marketing. Where a vendor would normally win in a book like this, this book stays silent. The discipline rule, the cadence cap, and the editorial review that produced it are documented in `CONFLICTS.md`. If you're using this for procurement evaluation, please read `CONFLICTS.md` first — it exists for that exact use case.

What I think is actually different — every claim carries an evidence-class tag, so you know whether you're holding a regulation, a customer engineering blog, a vendor blog post, or an architectural inference, and you can cite it back with the right weight. The Klarna CEO May 2025 reversal is in here as the canonical operational-lifecycle case study. The insurance gap — 68% generative adoption, 42% abandonment, zero LangGraph insurance footprint — is in here. The places we don't know are marked `[evidence-zero]` or `[reference design]` rather than papered over. We tell you what we don't know.

Three reader paths. Linear for the new hire — Foundations in the first two weeks, Patterns and Production as ongoing reference. Skip-to-tier for the practitioner who's already shipping. Look-up for the architect who wants the 10-axis matrix, the regulatory depth, or the audit-evidence cookbook on demand. Foundations has two tracks inside it — engineer-track reads the code, PM-track reads the concept boxes. Both tracks are welcome. The community is welcome to remix, translate, fork, and improve this — that's what CC BY-SA 4.0 is for. Issues and pull requests are the way in.

The LangGraph community has given a lot of us a lot to work with — open source, public docs, customer engineering write-ups, the Interrupt talks, the framework primitives themselves. This book is one way to give some of that back without an invoice attached. If it's useful, share it. If it's wrong, file an issue. If it's missing a named component, a clause, or an incident, send a pull request with a primary source. We'll fold it in.

Welcome to the field.

~af

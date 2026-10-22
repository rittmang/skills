---
name: name-project
description: Generate and compare names for a project, product, tool, or a company naming request, with optional domain research. Use for brainstorming names, renaming, or evaluating a naming shortlist. For a broader company identity covering positioning and social handles, use create-company-identity when available. Excludes code symbol naming and legal entity formation.
license: MIT
---

# Name a project

Turn a concrete brief into a distinctive, usable name and explain the tradeoffs. Separate creative suggestions from facts established through live research.

## Establish the brief

Use the conversation and project context to identify what it does, who it serves, its distinguishing idea, desired tone, and any language or naming constraints. Preserve names or directions the user already likes.

If the purpose is missing, ask one focused question. Otherwise start with stated assumptions instead of requiring a branding questionnaire. Treat domain research as optional: run it when requested or required by the brief. Ideation-only requests do not need network access. Do not select social platforms or check handles here; those belong to the company identity workflow.

When checking domains, establish preferred suffixes and budget constraints. If unspecified, state a reasonable suffix assumption, such as starting with `.com` and one category-relevant alternative. Do not imply the user has accepted a premium domain budget.

## Develop and compare names

1. Explore a few genuinely different directions: a useful metaphor, an evocative compound, a direct description, or a pronounceable coined word. Choose directions that fit the brief rather than mechanically filling every category.
2. Offer a manageable set of candidates, usually 8–12 for a broad first pass or fewer for a focused request. Give each a short rationale; include pronunciation when it is not obvious. Avoid padding the list with minor spelling variants or unexplained AI-themed suffixes.
3. Shortlist the strongest candidates using audience fit, memorability, ease of saying and spelling, distinctiveness, and room for the project to evolve. Explain meaningful tradeoffs in words; invented numerical precision adds little.
4. If research is requested, check the shortlist rather than every brainstormed name. Search exact names and relevant category combinations for obvious active-product collisions. Follow the evidence rules below for domains. An exact-name collision in an unrelated category is a tradeoff, not automatic disqualification.
5. Recommend a leading name and a small number of alternatives. Explain which constraint would change the recommendation. If a domain is essential, distinguish the strongest creative name from the strongest name with sufficiently verified domain evidence.

When another skill supplies a company brief, return naming rationale, the shortlist, collision findings, and any domain evidence. Let the company workflow make the overall identity decision.

## Optional domain research

Read [references/domain-research.md](references/domain-research.md) before making live domain claims. With Python 3.10+ and network access, the bundled helper can query registry RDAP services:

```bash
python3 <skill-directory>/scripts/check_domains.py candidate.com candidate.dev
```

Replace `<skill-directory>` with this skill's actual installed directory. The script uses the Python standard library, discovers services from IANA, and returns timestamped JSON. It accepts ASCII second-level domains such as `candidate.com`; use registry or registrar tools for `candidate.co.uk` or Unicode input. Unsupported services and failed requests remain `unknown`.

The script's `not_found` result means no registration object was returned by that RDAP service. It does **not** establish that a domain can be bought. Confirm registrability and any quoted price with a registrar. Missing DNS, a blank website, a search result, or an HTTP error from the candidate website does not establish availability.

## Deliver the decision

Scale the response to the request. A useful result includes the interpreted brief, candidates with rationale, a ranked shortlist, and a recommendation. When research was requested, add a compact evidence table with the exact domain, status, source link, and UTC check time. Label unperformed checks `not checked`; never present suggestions as verified identities.

Do not claim universal uniqueness from a web search or imply trademark clearance. Mention a specific collision when found. If the user asks for legal clearance, treat it as a separate task.

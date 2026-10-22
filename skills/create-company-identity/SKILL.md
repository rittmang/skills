---
name: create-company-identity
description: Develop a company or startup identity from an idea, combining a concise positioning brief, name selection, domain research, and consistent social media handles. Use when starting a company brand, rebranding, or seeking an identity across web and social channels. Reuse name-project when available. Excludes legal incorporation, account creation, and full business plans.
license: MIT
---

# Create a company identity

Build a coherent identity around what the company offers and who it serves. Name selection is one component; the outcome is a practical company identity with explicit evidence about its web and social footprint.

## Shape the company brief

Extract the audience, problem, proposed offer, differentiator, market/language, tone, and existing assets from the conversation. Summarize positioning in one sentence. Distinguish the company name from any product name if that distinction matters.

Ask only for missing information that materially changes the work. If the user has an idea but no positioning, propose a working brief and label assumptions. Do not expand this into a business plan, logo project, incorporation workflow, or account registration task.

Live identity research is part of this workflow unless the user asks for ideation only. Use platform and domain preferences already given. If platforms are unspecified, state a small, audience-relevant selection: for example, GitHub and X for a developer tool, or Instagram and TikTok for a consumer brand. Avoid checking every platform by default. Preserve known handle or domain assets and budget constraints.

## Use the naming component

If the `name-project` skill is available in the current environment, use it with the company brief and the requested domain constraints. Locate it through the environment's skill catalog or an existing sibling skill folder; do not assume the author's machine path. Pass along names already explored so it need not restart the discussion. Request naming directions, a shortlist with rationale, obvious category collisions, and domain findings if needed. Continue with the social and consistency work here.

If `name-project` is not installed, continue without installing anything: explore a few distinct naming directions, compare candidates for fit, memorability, pronunciation, and distinctiveness, and shortlist a few. When research is enabled, search obvious category collisions and use registry or registrar lookups for domains. This skill must remain useful when installed alone. For an existing company name, evaluate that name first rather than requiring another naming round.

## Research the identity

Skip this section's live checks for ideation-only requests. Otherwise read [references/identity-checks.md](references/identity-checks.md) before researching domains or social handles.

For the strongest candidates:

1. Compare exact-brand domains and preferred social handles on the selected platforms. A display name, account handle, company-page slug, and domain are different identifiers; record the exact one checked.
2. If exact matches are occupied, explore a small number of consistent alternatives, such as a relevant suffix or a single prefix across channels. Prefer an intelligible pattern to unrelated spellings, numbers, or punctuation on every platform. Explain the compromise rather than claiming a match is mandatory.
3. Search the company name and category for obvious existing businesses and products. Describe observed collisions with sources; absence of results does not establish global uniqueness or legal clearance.
4. Keep domain, social, and collision evidence separate. A good domain does not establish handle availability, and a free-looking handle does not make a crowded company name distinctive.
5. Stop blocked or rate-limited checks and label them unknown. Continue the rest of the identity work with the evidence available.

If live tools are unavailable, provide the positioning, naming, proposed identity pattern, and direct links for the user to check. Mark all live checks `not checked`; the identity is provisional.

## Deliver an identity decision

Provide a concise company brief, the recommended name and rationale, a short positioning line, and a coherent proposed domain/handle pattern. Compare the leading alternatives when the tradeoff is material.

For researched identities, include the exact domain and each platform identifier, evidence status, source URL, and UTC check time. Separate `confirmed occupied`, `not found/unconfirmed`, `available according to the platform or registrar`, `unknown`, and `not checked`. Do not summarize a partly checked identity as "available everywhere."

End with the unresolved checks that could change the decision and a practical next action. Naming and lookup requests authorize research, not purchasing a domain, creating accounts, contacting handle owners, or filing company paperwork. Keep those actions outside this skill unless the user separately requests them.

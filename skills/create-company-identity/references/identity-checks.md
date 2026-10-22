# Identity checks

## Domains

Use this skill's own domain workflow and bundled checker as described in [domain-research.md](domain-research.md), or perform the same checks through available registry, registrar, or browser tools. Domain research is independent of whether `name-project` is installed. Keep registration evidence separate from confirmation that a domain can be purchased, and record sources and UTC check times.

## Social handles

First identify the account type and exact identifier. A GitHub organization, an X username, an Instagram username, a TikTok username, a YouTube handle, and a LinkedIn company-page slug have different rules. Read the current platform rules if a candidate's syntax or eligibility is uncertain.

Use public profile pages and the platform's own messages. Search can help locate an account, but is not an availability API. A third-party handle checker can provide leads; verify its positive claims on the platform itself.

| Observation | Status |
| --- | --- |
| Exact requested identifier resolves to a matching account or company page | `occupied` |
| Platform explicitly confirms that exact identifier is selectable for the intended account type | `available according to platform at check time` |
| Public page is not found or a platform says the account does not exist | `not found; claimability unconfirmed` |
| Login wall, bot challenge, rate limit, generic redirect, unavailable account, or ambiguous response | `unknown` with the reason |
| No live check | `not checked` |

A missing page or HTTP 404 does not prove the handle can be claimed: it may be reserved, suspended, held after a rename, or subject to account requirements. A profile redirect counts as occupied only when the destination demonstrably corresponds to the requested identifier; otherwise record the redirect and leave the claimability unresolved.

Do not submit signup forms, change a logged-in user's username, or create a page to test a name. Use an existing account session only if its use is authorized. Stop at authentication requirements or access blocks; report what remains unresolved.

Useful public page patterns, subject to current platform behavior:

| Platform | Candidate URL | Check |
| --- | --- | --- |
| GitHub | `https://github.com/HANDLE` | User vs. organization, exact login |
| X | `https://x.com/HANDLE` | Username, not display name |
| Instagram | `https://www.instagram.com/HANDLE/` | Username, not display name |
| TikTok | `https://www.tiktok.com/@HANDLE` | Username |
| YouTube | `https://www.youtube.com/@HANDLE` | Handle, not channel title |
| LinkedIn | `https://www.linkedin.com/company/SLUG/` | Company-page slug, not personal profile |

Constructed URLs are check targets, not evidence until opened. Encode identifiers for URLs and reject candidates that violate the platform's current naming rules. Never infer claimability solely from an HTTP status code.

## Identity consistency

Assess the set of identifiers as a whole. Keep a preferred exact-brand pattern and, if necessary, one consistent fallback. Evaluate whether spelling changes, a different spoken name, or a competitor in the same category would make the identity hard to find.

Report findings in a table like:

| Candidate | Identifier | Status | Evidence | Checked at (UTC) |
| --- | --- | --- | --- | --- |
| Candidate A | Domain: candidate.example | not checked | Proposed only | — |
| Candidate A | GitHub organization: candidate | not checked | Proposed only | — |

Use real sources and timestamps for actual checks. Keep illustrative names clearly hypothetical. No combination of these checks establishes trademark clearance or worldwide uniqueness; report concrete observed conflicts without turning ordinary naming work into a legal review.

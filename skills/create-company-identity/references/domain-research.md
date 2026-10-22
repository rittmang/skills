# Domain evidence

Use this reference for the domain research stage of creating a company identity.

## Check a shortlist

1. Convert each shortlisted name into explicit candidate domains. Preserve the requested suffixes and budget. Keep the brand spelling consistent before trying a prefix or another suffix.
2. Query the authoritative registry through RDAP, or inspect an official registry or registrar lookup. The bundled `scripts/check_domains.py` discovers RDAP services from IANA. If no RDAP service exists, try an appropriate registry or registrar rather than guessing.
3. For promising names, inspect a registrar result that explicitly shows registration availability. Record any displayed first-year price, renewal price, currency, and premium or aftermarket status. Leave unavailable pricing fields unknown.
4. Report each source and the UTC check time. Recheck a finalist when the user is about to act; an earlier lookup does not reserve it.

Use these statuses precisely:

| Evidence | Report |
| --- | --- |
| Matching RDAP registration object | `registered` |
| Structured RDAP 404 from the discovered service | `not found in RDAP; registrar confirmation needed` |
| Registrar explicitly offers a new registration | `available at registrar at check time` |
| Existing registration offered for resale | `aftermarket listing`; include the observed asking price if shown |
| Registry/registrar explicitly identifies a reserved name | `reserved` |
| Unsupported suffix, timeout, rate limit, login wall, or ambiguous result | `unknown` with the reason |
| No lookup performed | `not checked` |

Do not translate `not_found` into a purchase recommendation. Registries can reserve names, restrict eligibility, or charge premium prices. A registered domain can be parked or have no DNS records. Conflicting sources remain a conflict to resolve, not an invitation to choose the more optimistic answer.

## Bundled checker

```bash
python3 <skill-directory>/scripts/check_domains.py candidate.com candidate.dev
```

- Requires Python 3.10+, HTTPS, and no API keys or third-party Python packages.
- Accepts up to 20 unique ASCII second-level domains per run. This keeps it a shortlist checker, not an enumeration tool. Multi-label names such as `candidate.co.uk`, URLs, and raw Unicode are rejected; use registry/registrar tools for those.
- Uses a 10-second timeout per request, configurable with `--timeout`. Requests run sequentially, without automatic retries. After a 429, remaining domains on that same service are marked unknown without more requests.
- Returns JSON with `domain`, `status`, `reason`, `source_url`, `checked_at`, `http_status`, and `detail`. It omits registrant contact data.
- Exit `0` means all results are either `registered` or `not_found`, not that any domain is available. Exit `1` means at least one result is `unknown`; the JSON is still useful. Exit `2` means invalid arguments.
- If terminal execution is unavailable, use a browser or an existing lookup tool with the same evidence distinctions. If network access is unavailable, deliver the identity brief and proposed identifiers, and label domain checks unperformed.

## Source mechanics

- [IANA RDAP bootstrap registry](https://www.iana.org/assignments/rdap-dns) identifies authoritative lookup services; the script reads its linked `dns.json`.
- [RFC 9082](https://www.rfc-editor.org/rfc/rfc9082.html) defines domain lookup paths.
- [RFC 9083](https://www.rfc-editor.org/rfc/rfc9083.html) defines domain objects and structured errors.
- [ICANN reserved names](https://www.icann.org/resources/pages/reserved-2013-06-28-en) explains why a name without a registration may still be withheld.

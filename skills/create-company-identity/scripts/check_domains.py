#!/usr/bin/env python3
"""Query registry RDAP evidence for company identity, not purchase availability."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import datetime, timezone
from urllib.error import HTTPError
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen

BOOTSTRAP_URL = "https://data.iana.org/rdap/dns.json"
MAX_RESPONSE_BYTES = 1_048_576
LABEL = re.compile(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\Z")


def normalize_domain(value: str) -> str:
    if not value.isascii():
        raise ValueError("use registry/registrar tools for raw Unicode domain names")
    domain = value.strip().lower().removesuffix(".")
    labels = domain.split(".")
    if len(labels) != 2 or not all(LABEL.fullmatch(label) for label in labels):
        raise ValueError(
            "expected an ASCII second-level domain such as example.com; "
            "use registry/registrar tools for Unicode names or example.co.uk"
        )
    if not re.fullmatch(r"(?:[a-z]{2,63}|xn--[a-z0-9-]+)", labels[-1]):
        raise ValueError("expected an alphabetic or ASCII-encoded international TLD")
    return domain


def positive_timeout(value: str) -> float:
    timeout = float(value)
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("timeout must be a finite positive number")
    return timeout


def fetch_json(url: str, timeout: float) -> tuple[int, object, str]:
    request = Request(
        url,
        headers={
            "Accept": "application/rdap+json, application/json",
            "User-Agent": "rittmang-skills-domain-checker/0.1 (+https://github.com/rittmang/skills)",
        },
    )
    try:
        response = urlopen(request, timeout=timeout)
    except HTTPError as error:
        response = error
    with response:
        status = response.code
        final_url = response.geturl()
        raw = response.read(MAX_RESPONSE_BYTES + 1)
        if len(raw) > MAX_RESPONSE_BYTES:
            raise ValueError("lookup response exceeded the one-megabyte limit")
        content_type = response.headers.get_content_type()
    payload = None
    if content_type == "application/json" or content_type.endswith("+json"):
        try:
            payload = json.loads(raw)
        except (ValueError, UnicodeError):
            pass
    return status, payload, final_url


def load_services(timeout: float) -> dict[str, str]:
    status, payload, _ = fetch_json(BOOTSTRAP_URL, timeout)
    if status != 200 or not isinstance(payload, dict):
        raise ValueError(f"IANA bootstrap lookup failed (HTTP {status})")
    services = payload.get("services")
    if not isinstance(services, list):
        raise ValueError("IANA bootstrap response has no services list")
    endpoints = {}
    for entry in services:
        if not isinstance(entry, list) or len(entry) != 2:
            raise ValueError("IANA bootstrap response contains a malformed service")
        suffixes, urls = entry
        if not isinstance(suffixes, list) or not isinstance(urls, list):
            raise ValueError("IANA bootstrap service lists are malformed")
        endpoint = None
        for url in urls:
            if not isinstance(url, str):
                continue
            parts = urlsplit(url)
            if parts.scheme == "https" and parts.hostname and not (
                parts.username or parts.password or parts.query or parts.fragment
            ):
                endpoint = url.rstrip("/") + "/"
                break
        if endpoint:
            for suffix in suffixes:
                if isinstance(suffix, str):
                    endpoints[suffix.lower()] = endpoint
    return endpoints


def evidence(domain: str, status: str, reason: str, source_url: str | None,
             detail: str, http_status: int | None = None) -> dict:
    return {
        "domain": domain,
        "status": status,
        "reason": reason,
        "source_url": source_url,
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "http_status": http_status,
        "detail": detail,
    }


def query_url(domain: str, endpoint: str) -> str:
    return endpoint.rstrip("/") + "/domain/" + quote(domain, safe="")


def check_domain(domain: str, endpoint: str, timeout: float) -> dict:
    url = query_url(domain, endpoint)
    try:
        status, payload, final_url = fetch_json(url, timeout)
    except (OSError, ValueError) as error:
        return evidence(domain, "unknown", "lookup_failed", url, str(error))
    if status == 200 and isinstance(payload, dict):
        name = payload.get("ldhName")
        if payload.get("objectClassName") == "domain" and isinstance(name, str):
            if name.lower().removesuffix(".") == domain:
                return evidence(domain, "registered", "matching_domain_object", final_url,
                                "The registry returned a matching registration object.", status)
    if status == 404 and isinstance(payload, dict) and payload.get("errorCode") == 404:
        return evidence(domain, "not_found", "rdap_404", final_url,
                        "No object found in RDAP; registrar confirmation of registrability and price is needed.",
                        status)
    reason = f"http_{status}" if status != 200 else "unexpected_response"
    return evidence(domain, "unknown", reason, final_url,
                    "No matching registration object or structured RDAP 404 was returned.", status)


def check_batch(domains: list[str], timeout: float) -> list[dict]:
    try:
        services = load_services(timeout)
    except (OSError, ValueError) as error:
        return [evidence(domain, "unknown", "bootstrap_failed", BOOTSTRAP_URL, str(error))
                for domain in domains]
    results = []
    blocked = set()
    for domain in domains:
        endpoint = services.get(domain.rsplit(".", 1)[-1])
        if not endpoint:
            result = evidence(domain, "unknown", "unsupported_suffix", BOOTSTRAP_URL,
                              "IANA lists no usable HTTPS RDAP service for this suffix.")
        elif endpoint in blocked:
            result = evidence(domain, "unknown", "service_rate_limited", query_url(domain, endpoint),
                              "Not queried: this service returned HTTP 429 earlier in the batch.")
        else:
            result = check_domain(domain, endpoint, timeout)
            if result["http_status"] == 429:
                blocked.add(endpoint)
        results.append(result)
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("domains", nargs="+", type=normalize_domain,
                        help="ASCII second-level domains, such as example.com")
    parser.add_argument("--timeout", type=positive_timeout, default=10.0,
                        help="per-request timeout in seconds (default: 10)")
    args = parser.parse_args(argv)
    domains = list(dict.fromkeys(args.domains))
    if len(domains) > 20:
        parser.error("check at most 20 unique domains per batch")
    results = check_batch(domains, args.timeout)
    print(json.dumps(results, indent=2, ensure_ascii=True))
    return int(any(result["status"] == "unknown" for result in results))


if __name__ == "__main__":
    sys.exit(main())

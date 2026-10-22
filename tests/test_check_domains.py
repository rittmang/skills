"""Offline acceptance tests for domain evidence, not domain availability."""

import contextlib
import importlib.util
import io
import json
import unittest
from email.message import Message
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError, URLError

SCRIPT = Path(__file__).resolve().parents[1] / "skills/name-project/scripts/check_domains.py"
SPEC = importlib.util.spec_from_file_location("check_domains", SCRIPT)
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)
SERVICE = "https://rdap.registry.example/"


class DomainEvidenceTests(unittest.TestCase):
    def lookup(self, status, payload, domain="example.com"):
        with patch.object(checker, "fetch_json", return_value=(status, payload, SERVICE)):
            return checker.check_domain(domain, SERVICE, 1)

    def test_matching_registration_is_registered(self):
        result = self.lookup(200, {"objectClassName": "domain", "ldhName": "EXAMPLE.COM"})
        self.assertEqual(result["status"], "registered")
        self.assertEqual(result["source_url"], SERVICE)
        self.assertTrue(result["checked_at"].endswith("Z"))

    def test_other_domain_does_not_establish_registration(self):
        result = self.lookup(200, {"objectClassName": "domain", "ldhName": "other.com"})
        self.assertEqual(result["status"], "unknown")

    def test_non_domain_response_stays_unknown(self):
        result = self.lookup(200, {"objectClassName": "entity", "ldhName": "example.com"})
        self.assertEqual(result["status"], "unknown")

    def test_structured_404_is_not_found_rather_than_available(self):
        result = self.lookup(404, {"errorCode": 404})
        self.assertEqual(result["status"], "not_found")
        self.assertEqual(result["http_status"], 404)
        self.assertIn("registrar confirmation", result["detail"])

    def test_unstructured_404_stays_unknown(self):
        for payload in (None, [], {"errorCode": 403}):
            with self.subTest(payload=payload):
                self.assertEqual(self.lookup(404, payload)["status"], "unknown")

    def test_blocked_and_malformed_responses_stay_unknown(self):
        for status, payload in ((403, {}), (429, None), (503, {}), (200, None), (200, [])):
            with self.subTest(status=status, payload=payload):
                result = self.lookup(status, payload)
                self.assertEqual(result["status"], "unknown")

    def test_network_failure_stays_unknown(self):
        with patch.object(checker, "fetch_json", side_effect=URLError("offline")):
            result = checker.check_domain("example.com", SERVICE, 1)
        self.assertEqual(result["status"], "unknown")
        self.assertIsNone(result["http_status"])

    def test_unsupported_suffix_is_not_queried(self):
        with patch.object(checker, "load_services", return_value={}), \
                patch.object(checker, "fetch_json") as fetch:
            result = checker.check_batch(["example.invalid"], 1)[0]
        fetch.assert_not_called()
        self.assertEqual(result["status"], "unknown")
        self.assertEqual(result["reason"], "unsupported_suffix")

    def test_rate_limit_stops_same_service_but_not_other_services(self):
        services = {"com": SERVICE, "net": SERVICE, "dev": "https://other.example/"}
        replies = [(429, None, SERVICE), (404, {"errorCode": 404}, "https://other.example/")]
        with patch.object(checker, "load_services", return_value=services), \
                patch.object(checker, "fetch_json", side_effect=replies) as fetch:
            results = checker.check_batch(["one.com", "two.net", "three.dev"], 1)
        self.assertEqual(fetch.call_count, 2)
        self.assertEqual([r["status"] for r in results], ["unknown", "unknown", "not_found"])
        self.assertIsNone(results[1]["http_status"])

    def test_bootstrap_failure_returns_unknown_for_every_domain(self):
        with patch.object(checker, "fetch_json", side_effect=TimeoutError("timed out")):
            results = checker.check_batch(["one.com", "two.dev"], 1)
        self.assertEqual([r["status"] for r in results], ["unknown", "unknown"])

    def test_bootstrap_uses_https_and_shared_services(self):
        payload = {"services": [[["com", "net"], ["http://insecure.example/", SERVICE]]]}
        with patch.object(checker, "fetch_json", return_value=(200, payload, checker.BOOTSTRAP_URL)):
            self.assertEqual(checker.load_services(1), {"com": SERVICE, "net": SERVICE})

    def test_invalid_bootstrap_is_unknown_instead_of_crashing(self):
        for payload in ({}, {"services": [None]}, {"services": [[None, []]]}):
            with self.subTest(payload=payload), \
                    patch.object(checker, "fetch_json", return_value=(200, payload, checker.BOOTSTRAP_URL)):
                self.assertEqual(checker.check_batch(["example.com"], 1)[0]["status"], "unknown")

    def test_normalization_and_invalid_inputs(self):
        self.assertEqual(checker.normalize_domain(" EXAMPLE.COM. "), "example.com")
        for value in ("https://example.com", "example.co.uk", "bad_name.com", "-bad.com",
                      "bad-.com", "localhost", "a..com", "a.123", "café.com", "K.com",
                      "a" * 64 + ".com"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                checker.normalize_domain(value)

    def test_cli_deduplicates_normalized_domains(self):
        reply = [{"domain": "example.com", "status": "not_found"}]
        output = io.StringIO()
        with patch.object(checker, "check_batch", return_value=reply) as batch, \
                contextlib.redirect_stdout(output):
            status = checker.main(["EXAMPLE.COM", "example.com."])
        batch.assert_called_once_with(["example.com"], 10.0)
        self.assertEqual(status, 0)
        self.assertEqual(json.loads(output.getvalue()), reply)

    def test_cli_unknown_results_have_nonzero_exit_and_json(self):
        output = io.StringIO()
        with patch.object(checker, "check_batch", return_value=[{"status": "unknown"}]), \
                contextlib.redirect_stdout(output):
            status = checker.main(["example.com"])
        self.assertEqual(status, 1)
        self.assertEqual(json.loads(output.getvalue())[0]["status"], "unknown")

    def test_cli_rejects_invalid_timeouts_and_large_batches_before_network(self):
        invalid = [["example.com", "--timeout", value] for value in ("0", "-1", "nan", "inf")]
        invalid.append([f"candidate{index}.com" for index in range(21)])
        with patch.object(checker, "check_batch") as batch:
            for args in invalid:
                with self.subTest(args=args), contextlib.redirect_stderr(io.StringIO()), \
                        self.assertRaises(SystemExit) as raised:
                    checker.main(args)
                self.assertEqual(raised.exception.code, 2)
        batch.assert_not_called()

    def test_transport_reads_structured_http_error(self):
        headers = Message()
        headers["Content-Type"] = "application/rdap+json"
        error = HTTPError(SERVICE, 404, "Not Found", headers, io.BytesIO(b'{"errorCode":404}'))
        with patch.object(checker, "urlopen", side_effect=error):
            status, payload, _ = checker.fetch_json(SERVICE, 1)
        self.assertEqual((status, payload), (404, {"errorCode": 404}))

    def test_html_404_does_not_become_rdap_absence(self):
        headers = Message()
        headers["Content-Type"] = "text/html"
        error = HTTPError(SERVICE, 404, "Not Found", headers, io.BytesIO(b'{"errorCode":404}'))
        with patch.object(checker, "urlopen", side_effect=error):
            result = checker.check_domain("example.com", SERVICE, 1)
        self.assertEqual(result["status"], "unknown")


if __name__ == "__main__":
    unittest.main()

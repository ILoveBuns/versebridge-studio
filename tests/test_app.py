import json
import os
import threading
import unittest
import urllib.request
from unittest.mock import patch

from app import (
    Handler,
    ThreadingHTTPServer,
    create_pack,
    retrieve_passage,
    validate_generated_pack,
)
from movement import BiometricSnapshot, detect_moment, select_delivery


class VerseBridgeTests(unittest.TestCase):
    def setUp(self):
        for name in ("YVP_APP_KEY", "GLOO_ACCESS_TOKEN", "GLOO_CLIENT_ID"):
            os.environ.pop(name, None)

    def test_demo_passage_is_explicitly_labelled(self):
        passage = retrieve_passage("3034", "JHN.3.16")
        self.assertTrue(passage["demo"])
        self.assertIn("Demo excerpt", passage["version"])
        self.assertTrue(passage["source_url"].startswith("https://"))

    def test_generated_commentary_remains_separate(self):
        passage = retrieve_passage("3034", "JHN.3.16")
        pack = create_pack(passage, "young adults", "carousel", "hopeful")
        self.assertTrue(pack["demo"])
        self.assertIn("do not present generated reflection as Scripture", pack["safety_note"])

    def test_live_pack_requires_exact_fields_reference_and_review_note(self):
        valid = {
            "headline": "Steady hope",
            "caption": "John 3:16 grounds this reflection.",
            "reflection": "Where can love become action?",
            "visual_direction": "High-contrast sunrise.",
            "safety_note": "Review generated commentary before publishing.",
        }
        self.assertEqual(valid, validate_generated_pack(valid, "John 3:16"))

        for invalid in (
            {**valid, "scripture": "invented quote"},
            {**valid, "caption": "No source reference here."},
            {**valid, "safety_note": "Generated content."},
        ):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    validate_generated_pack(invalid, "John 3:16")

    @patch("app.request_json")
    @patch("app.gloo_token", return_value="test-token")
    def test_live_pack_fails_closed_on_model_contract_violation(
        self, _token, request
    ):
        request.return_value = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "headline": "Hope",
                                "caption": "Missing the required reference.",
                                "reflection": "Keep moving.",
                                "visual_direction": "Sunrise.",
                                "safety_note": "Review before publishing.",
                            }
                        )
                    }
                }
            ]
        }
        passage = {
            "reference": "John 3:16",
            "content": "Licensed source text",
            "demo": False,
        }
        with self.assertRaises(ValueError):
            create_pack(passage, "runners", "wearable", "hopeful")

    def test_http_creation_flow(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            payload = json.dumps(
                {
                    "reference": "JHN.3.16",
                    "bible_id": "3034",
                    "audience": "young adults",
                    "format": "carousel",
                    "tone": "hopeful",
                }
            ).encode()
            request = urllib.request.Request(
                f"http://127.0.0.1:{server.server_port}/api/create",
                data=payload,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(request) as response:
                result = json.load(response)
            self.assertEqual(result["passage"]["reference"], "John 3:16")
            self.assertIn("headline", result["pack"])
        finally:
            server.shutdown()
            server.server_close()

    def test_peak_effort_selects_wearable_delivery(self):
        snapshot = BiometricSnapshot(174, 5, "running", 0.91, 72, 4.1, 18)
        self.assertEqual(detect_moment(snapshot), "peak_effort")
        delivery = select_delivery(snapshot)
        self.assertEqual(delivery["detected_moment"], "peak_effort")
        self.assertIn("verse_reference", delivery)
        self.assertIn("delivery_format", delivery)


if __name__ == "__main__":
    unittest.main()

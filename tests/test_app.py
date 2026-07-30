import json
import os
import threading
import unittest
import urllib.request

from app import Handler, ThreadingHTTPServer, create_pack, retrieve_passage


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


if __name__ == "__main__":
    unittest.main()

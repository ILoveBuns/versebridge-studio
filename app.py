#!/usr/bin/env python3
"""VerseBridge Studio: creator-ready Scripture packs with source grounding."""

from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request


ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "static"


def request_json(url: str, *, headers: dict[str, str], payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(url, data=data, headers=headers)
    if payload is not None:
        request.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def retrieve_passage(bible_id: str, reference: str) -> dict:
    app_key = os.getenv("YVP_APP_KEY")
    if not app_key:
        return {
            "reference": "John 3:16",
            "content": "For God so loved the world that he gave his one and only Son...",
            "version": "Demo excerpt — connect YouVersion for licensed full text",
            "source_url": "https://www.bible.com/bible/111/JHN.3.16",
            "demo": True,
        }
    encoded = urllib.parse.quote(reference, safe=".")
    result = request_json(
        f"https://api.youversion.com/v1/bibles/{bible_id}/passages/{encoded}",
        headers={"x-yvp-app-key": app_key, "Accept": "application/json"},
    )
    return {
        "reference": result.get("reference", reference),
        "content": result.get("content", ""),
        "version": result.get("copyright", f"YouVersion Bible {bible_id}"),
        "source_url": result.get("share_url", "https://www.bible.com/"),
        "demo": False,
    }


def gloo_token() -> str | None:
    direct = os.getenv("GLOO_ACCESS_TOKEN")
    if direct:
        return direct
    client_id = os.getenv("GLOO_CLIENT_ID")
    client_secret = os.getenv("GLOO_CLIENT_SECRET")
    token_url = os.getenv("GLOO_TOKEN_URL")
    if not all((client_id, client_secret, token_url)):
        return None
    token = request_json(
        token_url,
        headers={"Accept": "application/json"},
        payload={"client_id": client_id, "client_secret": client_secret},
    )
    return token.get("access_token")


def create_pack(passage: dict, audience: str, format_name: str, tone: str) -> dict:
    token = gloo_token()
    if not token:
        return {
            "headline": "Love that moves toward people",
            "caption": (
                f"{passage['reference']} anchors this moment in generous love. "
                f"For {audience}, pause and name one practical way to offer care today."
            ),
            "reflection": "Where can love become a concrete action in the next 24 hours?",
            "visual_direction": "Warm sunrise, open doorway, accessible high-contrast typography.",
            "safety_note": "Review for audience context; do not present generated reflection as Scripture.",
            "demo": True,
        }
    prompt = f"""Create a concise content pack for {format_name}.
Audience: {audience}
Tone: {tone}
Scripture reference: {passage['reference']}
Licensed source text: {passage['content']}

Return JSON with exactly: headline, caption, reflection, visual_direction, safety_note.
Keep the Scripture reference visible. Clearly separate quoted Scripture from generated commentary.
Do not invent verse text, citations, promises, or theological certainty beyond the supplied source."""
    result = request_json(
        "https://platform.ai.gloo.com/ai/v2/chat/completions",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        payload={
            "messages": [
                {"role": "system", "content": "You create faithful, source-grounded creator content."},
                {"role": "user", "content": prompt},
            ],
            "tradition": "evangelical",
            "auto_routing": True,
            "response_format": {"type": "json_object"},
        },
    )
    content = result["choices"][0]["message"]["content"]
    pack = json.loads(content)
    pack["demo"] = False
    return pack


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status: int, value: dict) -> None:
        body = json.dumps(value, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        target = STATIC / ("index.html" if self.path == "/" else self.path.lstrip("/"))
        if not target.is_file() or STATIC not in target.resolve().parents:
            self.send_error(404)
            return
        body = target.read_bytes()
        content_type = "text/html; charset=utf-8" if target.suffix == ".html" else "text/css"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        if self.path != "/api/create":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(length))
            passage = retrieve_passage(data.get("bible_id", "3034"), data["reference"])
            pack = create_pack(
                passage,
                data.get("audience", "a general audience"),
                data.get("format", "social post"),
                data.get("tone", "hopeful and grounded"),
            )
            self.send_json(200, {"passage": passage, "pack": pack})
        except (KeyError, ValueError, urllib.error.URLError) as error:
            self.send_json(400, {"error": str(error)})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    print(f"VerseBridge Studio: http://127.0.0.1:{port}")
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()

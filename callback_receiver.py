"""
Sample webhook receiver - stands in for the system that wants the call results
(e.g. an AutomationEdge workflow webhook).

    python callback_receiver.py            # listens on http://localhost:5058/visit-result

Send it as callback_url in POST /api/call:
    "callback_url": "http://localhost:5058/visit-result"

Each result is printed, its X-Signature checked with API_KEY from .env,
and appended to callback_results.jsonl.
"""
import hashlib
import hmac
import json
import os
import sys
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5058


def api_key():
    with open(os.path.join(BASE_DIR, ".env"), encoding="utf-8") as f:
        for line in f:
            if line.startswith("API_KEY="):
                return line.split("=", 1)[1].strip()
    return ""


KEY = api_key().encode()


class Receiver(BaseHTTPRequestHandler):
    def do_POST(self):
        raw = self.rfile.read(int(self.headers.get("Content-Length") or 0))
        expected = hmac.new(KEY, raw, hashlib.sha256).hexdigest()
        genuine = hmac.compare_digest(expected, self.headers.get("X-Signature", ""))
        result = json.loads(raw)
        workflow = (result.get("ticket") or {}).get("call_workflow") or {}
        print(f"\n[{datetime.now():%H:%M:%S}] {result.get('event')} for {result.get('ticket_id')}  "
              f"data={result.get('data')}  state={workflow.get('state')}  signature_valid={genuine}")
        print(f"  {workflow.get('response_summary')}", flush=True)
        with open(os.path.join(BASE_DIR, "callback_results.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(dict(result, signature_valid=genuine), ensure_ascii=False) + "\n")
        self.send_response(200 if genuine else 401)
        self.end_headers()

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print(f"Callback receiver on http://localhost:{PORT}/visit-result  (results -> callback_results.jsonl)",
          flush=True)
    HTTPServer(("127.0.0.1", PORT), Receiver).serve_forever()

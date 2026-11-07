"""Owner-only HTTP boundary, exercised against a real loopback server."""
import http.client
import io
import json
import secrets
import tempfile
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace

from salesroom.core import SalesRoom
from salesroom.server import OwnerServer, OwnerHandler, ROOT, owner_key


class OwnerHTTPTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        try:
            self.server = OwnerServer(Path(self.tmp.name), ROOT / "salesroom/catalog.demo.json", 0)
        except PermissionError:
            self.tmp.cleanup()
            self.skipTest("This environment prevents opening a loopback HTTP port")
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.port = self.server.server_address[1]
        self.cookie = None
        self.csrf = None

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.tmp.cleanup()

    def request(self, method, path, value=None, auth=True, origin=True, csrf=True, host=None):
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        headers = {}
        if host:
            headers["Host"] = host
        if auth and self.cookie:
            headers["Cookie"] = self.cookie
        if origin:
            headers["Origin"] = f"http://127.0.0.1:{self.port}"
        if csrf and self.csrf:
            headers["X-Salesroom-CSRF"] = self.csrf
        raw = None
        if value is not None:
            raw = json.dumps(value)
            headers["Content-Type"] = "application/json"
        connection.request(method, path, raw, headers)
        response = connection.getresponse()
        data = response.read().decode()
        status = response.status
        cookie = response.getheader("Set-Cookie")
        connection.close()
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            pass
        return status, data, cookie

    def login(self):
        code, result, cookie = self.request("POST", "/api/session", {"token": self.server.bootstrap_token})
        self.assertEqual(code, 200)
        self.cookie = cookie.split(";", 1)[0]
        self.csrf = result["csrf"]
        self.assertIn("HttpOnly", cookie)
        self.assertIn("SameSite=Strict", cookie)

    def create(self):
        brief = json.loads((ROOT / "examples/lead.complete.json").read_text())
        code, lead, _ = self.request("POST", "/api/leads", {"brief": brief, "event_id": "http-create"})
        self.assertEqual(code, 200, lead)
        return lead

    def test_anonymous_actor_claim_cannot_approve(self):
        code, _, _ = self.request("POST", "/api/leads/fake/approve", {
            "actor": "owner", "approved": True, "revision": 1, "quote_hash": "fake", "event_id": "fake"
        }, auth=False)
        self.assertEqual(code, 403)
        code, _, _ = self.request("GET", "/api/state", auth=False)
        self.assertEqual(code, 403)

    def test_origin_csrf_and_host_checks(self):
        self.login()
        code, _, _ = self.request("POST", "/api/leads", {}, origin=False)
        self.assertEqual(code, 403)
        code, _, _ = self.request("POST", "/api/leads", {}, csrf=False)
        self.assertEqual(code, 403)
        code, _, _ = self.request("GET", "/api/state", host="attacker.invalid")
        self.assertEqual(code, 403)

    def test_actual_owner_flow_and_stale_download_refused(self):
        self.login()
        lead = self.create()
        url = "/api/leads/" + lead["id"]
        code, _, _ = self.request("GET", url + "/proposal")
        self.assertEqual(code, 409)
        code, lead, _ = self.request("POST", url + "/review", {"event_id": "http-review"})
        self.assertEqual(code, 200, lead)
        self.assertEqual(lead["status"], "awaiting_approval")
        code, lead, _ = self.request("POST", url + "/approve", {
            "event_id": "http-approve", "revision": lead["revision"], "quote_hash": lead["quote"]["hash"]
        })
        self.assertEqual(code, 200, lead)
        self.assertEqual(lead["status"], "approved")
        code, exported, _ = self.request("POST", url + "/export", {})
        self.assertEqual(code, 200, exported)
        self.assertTrue((Path(self.tmp.name) / "proposals" / exported["filename"]).exists())
        code, proposal, _ = self.request("GET", url + "/proposal")
        self.assertEqual(code, 200)
        self.assertIn("Alma Studio", proposal)
        self.assertIn(lead["quote"]["hash"], proposal)
        code, revised, _ = self.request("POST", url + "/update", {
            "event_id": "http-change", "changes": {"budget_kzt": 400000}
        })
        self.assertEqual(code, 200, revised)
        self.assertIsNone(revised["approval"])
        code, _, _ = self.request("GET", url + "/proposal")
        self.assertIn(code, (403, 409))


class RequestPipelineTests(OwnerHTTPTests):
    """Exercise real HTTP parsing/authorization in memory; not a live browser claim."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        data_dir = Path(self.tmp.name)
        catalog = ROOT / "salesroom/catalog.demo.json"
        token = owner_key(data_dir)
        SalesRoom(data_dir / "sales.sqlite3", catalog, token)
        self.server = SimpleNamespace(
            data_dir=data_dir, catalog=catalog, owner_token=token,
            bootstrap_token=secrets.token_urlsafe(32),
            session_token=secrets.token_urlsafe(32), csrf_token=secrets.token_urlsafe(32),
            server_address=("127.0.0.1", 8787),
            room=lambda: SalesRoom(data_dir / "sales.sqlite3", catalog, token),
        )
        self.port, self.cookie, self.csrf = 8787, None, None

    def tearDown(self):
        self.tmp.cleanup()

    def request(self, method, path, value=None, auth=True, origin=True, csrf=True, host=None):
        raw = json.dumps(value).encode() if value is not None else b""
        lines = [f"{method} {path} HTTP/1.1", f"Host: {host or f'127.0.0.1:{self.port}'}", "Connection: close"]
        if auth and self.cookie:
            lines.append("Cookie: " + self.cookie)
        if origin:
            lines.append(f"Origin: http://127.0.0.1:{self.port}")
        if csrf and self.csrf:
            lines.append("X-Salesroom-CSRF: " + self.csrf)
        if value is not None:
            lines.extend(["Content-Type: application/json", f"Content-Length: {len(raw)}"])

        class MemorySocket:
            def __init__(self, request):
                self.input = io.BytesIO(request)
                self.output = io.BytesIO()

            def makefile(self, *_args, **_kwargs):
                return self.input

            def sendall(self, data):
                self.output.write(data)

        connection = MemorySocket(("\r\n".join(lines) + "\r\n\r\n").encode() + raw)
        OwnerHandler(connection, ("127.0.0.1", 1), self.server)
        response = http.client.HTTPResponse(MemorySocket(connection.output.getvalue()))
        response.begin()
        data = response.read().decode()
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            pass
        return response.status, data, response.getheader("Set-Cookie")


if __name__ == "__main__":
    unittest.main()

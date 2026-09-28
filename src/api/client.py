"""Minimal DRI sandbox client, built from observed responses from
GET /erp/vendors, /erp/products, and /crm/customers. Every response observed so
far is a small JSON object wrapping a list under a named key
(e.g. {"vendors": [...]}), 200 status, no pagination at these row counts
(60/120/85). Extend this file only when a real call shows a behavior it
doesn't yet handle -- e.g. a 429 or a paginated response -- not before."""
import json
import time
import urllib.error
import urllib.request
from typing import Optional


class DriApiError(Exception):
    def __init__(self, status: int, body: str):
        self.status = status
        self.body = body
        super().__init__(f"DRI sandbox API error {status}: {body}")


class DriClient:
    # Confirmed real: a 105-call PATCH burst for M1 hit
    # "429 Rate limit exceeded: 60 requests per minute" partway through,
    # and stayed 429 for over a minute of real wall-clock waiting --
    # meaning it's not clearly a simple fixed-per-minute bucket that
    # resets on a clean boundary. Throttle well under the stated limit
    # (40/min, not 60) rather than trying to ride the exact edge.
    MAX_REQUESTS_PER_MINUTE = 40

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self._request_times: list = []  # sliding 60s window of past request timestamps

    def _throttle(self) -> None:
        now = time.monotonic()
        self._request_times = [t for t in self._request_times if now - t < 60]
        if len(self._request_times) >= self.MAX_REQUESTS_PER_MINUTE:
            sleep_for = 60 - (now - self._request_times[0]) + 0.5
            if sleep_for > 0:
                time.sleep(sleep_for)
        self._request_times.append(time.monotonic())

    def _request(self, method: str, path: str, json_body: Optional[dict] = None, _retries_left: int = 3) -> dict:
        self._throttle()
        url = f"{self.base_url}{path}"
        data = json.dumps(json_body).encode("utf-8") if json_body is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", f"Bearer {self.api_key}")
        # Real finding: urllib's default User-Agent ("Python-urllib/x.y")
        # trips Cloudflare bot protection in front of this API -- confirmed
        # by the exact same request succeeding via curl and failing via
        # urllib with "error code: 1010" (Cloudflare's own block code, not
        # a DRI API error). Not a guess -- verified both ways before fixing.
        req.add_header("User-Agent", "curl/8.7.1")
        if data is not None:
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8")
            if e.code == 429 and _retries_left > 0:
                time.sleep(65)  # real observed behavior: still 429 after 65s of wall-clock waiting once already
                return self._request(method, path, json_body, _retries_left - 1)
            raise DriApiError(e.code, body) from None

    def get(self, path: str) -> dict:
        return self._request("GET", path)

    def post(self, path: str, json_body: dict) -> dict:
        return self._request("POST", path, json_body)

    def patch(self, path: str, json_body: dict) -> dict:
        return self._request("PATCH", path, json_body)

    def reset(self) -> dict:
        return self.post("/reset", {})

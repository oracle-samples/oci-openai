# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

import asyncio
import threading

import httpx

from oci_openai.oci_openai import HttpxOciAuth


class _NoopSigner:
    def do_request_sign(self, prepared_request):
        prepared_request.headers["authorization"] = "signed"


class _FakeAuth(HttpxOciAuth):
    def __init__(self):
        super().__init__(signer=_NoopSigner(), refresh_interval=3600)
        self.refreshes = 0

    def _refresh_signer(self) -> None:
        self.refreshes += 1


def test_async_401_retry_does_not_hold_lock_while_sending():
    """A request retried after a 401 must not keep the refresh lock while it is in flight.

    Otherwise any other request on the same event loop blocks the loop thread in
    _refresh_if_needed() and the retry can never finish (see #27).
    """
    auth = _FakeAuth()
    retry_in_flight = asyncio.Event()
    second_done = asyncio.Event()
    calls = {"slow": 0}

    async def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/slow":
            calls["slow"] += 1
            if calls["slow"] == 1:
                return httpx.Response(401)
            retry_in_flight.set()
            # The retry waits for the other request before it answers.
            await asyncio.wait_for(second_done.wait(), timeout=5)
            return httpx.Response(200)
        return httpx.Response(200)

    async def main():
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler), auth=auth) as client:

            async def second():
                await retry_in_flight.wait()
                r = await client.get("https://example.invalid/fast")
                second_done.set()
                return r

            return await asyncio.gather(client.get("https://example.invalid/slow"), second())

    result = {}

    def run():
        result["responses"] = asyncio.run(main())

    t = threading.Thread(target=run, daemon=True)
    t.start()
    t.join(timeout=10)
    assert not t.is_alive(), "event loop deadlocked on HttpxOciAuth._lock"
    slow, fast = result["responses"]
    assert slow.status_code == 200
    assert fast.status_code == 200
    assert auth.refreshes == 1


def test_sync_401_retries_once_with_refreshed_signer():
    auth = _FakeAuth()
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request.headers.get("authorization"))
        return httpx.Response(401 if len(seen) == 1 else 200)

    with httpx.Client(transport=httpx.MockTransport(handler), auth=auth) as client:
        r = client.get("https://example.invalid/x")

    assert r.status_code == 200
    assert len(seen) == 2
    assert auth.refreshes == 1
    assert not auth._lock.locked()

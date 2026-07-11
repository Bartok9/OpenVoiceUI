"""Mocked tests for experimental Grok realtime bridge (flag default OFF)."""

from __future__ import annotations

import json
from contextlib import contextmanager
from unittest.mock import patch

import pytest


class TestGrokRealtimeBridge:
    def test_flag_default_off(self, monkeypatch):
        monkeypatch.delenv("OPENVOICEUI_GROK_REALTIME", raising=False)
        from services.grok_realtime_bridge import is_realtime_enabled, build_server_session

        assert is_realtime_enabled() is False
        res = build_server_session()
        assert res.enabled is False
        assert "off" in res.detail.lower() or "default" in res.detail.lower()

    def test_session_update_shape(self):
        from services.grok_realtime_bridge import default_session_update

        msg = default_session_update(voice="eve")
        assert msg["type"] == "session.update"
        assert msg["session"]["voice"] == "eve"
        assert msg["session"]["turn_detection"]["type"] == "server_vad"

    def test_open_requires_flag(self, monkeypatch):
        monkeypatch.delenv("OPENVOICEUI_GROK_REALTIME", raising=False)
        from services.grok_realtime_bridge import open_realtime_connection

        with pytest.raises(RuntimeError, match="disabled"):
            open_realtime_connection()

    def test_open_mocked_ws_sends_session_update(self, monkeypatch):
        monkeypatch.setenv("OPENVOICEUI_GROK_REALTIME", "1")
        monkeypatch.setenv("XAI_API_KEY", "test-key")

        class WS:
            def __init__(self):
                self.sent = []

            def send(self, data):
                self.sent.append(data)

        ws = WS()

        @contextmanager
        def connect(url, headers):
            assert "realtime" in url
            assert headers["Authorization"] == "Bearer test-key"
            yield ws

        from services.grok_realtime_bridge import open_realtime_connection

        with open_realtime_connection(connect_fn=connect, force=True) as sock:
            assert sock is ws

        payload = json.loads(ws.sent[0])
        assert payload["type"] == "session.update"
        assert payload["session"]["voice"] == "eve"

    def test_ephemeral_secret_mock(self, monkeypatch):
        monkeypatch.setenv("OPENVOICEUI_GROK_REALTIME", "1")
        monkeypatch.setenv("XAI_API_KEY", "k")

        def fake_post(url, api_key, payload):
            return {"value": "xai-realtime-client-secret-test", "expires_at": 999}

        from services.grok_realtime_bridge import fetch_ephemeral_client_secret

        out = fetch_ephemeral_client_secret(http_post=fake_post)
        assert out["value"].startswith("xai-realtime-client-secret")

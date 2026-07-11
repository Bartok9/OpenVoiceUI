"""Mocked tests for Grok TTS WebSocket streaming (TTFA path)."""

from __future__ import annotations

import base64
import json
from contextlib import contextmanager
from unittest.mock import patch

import pytest


class _FakeWS:
    def __init__(self, frames):
        self._frames = list(frames)
        self.sent = []

    def send(self, data):
        self.sent.append(data)

    def recv(self):
        if not self._frames:
            raise RuntimeError("no more frames")
        return self._frames.pop(0)


@contextmanager
def _fake_connect(frames):
    ws = _FakeWS(frames)

    def connect(url, headers):
        @contextmanager
        def _cm():
            yield ws

        return _cm()

    yield connect, ws


class TestGrokTTSStream:
    def test_stream_speech_sync_yields_audio_deltas(self):
        from tts_providers.grok_provider import GrokProvider, TTS_WS_URL

        chunk1 = b"ID3chunk-1"
        chunk2 = b"more-audio"
        frames = [
            json.dumps(
                {
                    "type": "audio.delta",
                    "delta": base64.b64encode(chunk1).decode("ascii"),
                }
            ),
            json.dumps(
                {
                    "type": "audio.delta",
                    "delta": base64.b64encode(chunk2).decode("ascii"),
                }
            ),
            json.dumps({"type": "audio.done"}),
        ]

        with _fake_connect(frames) as (connect, ws):
            p = GrokProvider()
            p.api_key = "k"
            out = list(
                p.stream_speech_sync(
                    "Hello stream",
                    voice="eve",
                    language="en",
                    optimize_streaming_latency=1,
                    connect_fn=connect,
                )
            )

        assert out == [chunk1, chunk2]
        sent_types = [json.loads(s)["type"] for s in ws.sent]
        assert sent_types == ["text.delta", "text.done"]
        assert json.loads(ws.sent[0])["delta"] == "Hello stream"

    def test_stream_requires_key(self):
        from tts_providers.grok_provider import GrokProvider

        p = GrokProvider()
        p.api_key = ""
        with pytest.raises(RuntimeError, match="XAI_API_KEY"):
            list(p.stream_speech_sync("hi", connect_fn=lambda u, h: None))

    def test_stream_ws_query_ttfa_default(self):
        from tts_providers.grok_provider import GrokProvider, TTS_WS_URL

        p = GrokProvider()
        p.api_key = "k"
        uri = p._stream_ws_query(voice="ara", language="en", optimize_streaming_latency=2)
        assert uri.startswith(TTS_WS_URL + "?")
        assert "voice=ara" in uri
        assert "optimize_streaming_latency=2" in uri

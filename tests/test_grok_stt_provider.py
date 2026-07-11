"""Mocked unit tests for Grok / xAI STT provider."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest


def _make_provider(api_key: str = "test-key"):
    from providers.stt.grok_provider import GrokSTTProvider

    p = GrokSTTProvider({"api_key": api_key, "language": "en"} if api_key else {})
    if not api_key:
        p.api_key = ""
    return p


class TestGrokSTTProvider:
    def test_missing_key_raises(self):
        p = _make_provider("")
        with pytest.raises(Exception) as ei:
            p.transcribe(b"fake-audio")
        assert "XAI_API_KEY" in str(ei.value)

    def test_is_available(self):
        assert _make_provider("k").is_available() is True
        assert _make_provider("").is_available() is False

    def test_happy_path_multipart(self):
        p = _make_provider("secret")
        fake_resp = MagicMock()
        fake_resp.status_code = 200
        fake_resp.json.return_value = {
            "text": "hello world",
            "language": "English",
            "duration": 1.25,
            "words": [
                {"text": "hello", "start": 0.0, "end": 0.4},
                {"text": "world", "start": 0.4, "end": 0.9},
            ],
        }

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.post.return_value = fake_resp

        with patch("providers.stt.grok_provider.httpx.Client", return_value=mock_client):
            result = p.transcribe(b"\x00\x01audio", language="en", filename="clip.wav")

        assert result.text == "hello world"
        assert result.provider == "grok"
        assert result.segments and len(result.segments) == 2
        args, kwargs = mock_client.post.call_args
        assert args[0] == "https://api.x.ai/v1/stt"
        assert kwargs["headers"]["Authorization"] == "Bearer secret"
        assert "files" in kwargs
        assert kwargs["files"]["file"][0] == "clip.wav"

    def test_http_error(self):
        p = _make_provider("secret")
        fake_resp = MagicMock()
        fake_resp.status_code = 401
        fake_resp.text = "unauthorized"
        fake_resp.json.side_effect = ValueError("no json")

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.post.return_value = fake_resp

        with patch("providers.stt.grok_provider.httpx.Client", return_value=mock_client):
            with pytest.raises(Exception, match="401"):
                p.transcribe(b"x")

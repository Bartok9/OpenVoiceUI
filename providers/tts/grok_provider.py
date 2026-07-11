"""
Grok / xAI TTS provider (registry adapter).

Delegates to tts_providers.grok_provider.GrokProvider when present.
Canonical implementation: tts_providers/grok_provider.py
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, List

from providers.tts.base import TTSError, TTSProvider
from providers.registry import ProviderType, registry

logger = logging.getLogger(__name__)


class GrokTTSProvider(TTSProvider):
    """xAI Grok cloud TTS — structured API via registry."""

    def __init__(self, config: Dict[str, Any] = None) -> None:
        super().__init__(config)
        self.api_key = self._resolve_api_key()
        self.default_voice = self._config.get(
            "default_voice", self._config.get("voice", "eve")
        )
        self.default_language = self._config.get("language", "en")
        self._impl = None

    def _resolve_api_key(self) -> str:
        key = self._config.get("api_key", "")
        if key and not str(key).startswith("${"):
            return str(key)
        return os.getenv("XAI_API_KEY", "")

    def _get_impl(self):
        if self._impl is None:
            from tts_providers.grok_provider import GrokProvider

            impl = GrokProvider()
            # Allow registry config to override env for tests
            if self.api_key:
                impl.api_key = self.api_key
                impl._status = "active"
                impl._init_error = None
            self._impl = impl
        return self._impl

    def generate_speech(self, text: str, **kwargs) -> bytes:
        self.validate_text(text)
        if not self.api_key:
            raise TTSError("grok", "XAI_API_KEY not set")

        voice = kwargs.get("voice", self.default_voice)
        language = (
            kwargs.get("language") or kwargs.get("lang") or self.default_language
        )
        try:
            return self._get_impl().generate_speech(
                text,
                voice=voice,
                language=language,
                **{
                    k: v
                    for k, v in kwargs.items()
                    if k not in ("voice", "language", "lang")
                },
            )
        except TTSError:
            raise
        except Exception as exc:
            raise TTSError("grok", f"Generation failed: {exc}") from exc

    def stream_speech(self, text: str, **kwargs):
        """WebSocket streaming TTS (TTFA). Delegates to canonical GrokProvider."""
        self.validate_text(text)
        if not self.api_key:
            raise TTSError("grok", "XAI_API_KEY not set")
        # Non-destructive reads — match generate_speech so shared option dicts stay intact.
        voice = (
            kwargs.get("voice_id")
            or kwargs.get("voice")
            or self.default_voice
        )
        language = (
            kwargs.get("language")
            or kwargs.get("lang")
            or self.default_language
        )
        allowed = {
            "codec",
            "sample_rate",
            "bit_rate",
            "optimize_streaming_latency",
            "speed",
            "text_normalization",
            "connect_fn",
        }
        clean = {k: v for k, v in kwargs.items() if k in allowed}
        try:
            return self._get_impl().stream_speech_sync(
                text, voice=voice, language=language, **clean
            )
        except TTSError:
            raise
        except Exception as exc:
            raise TTSError("grok", f"Stream failed: {exc}") from exc

    def list_voices(self) -> List[str]:
        try:
            return self._get_impl().list_voices()
        except Exception:
            from tts_providers.grok_provider import DOCUMENTED_VOICES

            return DOCUMENTED_VOICES.copy()

    def is_available(self) -> bool:
        return bool(self.api_key)

    def get_info(self) -> Dict[str, Any]:
        return {
            "name": self._config.get("name", "Grok / xAI TTS"),
            "status": "active" if self.is_available() else "inactive",
            "available": self.is_available(),
            "default_voice": self.default_voice,
            "provider_id": "grok",
        }


# Auto-register when this module is imported
registry.register(ProviderType.TTS, "grok", GrokTTSProvider)

"""
Grok / xAI TTS Provider — api.x.ai text-to-speech.

POST https://api.x.ai/v1/tts with Bearer XAI_API_KEY.
JSON body: text, voice_id, language (and optional output_format, speed).

API key: XAI_API_KEY env var
Docs: https://docs.x.ai/developers/model-capabilities/audio/text-to-speech
"""

from __future__ import annotations

import logging
import os
import time
from typing import Any, Dict, List, Optional

import httpx

from .base_provider import TTSProvider

logger = logging.getLogger(__name__)

API_BASE = "https://api.x.ai/v1"
TTS_URL = f"{API_BASE}/tts"
VOICES_URL = f"{API_BASE}/tts/voices"

GENERATE_TIMEOUT = 30.0
LIST_TIMEOUT = 15.0
HEALTH_TIMEOUT = 10.0

# Documented public roster (case-insensitive IDs). Prefer these for agents;
# do not embed private Team-of-Light / tenant custom voice secrets here.
# Default product preference for agents: eve (xAI default) then ara / rex.
DOCUMENTED_VOICES: List[str] = [
    "eve",  # default — general agents & UI confirmations
    "ara",  # warm / support-style
    "rex",  # clearer / media narration
    "sal",
    "leo",
]

AGENT_VOICE_PREFERENCE_NOTES = (
    "Agents: default voice_id=eve (xAI default). Prefer documented IDs only; "
    "pass custom voice_ids via config/env if operators clone voices registry-side. "
    "Do not commit private custom voice secrets into this package."
)

MAX_CHARACTERS = 15000


class GrokProvider(TTSProvider):
    """
    TTS Provider using xAI Grok Text-to-Speech API.

    Output: MP3 audio bytes by default (24 kHz / 128 kbps).
    """

    def __init__(self) -> None:
        super().__init__()
        self.api_key = os.getenv("XAI_API_KEY", "")
        self._status = "active" if self.api_key else "error"
        self._init_error: Optional[str] = None if self.api_key else "XAI_API_KEY not set"
        self._voices_cache: Optional[List[str]] = None
        self._voices_cache_time = 0.0

    def _auth_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def generate_speech(self, text: str, voice: str = "eve", **kwargs) -> bytes:
        """
        Generate speech via xAI TTS.

        Args:
            text: Text to synthesize (max 15_000 chars). Supports speech tags.
            voice: voice_id (default ``eve``). Also accepts kwargs ``voice_id``.
            **kwargs:
                language: BCP-47 code or ``auto`` (default ``en``).
                speed: 0.7–1.5 (optional).
                output_format: optional dict ``{codec, sample_rate, bit_rate}``.

        Returns:
            Raw audio bytes (default MP3).
        """
        if not self.api_key:
            raise RuntimeError("XAI_API_KEY not set")

        self.validate_text(text)
        if len(text) > MAX_CHARACTERS:
            raise ValueError(f"Text exceeds max {MAX_CHARACTERS} characters")

        voice_id = kwargs.get("voice_id") or voice or "eve"
        language = kwargs.get("language") or kwargs.get("lang") or "en"

        body: Dict[str, Any] = {
            "text": text,
            "voice_id": voice_id,
            "language": language,
        }
        if "speed" in kwargs and kwargs["speed"] is not None:
            body["speed"] = float(kwargs["speed"])
        if kwargs.get("output_format"):
            body["output_format"] = kwargs["output_format"]
        if kwargs.get("text_normalization") is not None:
            body["text_normalization"] = bool(kwargs["text_normalization"])
        if kwargs.get("optimize_streaming_latency") is not None:
            body["optimize_streaming_latency"] = int(kwargs["optimize_streaming_latency"])

        t = time.time()
        logger.info("[Grok/xAI] TTS request: '%s' voice=%s lang=%s", text[:60], voice_id, language)

        try:
            with httpx.Client(timeout=httpx.Timeout(GENERATE_TIMEOUT, connect=10.0)) as client:
                resp = client.post(TTS_URL, headers=self._auth_headers(), json=body)
                if resp.status_code >= 400:
                    detail = (resp.text or "")[:400]
                    raise RuntimeError(f"[grok:{resp.status_code}] {detail}")
                audio_bytes = resp.content
        except httpx.TimeoutException as exc:
            raise RuntimeError(f"[grok:timeout] TTS after {GENERATE_TIMEOUT}s") from exc
        except httpx.RequestError as exc:
            raise RuntimeError(f"[grok:network] {exc}") from exc

        if not audio_bytes:
            raise RuntimeError("[grok:empty] Empty audio body from xAI TTS")

        elapsed = int((time.time() - t) * 1000)
        logger.info("[Grok/xAI] Generated %s bytes in %sms", len(audio_bytes), elapsed)
        return audio_bytes

    def list_voices(self) -> List[str]:
        """
        Return voice IDs: live GET /v1/tts/voices when keyed, else documented roster.
        """
        if not self.api_key:
            return DOCUMENTED_VOICES.copy()

        # Short TTL cache
        now = time.time()
        if self._voices_cache is not None and (now - self._voices_cache_time) < 300:
            return self._voices_cache.copy()

        try:
            with httpx.Client(timeout=httpx.Timeout(LIST_TIMEOUT, connect=5.0)) as client:
                resp = client.get(
                    VOICES_URL,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                )
                if resp.status_code >= 400:
                    logger.warning(
                        "[Grok/xAI] list voices HTTP %s — using documented roster",
                        resp.status_code,
                    )
                    return DOCUMENTED_VOICES.copy()
                payload = resp.json()
                voices = payload.get("voices") or []
                ids = [
                    str(v.get("voice_id") or v.get("id") or "").strip()
                    for v in voices
                    if isinstance(v, dict)
                ]
                ids = [i for i in ids if i]
                if not ids:
                    return DOCUMENTED_VOICES.copy()
                self._voices_cache = ids
                self._voices_cache_time = now
                return ids.copy()
        except Exception as exc:
            logger.warning("[Grok/xAI] list_voices failed: %s — documented roster", exc)
            return DOCUMENTED_VOICES.copy()

    def get_default_voice(self) -> str:
        return "eve"

    def is_available(self) -> bool:
        return bool(self.api_key)

    def health_check(self) -> dict:
        if not self.api_key:
            return {"ok": False, "latency_ms": 0, "detail": "XAI_API_KEY not set"}
        t = time.time()
        try:
            with httpx.Client(timeout=httpx.Timeout(HEALTH_TIMEOUT, connect=5.0)) as client:
                resp = client.get(
                    VOICES_URL,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                )
                latency_ms = int((time.time() - t) * 1000)
                if resp.status_code >= 400:
                    return {
                        "ok": False,
                        "latency_ms": latency_ms,
                        "detail": f"HTTP {resp.status_code}: {(resp.text or '')[:200]}",
                    }
                return {
                    "ok": True,
                    "latency_ms": latency_ms,
                    "detail": "xAI TTS reachable — /v1/tts/voices OK",
                }
        except Exception as exc:
            latency_ms = int((time.time() - t) * 1000)
            return {"ok": False, "latency_ms": latency_ms, "detail": str(exc)}

    def get_info(self) -> dict:
        return {
            "name": "Grok / xAI TTS",
            "provider_id": "grok",
            "status": self._status if self.api_key else "error",
            "description": "xAI Text-to-Speech (Grok voices) — cloud MP3 TTS with speech tags",
            "quality": "high",
            "latency": "fast",
            "cost_per_minute": 0.0,  # operators: check console.x.ai for current pricing
            "voices": DOCUMENTED_VOICES.copy(),
            "features": [
                "cloud",
                "multilingual",
                "speech-tags",
                "mp3-output",
                "custom-voices-api",
                "agent-friendly-defaults",
            ],
            "requires_api_key": True,
            "languages": [
                "en",
                "zh",
                "fr",
                "de",
                "hi",
                "id",
                "it",
                "ja",
                "ko",
                "pt-BR",
                "pt-PT",
                "ru",
                "es-MX",
                "es-ES",
                "tr",
                "vi",
                "bn",
                "ar-EG",
                "ar-SA",
                "ar-AE",
                "auto",
            ],
            "max_characters": MAX_CHARACTERS,
            "notes": (
                "XAI_API_KEY required. Default voice_id=eve. "
                + AGENT_VOICE_PREFERENCE_NOTES
            ),
            "default_voice": "eve",
            "audio_format": "mp3",
            "sample_rate": 24000,
            "documentation_url": (
                "https://docs.x.ai/developers/model-capabilities/audio/text-to-speech"
            ),
            "error": self._init_error,
            "agent_voice_preference": AGENT_VOICE_PREFERENCE_NOTES,
        }


__all__ = [
    "GrokProvider",
    "DOCUMENTED_VOICES",
    "AGENT_VOICE_PREFERENCE_NOTES",
    "TTS_URL",
]

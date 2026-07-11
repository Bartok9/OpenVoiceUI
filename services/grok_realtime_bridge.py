"""
Experimental Grok Voice realtime bridge (server-side only).

Feature flag (default OFF):
  OPENVOICEUI_GROK_REALTIME=0|false|off  (default)
  OPENVOICEUI_GROK_REALTIME=1|true|on    enables helpers

Connects to:
  wss://api.x.ai/v1/realtime?model=grok-voice-latest

Uses XAI_API_KEY from the environment only. Never expose raw keys to browsers;
for browser use, mint ephemeral client secrets via POST /v1/realtime/client_secrets
(not implemented here beyond a small helper).

Minimal session.update posture: voice=eve, turn_detection server_vad.
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

REALTIME_WS_BASE = "wss://api.x.ai/v1/realtime"
CLIENT_SECRETS_URL = "https://api.x.ai/v1/realtime/client_secrets"
DEFAULT_MODEL = "grok-voice-latest"


def is_realtime_enabled() -> bool:
    """Return True only when OPENVOICEUI_GROK_REALTIME is truthy."""
    raw = (os.getenv("OPENVOICEUI_GROK_REALTIME") or "").strip().lower()
    return raw in {"1", "true", "yes", "on", "enabled"}


def realtime_ws_url(model: str = DEFAULT_MODEL) -> str:
    return f"{REALTIME_WS_BASE}?{urlencode({'model': model})}"


def default_session_update(
    *,
    voice: str = "eve",
    instructions: Optional[str] = None,
) -> Dict[str, Any]:
    """Minimal session.update payload (voice + server_vad)."""
    session: Dict[str, Any] = {
        "voice": voice or "eve",
        "turn_detection": {"type": "server_vad"},
    }
    if instructions:
        session["instructions"] = instructions
    return {"type": "session.update", "session": session}


@dataclass
class RealtimeSessionResult:
    url: str
    session_update: Dict[str, Any]
    enabled: bool
    detail: str


def build_server_session(
    *,
    model: str = DEFAULT_MODEL,
    voice: str = "eve",
    instructions: Optional[str] = None,
    force: bool = False,
) -> RealtimeSessionResult:
    """
    Prepare connection parameters. Does not open a socket unless force and enabled.

    Raises RuntimeError if enabled/force and XAI_API_KEY is missing.
    """
    enabled = is_realtime_enabled()
    if not enabled and not force:
        return RealtimeSessionResult(
            url=realtime_ws_url(model),
            session_update=default_session_update(voice=voice, instructions=instructions),
            enabled=False,
            detail="OPENVOICEUI_GROK_REALTIME is off (default) — bridge not active",
        )

    api_key = os.getenv("XAI_API_KEY", "")
    if not api_key:
        raise RuntimeError("XAI_API_KEY not set (required for Grok realtime bridge)")

    return RealtimeSessionResult(
        url=realtime_ws_url(model),
        session_update=default_session_update(voice=voice, instructions=instructions),
        enabled=True,
        detail="ready (server-side WS; do not send XAI_API_KEY to browsers)",
    )


def open_realtime_connection(
    *,
    model: str = DEFAULT_MODEL,
    voice: str = "eve",
    instructions: Optional[str] = None,
    connect_fn=None,
    force: bool = False,
):
    """
    Open a server-side WebSocket to Grok realtime and send session.update.

    Flag must be on (or force=True for tests). Returns the open WS context manager
    result from websockets / inject connect_fn(url, headers) -> ctx manager.

    Usage (live, flag on)::

        with open_realtime_connection() as ws:
            ...
    """
    if not is_realtime_enabled() and not force:
        raise RuntimeError(
            "Grok realtime bridge disabled — set OPENVOICEUI_GROK_REALTIME=1 to enable"
        )

    api_key = os.getenv("XAI_API_KEY", "")
    if not api_key:
        raise RuntimeError("XAI_API_KEY not set")

    url = realtime_ws_url(model)
    headers = {"Authorization": f"Bearer {api_key}"}
    update = default_session_update(voice=voice, instructions=instructions)

    def _default_connect(ws_url: str, hdrs: Dict[str, str]):
        from websockets.sync.client import connect as ws_connect

        return ws_connect(ws_url, additional_headers=hdrs, open_timeout=15, close_timeout=5)

    connector = connect_fn or _default_connect
    # Return a small wrapper that sends session.update after enter
    class _Session:
        def __init__(self):
            self._cm = connector(url, headers)
            self.ws = None

        def __enter__(self):
            self.ws = self._cm.__enter__()
            self.ws.send(json.dumps(update))
            logger.info("[Grok realtime] session.update sent voice=%s", voice)
            return self.ws

        def __exit__(self, *exc):
            return self._cm.__exit__(*exc)

    return _Session()


def fetch_ephemeral_client_secret(
    *,
    expires_seconds: int = 300,
    model: str = DEFAULT_MODEL,
    http_post=None,
) -> Dict[str, Any]:
    """
    Server-only helper: POST /v1/realtime/client_secrets.

    Browsers can use the returned short-lived token; never the long-lived XAI_API_KEY.
    Requires flag ON for production callers; tests may pass http_post mock.
    """
    if not is_realtime_enabled() and http_post is None:
        raise RuntimeError(
            "Grok realtime bridge disabled — set OPENVOICEUI_GROK_REALTIME=1"
        )
    api_key = os.getenv("XAI_API_KEY", "")
    if not api_key and http_post is None:
        raise RuntimeError("XAI_API_KEY not set")

    payload = {
        "expires_after": {"seconds": int(expires_seconds)},
        "session": {"model": model},
    }

    if http_post is not None:
        return http_post(CLIENT_SECRETS_URL, api_key, payload)

    import httpx

    with httpx.Client(timeout=httpx.Timeout(15.0, connect=5.0)) as client:
        resp = client.post(
            CLIENT_SECRETS_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        if resp.status_code >= 400:
            raise RuntimeError(
                f"client_secrets HTTP {resp.status_code}: {(resp.text or '')[:300]}"
            )
        return resp.json()


__all__ = [
    "REALTIME_WS_BASE",
    "DEFAULT_MODEL",
    "is_realtime_enabled",
    "realtime_ws_url",
    "default_session_update",
    "build_server_session",
    "open_realtime_connection",
    "fetch_ephemeral_client_secret",
    "RealtimeSessionResult",
]

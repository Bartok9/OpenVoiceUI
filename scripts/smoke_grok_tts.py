#!/usr/bin/env python3
"""
Live smoke for Grok / xAI TTS (unary).

Requires XAI_API_KEY in the environment.
Writes audio under /tmp only (never the repo).

Exit codes:
  0 — ok / skipped with reason printed when key missing (default soft-skip)
  1 — request failed
  2 — hard fail when OPENVOICEUI_SMOKE_REQUIRE_KEY=1 and key missing

Usage:
  export XAI_API_KEY=...
  python3 scripts/smoke_grok_tts.py
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

# Allow running from repo root without install
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


def main() -> int:
    key = os.getenv("XAI_API_KEY", "").strip()
    require = (os.getenv("OPENVOICEUI_SMOKE_REQUIRE_KEY") or "").strip() in {
        "1",
        "true",
        "yes",
    }
    if not key:
        msg = "XAI_API_KEY not set — skip live Grok TTS smoke (unary # works when set)"
        print(msg)
        return 2 if require else 0

    from tts_providers.grok_provider import GrokProvider

    out = Path(f"/tmp/openvoiceui-grok-tts-smoke-{int(time.time())}.mp3")
    provider = GrokProvider()
    text = os.getenv("OPENVOICEUI_SMOKE_TEXT") or "OpenVoiceUI Grok TTS smoke test."
    t0 = time.time()
    try:
        audio = provider.generate_speech(text, voice="eve", language="en")
    except Exception as exc:
        print(f"FAIL: {exc}")
        return 1

    out.write_bytes(audio)
    ms = int((time.time() - t0) * 1000)
    print(f"OK wrote {out} ({len(audio)} bytes, {ms}ms)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

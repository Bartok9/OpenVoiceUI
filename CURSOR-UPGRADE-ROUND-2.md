# Cursor — OpenVoiceUI upgrade round 2

Model: Grok quality. Public fork — **no secrets**. Env-only XAI_API_KEY.

## Already shipped (#1–#4)
VISION/ARCHITECTURE, Grok TTS provider, radar, stability+SECURITY, sample phone hygiene.

## Priority implementation PRs

### A — Stream Grok TTS (first audio latency)
1. Add streaming method on `GrokProvider` (WS or chunked if API documents)
2. Tests with mocked sockets
3. Route or canvas hook optional behind flag

### B — Grok STT provider
1. `stt_providers/grok_provider.py` or analog matching existing STT base
2. Unit tests for missing key + happy path mock
3. Docs in docs/features/

### C — Experimental Realtime bridge (flagged)
1. Server-side WS proxy to `wss://api.x.ai/v1/realtime?model=grok-voice-latest`
2. Never ship browser-facing raw XAI_API_KEY (ephemeral tokens if easy; else server only)
3. Minimal session.update (voice=eve, server_vad)
4. Feature flag default off
5. Smoke integration test with mocked WS

### D — Dev smoke
1. `scripts/smoke_grok_tts.py` → writes under /tmp, exits 0/1
2. README link "Grok works if you have XAI_API_KEY"

```bash
pytest -q tests/test_grok_tts_provider.py
# full suite needs requirements.txt
```

# Voice stack state — Bartok review 2026-07-11 (post-live test)

## Can we use it?

**Yes for cascaded TTS.** Live dogfood on main:

| Check | Result |
|-------|--------|
| `pytest tests/test_grok_tts_provider.py` | **17 passed** |
| `GrokProvider.list_voices()` | live xAI roster (26+ ids) |
| `generate_speech(..., voice=eve/ara)` | MP3 bytes returned (eve ~69KB for short line) |
| Missing key | `is_available() False` clean fail |
| Secrets in tree | none — env only |

**Not yet a full Grok Voice Agent shell.** Industry moved to **speech-to-speech realtime** (OpenAI Realtime-compat at `wss://api.x.ai/v1/realtime`, Gemini Live, Inworld). We still excel at multi-provider **turn-based** STT→LLM→TTS + canvas. That's valuable — but not the 2026 state of the art end-to-end latency story.

## Cutting edge (research snapshot)

External sources (verify before build):

1. **xAI Grok Voice Agent API** — WebSocket realtime, OpenAI Realtime-compatible, tools (web_search), server_vad, LiveKit plugin, ephemeral tokens for client.
2. **Standalone STT/TTS** — we integrated **TTS**; STT + streaming TTS WebSocket densely underused.
3. **Speech tags** — xAI TTS supports expressive tags (laughter, pauses) — partial in docs, not exercised in UI.
4. **Competitors** — Gemini flash-live 2026, Inworld realtime + router, Cartesia/Eleven streaming, Pipecat Grok S2S service.
5. **Phone** — cascaded still wins for telephony; S2S for browser/app chat.

## Suggested upgrade PRs (serial)

### PR U1 — Streaming Grok TTS WebSocket (latency)
- Unary `POST /v1/tts` already works
- Add optional stream path for partial play-out in canvas
- Metrics: time-to-first-audio

### PR U2 — Grok STT provider (parity with our clawd transcribe)
- File + stream STT via `api.x.ai/v1/stt`
- Wire to existing STT registry; word timestamps if curated

### PR U3 — Realtime voice agent bridge (experimental flag)
- Thin adapter: OpenAI-Realtime-compatible client → xAI `wss://api.x.ai/v1/realtime?model=grok-voice-latest`
- Feature flag `VOICE_MODE=cascaded|realtime`
- Ephemeral token endpoint or server-mediated WS (never expose key to browser)
- Do **not** replace canvas/tools path v1 — dual-path

### PR U4 — Dev ergonomics
- `make smoke-grok` writes sample wav/mp3 under /tmp only
- Dependable pytest env: document venv/`pip install -r requirements.txt`
- Full suite green in CI continue; local bare python 3.14 needs deps
- Close stale checklist-only PR if superseded

### NON_GOAL this week
- Publishing keys, forking OpenAI Realtime full UI, replacing all providers

## Use bar for Bartok today
Use as **library TTS provider** anytime we need Grok eve/ara speech in OpenVoiceUI or glue scripts. Full voice UX still wants Realtime path for natural barge-in.

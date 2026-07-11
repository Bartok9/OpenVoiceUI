# Cursor upgrade checklist — OpenVoiceUI → Bartok Design doc bar + modern voice stack

**Model preference:** Grok 4.5 for bulk coding.  
**Branch pattern:** `cursor/openvoiceui-<slice>-YYYYMMDD`  
**Rule:** one focused PR at a time when possible · tests green · human review merge.

---

## Pass 0 — orientation (human already ran summary)

- [x] Confirm public fork of MCERQUA/OpenVoiceUI  
- [x] Identify gap: no VISION/ARCHITECTURE/AGENTS historically  
- [x] TTS pete activitiy: groq, elevenlabs, hume, qwen3, resemble, supertonic — **no Grok/xAI yet**  
- [x] Docs: strong README/SETUP; OpenClaw-centric  
- [x] Tests: substantial `tests/` + CI workflows  

---

## PR A — Docs foundation (can ship without product risk)

- [x] Add `VISION.md`  
- [x] Add `ARCHITECTURE.md`  
- [x] Add `AGENTS.md`  
- [x] Add this checklist  
- [ ] Link them from README (short "Bartok track / for agents" section)  
- [ ] `docs/getting-started/HERMES.md` dual-runtime sketch (env table OpenClaw vs Hermes)  
- [ ] Keep upstream attribution clear in README  

---

## PR B — Grok / xAI TTS provider (priority product)

- [ ] `tts_providers/grok_provider.py` implementing `TTSProvider`  
  - Unary `POST https://api.x.ai/v1/tts`  
  - Auth `XAI_API_KEY`  
  - Voices listing (document defaults; include male voices useful for agent personas, e.g. vendor roster — **do not hardcode TOL private mapping secrets**)  
  - Format handling (mp3 bytes) matching other providers  
- [ ] Register in `tts_providers/providers_config.json` + discovery/__init__  
- [ ] Config / `.env.example` entries + loader keys if needed  
- [ ] `tests/test_grok_tts_provider.py` with **mocked** HTTP (no network required)  
- [ ] Admin/UI: provider appears in settings if auto-discovered  
- [ ] Docs: `docs/features/grok-tts.md`  

Optional follow-up (same or next PR if small): streaming TTS websocket; STT provider stub interface for `POST /v1/stt`.

---

## PR C — Dual runtime OpenClaw + Hermes

- [ ] `config/runtimes/openclaw.yaml` & `config/runtimes/hermes.yaml` (or documented env matrix only if code adapter is heavy)  
- [ ] Docs: step-by-step Hermes gateway + canvas mount  
- [ ] Smoke script `scripts/check-runtime.sh` that prints which envs are set  
- [ ] CI job dry-run config load for both matrices  

---

## PR D — Tech radar (self-improving awareness)

- [ ] `scripts/voice-tech-radar.mjs` or `.py`:  
  - scan sources (xAI models endpoint if keyed; static list of providers; GitHub search low-noise)  
  - write `docs/radar/YYYY-MM-DD.md` summary  
  - exit 0 even on empty results  
- [ ] GitHub Action weekly scheduled (bartok9 fork) opening **draft** PR or issue on delta  
- [ ] Never auto-merge dependency bumps without human  

---

## PR E — Test & quality polish

- [ ] Ensure `pytest -q` documented in CONTRIBUTING  
- [ ] Coverage critical for new providers  
- [ ] Pin notes on fragile tests  
- [ ] SECURITY.md note on audio processing vendors  

---

## Research anchors (2026-07-11)

| Topic | URL / path |
|-------|------------|
| xAI Voice overview | https://docs.x.ai/developers/model-capabilities/audio/voice |
| xAI Realtime | `wss://api.x.ai/v1/realtime?model=grok-voice-latest` |
| xAI unary TTS | `POST https://api.x.ai/v1/tts` |
| xAI STT | `POST https://api.x.ai/v1/stt` |
| LiveKit xAI | https://docs.livekit.io/agents/models/realtime/plugins/xai/ |
| Local Grok audio scaffold | `~/clawd/tools/grok-audio/` (TOL private reference) |

---

## Merge policy (public fork)

1. CI green  
2. No secrets  
3. Credit upstream where we port  
4. Small PR if possible  
5. Bartok reviews Bugbot autofix before merge when present

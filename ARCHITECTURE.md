# ARCHITECTURE — OpenVoiceUI (Bartok9 track)

**Date:** 2026-07-11  
**Sources of truth in code:** `app.py` / routes / `providers/` / `tts_providers/` / `cli/` / Docker compose  

---

## Context

OpenVoiceUI is a **voice + canvas shell** around an agent gateway:

```
  Mic / STT  ──►  Gateway (OpenClaw | Hermes)  ──►  LLM / tools / skills
                       │
                       ├── TTS providers (play response)
                       ├── Canvas pages (live HTML apps)
                       ├── Profiles / faces / theme
                       └── Optional music / vision / plugins
```

### C4-ish layers

| Layer | Location (representative) | Notes |
|-------|---------------------------|--------|
| HTTP/UI shell | `app.py`, `index.html`, `src/`, `static/` | Browser voice session + admin |
| Routes | `routes/` | REST/API surfaces (canvas, conversation, music, admin, vision…) |
| TTS providers | `tts_providers/` | Pluggable `TTSProvider` interface |
| LLM / STT providers | `providers/` | Registry + STT/LLM modules |
| Config | `config/*.yaml`, `.env` | Provider selection, flags |
| Runtime glue | `cli/`, Docker Compose | Setup, start, gateway process wiring |
| Docs site content | `docs/` | Feature/setup guides |

---

## Critical integrations

### OpenClaw (default historical path)

- Gateway WebSocket, token env historically `CLAWDBOT_*` (compat names).  
- Canvas pages volume shared with agent workspace.  
- Documented pin version in SETUP / openclaw-requirements.

### Hermes (target parity)

- Must map: gateway URL, auth, workspace/canvas mounts, coding CLI, session profiles.  
- Prefer adapter module over forking the whole shell — keep Hermes config under `config/runtimes/hermes.yaml` (planned) + docs/getting-started/hermes.md (planned).

### TTS provider contract

All providers implement `tts_providers/base_provider.py::TTSProvider`:

- Voice listing + synthesize  
- Metadata (latency tier, online/offline, key requirements)  
- Registration in `providers_config.json` + discovery path used by admin UI

**Grok/xAI** (upgrade target):

| Mode | Endpoint / notes |
|------|------------------|
| Unary TTS | `POST https://api.x.ai/v1/tts` (`text`, `voice_id`, …) |
| Streaming TTS | xAI TTS WebSocket family (see xAI docs) |
| STT | `POST https://api.x.ai/v1/stt` |
| Realtime voice agent | `wss://api.x.ai/v1/realtime?model=grok-voice-latest` (OpenAI-realtime-compatible schema) |

Env: `XAI_API_KEY` (and/or gateway bridged keys — never commit secrets).

---

## Data & security

- API keys only via env / secret mounts.  
- Device approval flows for pairings.  
- Canvas content treated as agent-produced HTML — sanitize/framing assumptions documented for operators.  
- No training claims around user audio when using xAI (vendor: not stored for training per xAI voice overview).

---

## Testing strategy

| Band | Tooling | Target |
|------|---------|--------|
| Unit / route | `pytest` under `tests/` | providers, routes, config load |
| Provider smoke | optional network marks | skip without keys |
| CI | `.github/workflows/tests.yml` | green on PR |

New providers: **unit with mocked HTTP** + optional live smoke.

---

## Extension points

1. New TTS → subclass provider + config entry + tests  
2. New agent runtime → runtime adapter + docs + compose overlay  
3. Canvas skills → default-pages / plugins catalog  
4. Tech radar → `scripts/voice-tech-radar.*` writes `docs/radar/` + optional PR

---

## Fork policy (Bartok9)

- Track upstream regularly; prefer small reverse-port PRs.  
- TOL-local IDs (Grok voices, Hermes, radar) may live first on Bartok9 — document in CHANGELOG.  
- Public repo: no private TOL secrets, no private person dossiers.

---

## Related docs

- `VISION.md` · `AGENTS.md` · `SETUP.md` · `docs/` tree · `CURSOR-UPGRADE-CHECKLIST.md`

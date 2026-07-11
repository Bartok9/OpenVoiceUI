# AGENTS.md — working on OpenVoiceUI (Bartok9)

## What this is

Voice + live-canvas shell for AI agents. Brain is **not** in this repo — gateways are.

## Runtimes

| Runtime | Status in tree | How to help |
|---------|----------------|-------------|
| OpenClaw | Documented default | Keep `docs/openclaw-requirements.md` current |
| Hermes | Upgrade target | Dual-runtime docs + adapter env map |

## Do

- Prefer provider plugins over hardcoding vendors in `app.py`.  
- Add tests next to behavior (`tests/`).  
- Document env vars in `.env.example`.  
- Keep public: no TOL secrets.

## Do not

- Break MCERQUA upstream mergeability without a clear fork note.  
- Force a single LLM vendor.  
- Land Grok keys in repo.  

## Useful commands

```bash
# Python tests (from repo root, venv as project standard)
pytest -q

# TTS registration check (after Grok lands)
rg -n "grok|xai" tts_providers config
```

## Cursor

See `CURSOR-UPGRADE-CHECKLIST.md` for the upgrade sequence.

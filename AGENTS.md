# AGENTS.md — OpenVoiceUI (OpenClaw + Hermes)

**Dual-agent workspace.** Optimized for **OpenClaw** (SOUL.md, skills) and **Hermes** (AGENTS.md, SKILL.md discovery).

**Read first:** [llms.txt](llms.txt) · [SOUL.md](SOUL.md) · [README.md](README.md) · [VISION.md](VISION.md) · [DUAL_AGENT_CHECKLIST.md](DUAL_AGENT_CHECKLIST.md)

## Compatibility scores (post dual-agent elevation)

| Agent | Score | Notes |
|-------|------:|-------|
| OpenClaw | **95** | SOUL + skills + CI + llms |
| Hermes | **95** | AGENTS + skill tree + docs/getting-started/HERMES.md |
| **Dual overall** | **95** | Upstream MIT lineage + Bartok9 Grok track |

## Upstream
- Parent: [MCERQUA/OpenVoiceUI](https://github.com/MCERQUA/OpenVoiceUI)
- Our track: Grok TTS, VISION/ARCHITECTURE, dual-runtime docs, radar

## Commands

```bash
pytest -q tests/test_grok_tts_provider.py
bash scripts/check-runtime.sh
python3 scripts/voice_tech_radar.py --help
ls SOUL.md AGENTS.md llms.txt DUAL_AGENT_CHECKLIST.md
```

## Skills
| Skill | Path |
|-------|------|
| orient-openvoiceui | `.agents/skills/orient-openvoiceui/SKILL.md` |
| validate-openvoiceui | `.agents/skills/validate-openvoiceui/SKILL.md` |

## Boundaries
- Env-only keys (`XAI_API_KEY`, etc.). Never commit `.env`.
- Docs-only elevation must not change runtime defaults without tests.


---

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

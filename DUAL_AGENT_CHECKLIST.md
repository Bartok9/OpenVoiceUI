# DUAL_AGENT_CHECKLIST — OpenVoiceUI

_Elevated: 2026-07-11 · public fork of MCERQUA/OpenVoiceUI_

## Scores (target after this elevation)

| Agent | Score | Notes |
|-------|------:|-------|
| OpenClaw | **95** | SOUL + orient skills + CI + llms |
| Hermes | **95** | AGENTS + skills + HERMES.md |
| Dual | **95** | Required surface present |

## Required surface

| File / area | Status |
|-------------|--------|
| SOUL.md | ✅ |
| AGENTS.md | ✅ |
| llms.txt | ✅ |
| DUAL_AGENT_CHECKLIST.md | ✅ |
| skills / .agents/skills | ✅ orient + validate |
| CI (.github/workflows) | ✅ existing |
| CONTRIBUTING | ✅ (upstream) |
| README | ✅ |

## Soft

| Item | Status |
|------|--------|
| VISION / ARCHITECTURE | ✅ Bartok9 track |
| Security notes | ✅ SECURITY.md |

## Notes
- Public: no personal data in SOUL/AGENTS.
- Grok TTS is env-gated (`XAI_API_KEY`).
- Master private checklist does **not** include this public fork; this file is repo-local.

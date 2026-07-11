# VISION — OpenVoiceUI (Bartok9 track)

**Repo:** [Bartok9/OpenVoiceUI](https://github.com/Bartok9/OpenVoiceUI) · **Upstream:** [MCERQUA/OpenVoiceUI](https://github.com/MCERQUA/OpenVoiceUI) (public fork, MIT)  
**Status:** Living vision — Bartok world-class track (2026-07-11)  
**Audience:** OpenClaw + Hermes + standalone agents · Team of Light + public contributors  

---

## The statement

**OpenVoiceUI is the open voice surface for agents that do work** — not a chat widget with a microphone.

You speak. The agent plans, builds, and **shows**: live canvas pages, tools, music, face/presence — on hardware you control.

We hold a Bartok9 fork so Team of Light can land **local reliability, dual-runtime support (OpenClaw + Hermes), Grok/xAI voice depth, and continuous tech radar** without waiting on upstream for every cut. We still respect the MIT lineage and the excellent product core from MCERQUA.

---

## Goals (next 90 days)

1. **Agent-runtime parity** — first-class OpenClaw *and* Hermes gateway recipes (not OpenClaw-only folklore).  
2. **Grok/xAI voice stack** — Grok TTS (unary + stream) as a first-class provider; path to Grok Voice realtime / STT.  
3. **Honest docs bar** — VISION + ARCHITECTURE + AGENTS + dual-runtime setup (Bartok Design bar).  
4. **Test gate** — providers and dual-runtime config covered; CI actionable.  
5. **Self-update radar** — scheduled check for new STT/TTS/realtime options with human-review PR, not silent dependency ndrape.

## Non-goals

- Replacing OpenClaw ot Hermes as the agent brain (we are the voice/canvas shell).  
- Stealing proprietary cloud UX; rebuild capabilities clean-room when we take product inspiration.  
- Breaking selectors for upstream mergeability without clear fork policy.

---

## Success looks like

- `npx` / docker path still works for newcomers.  
- A document can stand up OpenClaw **or** Hermes in under an hour.  
- Grok TTS (e.g. primary agent voices such as `sal`) is a settings-panel selection with tests.  
- Nightly/weekly radar file updates and optionally opens a draft PR when a new provider appears.  
- Contributors open PRs against clear ARCHITECTURE layers.

---

## Relationship to Bartok tools

| Asset | Role |
|-------|------|
| `~/clawd/tools/grok-audio/` | Existing Grok STT/TTS/realtime scaffolding |
| OpenClaw gateway | Primary local agent runtime (historical default) |
| Hermes | Parallel TOL runtime — must get equal-class docs + env bridges |
| Bartok Design | Visual system for canvas/pages when we want brand-grade UI |

---

*"Talk less typed prompt, show more working canvas."*

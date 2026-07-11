# Hermes gateway pairing (draft — implement with adapter PRs)

OpenVoiceUI historically assumes **OpenClaw**. Bartok9 track: first-class **Hermes** as well.

## Env matrix (sketch)

| Concern | OpenClaw (classic) | Hermes (target) |
|---------|--------------------|-----------------|
| Gateway WS | `CLAWDBOT_GATEWAY_URL` / openclaw defaults | Hermes gateway URL (document version) |
| Auth | `CLAWDBOT_AUTH_TOKEN` | Hermes token / API key env |
| Workspace / canvas | shared `canvas-pages` volume | map Hermes workspace/canvas path |
| Coding CLI | COORD with openclaw coding setting | Hermes tool surface / coding agent |
| Skills | OpenClaw skills | Hermes skills hub paths |

## Operator steps (target UX)

1. Run Hermes gateway locally with LAN bind if Docker-split.  
2. Copy token into OpenVoiceUI `.env`.  
3. `scripts/check-runtime.sh` should print `runtime=hermes` and green checks.  
4. Voice session → agent reply → TTS.

Until the adapter lands, keep OpenClaw as default and treat Hermes as **documented intent** in VISION.

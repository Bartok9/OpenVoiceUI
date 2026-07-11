---
name: orient-openvoiceui
description: >
  Orient to OpenVoiceUI (Bartok9 fork of MCERQUA). Read dual-agent entry files
  and map install/test/Grok TTS paths before changing anything.
---

# Orient — OpenVoiceUI

1. Read `llms.txt`, then `AGENTS.md`, then `SOUL.md`, then `README.md`.
2. Note upstream MIT parent: MCERQUA/OpenVoiceUI.
3. Grok TTS: `tts_providers/grok_provider.py` (requires `XAI_API_KEY`).
4. Smoke: `pytest -q tests/test_grok_tts_provider.py`.
5. Do not commit secrets.

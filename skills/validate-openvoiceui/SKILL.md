---
name: validate-openvoiceui
description: >
  Validate OpenVoiceUI dual-agent surfaces and Grok TTS unit tests.
---

# Validate — OpenVoiceUI

```bash
set -e
test -f SOUL.md && test -f AGENTS.md && test -f llms.txt && test -f DUAL_AGENT_CHECKLIST.md
pytest -q tests/test_grok_tts_provider.py
bash scripts/check-runtime.sh
```

Exit non-zero if dual files missing.

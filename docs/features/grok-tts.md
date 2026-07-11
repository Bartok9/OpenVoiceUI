# Grok / xAI TTS

Cloud text-to-speech via xAI (`POST https://api.x.ai/v1/tts`).

## Enable

1. Get an API key from [console.x.ai](https://console.x.ai/team/default/api-keys).
2. Set in `.env`:

```bash
XAI_API_KEY=your-xai-api-key
```

3. Select provider id **`grok`** in admin Provider Config, or call:

```python
from tts_providers import get_provider

provider = get_provider("grok")
audio_mp3 = provider.generate_speech(
    "Hello from OpenVoiceUI.",
    voice="eve",
    language="en",
)
```

## Request shape

| Field | Required | Notes |
|-------|----------|--------|
| `text` | yes | Max 15,000 chars; [speech tags](https://docs.x.ai/developers/model-capabilities/audio/text-to-speech#speech-tags) supported |
| `voice_id` | no | Default **`eve`** |
| `language` | yes in API; we default **`en`** | BCP-47 or `auto` |

Optional: `speed` (0.7–1.5), `output_format`, `text_normalization`.

## Voices (agents)

Documented public roster shipped in-repo (non-exhaustive; live list via `GET /v1/tts/voices`):

- **`eve`** — default for agents and UI
- **`ara`**, **`rex`**, **`sal`**, **`leo`**

Do **not** commit private Team custom voice IDs into the repository. Operators may pass clone IDs at runtime after creating them in console / Custom Voices API.

## Registry adapter

- Canonical: `tts_providers/grok_provider.py` (`GrokProvider`)
- ADR registry: `providers/tts/grok_provider.py` (`GrokTTSProvider`, id `grok`)
- Config metadata: `tts_providers/providers_config.json` → `providers.grok`

## Ops notes

- Response body is **raw audio** (default MP3 24 kHz / 128 kbps) unless `with_timestamps` is used (JSON — not used by the default provider path).
- Health signal: list voices endpoint when the key is set.
- Official docs: [Text to Speech](https://docs.x.ai/developers/model-capabilities/audio/text-to-speech)

## Tests

```bash
pytest -q tests/test_grok_tts_provider.py
```

Mocks only — no live xAI network in CI.

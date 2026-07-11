# Grok / xAI STT

Cloud speech-to-text via xAI (`POST https://api.x.ai/v1/stt`).

**Implementation:** `providers/stt/grok_provider.py` (`GrokSTTProvider`, registry id **`grok`**).

Higher-level: [VISION.md](https://github.com/MCERQUA/OpenVoiceUI/blob/main/VISION.md) · [ARCHITECTURE.md](https://github.com/MCERQUA/OpenVoiceUI/blob/main/ARCHITECTURE.md) · [SECURITY.md](https://github.com/MCERQUA/OpenVoiceUI/blob/main/SECURITY.md) (env-only keys).

## Enable

```bash
export XAI_API_KEY=your-xai-api-key
pytest -q tests/test_grok_stt_provider.py
```

```python
from providers.stt.grok_provider import GrokSTTProvider

stt = GrokSTTProvider()
result = stt.transcribe(open("clip.wav", "rb").read(), language="en", filename="clip.wav")
print(result.text)
```

## Request shape

Multipart form (xAI requires **`file` last**):

| Field | Notes |
|-------|--------|
| `file` or `url` | One required — we send `file` from bytes |
| `language` | Formatting / ITN when `format=true` |
| `format` | Inverse text normalization (default on in our provider) |
| `keyterm` | Repeatable bias terms |
| `diarize` / `filler_words` | Optional |

Official docs: [Speech to Text](https://docs.x.ai/developers/model-capabilities/audio/speech-to-text)

Live streaming WS is documented at `wss://api.x.ai/v1/stt` (not shipped in this unary provider; Pair with your own binary frame uploader or the experimental realtime bridge).

## Security

- **Keys:** `XAI_API_KEY` in process env only — never commit, never browser-side.
- Tests mock HTTP; no live xAI in CI.

# Cursor next pass — OpenVoiceUI (post docs #1 + Grok TTS #2)

**Public fork of MCERQUA/OpenVoiceUI** · **No real API keys in tree · always env-only**

## Privacy / safety (already checked)
- No XAI live keys; docs use placeholders  
- Do **not** commit `.env`, Christmas-morning tokens, Telegram IDs, Alice/Daniel private data  
- Replace or clearly label sample phones in docs if they look real (e.g. routes/transcripts.py examples)

## PR A — Grok TTS stability + docs polish
1. Ensure both provider entrypoints (providers/tts + tts_providers) stay in sync or document single source of truth.  
2. Unit tests: missing key, HTTP error path, voice_id default eve, content-type audio.  
3. Docs: quick-start for Grok-only TTS (5 lines), link VISION/ARCHITECTURE.  
4. `scripts/check-runtime.sh` self-explanatory + documents :exit 0 without keys.  
5. Radar: ensure `scripts/voice_tech_radar.py --help` and cron-less manual regen instructions.

## PR B — Docs + security hygiene
1. SECURITY.md slice: never commit XAI_API_KEY; use .env.example only.  
2. Scrub any final real-looking sample PII in docs (upstream samples ok if marked EXAMPLE).  
3. CONTRIBUTING.md for dual-agent (OpenClaw + Hermes) already started — plum complete if incomplete.  
4. Fix any flaky tests from #2.

## PR C — optional product
- Feature flag wiring in config/default.yaml for `tts.provider: grok` documented  
- Health endpoint reports provider configured vs missing key (no key leak)

```bash
pytest -q tests/test_grok_tts_provider.py
XAI_API_KEY= pytest -q  # must not hang / not print secrets
```

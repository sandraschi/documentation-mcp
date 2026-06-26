# Google AI MCP — Central project documentation

**Repo path:** D:/Dev/repos/google-ai-mcp
**Status:** active — FastMCP 3.2 gateway for Google AI cloud services + local LeWM bridge
**Ports:** 11014 (backend) / 11015 (frontend)

## Services

- **Gemini Chat** (google-genai, GOOGLE_API_KEY)
- **Nano Banana Image** (google-genai, GOOGLE_API_KEY)
- **Veo Video** (Vertex AI, GOOGLE_CLOUD_PROJECT)
- **Lyria Music** (Vertex global, GOOGLE_CLOUD_PROJECT)
- **Gemini TTS / Live** (google-genai, GOOGLE_API_KEY)
- **Text Embeddings** (google-genai, GOOGLE_API_KEY)
- **LeWorldModel bridge** (proxied to lewm-mcp port 10927)

## MCP Tools (10)

google_ai_chat, google_ai_image, google_ai_video, google_ai_music,
google_ai_speech, google_ai_embeddings, google_ai_world, google_ai_status,
show_google_ai_status_card

## Tests

- 17 pytest backend tests
- 9 Playwright E2E tests
- Automated via just e2e (playwright-audit.ps1)

## Related docs

- Port registry: operations/WEBAPP_PORTS.md
- LeWM integration: projects/lewm-mcp/README.md

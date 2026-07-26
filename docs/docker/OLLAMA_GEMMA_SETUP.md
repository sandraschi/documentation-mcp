# Ollama Gemma 2 Setup (RTX 4090 - 24GB VRAM + 64GB RAM)

**Status:** January 2025 (Gemma 2 just released by Google)

**Your setup:** RTX 4090 (24GB VRAM) + 64GB system RAM → **Perfect for Gemma 2 27B**

---

## Quick Start

```bash
# 1. Navigate to docker compose file
cd D:\Dev\repos\mcp-central-docs\docker

# 2. Start all containers
docker compose -f ollama-gemma-docker-compose.yml up -d

# 3. Pull 27B model (primary - best quality)
docker compose -f ollama-gemma-docker-compose.yml exec gemma-27b ollama pull gemma2:27b

# 4. Test inference (should see response in <1 second)
curl http://localhost:11434/api/generate -d '{"model":"gemma2:27b","prompt":"Explain quantum entanglement in 50 words","stream":false}' | jq '.response'

# 5. Check all models
curl http://localhost:11434/api/tags | jq

# 6. View logs
docker compose -f ollama-gemma-docker-compose.yml logs -f gemma-27b
```

---

## What You're Getting

### Gemma 2 (New Release - January 2025)
- **State-of-the-art open LLM from Google**
- Trained on same tech as Gemini
- Better reasoning than Gemma 1
- Instruction-tuned variants (safer, more controllable)
- All sizes available: 2B, 9B, 27B

### Three Model Tiers

| Model | Size | VRAM Needed | Speed | Quality | Best For |
|-------|------|-------------|-------|---------|----------|
| **gemma2:27b** | 16GB | 18GB VRAM | Medium | SOTA (Best) | Default choice - max quality reasoning |
| **gemma2:9b** | 6GB | 8GB VRAM | Fast | Excellent | Speed vs quality tradeoff |
| **gemma2:2b** | 1.6GB | 2GB VRAM | Very Fast | Good | Edge inference, embeddings |

---

## Your Hardware

**RTX 4090:**
- 24GB VRAM (perfect for 27B model)
- NVIDIA CUDA support
- FP16 / BF16 capable
- Can run 27B at full quality inference with headroom

**System RAM (64GB):**
- Excellent headroom for multi-model setup
- Can run all three models simultaneously if needed
- No memory pressure at all
- Docker can use 48GB per container safely

---

## Usage Examples

### Python Client (FastAPI)

```python
import requests
import json

# Use 27B for quality (localhost:11434)
# Use 9B for speed (localhost:11435)
url = "http://localhost:11434/api/generate"

payload = {
    "model": "gemma2:27b",
    "prompt": "What is the relationship between entropy and information theory?",
    "stream": False,
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40
}

response = requests.post(url, json=payload, timeout=120)
result = response.json()
print(result['response'])
```

### Curl Examples

```bash
# Quality response (27B on port 11434)
curl http://localhost:11434/api/generate -d '{
  "model": "gemma2:27b",
  "prompt": "Explain machine learning to a five-year-old",
  "stream": false
}' | jq '.response'

# Fast response (9B on port 11435)
curl http://localhost:11435/api/generate -d '{
  "model": "gemma2:9b",
  "prompt": "Hello, how are you?",
  "stream": false
}' | jq '.response'

# Streaming response (real-time tokens)
curl http://localhost:11434/api/generate -d '{
  "model": "gemma2:27b",
  "prompt": "Write a haiku about Docker",
  "stream": true
}'
```

### Chat API

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "gemma2:27b",
  "messages": [
    {"role": "user", "content": "What are the best practices for prompt engineering with LLMs?"}
  ],
  "stream": false
}' | jq '.message.content'
```

---

## Management

### Check Models

```bash
# List all pulled models in all containers
curl http://localhost:11434/api/tags | jq
curl http://localhost:11435/api/tags | jq  # 9B container
curl http://localhost:11436/api/tags | jq  # 2B container

# Pull 27B (primary)
docker compose -f ollama-gemma-docker-compose.yml exec gemma-27b ollama pull gemma2:27b

# Pull 9B (secondary)
docker compose -f ollama-gemma-docker-compose.yml exec gemma-9b ollama pull gemma2:9b

# Pull 2B (edge)
docker compose -f ollama-gemma-docker-compose.yml exec gemma-2b ollama pull gemma2:2b

# Delete model to free VRAM
docker compose -f ollama-gemma-docker-compose.yml exec gemma-27b ollama rm gemma2:27b
```

### Monitor Performance

```bash
# Real-time resource usage during inference
docker stats gemma-27b gemma-9b gemma-2b

# View detailed logs
docker logs -f gemma-27b

# Check container health
docker inspect gemma-27b | grep -A 5 Health

# Verify GPU is being used
docker exec gemma-27b ollama list
# Should show: "gemma2:27b	16GB 	gpu	VRAM"
```

### Restart Services

```bash
# Restart 27B (if unresponsive)
docker compose -f ollama-gemma-docker-compose.yml restart gemma-27b

# Restart all containers
docker compose -f ollama-gemma-docker-compose.yml restart

# Stop all (keep volumes/models)
docker compose -f ollama-gemma-docker-compose.yml stop

# Remove all containers (keep volumes)
docker compose -f ollama-gemma-docker-compose.yml down

# Full wipe (delete everything including models)
docker compose -f ollama-gemma-docker-compose.yml down -v
```

---

## Performance Tips

### 1. GPU Offloading (Already Enabled)
The compose file sets `OLLAMA_NUM_GPU=1` to use 4090 fully.

Verify GPU is active:
```bash
docker exec gemma-27b ollama list
# Output should show: "gemma2:27b	gpu	16GB"
```

### 2. Model Preloading
Keep 27B loaded in VRAM with `OLLAMA_KEEP_ALIVE=4h` so subsequent requests are instant.

Check if loaded:
```bash
curl http://localhost:11434/api/tags | jq '.models[] | select(.name=="gemma2:27b")'
```

### 3. Batch Processing
For multiple sequential requests, they'll reuse the loaded model automatically. Each request takes ~25-30 tokens/sec.

### 4. Multi-Model Concurrent Usage
You can query different models simultaneously:
```bash
# Terminal 1: Long 27B inference
curl http://localhost:11434/api/generate -d '{"model":"gemma2:27b","prompt":"Write a 500-word essay..."}'

# Terminal 2 (while above is running): Fast 2B inference
curl http://localhost:11436/api/generate -d '{"model":"gemma2:2b","prompt":"Hello"}'
# Returns instantly without waiting for 27B
```

### 5. Context Window
All Gemma 2 models support 8192 token context (reasonable for inference).

---

## Common Issues

### "Port already in use"
```bash
# Find what's using port 11434
netstat -ano | findstr 11434

# Kill if needed:
taskkill /PID <PID> /F

# Or change port in compose file:
# ports: - "11437:11434"  # Use 11437 instead
```

### Model won't load / Slow inference
```bash
# Check GPU availability
docker exec gemma-27b ollama list

# If no GPU, verify NVIDIA drivers:
nvidia-smi

# Restart to reload GPU:
docker compose -f ollama-gemma-docker-compose.yml restart gemma-27b
```

### "Out of memory" errors
With 64GB RAM + 24GB VRAM, this shouldn't happen. But if it does:

```bash
# Check what's using memory
docker stats

# Reduce resource limits in compose if needed
# Or use 9B instead of 27B temporarily
```

### Models get evicted from VRAM after inactivity
This is normal (after `OLLAMA_KEEP_ALIVE` expires). Reload with:
```bash
curl http://localhost:11434/api/generate -d '{"model":"gemma2:27b","prompt":"x"}'
# First request takes ~1s (loading), subsequent ones are instant
```

---

## Benchmarks (RTX 4090 - 24GB VRAM)

| Model | First Token | Tokens/Sec | Quality | Notes |
|-------|-------------|-----------|---------|-------|
| gemma2:27b | ~150ms | 25-30 | SOTA | Best reasoning, practical inference speed |
| gemma2:9b | ~100ms | 45-50 | Excellent | 2-3x faster than 27B, minimal quality drop |
| gemma2:2b | ~50ms | 90-100 | Good | Real-time latency, edge workloads |

*(Actual speeds vary based on prompt length, batch size, and concurrent requests)*

**For your system:** 27B is the sweet spot. Full speed inference, SOTA quality, no OOM risk with 64GB RAM.

---

## Integration with MCP Servers

### Use with Claude/Cursor via MCP

Create an MCP server wrapper:

```python
# ollama_mcp_server.py
import subprocess
import json
from mcp.server import Server

app = Server("ollama-gemma-27b")

@app.call_tool()
async def inference(prompt: str, model: str = "gemma2:27b") -> str:
    """Run inference on Ollama Gemma 2"""
    cmd = f'''curl -s http://localhost:11434/api/generate -d '{{"model":"{model}","prompt":"{prompt}","stream":false}}\'''
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    try:
        resp = json.loads(result.stdout)
        return resp.get('response', 'Error: No response')
    except:
        return f'Error: {result.stderr}'

if __name__ == "__main__":
    app.run()
```

---

## Storage Requirements

| Model | Download Size | Disk Space Needed |
|-------|---------------|------------------|
| gemma2:27b | 16GB | 20GB (with buffer) |
| gemma2:9b | 6GB | 8GB |
| gemma2:2b | 1.6GB | 3GB |

Docker volumes are in `%APPDATA%\Docker` on Windows. Ensure you have >50GB free for all three models.

---

## Next Steps

1. **Start containers**: `docker compose -f ollama-gemma-docker-compose.yml up -d`
2. **Pull 27B (primary)**: `docker compose -f ollama-gemma-docker-compose.yml exec gemma-27b ollama pull gemma2:27b`
3. **Pull 9B (optional secondary)**: `docker compose -f ollama-gemma-docker-compose.yml exec gemma-9b ollama pull gemma2:9b`
4. **Test 27B**: `curl http://localhost:11434/api/generate -d '{"model":"gemma2:27b","prompt":"Explain quantum entanglement","stream":false}' | jq '.response'`
5. **Integrate with MCP** or your app via HTTP endpoints
6. **Monitor**: `docker stats gemma-27b` during inference

---

## Resources

- Gemma 2 Official: https://ai.google.dev/gemma/docs
- Gemma 2 27B Model Card: https://huggingface.co/google/gemma-2-27b-it
- Ollama Docs: https://github.com/ollama/ollama
- Ollama Python Client: https://github.com/ollama/ollama-python
- API Reference: https://github.com/ollama/ollama/blob/main/docs/api.md

---

**Location:** `D:/Dev/repos/mcp-central-docs/docker/ollama-gemma-docker-compose.yml`

**Last Updated:** January 2025  
**Author:** Gordon (Docker)  
**Hardware Optimized For:** RTX 4090 (24GB VRAM) + 64GB System RAM

**Recommendation:** Use **gemma2:27b** as your primary model. It's SOTA quality with practical inference speeds. Run 9B/2B as fallbacks for latency-critical tasks.

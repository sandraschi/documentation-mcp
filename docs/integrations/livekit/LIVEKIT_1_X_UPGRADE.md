# LiveKit Agents 1.x Upgrade Guide

This document outlines the major changes in the **LiveKit Agents 1.0 (Python SDK)** release and how to leverage the new features in our architecture.

## 1. Core Architecture Changes

### Unified Agent Interface
The specialized `VoicePipelineAgent` and `MultimodalAgent` classes from 0.x are now merged into a unified `Agent` (and `AgentSession`) system. This allows for a more flexible orchestrator that handles speech-to-speech, pipelined, and multimodal models under one interface.

### Worker -> AgentServer
The `Worker` class has been renamed to `AgentServer`. While `WorkerOptions` remains for backward compatibility in some CLI wrappers, the underlying architecture has moved to a more robust "server" model.

### LLM Streaming Interface
The 0.x `__aiter__` pattern for custom LLMs is deprecated. 1.x uses `LLMStream._run()` as a coroutine that pushes chunks to an internal channel.

## 2. New Features & Patterns

### Simplified Tool Definition
No more `llm.FunctionContext` boilerplate. Use the `@llm.function_tool` decorator directly on your logic methods.

```python
@assistant.function_tool
async def control_iot_device(state: bool):
    """Control local smart home devices."""
    # Logic here
    return f"Device set to {state}"
```

### Enhanced Chat Context Management
Context management is now more robust. Use `agent.update_chat_ctx()` instead of manually modifying list indices.

### Native Text Input Handling
Agents 1.x automatically receives text input from the `lk.chat` topic, enabling seamless hybrid (voice + text) interaction without additional `ChatManager` configuration.

## 3. Why We Need These Features

### "Local Mode" Efficiency
The unified interface simplifies our "Local Mode" (Ollama/Whisper/Piper) significantly, as the same orchestration logic can handle different plugin substrates without switching agent classes.

### Industrial Precision
The move to `LLMStream._run()` allows for better error handling and "Reductionist" logging during the generation phase, reducing "Ontological Drift" in the SOTA pipeline.

### Lower Latency
1.x features optimized turn detection and improved VAD integration, critical for the high-intensity interactions required by AG-Visio.

---

**Status:** Draft / Research Complete
**Integration:** Update `agent.py` and `LIVEKIT_INTEGRATION_GUIDE.md` to follow these patterns.

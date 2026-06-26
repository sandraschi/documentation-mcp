# AI/LLM Integration Pattern

**Last Updated:** 2025-12-29

**Pattern for integrating AI/LLM capabilities into MCP servers and web applications**

---

## Overview

This pattern describes how to integrate AI/LLM functionality into applications using the `local-llm-mcp` server, supporting multiple providers (Ollama, LM Studio, OpenAI, Anthropic, Google).

**Reference Implementation:** `robotics-webapp` - Full AI/LLM management interface with chatbot, model management, and personality system.

---

## Architecture

### LLM Integration Stack

```
┌─────────────────────────────────────┐
│   Frontend (React)                  │
│   - Chatbot Interface               │
│   - Model Management UI             │
│   - Settings Configuration          │
└──────────────┬──────────────────────┘
               │ HTTP API
┌──────────────▼──────────────────────┐
│   Backend API (FastAPI)             │
│   - LLM Service Layer               │
│   - Personality Management          │
│   - Model State Tracking            │
└──────────────┬──────────────────────┘
               │ HTTP API
┌──────────────▼──────────────────────┐
│   Local LLM MCP Server              │
│   - Provider Abstraction            │
│   - Model Management                │
│   - Generation Engine               │
└──────────────┬──────────────────────┘
               │ Provider APIs
┌──────────────▼──────────────────────┐
│   LLM Providers                     │
│   - Ollama (local)                  │
│   - LM Studio (local)               │
│   - OpenAI (cloud)                  │
│   - Anthropic (cloud)               │
│   - Google AI (cloud)               │
└─────────────────────────────────────┘
```

---

## Components

### 1. Local LLM MCP Server

The `local-llm-mcp` server provides unified access to all LLM providers:

**Portmanteau Tools:**
- `llm_health` - Health checks and system info
- `llm_models` - Model management (list, load, unload, pull)
- `llm_generation` - Text generation and chat completion
- `llm_multimodal` - Image/audio processing (future)
- `llm_finetuning` - Model fine-tuning (future)

**Example Tool Call:**

```python
# List Ollama models
result = await mcp_client.call_tool(
    'local_llm',
    'llm_models',
    {
        'operation': 'ollama_list'
    }
)

# Load a model
result = await mcp_client.call_tool(
    'local_llm',
    'llm_models',
    {
        'operation': 'ollama_load',
        'model_id': 'llama3'
    }
)

# Generate text
result = await mcp_client.call_tool(
    'local_llm',
    'llm_generation',
    {
        'operation': 'generate',
        'model_id': 'llama3',
        'prompt': 'Explain quantum computing',
        'temperature': 0.7,
        'max_tokens': 500
    }
)
```

### 2. Backend LLM Service

Service layer for LLM operations:

```python
# backend/llm_service.py
from backend.mcp_client import mcp_client
from datetime import datetime

class LLMService:
    def __init__(self):
        self.active_models: dict[str, dict] = {}
        self.personalities = {
            'assistant': {
                'name': 'Assistant',
                'system_prompt': 'You are a helpful, harmless, honest assistant.',
                'temperature': 0.7,
                'max_tokens': 2000
            },
            'robotics_expert': {
                'name': 'Robotics Expert',
                'system_prompt': 'You are an expert in robotics and automation...',
                'temperature': 0.6,
                'max_tokens': 2000
            }
            # ... more personalities
        }

    async def list_models(self, provider: str = "all") -> list[dict]:
        """List available models"""
        result = await mcp_client.call_tool(
            'local_llm',
            'llm_models',
            {'operation': f'{provider}_list'}
        )
        return result.get('data', {}).get('models', [])

    async def load_model(self, model_id: str, provider: str) -> dict:
        """Load a model for inference"""
        result = await mcp_client.call_tool(
            'local_llm',
            'llm_models',
            {
                'operation': f'{provider}_load',
                'model_id': model_id
            }
        )
        if result.get('success'):
            self.active_models[model_id] = {
                'model_id': model_id,
                'provider': provider,
                'loaded_at': datetime.now().isoformat()
            }
        return result

    async def chat_completion(
        self,
        model_id: str,
        messages: list[dict],
        personality: str = 'assistant',
        **kwargs
    ) -> dict:
        """Chat completion with personality"""
        personality_config = self.personalities.get(personality, self.personalities['assistant'])
        
        # Prepend system message with personality
        system_message = {
            'role': 'system',
            'content': personality_config['system_prompt']
        }
        messages_with_personality = [system_message] + messages

        result = await mcp_client.call_tool(
            'local_llm',
            'llm_generation',
            {
                'operation': 'chat',
                'model_id': model_id,
                'messages': messages_with_personality,
                'temperature': kwargs.get('temperature', personality_config['temperature']),
                'max_tokens': kwargs.get('max_tokens', personality_config['max_tokens'])
            }
        )
        return result
```

### 3. Frontend LLM Service

TypeScript service for frontend:

```typescript
// src/services/llmService.ts
interface LLMModel {
  id: string
  name: string
  provider: string
  context_length?: number
  max_tokens?: number
  description?: string
}

interface ChatMessage {
  role: 'user' | 'assistant' | 'system'
  content: string
}

interface Personality {
  id: string
  name: string
  description: string
  system_prompt: string
  temperature: number
  max_tokens: number
}

class LLMService {
  private baseUrl: string

  constructor(baseUrl: string = 'http://localhost:8354') {
    this.baseUrl = baseUrl
  }

  async listModels(provider: string = 'all'): Promise<LLMModel[]> {
    const response = await fetch(
      `${this.baseUrl}/api/llm/models?provider=${provider}`
    )
    const data = await response.json()
    return data.models || []
  }

  async loadModel(modelId: string, provider: string): Promise<any> {
    const response = await fetch(
      `${this.baseUrl}/api/llm/models/${modelId}/load`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ provider })
      }
    )
    return response.json()
  }

  async chatCompletion(
    modelId: string,
    messages: ChatMessage[],
    personality: string = 'assistant',
    temperature?: number,
    maxTokens?: number
  ): Promise<any> {
    const response = await fetch(
      `${this.baseUrl}/api/llm/chat`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model_id: modelId,
          messages,
          personality,
          temperature,
          max_tokens: maxTokens
        })
      }
    )
    return response.json()
  }

  async getPersonalities(): Promise<Personality[]> {
    const response = await fetch(`${this.baseUrl}/api/llm/personalities`)
    const data = await response.json()
    return data.personalities || []
  }
}

export default new LLMService()
```

### 4. Chatbot Component

React chatbot interface:

```typescript
// src/components/ChatbotModal.tsx
import { useState, useCallback } from 'react'
import llmService from '../services/llmService'

interface Props {
  defaultModelId?: string
  onClose: () => void
}

export default function ChatbotModal({ defaultModelId, onClose }: Props) {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [selectedModel, setSelectedModel] = useState(defaultModelId || '')
  const [selectedPersonality, setSelectedPersonality] = useState('assistant')
  const [loading, setLoading] = useState(false)
  const [models, setModels] = useState<LLMModel[]>([])
  const [personalities, setPersonalities] = useState<Personality[]>([])

  useEffect(() => {
    loadModels()
    loadPersonalities()
  }, [])

  const sendMessage = useCallback(async () => {
    if (!input.trim() || !selectedModel) return

    const userMessage: ChatMessage = { role: 'user', content: input }
    const newMessages = [...messages, userMessage]
    setMessages(newMessages)
    setInput('')
    setLoading(true)

    try {
      const result = await llmService.chatCompletion(
        selectedModel,
        newMessages,
        selectedPersonality
      )

      if (result.success) {
        const assistantMessage: ChatMessage = {
          role: 'assistant',
          content: result.data.content || result.data.text
        }
        setMessages([...newMessages, assistantMessage])
      } else {
        // Handle error
        console.error('Chat error:', result.error)
      }
    } finally {
      setLoading(false)
    }
  }, [input, messages, selectedModel, selectedPersonality])

  return (
    <div className="chatbot-modal">
      {/* Model and personality selectors */}
      {/* Message history */}
      {/* Input field */}
      {/* Send button */}
    </div>
  )
}
```

---

## Key Features

### 1. Multi-Provider Support

- **Ollama**: Local models, fast inference
- **LM Studio**: Local models, GUI management
- **OpenAI**: Cloud models (GPT-4, GPT-3.5)
- **Anthropic**: Cloud models (Claude Opus, Sonnet, Haiku)
- **Google AI**: Cloud models (Gemini Pro, Ultra)

### 2. Model Management

- **List Models**: Query available models per provider
- **Load/Unload**: Manage model memory
- **Pull Models**: Download models (Ollama)
- **Active Tracking**: Monitor loaded models

### 3. Personality System

- **Built-in Personalities**: 6+ predefined personalities
- **Custom Personalities**: User-defined system prompts
- **Temperature Control**: Per-personality creativity settings
- **Token Limits**: Per-personality response length

### 4. Chat Interface

- **Message History**: Persistent conversation context
- **Model Selection**: Switch models on the fly
- **Personality Selection**: Change AI behavior
- **Settings Panel**: Configure temperature, tokens, etc.

---

## Configuration

### Backend Environment Variables

```env
# Local LLM MCP Server
LOCAL_LLM_MCP_URL=http://localhost:8007

# Provider URLs (optional, defaults shown)
OLLAMA_BASE_URL=http://localhost:11434
LM_STUDIO_BASE_URL=http://localhost:1234

# API Keys (optional, for cloud providers)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...
```

### Frontend Settings

```typescript
// Settings stored in localStorage
interface LLMSettings {
  defaultModel: string
  defaultPersonality: string
  temperature: number
  maxTokens: number
  ollamaUrl: string
  lmStudioUrl: string
  openaiApiKey?: string
  anthropicApiKey?: string
  googleApiKey?: string
}
```

---

## Best Practices

### 1. Model Loading

- Load models on-demand to save memory
- Unload models when not in use
- Track active models to prevent duplicates

### 2. Error Handling

- Handle provider unavailable gracefully
- Show clear error messages for model loading failures
- Fallback to alternative providers when possible

### 3. Performance

- Cache model lists
- Batch model operations
- Use streaming for long responses (future)

### 4. Security

- Never expose API keys in frontend code
- Store API keys securely in backend
- Validate all user inputs
- Rate limit API calls

### 5. User Experience

- Show loading states during model operations
- Display model status (loaded/unloaded)
- Provide clear error messages
- Allow model switching without losing context

---

## Example: Complete Integration

### Backend API Endpoints

```python
# backend/main.py
from fastapi import FastAPI
from backend.llm_service import LLMService

app = FastAPI()
llm_service = LLMService()

@app.get("/api/llm/models")
async def list_models(provider: str = "all"):
    """List available models"""
    models = await llm_service.list_models(provider)
    return {"models": models}

@app.post("/api/llm/models/{model_id}/load")
async def load_model(model_id: str, provider: str):
    """Load a model"""
    result = await llm_service.load_model(model_id, provider)
    return result

@app.post("/api/llm/chat")
async def chat(request: ChatRequest):
    """Chat completion"""
    result = await llm_service.chat_completion(
        request.model_id,
        request.messages,
        request.personality,
        temperature=request.temperature,
        max_tokens=request.max_tokens
    )
    return result
```

### Frontend Page

```typescript
// src/app/ai-llm/page.tsx
export default function AILLMPage() {
  const [models, setModels] = useState<LLMModel[]>([])
  const [activeModels, setActiveModels] = useState<string[]>([])
  const [showChatbot, setShowChatbot] = useState(false)

  useEffect(() => {
    loadModels()
    loadActiveModels()
  }, [])

  const loadModels = async () => {
    const models = await llmService.listModels()
    setModels(models)
  }

  const handleLoadModel = async (modelId: string, provider: string) => {
    const result = await llmService.loadModel(modelId, provider)
    if (result.success) {
      await loadActiveModels()
    }
  }

  return (
    <div>
      <MCPStatusBanner serverName="local_llm" serverDisplayName="Local LLM" />
      
      <h1>AI & LLM Management</h1>
      
      <button onClick={() => setShowChatbot(true)}>
        Open Chatbot
      </button>

      <ModelList
        models={models}
        activeModels={activeModels}
        onLoad={handleLoadModel}
      />

      {showChatbot && (
        <ChatbotModal
          defaultModelId={activeModels[0]}
          onClose={() => setShowChatbot(false)}
        />
      )}
    </div>
  )
}
```

---

## Reference Implementation

**Full Example:** `robotics-webapp`
- Repository: `https://github.com/sandraschi/robotics-webapp`
- AI/LLM Page: `/ai-llm`
- Settings Page: `/settings` (LLM configuration)
- Chatbot Component: `src/components/ChatbotModal.tsx`

**Key Files:**
- `backend/llm_service.py` - Backend LLM service
- `src/services/llmService.ts` - Frontend LLM service
- `src/app/ai-llm/page.tsx` - AI/LLM management page
- `src/components/ChatbotModal.tsx` - Chatbot interface

**Documentation:**
- [AI/LLM Features Guide](../../robotics-webapp/docs/AI_LLM_FEATURES.md)
- [Local LLM MCP Server](../../local-llm-mcp/README.md)

---

## Related Patterns

- [Webapp Integration Pattern](./webapp-integration-pattern.md) - General webapp integration
- [MCP Server Composition Pattern](./mcp-server-composition.md) - Compose multiple MCP servers
- [Portmanteau Pattern](./MCP_PORTMANTEAU_BEST_PRACTICES.md) - Organize tools into families

---

**Last Updated:** 2025-12-29

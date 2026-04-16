# MyVRWorlds

Beautiful React Tailwind VR Worlds Control Center integrating Avatar MCP, Blender MCP, VRChat MCP, Resonite MCP, OSC MCP, Unity3D MCP with ikubaysan dual-STT AI chatbot architecture.

## 🚀 Features

### VR Platform Integrations
- **Avatar MCP**: Real-time avatar creation and animation control
- **Blender MCP**: 3D modeling and rendering integration
- **VRChat MCP**: OSC-based VRChat avatar and world control
- **Resonite MCP**: Session management and Logix scripting
- **OSC MCP**: Open Sound Control protocol handling
- **Unity MCP**: Unity game engine VR development integration

### Revolutionary Voice AI (ikubaysan Architecture)
- **Dual STT Pipeline**: Sphinx wake-word detection + Google Cloud accurate transcription
- **Multi-Provider LLM Support**: Local (Ollama, LM Studio) + Cloud (OpenAI, Anthropic, Gemini)
- **Character State Machine**: Wandering → Conversing → Performing Actions
- **Structured AI Responses**: TYPE_NORMAL, TYPE_ENDING, TYPE_YES, TYPE_NO, TYPE_CMD
- **Physical Embodiment**: Voice-controlled VR avatar behaviors

### Modern Web Interface
- **React 18** with TypeScript for type safety
- **Tailwind CSS** for beautiful, responsive design
- **Radix UI** components for accessibility
- **React Query** for efficient data fetching
- **Dark theme** optimized for VR control interfaces

## 🔌 Port Management System

MyVRWorlds is part of the Sandraschi port management system. All web applications run on ports above 11000 to avoid system conflicts.

### Current Port Assignments
- **MyVRWorlds**: 11101 (VR MCP Control Center)
- **Advanced Memory MCP Frontend**: 11102 (planned)
- **OCR Webapp**: 11103
- **Robotics Webapp**: 11104
- **Home Automation**: 11105
- **Calibre Plus**: 11106
- **Plex Plus**: 11107
- **Immich Plus**: 11108
- **Document Viewer**: 11109
- **Video Generator**: 11110
- **Voice AI Suite**: 11111
- **Research Assistant**: 11112
- **Code Assistant**: 11113
- **Character Conversation**: 11114
- **Gemini Tools**: 11115
- **Bob & Alice**: 11116
- **Teams Debate**: 11117

### Port Management Tools
```bash
# Check if a port is available
node scripts/port-manager.js check 11101

# List all assigned ports
node scripts/port-manager.js list

# Assign next available port to new app
node scripts/port-manager.js assign my-new-app

# Validate all port assignments
node scripts/port-manager.js validate

# Update app configuration
node scripts/port-manager.js update myvrworlds status active
```

### Port Assignment Rules
1. All ports must be above 11000
2. Ports 11000-11004 are reserved for system services
3. Port format: 11XXX (where XXX is sequential)
4. Document all changes in `config/ports.json`
5. Use the port manager script for all assignments

## 🏗️ Architecture

### Dual STT Voice Pipeline
```
🎤 Audio Input → Sphinx Wake Detection → Google Cloud Transcription → AI Processing → Voice Response
     ↓              ↓                           ↓                    ↓              ↓
Always-on       Fast keyword               High accuracy        Context-aware    Physical actions
Low CPU         spotting                   transcription        responses        & gestures
```

### Character State Machine
- **WanderingState**: Random movements, wake word listening
- **ConversingState**: Active voice interaction, AI responses
- **PerformingActionState**: Executing movement/gesture commands

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- npm or yarn
- VR MCP servers running (see individual repos)
- **Local LLM Option**: Ollama or LM Studio (recommended for privacy)
- **Cloud LLM Option**: OpenAI, Anthropic, or Google API keys

### Local LLM Setup (Recommended)

**Option 1: Ollama (Most Popular)**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a conversational model
ollama pull llama2

# Start Ollama server (runs automatically)
ollama serve
```

**Option 2: LM Studio (User-Friendly)**
```bash
# Download from https://lmstudio.ai/
# Load any GGUF model
# Start local server (default: localhost:1234)
```

### Installation
```bash
# Clone the repository
git clone https://github.com/sandraschi/myvrworlds.git
cd myvrworlds

# Install dependencies
npm install

# Start development server (port 11101)
npm run dev
```

### Access the Interface
Open http://localhost:11101 in your browser

**Note**: MyVRWorlds uses port 11101 as part of the Sandraschi port management system. All web applications run on ports 11000+ to avoid conflicts.

### First-Time Setup
1. Go to **Settings** → **LLM Configuration**
2. Choose your preferred LLM provider:
   - **Ollama** (local, private, no API costs)
   - **LM Studio** (local, easy to use)
   - **OpenAI/Anthropic/Gemini** (cloud, requires API keys)
3. Configure your model settings
4. Test the connection
5. Start using voice control in VR!

## 🎯 VR MCP Server Setup

Start the required MCP servers before using the interface:

```bash
# Terminal 1: Avatar MCP
cd ../avatar-mcp && python -m src.avatar_mcp.server

# Terminal 2: VRChat MCP
cd ../vrchat-mcp && python -m src.vrchat_mcp.server

# Terminal 3: OSC MCP
cd ../osc-mcp && python -m src.osc_mcp.server

# ... start other VR MCP servers as needed
```

## 🎙️ Voice Control Features

### Dual STT Architecture
1. **Sphinx Wake Detection**: Always listening for character names ("ringo", "hey ringo")
2. **Google Cloud Transcription**: High-accuracy full conversation processing
3. **AI Response Classification**: Structured responses for avatar behaviors
4. **Physical Actions**: Voice-controlled movements and gestures

### Voice Commands
- **Wake Words**: "ringo", "hey ringo", "listen ringo"
- **Action Commands**: "turn left", "move forward", "stop"
- **Conversation Control**: "bye", "goodbye" to end sessions

## 🎮 Usage Examples

### Basic Voice Interaction
1. Character wanders randomly (listening for wake words)
2. User says "Hey ringo" → Character enters conversation mode
3. Full transcription via Google Cloud STT
4. AI generates contextual response
5. Character performs appropriate gestures/voice response

### Avatar Control
- Real-time blendshape animation
- OSC parameter manipulation
- Gesture recognition and playback
- IK rigging control

### World Management
- VRChat instance joining/leaving
- Resonite session control
- Asset synchronization
- Multi-user coordination

## 🛠️ Development

### Tech Stack
- **Frontend**: React 18, TypeScript, Tailwind CSS
- **UI Components**: Radix UI, Lucide Icons
- **State Management**: React Query, Context API
- **3D Integration**: React Three Fiber (planned)
- **Real-time**: Socket.io, WebRTC
- **Voice Processing**: Web Audio API, MediaRecorder

### Project Structure
```
src/
├── components/
│   ├── ui/                 # Radix UI components
│   └── Layout.tsx          # Main app layout
├── pages/                  # Route components
├── hooks/                  # Custom React hooks
├── lib/                    # Utilities
└── types/                  # TypeScript definitions

docs/
├── integrations/          # MCP server docs
└── README.md              # Main documentation
```

### Available Scripts
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run lint         # Run ESLint
npm run type-check   # Run TypeScript checks
```

## 📚 Documentation

- [Main Documentation](./docs/README.md)
- [Voice Control Integration](./docs/integrations/voice-control.md)
- [VR MCP Server Integrations](./docs/integrations/README.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **ikubaysan** for the revolutionary dual STT architecture
- **Anthropic** for the MCP protocol
- **VR Community** for inspiration and feedback

## 🎯 Roadmap

### Phase 1 (Current)
- ✅ Basic React Tailwind interface
- ✅ VR MCP server integration structure
- ✅ Dual STT voice pipeline implementation
- ✅ Character state machine
- ✅ **Multi-provider LLM support (local + cloud)**

### Phase 2 (Next)
- 🔄 Real-time 3D avatar preview
- 🔄 Multi-character voice interactions
- 🔄 Advanced gesture recognition
- 🔄 World streaming capabilities
- 🔄 Production backend API integration

### Phase 3 (Future)
- 🔄 Neural voice synthesis
- 🔄 Emotion recognition
- 🔄 Multi-language support
- 🔄 Cloud deployment options
- 🔄 Advanced avatar animation blending

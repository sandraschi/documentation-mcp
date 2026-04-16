# The Specialist Council

The Dark App Factory is powered by **19 specialized AI agents**, each with a distinct domain, temperature profile, and validation logic.

## 🛠️ Specialist Matrix

| Agent | Domain | Temperature | Dependency | Key Mission |
| :--- | :--- | :--- | :--- | :--- |
| **Professor** | Skill Battery | 0.2 | None | Seeds domain-specific knowledge. |
| **Plumber** | Backend | 0.15 | Professor | Mandatory `/health` endpoints and async logic. |
| **Sculptor** | Frontend | 0.4 | Professor | Aesthetic delivery (Glassmorphism/Framer). |
| **Registrar** | Infrastructure | 0.1 | None | Docker, requirements, and package.json logic. |
| **Morpheus** | Security | 0.1 | Plumber | Auth, middleware, and encryption protocols. |
| **Nervos** | Heartbeat | 0.2 | None | Sockets, messaging connectors, and status loops. |
| **Amodei** | AI Integration | 0.3 | Plumber | LLM streaming, SSE, and Ollama connections. |
| **Shakespeare** | Copywriting | 0.7 | None | High-creative in-app copy and narratives. |
| **Propagandist** | Distribution | 0.65 | Shakespeare | Platform-specific marketing assets. |

## 🧠 Sophistication Mechanisms

### Context Injection
Specialists are not isolated. Upstream context from dependencies (e.g., `Plumber`'s routes) is injected into downstream specialists (e.g., `Librarian`) to ensure documentation matches code exactly.

### Temperature Tuning
- **Precision Agents (0.1-0.2)**: `Registrar`, `Plumber`, `Morpheus`. Focus on syntax accuracy and security.
- **Creative Agents (0.4-0.7)**: `Sculptor`, `Shakespeare`, `Propagandist`. Focus on aesthetics and engagement.

### Self-Declaration
Specialists can "declare" files. If `Morpheus` detects "auth" in the specs, it automatically injects `auth_middleware.py` and `security_config.py` into the build queue without being explicitly asked.

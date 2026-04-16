# OCR-MCP Project Structure

**Last Updated**: 2026-03-16 (FastMCP 3.1)

## Repository Structure

```
D:\Dev\repos\ocr-mcp\
├── src\ocr_mcp\
│   ├── __init__.py                 # Package initialization
│   ├── server.py                   # FastMCP server implementation
│   ├── core\
│   │   ├── __init__.py
│   │   ├── config.py              # OCR configuration management
│   │   └── backend_manager.py     # Multi-engine OCR orchestration
│   ├── backends\
│   │   ├── __init__.py
│   │   ├── got_ocr_backend.py     # GOT-OCR2.0 integration (legacy)
│   │   ├── deepseek_backend.py    # DeepSeek-OCR implementation
│   │   ├── florence_backend.py    # Florence-2 implementation
│   │   ├── dots_backend.py        # DOTS.OCR implementation
│   │   ├── ppocr_backend.py       # PP-OCRv5 implementation
│   │   ├── qwen_layered_backend.py # Qwen-Image-Layered decomposition
│   │   ├── document_processor.py  # PDF/CBZ processing
│   │   └── scanner\
│   │       ├── __init__.py
│   │       ├── wia_scanner.py     # Windows scanner control
│   │       └── scanner_manager.py # Scanner abstraction layer
│   ├── tools\
│   │   ├── __init__.py
│   │   ├── ocr_tools.py           # Main OCR processing tools
│   │   └── scanner_tools.py       # Scanner control tools
│   └── services\
│       ├── __init__.py
│       └── watch_folder.py        # Automated document monitoring
├── webapp\
│   ├── backend\                    # FastAPI application
│   │   ├── app.py                  # Main API entry point (Singleton Backend)
│   │   └── models.py               # Pydantic data models
│   └── frontend-new\               # Professional React/Next.js UI
│       ├── src\
│       ├── tailwind.config.ts
│       └── next.config.ts
├── scripts\
│   ├── run_webapp.py               # Webapp launcher script
│   └── start_all.bat               # Integrated startup script
├── tests\
├── docs\
│   ├── OCR-MCP_MASTER_PLAN.md     # Development roadmap
│   └── api_reference.md           # Tool documentation
├── pyproject.toml                 # Poetry configuration
├── README.md                      # Main documentation
├── LICENSE                        # MIT License
└── .gitignore                     # Git ignore rules
```

## Core Architecture

### Server Layer (`server.py`)
- **FastMCP 3.1** server: sampling_handler, lifespan, prompts (5), resources (logs, capabilities, skills)
- **Tool registration** for portmanteau tools + agentic_document_workflow
- **Error handling** and logging configuration
- **Lifespan management** for backend manager and sampling handler

### Backend Management (`backend_manager.py`)
- **Engine orchestration** with automatic selection
- **Singleton Pattern**: Managed as a global instance for resource stability and COM context preservation.
- **Fallback handling** when engines fail
- **Configuration management** for all OCR engines

### OCR Backends
Each backend implements a consistent interface:
- `is_available()` - Check if engine can be loaded
- `load_model()` - Initialize the OCR engine
- `process_document()` - Perform OCR on document
- `get_capabilities()` - Return engine-specific features

## Tool Organization

### Portmanteau Pattern Implementation

OCR-MCP uses comprehensive "portmanteau tools" that consolidate related operations:

#### 1. OCR Processing Tools (`ocr_tools.py`)
- **`process_document`**: Single document OCR with auto-backend selection
- **`process_batch_documents`**: Concurrent batch processing
- **`ocr_health_check`**: Backend availability and diagnostics
- **`list_backends`**: Available OCR engines and capabilities

#### 2. Scanner Control Tools (`scanner_tools.py`)
- **`list_scanners`**: Discover available scanner devices
- **`scanner_properties`**: Detailed scanner capabilities
- **`configure_scan`**: Set scanning parameters (DPI, color mode, etc.)
- **`scan_document`**: Perform single document scan
- **`scan_batch`**: Batch scanning with ADF support
- **`preview_scan`**: Preview scanning for positioning

## Configuration System

### Configuration Files
- **`pyproject.toml`**: Poetry dependencies and project metadata
- **Environment variables**: Runtime configuration (API keys, paths)
- **`config.py`**: Pydantic-based configuration validation

### Backend Configuration
Each OCR backend can be configured independently:
```python
@dataclass
class OCRConfig:
    deepseek_enabled: bool = True
    florence_enabled: bool = True
    qwen_layered_enabled: bool = True
    cache_dir: Path = Path.home() / ".ocr_mcp_cache"
    scanner_timeout: int = 30
```

## Data Flow Architecture

### Document Processing Pipeline

1. **Input Reception**: Document uploaded via tool or file path
2. **Format Detection**: Automatic format identification (PDF, CBZ, image)
3. **Pre-processing**: Qwen-Image-Layered decomposition (optional)
4. **Backend Selection**: Auto-select best OCR engine for content
5. **OCR Processing**: Text extraction with layout preservation
6. **Post-processing**: Result formatting and metadata attachment
7. **Output Delivery**: Structured results to client

### Scanner Pipeline

1. **Device Discovery**: WIA scanner enumeration
2. **Configuration**: DPI, color mode, paper size settings
3. **Preview Scan**: Optional positioning verification
4. **Document Scan**: Image acquisition from scanner
5. **Image Processing**: Format conversion and optimization
6. **OCR Integration**: Seamless handoff to OCR pipeline

## Integration Points

### Claude Desktop Integration
- **MCP configuration** in `.cursor\mcp.json`
- **Stdio transport** for reliable communication
- **Tool discovery** and execution
- **Error handling** and user feedback

### Document Format Support

#### Input Formats
- **Images**: JPEG, PNG, TIFF, BMP, WebP
- **Documents**: PDF (with/without text layers)
- **Comics**: CBZ, CBR archives
- **Scanned**: Direct scanner input

#### Output Formats
- **Text**: Plain text extraction
- **Structured**: JSON with layout coordinates
- **Rich**: HTML with visual formatting
- **Metadata**: Document structure and properties

## Error Handling Architecture

### Hierarchical Error Management
1. **Tool Level**: User-friendly error messages
2. **Backend Level**: Engine-specific error handling
3. **System Level**: Logging and diagnostics
4. **Recovery**: Automatic fallback to alternative backends

### Logging Strategy
- **Stderr output** for MCP stdio compatibility
- **Structured logging** with JSON format
- **Performance metrics** collection
- **Debug information** for troubleshooting

## Testing Strategy

### Unit Tests
- **Backend isolation** testing
- **Tool functionality** verification
- **Error condition** handling
- **Configuration** validation

### Integration Tests
- **End-to-end OCR** processing
- **Scanner integration** testing
- **Document pipeline** validation
- **Performance benchmarking**

### Manual Testing
- **Accuracy validation** on real documents
- **Scanner compatibility** testing
- **Edge case handling** verification

---

**Architecture designed for extensibility and performance in OCR workflows.** 🔧📐







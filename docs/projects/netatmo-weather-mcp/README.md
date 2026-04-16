# 🌤️ Netatmo Weather MCP Server

[![FastMCP 3.1.1+.3](https://img.shields.io/badge/FastMCP-3.1.1+.3-blue.svg)](https://github.com/modelcontextprotocol)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI-powered weather monitoring with sampling and predictive analytics for Netatmo weather stations.**

The Netatmo Weather MCP Server provides comprehensive weather monitoring capabilities with advanced AI features including iterative sampling, predictive analytics, anomaly detection, and conversational tool returns. Built with FastMCP 3.1.1+.3 for maximum compatibility with AI assistants.

## ✨ Features

### 🤖 AI-Powered Weather Intelligence
- **Iterative Sampling**: AI-guided weather pattern discovery with continuous refinement
- **Predictive Analytics**: Short-term weather forecasting with confidence scoring
- **Anomaly Detection**: Statistical analysis for unusual weather patterns
- **Pattern Recognition**: Automated identification of weather trends and cycles

### 💬 Conversational AI Interface
- **Context-Aware Responses**: Tools provide conversational context and next-step suggestions
- **Workflow Guidance**: AI suggests optimal sequences of operations
- **Error Recovery**: Helpful hints when operations fail
- **Progress Tracking**: Real-time feedback on long-running operations

### 🔮 Smart Weather Predictions
- **Multi-Modal Forecasting**: Temperature, humidity, pressure, wind, and rain predictions
- **Confidence Scoring**: Each prediction includes reliability metrics
- **Trend Analysis**: Long-term weather pattern analysis and visualization
- **Automation Suggestions**: Smart home integration recommendations based on weather patterns

### 📊 Comprehensive Monitoring
- **Prometheus Metrics**: Performance metrics and health indicators
- **Structured Logging**: JSON-formatted logs with full context
- **Health Checks**: System status and connectivity monitoring
- **Real-Time Dashboards**: Grafana integration for weather visualization

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Netatmo Developer Account ([dev.netatmo.com](https://dev.netatmo.com))
- Netatmo Weather Station

## 🚀 Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

### 📦 Quick Start
Run immediately via `uvx`:
```bash
uvx netatmo-weather-mcp
```

### 🎯 Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "netatmo-weather-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/netatmo-weather-mcp", "run", "netatmo-weather-mcp"]
  }
}
```
### Configuration

1. **Get Netatmo API Credentials:**
   - Visit [dev.netatmo.com](https://dev.netatmo.com) and create an app
   - Note your Client ID and Client Secret

2. **Set Environment Variables:**
   ```bash
   export NETATMO_CLIENT_ID="your_client_id"
   export NETATMO_CLIENT_SECRET="your_client_secret"
   export NETATMO_USERNAME="your_email@domain.com"
   export NETATMO_PASSWORD="your_password"
   ```

3. **Run the Server:**
   ```bash
   netatmo-weather-mcp
   ```

## 🛠️ Usage

### Basic Weather Monitoring

```python
# Discover weather stations
weather_station_management(operation="list")

# Get current weather data
weather_data_operations(operation="current", station_id="70:ee:50:12:34:56")

# Get historical data (last 24 hours)
weather_data_operations(operation="historical", station_id="70:ee:50:12:34:56", timeframe="24h")
```

### AI Sampling & Analysis

```python
# Iterative AI sampling for pattern discovery
ai_weather_sampling(
    sampling_mode="iterative",
    station_id="70:ee:50:12:34:56",
    iterations=5,
    refinement_prompt="focus on temperature patterns"
)

# Predictive sampling for forecasting
ai_weather_sampling(
    sampling_mode="predictive",
    station_id="70:ee:50:12:34:56",
    iterations=3
)

# Anomaly detection
ai_weather_sampling(
    sampling_mode="anomaly",
    station_id="70:ee:50:12:34:56",
    iterations=3
)
```

### Weather Predictions & Automation

```python
# Short-term weather predictions
weather_prediction_engine(
    prediction_type="short_term",
    station_id="70:ee:50:12:34:56",
    forecast_hours=24,
    confidence_threshold=0.8
)

# Trend analysis with automation suggestions
weather_prediction_engine(
    prediction_type="trend_analysis",
    station_id="70:ee:50:12:34:56",
    forecast_hours=168  # 1 week
)
```

## 🏗️ Architecture

### Core Components

```
netatmo-weather-mcp/
├── src/netatmo_weather_mcp/
│   ├── server.py              # FastMCP 3.1.1+.3 server implementation
│   ├── core/
│   │   ├── netatmo_client.py  # Netatmo API client with authentication
│   │   └── exceptions.py      # Custom exception handling
│   ├── tools/
│   │   ├── weather_monitoring.py    # Weather station management
│   │   ├── ai_sampling.py           # AI sampling tools
│   │   └── predictive_analytics.py  # Prediction engine
│   └── sampling/
│       └── weather_sampling.py      # Sampling algorithms
├── mcpb/                    # MCPB packaging
├── monitoring/              # Prometheus & logging config
└── tests/                   # Comprehensive test suite
```

### FastMCP 3.1.1+.3 Features

- **Sampling Method Support**: Advanced AI sampling for creative weather analysis
- **Enhanced Response Patterns**: Conversational tool returns with context
- **Server Lifespan Management**: Proper resource initialization and cleanup
- **Advanced Tool Management**: Portmanteau patterns for consolidated functionality

## 📋 API Reference

### Tools

#### `weather_station_management`
**Portmanteau Rationale**: Consolidates station discovery, status monitoring, and configuration into single interface. Prevents tool explosion while maintaining full weather station management capabilities.

- `operation="list"`: Discover all available weather stations
- `operation="get_info"`: Get detailed station information
- `operation="get_status"`: Check station connectivity and health

#### `weather_data_operations`
**Portmanteau Rationale**: Consolidates current weather retrieval, historical data access, and sampling operations. Prevents tool explosion while enabling comprehensive weather data workflows.

- `operation="current"`: Get real-time weather data
- `operation="historical"`: Retrieve historical weather data
- `operation="sample"`: Generate AI-sampled weather data
- `operation="analyze"`: Analyze weather patterns and trends

#### `ai_weather_sampling`
**Portmanteau Rationale**: Consolidates AI-driven weather sampling, iterative refinement, and predictive workflows. Enables true AI-weather station interaction with sampling-based learning.

- `sampling_mode="iterative"`: AI-guided pattern discovery with refinement
- `sampling_mode="predictive"`: Forecasting-focused sampling
- `sampling_mode="anomaly"`: Statistical anomaly detection

#### `weather_prediction_engine`
**Portmanteau Rationale**: Consolidates weather prediction, trend analysis, and anomaly detection. Provides comprehensive predictive analytics for weather patterns and automation.

- `prediction_type="short_term"`: Short-term weather forecasting
- `prediction_type="trend_analysis"`: Long-term trend analysis
- `prediction_type="anomaly_detection"`: Anomaly prediction and alerting

## 🔧 Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `NETATMO_CLIENT_ID` | Yes | - | Netatmo app client ID |
| `NETATMO_CLIENT_SECRET` | Yes | - | Netatmo app client secret |
| `NETATMO_USERNAME` | Yes | - | Netatmo account email |
| `NETATMO_PASSWORD` | Yes | - | Netatmo account password |
| `NETATMO_SCOPE` | No | `read_station` | API permissions |
| `METRICS_PORT` | No | `9091` | Prometheus metrics port |
| `ENABLE_METRICS` | No | `true` | Enable Prometheus metrics |
| `LOG_LEVEL` | No | `INFO` | Logging level |

### MCP Client Configuration

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "netatmo-weather": {
      "command": "python",
      "args": ["-m", "netatmo_weather_mcp.server"],
      "env": {
        "NETATMO_CLIENT_ID": "your_client_id",
        "NETATMO_CLIENT_SECRET": "your_client_secret",
        "NETATMO_USERNAME": "your_email",
        "NETATMO_PASSWORD": "your_password"
      }
    }
  }
}
```

## 📊 Monitoring & Observability

### Metrics

- **API Performance**: Request count, latency, error rates
- **Weather Data**: Sample counts, data quality scores
- **AI Operations**: Sampling quality, prediction accuracy
- **System Health**: Connection status, resource usage

### Dashboards

- **Weather Station Dashboard**: Real-time weather metrics and trends
- **AI Performance Dashboard**: Sampling and prediction analytics
- **System Health Dashboard**: Server performance and error tracking

### Logging

Structured JSON logs with correlation IDs for full request tracing.

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=netatmo_weather_mcp

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest tests/ai/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastMCP](https://github.com/modelcontextprotocol) for the excellent MCP framework
- [Netatmo](https://dev.netatmo.com) for their comprehensive weather API
- The MCP community for standards and best practices

## 🔗 Links

- [Netatmo Developer Portal](https://dev.netatmo.com)
- [FastMCP Documentation](https://modelcontextprotocol.io)
- [MCP Central Docs](https://github.com/sandra/mcp-central-docs)
- [Weather Station Setup Guide](docs/SETUP.md)

---

**Built with ❤️ for AI-powered weather monitoring**

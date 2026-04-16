# Vienna Live MCP Server

[![Beta](https://img.shields.io/badge/Status-Beta-orange.svg)](https://github.com/sandraschi/vienna-live-mcp)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastMCP](https://img.shields.io/badge/FastMCP-3.1.1++-green.svg)](https://github.com/sugarforever/FastMCP)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive MCP server providing programmatic access to Vienna Life Assistant functionality through consolidated portmanteau tools.

## ðŸŽ¯ Overview

The **vienna-live-mcp** server transforms Vienna Life Assistant into a fully programmable personal assistant. It implements the **Portmanteau Pattern** to organize 63 tools across 5 logical categories, providing clean, discoverable APIs for:

- **Shopping Management** - Store offers, shopping lists, budget tracking
- **Travel Planning** - Transport schedules, trip planning, weather integration
- **Expense Tracking** - Financial management, budget analysis, spending insights
- **Media Management** - Unified access to Plex, Calibre, and Immich libraries
- **Personal Planning** - Todo management, calendar, goals, and productivity tools

## ðŸ—ï¸ Architecture

### Portmanteau Pattern

Each portmanteau provides a cohesive set of tools for a specific domain:

```mermaid
graph TD
    A[Vienna Live MCP Server] --> B[shopping_manager]
    A --> C[travel_manager]
    A --> D[expenses_manager]
    A --> E[media_manager]
    A --> F[planning_manager]

    B --> B1[get_store_offers]
    B --> B2[compare_prices]
    B --> B3[shopping_list_create]

    C --> C1[get_next_tram]
    C --> C2[plan_day_trip]
    C --> C3[get_train_schedule]

    D --> D1[add_expense]
    D --> D2[analyze_spending_patterns]
    D --> D3[set_budget]

    E --> E1[search_plex_library]
    E --> E2[search_calibre_library]
    E --> E3[search_immich_photos]

    F --> F1[create_todo]
    F --> F2[get_productivity_stats]
    F --> F3[set_goal]
```

### Dual Transport Support

The server supports both MCP transports:
- **STDIO Transport**: For integration with MCP clients (Cursor, Claude Desktop, etc.)
- **HTTP Transport**: For direct web API access and web app integration

## ðŸš€ Quick Start

### Prerequisites

- Python 3.11+
- **Database**: SQLite (default, no setup required) or PostgreSQL (optional, for production)
- **Optional External APIs**:
  - Wiener Linien API (Vienna public transport)
  - OpenWeatherMap API (weather data)
  - Currency exchange APIs
  - Ã–BB API (Austrian railways)
  - Plex, Calibre, Immich APIs (media services)

**Note**: The server works with mock data by default. Real API integrations are optional and require API keys.

## ðŸš€ Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

### ðŸ“¦ Quick Start
Run immediately via `uvx`:
```bash
uvx vienna-live-mcp
```

### ðŸŽ¯ Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "vienna-live-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/vienna-live-mcp", "run", "vienna-live-mcp"]
  }
}
```
### Running the Server

**STDIO Mode (MCP Client Integration):**
```bash
python -m vienna_live_mcp.server
```

**HTTP Mode (Direct API Access):**
```bash
python -m vienna_live_mcp.server --transport http --port 8000
```

## ðŸ“š Tool Categories

### ðŸ›ï¸ Shopping Manager (11 Tools)

| Tool | Description |
|------|-------------|
| `get_store_offers` | Get current offers from Spar, Billa, Hofer |
| `compare_prices` | Compare prices across stores |
| `find_stores_nearby` | Find stores near a location |
| `shopping_list_create` | Create shopping lists |
| `shopping_list_add_item` | Add items to lists |
| `get_shopping_recommendations` | AI-powered shopping suggestions |
| `budget_check_item` | Check purchases against budget |
| `find_coupons` | Find available coupons and discounts |
| `analyze_receipt` | OCR and categorize receipt items |
| `get_shopping_history` | Historical shopping data and patterns |

### ðŸšŠ Travel Manager (15 Tools)

| Tool | Description |
|------|-------------|
| `get_next_tram` | Next departures from Wiener Linien stations |
| `get_transport_schedule` | Full schedules for lines and stations |
| `get_transport_disruptions` | Current delays and service disruptions |
| `plan_day_trip` | Complete day trip itineraries |
| `get_travel_info` | Comprehensive city travel information |
| `get_weather_for_travel` | Weather forecasts optimized for travel |
| `get_train_schedule` | Ã–BB train schedules |
| `get_bus_schedule` | Long-distance bus schedules |
| `get_flight_info` | Flight information (ready for API integration) |
| `get_currency_exchange` | Current exchange rates |
| `get_visa_requirements` | Visa information for destinations |
| `calculate_travel_cost` | Total travel cost calculations |
| `get_sleeper_train_schedule` | Nightjet sleeper train schedules |
| `get_traffic_info` | Real-time traffic information |
| `book_transport_ticket` | Transport ticket booking (API ready) |

### ðŸ’° Expenses Manager (12 Tools)

| Tool | Description |
|------|-------------|
| `add_expense` | Add expense entries |
| `update_expense` | Update existing expenses |
| `delete_expense` | Remove expense entries |
| `get_expenses_by_category` | Expenses grouped by category |
| `get_expenses_by_date_range` | Expenses within date ranges |
| `get_top_spending_categories` | Highest spending categories |
| `analyze_spending_patterns` | AI-powered spending analysis |
| `set_budget` | Set category budgets |
| `get_budget_status` | Current budget status and alerts |
| `predict_monthly_expense` | Expense predictions |
| `compare_expenses_period` | Period-over-period comparisons |
| `get_savings_recommendations` | Personalized savings suggestions |
| `export_expenses` | Export in CSV/JSON/PDF formats |
| `import_expenses` | Import from external sources |

### ðŸŽ¬ Media Manager (10 Tools)

| Tool | Description |
|------|-------------|
| `search_plex_library` | Search Plex media collections |
| `get_currently_watching` | Currently watching/reading items |
| `get_recently_added` | Recently added media across services |
| `get_plex_recommendations` | Personalized media recommendations |
| `search_calibre_library` | Search ebook library |
| `get_reading_progress` | Reading progress tracking |
| `search_immich_photos` | Search photo library |
| `get_recent_photos` | Recent photos with metadata |
| `create_media_playlist` | Create playlists across services |
| `get_media_stats` | Comprehensive media consumption stats |
| `find_similar_media` | Find similar content across libraries |
| `analyze_media_preferences` | Media preference analysis |
| `get_media_suggestions` | AI-powered media suggestions |

### ðŸ“… Planning Manager (15 Tools)

| Tool | Description |
|------|-------------|
| `create_todo` | Create todo items with priorities |
| `update_todo` | Update existing todos |
| `get_todos_by_category` | Filter todos by category/status |
| `complete_todo` | Mark todos as completed |
| `get_calendar_events` | Calendar events within date ranges |
| `schedule_meeting` | Schedule meetings and appointments |
| `check_schedule_conflicts` | Detect scheduling conflicts |
| `get_productivity_stats` | Productivity metrics and insights |
| `set_goal` | Set and track goals |
| `get_goals_progress` | Goal progress monitoring |
| `create_habit` | Create habits to track |
| `log_habit_completion` | Log habit completions |
| `get_habit_streak` | Habit streak tracking |
| `get_motivational_quote` | Motivational quotes by category |
| `plan_week` | Generate weekly planning suggestions |

## ðŸ”§ Configuration

### Environment Variables

```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/vienna_life_assistant

# External API Keys
WIENER_LINIEN_API_KEY=your_wiener_linien_key
OPENWEATHER_API_KEY=your_weather_key
CURRENCY_API_KEY=your_currency_key

# Media Service URLs
PLEX_SERVER_URL=http://plex.local:32400
PLEX_TOKEN=your_plex_token
CALIBRE_URL=http://calibre.local:8080
IMMICH_URL=http://immich.local:2283
IMMICH_API_KEY=your_immich_key

# Redis (for background tasks)
REDIS_URL=redis://localhost:6379/0
```

### Service Integration

The server integrates with Vienna Life Assistant's ecosystem:

- **Database**: Shared PostgreSQL with web app
- **Wiener Linien**: Public transport data
- **Plex**: Media server integration
- **Calibre**: Ebook library access
- **Immich**: Photo management
- **Weather APIs**: Travel planning support
- **Currency APIs**: Travel cost calculations

## ðŸ§ª Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=vienna_live_mcp

# Run specific portmanteau tests
pytest tests/test_shopping_manager.py
pytest tests/test_travel_manager.py
```

## ðŸ“¦ MCPB Packaging

The server supports MCPB (MCP Binary) packaging for easy distribution:

```bash
# Build MCPB package
mcpb build

# Install from MCPB
mcpb install vienna-live-mcp.mcpb
```

## ðŸ¤ Integration

### MCP Client Integration

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Connect to vienna-live-mcp server
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "vienna_live_mcp.server"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Use shopping manager tools
            result = await session.call_tool("get_store_offers", {"store_name": "spar"})
            print(f"Spar offers: {result}")

            # Use travel manager tools
            tram_info = await session.call_tool("get_next_tram", {"station_name": "Stephansplatz"})
            print(f"Next tram: {tram_info}")
```

### Web App Integration

The Vienna Life Assistant web app integrates with this MCP server for enhanced functionality:

```typescript
// Example: Using MCP client in React
import { MCPClient } from '@vienna-life-assistant/mcp-client';

const client = new MCPClient({
  transport: 'http',
  baseURL: 'http://localhost:8000'
});

// Get shopping recommendations
const recommendations = await client.callTool('get_shopping_recommendations', {
  based_on: 'recent_purchases'
});
```

## ðŸ”® Future Enhancements

- **Real API Integration**: Complete integration with all external services
- **Machine Learning**: Enhanced AI recommendations and predictions
- **Multi-User Support**: User isolation and permissions
- **Advanced Analytics**: Deep insights and trend analysis
- **Mobile SDK**: Native mobile app integration
- **Plugin System**: Extensible tool architecture

## ðŸ“„ License

MIT License - see [LICENSE](LICENSE) for details.

## ðŸ¤ Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## ðŸ“ž Support

- **Issues**: [GitHub Issues](https://github.com/sandraschi/vienna-live-mcp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sandraschi/vienna-live-mcp/discussions)
- **Documentation**: [MCP Central Docs](https://github.com/sandraschi/mcp-central-docs)

## ðŸ™ Acknowledgments

- Built with [FastMCP](https://github.com/sugarforever/FastMCP)
- Part of the [Vienna Life Assistant](https://github.com/sandraschi/vienna-life-assistant) ecosystem
- Follows [MCP Central Standards](https://github.com/sandraschi/mcp-central-docs)

---

**Made with â¤ï¸ in Vienna** ðŸ‡¦ðŸ‡¹


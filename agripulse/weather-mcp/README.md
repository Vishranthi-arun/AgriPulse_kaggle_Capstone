# Weather MCP Server

This is a Model Context Protocol (MCP) server that provides weather information using the free Open-Meteo API.

## Setup

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Add to your MCP client configuration (e.g., Claude Desktop or Cursor/Gemini):
   ```json
   "mcpServers": {
     "weather-mcp": {
       "command": "python",
       "args": ["c:/Users/vishranthi.a/OneDrive - ascendion/Documents/AGENTS/Kaggle/Capstone/agripulse/weather-mcp/server.py"]
     }
   }
   ```

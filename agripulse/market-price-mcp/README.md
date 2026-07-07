# Market Price MCP Server

This is a Model Context Protocol (MCP) server that provides agricultural market prices.
Currently, it uses a simulated backend to provide real-time-like responses without requiring an API key.

## Setup

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Add to your MCP client configuration (e.g., Claude Desktop or Cursor/Gemini):
   ```json
   "mcpServers": {
     "market-price-mcp": {
       "command": "python",
       "args": ["c:/Users/vishranthi.a/OneDrive - ascendion/Documents/AGENTS/Kaggle/Capstone/agripulse/market-price-mcp/server.py"]
     }
   }
   ```

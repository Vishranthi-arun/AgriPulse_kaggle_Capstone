import httpx
# pyrefly: ignore [missing-import]
from mcp.server.fastmcp import FastMCP
import json

# Create an MCP server using FastMCP
mcp = FastMCP("Market Price Server")

# Simulated database of crop prices (in USD per metric ton)
MOCK_PRICES = {
    "wheat": {"price": 230.50, "currency": "USD", "unit": "metric ton"},
    "corn": {"price": 185.20, "currency": "USD", "unit": "metric ton"},
    "soybeans": {"price": 450.75, "currency": "USD", "unit": "metric ton"},
    "rice": {"price": 320.00, "currency": "USD", "unit": "metric ton"},
    "coffee": {"price": 4100.00, "currency": "USD", "unit": "metric ton"}
}

MOCK_TRENDS = {
    "wheat": "Upward trend due to recent weather events.",
    "corn": "Stable, standard seasonal variation.",
    "soybeans": "Downward trend as harvest exceeds expectations.",
    "rice": "Stable.",
    "coffee": "Highly volatile, currently trending up."
}

@mcp.tool()
async def get_latest_crop_price(crop: str) -> str:
    """Get the latest market price for a given agricultural crop.
    
    Args:
        crop: Name of the crop (e.g., 'wheat', 'corn', 'soybeans')
    """
    crop_key = crop.lower().strip()
    if crop_key in MOCK_PRICES:
        return json.dumps({
            "status": "success",
            "crop": crop_key,
            "data": MOCK_PRICES[crop_key]
        })
    else:
        return json.dumps({
            "status": "error",
            "message": f"Crop '{crop}' not found or not supported. Use list_supported_crops to see available options."
        })

@mcp.tool()
async def get_market_price_trends(crop: str) -> str:
    """Get the current market price trend analysis for a given agricultural crop.
    
    Args:
        crop: Name of the crop (e.g., 'wheat', 'corn')
    """
    crop_key = crop.lower().strip()
    if crop_key in MOCK_TRENDS:
        return json.dumps({
            "status": "success",
            "crop": crop_key,
            "trend": MOCK_TRENDS[crop_key]
        })
    else:
        return json.dumps({
            "status": "error",
            "message": f"Crop '{crop}' not found or not supported."
        })

@mcp.tool()
async def list_supported_crops() -> str:
    """List all the crops that are currently supported by the Market Price API."""
    crops = list(MOCK_PRICES.keys())
    return json.dumps({
        "status": "success",
        "supported_crops": crops
    })

if __name__ == "__main__":
    # Run the server on standard input/output
    mcp.run()

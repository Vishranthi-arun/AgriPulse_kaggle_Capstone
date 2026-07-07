import httpx
import json
import logging
import ssl

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("weather-mcp")
from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("Weather Server")


@mcp.tool()
async def get_weather(latitude: float, longitude: float) -> str:
    print("***** NEW WEATHER MCP IS RUNNING *****")
    """
    Get the current weather for a location.

    If the live Weather API is unavailable, automatically return demo weather
    so the AgriPulse agent can continue operating.
    """

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        f"&current=temperature_2m,wind_speed_10m"
        f"&hourly=temperature_2m,relative_humidity_2m,precipitation_probability"
    )

    try:
        # Build an SSL context from the OS/Windows certificate store first.
        # This picks up corporate proxy CA certificates that certifi does not include.
        ssl_context = ssl.create_default_context()
        async with httpx.AsyncClient(timeout=10.0, verify=ssl_context) as client:
            response = await client.get(url)

            response.raise_for_status()

            data = response.json()

            current = data.get("current", {})
            hourly = data.get("hourly", {})

            temperature = current.get("temperature_2m", "N/A")
            wind = current.get("wind_speed_10m", "N/A")

            humidity = (
                hourly.get("relative_humidity_2m", ["N/A"])[0]
                if hourly.get("relative_humidity_2m")
                else "N/A"
            )

            rain_probability = (
                hourly.get("precipitation_probability", ["N/A"])[0]
                if hourly.get("precipitation_probability")
                else "N/A"
            )

            return json.dumps(
                {
                    "status": "success",
                    "source": "Open-Meteo Weather API",
                    "temperature": temperature,
                    "humidity": humidity,
                    "wind_speed": wind,
                    "rain_probability": rain_probability,
                }
            )

    except Exception as exc:

        # -------- DEMO FALLBACK -------- #
        logger.warning("Weather API unavailable (%s). Returning demo data.", exc)

        return json.dumps(
            {
                "status": "success",
                "source": "Demo Weather Data (Weather API unavailable)",
                "temperature": 30,
                "humidity": 78,
                "wind_speed": 12,
                "rain_probability": 15,
            }
        )


if __name__ == "__main__":
    mcp.run()
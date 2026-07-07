"""
AgriPulse — Centralized Configuration

Loads settings from environment variables (.env file) and provides
constants used across all agent components.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
_PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(_PROJECT_ROOT / ".env")


# ── Model ──────────────────────────────────────────────────────────────
MODEL = os.getenv("AGRIPULSE_MODEL", "gemini-2.0-flash")

# ── Defaults ───────────────────────────────────────────────────────────
DEFAULT_REGION = os.getenv("AGRIPULSE_DEFAULT_REGION", "Karnataka, India")
DEFAULT_CROP = os.getenv("AGRIPULSE_DEFAULT_CROP", "rice")

# ── Memory ─────────────────────────────────────────────────────────────
MEMORY_BACKEND = os.getenv("AGRIPULSE_MEMORY_BACKEND", "json")
MEMORY_FILE = os.getenv(
    "AGRIPULSE_MEMORY_FILE",
    str(_PROJECT_ROOT / "data" / "memory.json"),
)

# Retention policies (days)
MEMORY_RETENTION = {
    "irrigation_history": 90,
    "pest_alerts": 90,
    "farmer_preferences": None,  # permanent
    "notification_log": 30,
}

# ── Notification ───────────────────────────────────────────────────────
NOTIFICATION_CHANNEL = os.getenv("AGRIPULSE_NOTIFICATION_CHANNEL", "console")

# ── HITL Risk Classification ───────────────────────────────────────────
# Maps action keywords to risk levels for the guardrail callback.
RISK_KEYWORDS = {
    "LOW": [
        "irrigation", "watering", "rain reminder",
        "crop calendar", "planting date", "harvest date",
    ],
    "MEDIUM": [
        "pest control", "organic treatment", "fertilizer",
        "nutrient", "compost",
    ],
    "HIGH": [
        "pesticide", "purchase", "buy", "sell", "selling",
        "market order", "financial", "payment", "price decision",
    ],
}

# ── Tool Permission Allowlist ──────────────────────────────────────────
# Only these tool function names may be invoked (from AGENTS.md).
ALLOWED_TOOLS = frozenset([
    # Weather MCP
    "get_weather_forecast",
    "get_soil_moisture",
    # Market Price MCP
    "get_market_prices",
    # Calendar
    "get_crop_calendar",
    # Notification
    "send_notification",
    # Memory
    "recall_memory",
    "store_memory",
    "get_farmer_preferences",
    "update_farmer_preferences",
])

# ── Server ─────────────────────────────────────────────────────────────
PORT = int(os.getenv("PORT", "8000"))

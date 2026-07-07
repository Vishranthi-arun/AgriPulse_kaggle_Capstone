"""
AgriPulse Memory Tools

ADK-compatible tool functions that wrap MemoryStore.
These are passed directly into each sub-agent's `tools` list so the
LLM can call them as regular function tools.

Usage in agent definition:
    from agripulse.memory.memory_tools import recall_memory, store_memory
    agent = Agent(tools=[recall_memory, store_memory, ...])
"""

from __future__ import annotations

from typing import Any, Optional

from .memory_store import MemoryStore

# Singleton store instance — shared across all agents in the process
_store: Optional[MemoryStore] = None


def _get_store() -> MemoryStore:
    """Lazy-initialize the global MemoryStore singleton."""
    global _store
    if _store is None:
        _store = MemoryStore()
    return _store


# ── ADK Tool Functions ─────────────────────────────────────────────────


def recall_memory(category: str, limit: int = 5, crop: str = None) -> dict:
    """Retrieve recent memory entries for context before giving advice.

    Call this BEFORE generating a recommendation to check what advice
    was previously given. This avoids contradicting recent advice and
    helps track patterns over time.

    Args:
        category: One of 'irrigation_history', 'pest_alerts',
                  'farmer_preferences', or 'notification_log'.
        limit:    Maximum number of entries to return (default 5).
        crop:     Optional crop name to filter entries by.

    Returns:
        A dict with 'entries' (list of past memory items, newest first)
        and 'count' (number of entries returned).
    """
    filters = {}
    if crop:
        filters["crop"] = crop

    entries = _get_store().recall(category, limit=limit, filters=filters or None)
    return {
        "status": "ok",
        "category": category,
        "count": len(entries),
        "entries": entries,
    }


def store_memory(category: str, summary: str, details: dict = None) -> dict:
    """Store a memory entry after giving advice or sending a notification.

    Call this AFTER providing a recommendation so the agent can recall
    this advice in future sessions.

    Args:
        category: One of 'irrigation_history', 'pest_alerts',
                  'farmer_preferences', or 'notification_log'.
        summary:  A short human-readable summary of what was stored.
        details:  Additional structured data to persist (e.g., weather
                  conditions, crop type, pest species, price data).

    Returns:
        A dict confirming the store operation with a timestamp.
    """
    entry: dict[str, Any] = {"summary": summary}
    if details:
        entry.update(details)

    return _get_store().store(category, entry)


def get_farmer_preferences(farmer_id: str = "default") -> dict:
    """Fetch a farmer's stored preferences (crops, region, language, etc.).

    Use this to personalize recommendations — for example, greeting in
    the farmer's preferred language or filtering advice by their crops.

    Args:
        farmer_id: Identifier for the farmer (default: 'default').

    Returns:
        A dict of stored preferences, or a 'no_preferences_found' status.
    """
    return _get_store().get_preferences(farmer_id)


def update_farmer_preferences(farmer_id: str = "default", preferences: dict = None) -> dict:
    """Save or update a farmer's preferences.

    Args:
        farmer_id:   Identifier for the farmer (default: 'default').
        preferences: Dict of preferences to save. Common keys:
                     'crops', 'region', 'language',
                     'notification_time', 'notification_channel'.

    Returns:
        A dict confirming the update.
    """
    if preferences is None:
        preferences = {}
    return _get_store().update_preferences(farmer_id, preferences)

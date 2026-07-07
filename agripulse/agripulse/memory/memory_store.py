"""
AgriPulse Memory Store

Provides persistent storage for agent memory with a pluggable backend.
Default backend writes to a local JSON file; can be swapped for Firestore
in production.

Categories:
    - irrigation_history : past irrigation advice & weather context
    - pest_alerts        : previous pest alerts, severity, actions
    - farmer_preferences : crops, region, notification prefs (permanent)
    - notification_log   : every notification sent + HITL outcome
"""

from __future__ import annotations

import json
import logging
import os
import threading
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger("agripulse.memory")

# ── Valid memory categories ────────────────────────────────────────────
VALID_CATEGORIES = frozenset([
    "irrigation_history",
    "pest_alerts",
    "farmer_preferences",
    "notification_log",
])


def _now_iso() -> str:
    """Return the current UTC time as an ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat()


class MemoryStore:
    """
    Thread-safe, file-backed memory store.

    Usage:
        store = MemoryStore()                     # uses config defaults
        store = MemoryStore("path/to/memory.json")

        store.store("irrigation_history", {"advice": "...", "crop": "rice"})
        recent = store.recall("irrigation_history", limit=5)
    """

    def __init__(self, filepath: Optional[str] = None) -> None:
        if filepath is None:
            # Import here to avoid circular deps at module level
            from config import MEMORY_FILE
            filepath = MEMORY_FILE

        self._filepath = Path(filepath)
        self._lock = threading.Lock()
        self._ensure_file()
        self._auto_prune()

    # ── Core API ───────────────────────────────────────────────────────

    def store(self, category: str, entry: dict[str, Any]) -> dict:
        """Append a timestamped entry to a memory category."""
        self._validate_category(category)
        stamped = {
            "timestamp": _now_iso(),
            **entry,
        }
        with self._lock:
            data = self._read()
            data[category].append(stamped)
            self._write(data)
        logger.info("Stored memory in '%s': %s", category, stamped.get("summary", ""))
        return {"status": "stored", "category": category, "timestamp": stamped["timestamp"]}

    def recall(
        self,
        category: str,
        limit: int = 5,
        filters: Optional[dict[str, Any]] = None,
    ) -> list[dict]:
        """
        Retrieve the most recent entries from a category.

        Args:
            category: Memory category name.
            limit:    Max entries to return (most recent first).
            filters:  Optional key-value pairs to filter entries.
        """
        self._validate_category(category)
        with self._lock:
            data = self._read()
        entries = data.get(category, [])

        # Apply optional filters
        if filters:
            entries = [
                e for e in entries
                if all(e.get(k) == v for k, v in filters.items())
            ]

        # Return most recent entries
        return entries[-limit:][::-1]  # newest first

    def get_preferences(self, farmer_id: str = "default") -> dict:
        """Return stored preferences for a farmer."""
        with self._lock:
            data = self._read()
        prefs = data.get("farmer_preferences", [])
        for entry in prefs:
            if entry.get("farmer_id") == farmer_id:
                return entry
        return {"farmer_id": farmer_id, "status": "no_preferences_found"}

    def update_preferences(self, farmer_id: str, prefs: dict[str, Any]) -> dict:
        """Upsert preferences for a farmer."""
        with self._lock:
            data = self._read()
            pref_list = data.get("farmer_preferences", [])
            # Find existing or create new
            found = False
            for i, entry in enumerate(pref_list):
                if entry.get("farmer_id") == farmer_id:
                    pref_list[i] = {
                        "farmer_id": farmer_id,
                        "timestamp": _now_iso(),
                        **prefs,
                    }
                    found = True
                    break
            if not found:
                pref_list.append({
                    "farmer_id": farmer_id,
                    "timestamp": _now_iso(),
                    **prefs,
                })
            data["farmer_preferences"] = pref_list
            self._write(data)
        logger.info("Updated preferences for farmer '%s'", farmer_id)
        return {"status": "updated", "farmer_id": farmer_id}

    def prune(self, retention_days: Optional[dict[str, Optional[int]]] = None) -> dict:
        """
        Remove entries older than the retention policy.

        Args:
            retention_days: Mapping of category → max age in days.
                            None means permanent (no pruning).
        """
        if retention_days is None:
            from config import MEMORY_RETENTION
            retention_days = MEMORY_RETENTION

        pruned_counts: dict[str, int] = {}
        now = datetime.now(timezone.utc)

        with self._lock:
            data = self._read()
            for category, max_days in retention_days.items():
                if max_days is None:
                    continue  # permanent
                cutoff = now - timedelta(days=max_days)
                original = data.get(category, [])
                filtered = [
                    e for e in original
                    if self._parse_ts(e.get("timestamp", "")) >= cutoff
                ]
                pruned_counts[category] = len(original) - len(filtered)
                data[category] = filtered
            self._write(data)

        if any(v > 0 for v in pruned_counts.values()):
            logger.info("Pruned memory: %s", pruned_counts)
        return {"status": "pruned", "removed": pruned_counts}

    # ── Private helpers ────────────────────────────────────────────────

    def _ensure_file(self) -> None:
        """Create the memory file and parent dirs if they don't exist."""
        if not self._filepath.exists():
            self._filepath.parent.mkdir(parents=True, exist_ok=True)
            empty: dict[str, list] = {cat: [] for cat in VALID_CATEGORIES}
            self._filepath.write_text(json.dumps(empty, indent=2), encoding="utf-8")
            logger.info("Created new memory file: %s", self._filepath)

    def _read(self) -> dict:
        """Read the JSON file (caller must hold lock)."""
        try:
            return json.loads(self._filepath.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, FileNotFoundError):
            logger.warning("Corrupt or missing memory file — reinitializing")
            empty: dict[str, list] = {cat: [] for cat in VALID_CATEGORIES}
            self._write(empty)
            return empty

    def _write(self, data: dict) -> None:
        """Write dict to JSON file (caller must hold lock)."""
        self._filepath.write_text(
            json.dumps(data, indent=2, default=str),
            encoding="utf-8",
        )

    def _auto_prune(self) -> None:
        """Run prune on initialization to enforce retention."""
        try:
            self.prune()
        except Exception:
            logger.debug("Auto-prune skipped (config not available yet)")

    @staticmethod
    def _validate_category(category: str) -> None:
        if category not in VALID_CATEGORIES:
            raise ValueError(
                f"Invalid memory category '{category}'. "
                f"Must be one of: {sorted(VALID_CATEGORIES)}"
            )

    @staticmethod
    def _parse_ts(ts: str) -> datetime:
        """Parse an ISO-8601 timestamp, returning epoch on failure."""
        try:
            return datetime.fromisoformat(ts)
        except (ValueError, TypeError):
            return datetime.min.replace(tzinfo=timezone.utc)

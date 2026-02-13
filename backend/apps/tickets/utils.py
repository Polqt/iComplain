"""
Reusable helpers for the tickets app (history formatting, status/priority mapping).
"""
from django.utils import timezone


def format_date(dt):
    """Return date string for history display (e.g. "08 Feb 2026")."""
    return timezone.localtime(dt).strftime("%d %b %Y")


def format_timestamp(dt):
    """Return ISO timestamp for history API."""
    return timezone.localtime(dt).isoformat()


def map_status_for_history(db_status: str) -> str:
    """Map DB status to history API value (e.g. in_progress -> in-progress)."""
    if db_status == "in_progress":
        return "in-progress"
    return db_status


def map_priority_for_history(priority_name: str) -> str:
    """Map priority name to history API value (low/medium/high)."""
    if not priority_name:
        return "medium"
    name = (priority_name or "").strip().lower()
    if name == "low":
        return "low"
    if name in ("high", "urgent"):
        return "high"
    return "medium"


def history_action_for_status_change(old_status: str, new_status: str) -> str:
    """Derive history action from status transition (resolved/closed/reopened/updated)."""
    if new_status == "resolved":
        return "resolved"
    if new_status == "closed":
        return "closed"
    if new_status == "pending" and old_status in ("resolved", "closed"):
        return "reopened"
    return "updated"

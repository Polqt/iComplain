from django.utils import timezone


def format_date(dt):
    return timezone.localtime(dt).strftime("%d %b %Y")


def format_timestamp(dt):
    return timezone.localtime(dt).isoformat()


def map_status_for_history(db_status: str) -> str:
    if db_status == "in_progress":
        return "in-progress"
    return db_status


def map_priority_for_history(priority_name: str) -> str:
    if not priority_name:
        return "medium"
    name = (priority_name or "").strip().lower()
    if name == "low":
        return "low"
    if name in ("high", "urgent"):
        return "high"
    return "medium"


def history_action_for_status_change(old_status: str, new_status: str) -> str:
    if new_status == "resolved":
        return "resolved"
    if new_status == "closed":
        return "closed"
    if new_status == "pending" and old_status in ("resolved", "closed"):
        return "reopened"
    return "updated"

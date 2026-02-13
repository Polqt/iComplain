import type { HistoryAction, HistoryStatus, HistoryPriority, HistoryItem, HistoryFilterType, HistorySortType } from "../types/history.ts";

export const historyConfig: Record<HistoryAction, {
    label: string;
    icon: string;
    color: string;
    bgColor: string;
}> = {
    created: { 
        label: "Created", 
        icon: "mdi:plus-circle", 
        color: "text-info",
        bgColor: "bg-info/10"
    },
    updated: { 
        label: "Updated", 
        icon: "mdi:pencil", 
        color: "text-warning",
        bgColor: "bg-warning/10"
    },
    resolved: { 
        label: "Resolved", 
        icon: "mdi:check-circle", 
        color: "text-success",
        bgColor: "bg-success/10"
    },
    closed: { 
        label: "Closed", 
        icon: "mdi:close-circle", 
        color: "text-error",
        bgColor: "bg-error/10"
    },
    commented: { 
        label: "Commented", 
        icon: "mdi:message", 
        color: "text-primary",
        bgColor: "bg-primary/10"
    },
    reopened: { 
        label: "Reopened", 
        icon: "mdi:refresh", 
        color: "text-secondary",
        bgColor: "bg-secondary/10"
    },
};

export const statusConfig: Record<HistoryStatus, {
    label: string;
    color: string;
}> = {
    pending: { label: "Pending", color: "badge-warning" },
    "in-progress": { label: "In Progress", color: "badge-info" },
    resolved: { label: "Resolved", color: "badge-success" },
    closed: { label: "Closed", color: "badge-ghost" },
};

export const priorityConfig: Record<HistoryPriority, {
    label: string;
    color: string;
}> = {
    low: { label: "Low", color: "badge-info" },
    medium: { label: "Medium", color: "badge-warning" },
    high: { label: "High", color: "badge-error" },
};

export function filterHistoryByAction(
    items: HistoryItem[],
    filter: HistoryFilterType
): HistoryItem[] {
    if (filter === "all") return items;
    return items.filter(item => item.action === filter);
}

export function searchHistory(
    items: HistoryItem[],
    query: string
): HistoryItem[] {
    if (!query.trim()) return items;
    
    const lowerQuery = query.toLowerCase();
    return items.filter(item =>
        item.title.toLowerCase().includes(lowerQuery) ||
        item.ticketId.toLowerCase().includes(lowerQuery) ||
        item.description.toLowerCase().includes(lowerQuery)
    );
}

/** Get a numeric time for sorting; uses timestamp if parseable, otherwise date (e.g. "08 Feb 2026"). */
function getSortTime(item: HistoryItem): number {
    const fromTimestamp = new Date(item.timestamp).getTime();
    if (!Number.isNaN(fromTimestamp)) return fromTimestamp;
    const fromDate = new Date(item.date).getTime();
    return Number.isNaN(fromDate) ? 0 : fromDate;
}

export function sortHistory(
    items: HistoryItem[],
    sortBy: HistorySortType
): HistoryItem[] {
    return [...items].sort((a, b) => {
        const timeA = getSortTime(a);
        const timeB = getSortTime(b);
        return sortBy === "newest" ? timeB - timeA : timeA - timeB;
    });
}

/**
 * Format an ISO or date string as a relative time label (e.g. "2 hours ago").
 * Uses fallbackDate when the input is invalid or older than ~1 week.
 */
export function formatRelativeTime(isoOrDate: string, fallbackDate: string): string {
  const d = new Date(isoOrDate);
  if (Number.isNaN(d.getTime())) return fallbackDate;
  const now = new Date();
  const sec = Math.floor((now.getTime() - d.getTime()) / 1000);
  if (sec < 60) return "just now";
  const mins = Math.floor(sec / 60);
  if (sec < 3600) return mins === 1 ? "1 min ago" : `${mins} mins ago`;
  const hours = Math.floor(sec / 3600);
  if (sec < 86400) return hours === 1 ? "1 hour ago" : `${hours} hours ago`;
  const days = Math.floor(sec / 86400);
  if (sec < 604800) return days === 1 ? "1 day ago" : `${days} days ago`;
  return fallbackDate;
}

/** Return "activity" or "activities" for display (e.g. "Showing 5 activities"). */
export function getActivityLabel(count: number): "activity" | "activities" {
  return count === 1 ? "activity" : "activities";
}

/**
 * Apply all filters and sorting to history items
 */
export function filterAndSortHistory(
    items: HistoryItem[],
    filter: HistoryFilterType,
    searchQuery: string,
    sortBy: HistorySortType
): HistoryItem[] {
    let result = items;
    
    // Apply action filter
    result = filterHistoryByAction(result, filter);
    
    // Apply search
    result = searchHistory(result, searchQuery);
    
    // Apply sorting
    result = sortHistory(result, sortBy);
    
    return result;
}

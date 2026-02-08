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

export function sortHistory(
    items: HistoryItem[],
    sortBy: HistorySortType
): HistoryItem[] {
    return [...items].sort((a, b) => {
        const dateA = new Date(a.timestamp).getTime();
        const dateB = new Date(b.timestamp).getTime();
        return sortBy === "newest" ? dateB - dateA : dateA - dateB;
    });
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

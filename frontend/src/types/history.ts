export type HistoryAction = "created" | "updated" | "resolved" | "closed" | "commented" | "reopened";

export type HistoryStatus = "pending" | "in-progress" | "resolved" | "closed";

export type HistoryPriority = "low" | "medium" | "high";

export type HistoryFilterType = "all" | "created" | "updated" | "resolved" | "closed" | "commented" | "reopened";

export type HistorySortType = "newest" | "oldest";

export type HistoryItem = {
  id: string;
  ticketPk: number;
  ticketId: string;
  title: string;
  action: HistoryAction;
  description: string;
  timestamp: string;
  date: string;
  status: HistoryStatus;
  priority: HistoryPriority;
  category?: string;
};

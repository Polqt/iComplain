import type { TicketPriority, TicketStatus } from "../types/tickets.ts";

export const statusConfig: Record<
  TicketStatus,
  { label: string; color: string }
> = {
  pending: { label: "Pending", color: "badge-warning" },
  in_progress: { label: "In Progress", color: "badge-info" },
  resolved: { label: "Resolved", color: "badge-success" },
  closed: { label: "Closed", color: "badge-ghost" },
};

export const priorityConfig: Record<
  TicketPriority,
  { label: string; color: string }
> = {
  low: { label: "Low", color: "badge-info" },
  medium: { label: "Medium", color: "badge-warning" },
  high: { label: "High", color: "badge-error" },
};

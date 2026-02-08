import type { TicketPriority, TicketStatus } from "../types/tickets.js";

export const statusConfig: Record<
  TicketStatus,
  { label: string; color: string }
> = {
  "not-started": { label: "Not Started", color: "badge-primary" },
  "in-research": { label: "In Research", color: "badge-warning" },
  "on-track": { label: "On Track", color: "badge-secondary" },
  complete: { label: "Complete", color: "badge-success" },
};

export const priorityConfig: Record<
  TicketPriority,
  { label: string; color: string }
> = {
  low: { label: "Low", color: "badge-info" },
  medium: { label: "Medium", color: "badge-warning" },
  high: { label: "High", color: "badge-error" },
};

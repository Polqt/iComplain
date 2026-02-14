import type { Column, PipelineStep, Ticket, TicketColumn, TicketPriority, TicketStatus } from "../types/tickets.ts";

export type PriorityKey = "low" | "medium" | "high" | "urgent";

export const statuses = ["pending", "in_progress", "resolved", "closed"] as const;
export const priorities = ["low", "medium", "high", "urgent"] as const;
export const priorityIdMap: Record<string, number> = { low: 1, medium: 2, high: 3 };

export function getPriorityKey(priority: TicketPriority | string | any): PriorityKey {
  if (!priority) return "low";
  if (typeof priority === "string") {
    const k = priority.toLowerCase();
    return k === "high" ? "high" : k === "medium" ? "medium" : "low";
  }
  if (typeof priority === "object") {
    const name = priority.name ? String(priority.name).toLowerCase() : undefined;
    if (name === "high" || name === "medium" || name === "low") return name as PriorityKey;
    if (typeof priority.level === "number") {
      return priority.level >= 3 ? "high" : priority.level === 2 ? "medium" : "low";
    }
  }
  return "low";
}

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
  PriorityKey,
  { label: string; color: string }
> = {
  low: { label: "Low", color: "badge-info" },
  medium: { label: "Medium", color: "badge-warning" },
  high: { label: "High", color: "badge-error" },
  urgent: { label: "Urgent", color: "badge-error" },
};

export const priorityIcons: Record<string, string> = {
  low: "mdi:arrow-down",
  medium: "mdi:minus",
  high: "mdi:arrow-up",
  urgent: "mdi:alert",
};

export const priorityAccent: Record<string, string> = {
  low: "border-l-info",
  medium: "border-l-warning",
  high: "border-l-error",
  urgent: "border-l-error",
};

export const columnAccent: Record<string, string> = {
  pending: "border-l-yellow-400",
  in_progress: "border-l-sky-400",
  resolved: "border-l-emerald-400",
  closed: "border-l-base-content/25",
};

 export const baseColumns: Omit<TicketColumn, "reports">[] = [
    {
      id: "pending",
      title: "Pending",
      color: "text-yellow-300",
      dotColor: "bg-yellow-300",
    },
    {
      id: "in_progress",
      title: "In Progress",
      color: "text-info",
      dotColor: "bg-info",
    },
    {
      id: "resolved",
      title: "Resolved",
      color: "text-green-300",
      dotColor: "bg-green-300",
    },
    {
      id: "closed",
      title: "Closed",
      color: "text-gray-300",
      dotColor: "bg-gray-300",
    },
  ];

export const columnConfigs: Column[] = [
    {
      id: "pending",
      title: "Pending",
      color: "text-yellow-300",
      dotColor: "bg-yellow-300",
    },
    {
      id: "in_progress",
      title: "In Progress",
      color: "text-info",
      dotColor: "bg-info",
    },
    {
      id: "resolved",
      title: "Resolved",
      color: "text-green-300",
      dotColor: "bg-green-300",
    },
    {
      id: "closed",
      title: "Closed",
      color: "text-gray-300",
      dotColor: "bg-gray-300",
    },
  ];

export const pipelineSteps = [
  { id: "pending",     label: "Pending",     icon: "mdi:clock-outline"        },
  { id: "in_progress", label: "In Progress", icon: "mdi:progress-wrench"      },
  { id: "resolved",    label: "Resolved",    icon: "mdi:check-circle-outline" },
  { id: "closed",      label: "Closed",      icon: "mdi:lock-outline"         },
] satisfies PipelineStep[];;

export function getStepState(
  currentStatus: TicketStatus,
  stepId: TicketStatus,
): "active" | "past" | "future" {
  const currentIdx = TICKET_STATUSES.indexOf(currentStatus);
  const stepIdx    = TICKET_STATUSES.indexOf(stepId);
  if (currentIdx === stepIdx) return "active";
  if (currentIdx > stepIdx)   return "past";
  return "future";
}

export const TICKET_STATUSES = [
  "pending", "in_progress", "resolved", "closed",
] as const satisfies readonly TicketStatus[];

/**
 * Groups tickets into columns based on their status.
 *
 * Each column's `id` is treated as a status value, and the returned
 * `TicketColumn` objects will contain only the tickets whose `status`
 * matches that column `id`.
 *
 * @param tickets - Array of tickets to be grouped by status.
 * @param columns - Column configurations; each column's `id` should map to a ticket status.
 * @returns Array of ticket columns with `reports` filtered to tickets matching the column status.
 */
export function groupTicketsByStatus(
  tickets: Ticket[],
  columns: Column[]
): TicketColumn[] {
  return columns.map((column) => ({
    ...column,
    reports: tickets.filter(t => t.status === column.id),
  }))
}
import type { Column, Ticket, TicketColumn, TicketPriority, TicketStatus } from "../types/tickets.ts";

export type PriorityKey = "low" | "medium" | "high" | "urgent";


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

/**
 * @param tickets - Array of tickets to be sorted
 */
// export function calculateTicketStatus(tickets: Ticket[]) {
//   const total = tickets.length;
//   const byStatus = tickets.reduce((acc, ticket) => {
//       acc[ticket.status as Status] = (acc[ticket.status as Status] || 0) + 1;
//       return acc;
//     },
//   {} as Record<Status, number>)

//   const byPriority = tickets.reduce((acc, ticket) => {
//     acc[ticket.priority] = (acc[ticket.priority] || 0) + 1;
//     return acc;
//   }, {} as Record<string, number>)

//   return {
//     total, byStatus, byPriority
//   }
// }

/**
 * Sorts tickets by various criteria
 */
// export function sortTickets(
//   tickets: Ticket[],
//   sortBy: "date" | "priority" | "title" = "date",
//   order: "asc" | "desc" = "desc"
// ): Ticket[] {
//   const sorted = [...tickets].sort((a, b) => {
//     switch (sortBy) {
//       case "title":
//         return a.title.localeCompare(b.title);
//       case "priority": {
//         const priorityOrder = { high: 3, medium: 2, low: 1 };
//         return priorityOrder[b.priority] - priorityOrder[a.priority];
//       }
//       case "date":
//       default:
//         return new Date(b.date).getTime() - new Date(a.date).getTime();
//     }
//   });

//   return order === "asc" ? sorted.reverse() : sorted;
// }
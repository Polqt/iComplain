export interface Ticket {
  id: string;
  title: string;
  description: string;
  status: TicketStatus;
  priority: TicketPriority;
  assignees: string[];
  date: string;
  comments: number;
  links: number;
  attachments: string;
}

export type TicketStatus = "not-started" | "in-research" | "on-track" | "complete";
export type TicketPriority = "low" | "medium" | "high";

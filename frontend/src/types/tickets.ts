import type { User } from "./user.ts";

export type RawTicket = Omit<Ticket, "category" | "priority"> & {
  category?: Category | null;
  priority?: TicketPriority | null;
};

export type Category = {
    id: number;
    name: string;
}

export type TicketStatus = "pending" | "in_progress" | "resolved" | "closed";

export type TicketPriority = {
    id: number;
    name: string;
    level: number;
    color_code: string;
};

export type Ticket = {
    id: number;
    ticket_number: string;
    title: string;
    description: string;
    student: User;
    category: Category;
    priority: TicketPriority;
    building: string;
    room_name: string;
    status: TicketStatus;
    created_at: string;
    updated_at: string;
}

export type TicketCreatePayload = {
    title: string;
    description: string;
    category: number;
    building: string;
    room_name: string;
}

export type TicketUpdatePayload = {
    title?: string;
    description?: string;
    category?: number;
    priority?: number;
    building?: string;
    room_name?: string;
    status?: TicketStatus;
}

export type TicketColumn = {
    id: TicketStatus;
    title: string;
    color: string;
    dotColor: string;
    reports: Ticket[];
}

export type Column = {
    id: TicketStatus;
    title: string;
    color: string;
    dotColor: string;
}

export type TicketsState = {
    tickets: Ticket[];
    isLoading: boolean;
    error: string | null;
};

export type ViewMode = "grid" | "list";

export type ModalMode = "create" | "edit" | "delete" | null;

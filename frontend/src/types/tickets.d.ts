import type { User } from "./user.ts";
export type Category = {
    id: number;
    name: string;
};
export type TicketStatus = "pending" | "in_progress" | "resolved" | "closed";
export type TicketPriority = {
    id: number;
    name: string;
    level: number;
    color_code: string;
};
export type Ticket = {
    id: string;
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
    ticket_number: string;
    attachments: string;
    comments: number;
};
export type TicketColumn = {
    id: TicketStatus;
    title: string;
    color: string;
    dotColor: string;
    reports: Ticket[];
};
export type Column = {
    id: TicketStatus;
    title: string;
    color: string;
    dotColor: string;
};
export type ViewMode = "grid" | "list";
export type ModalMode = "create" | "edit" | "delete" | null;

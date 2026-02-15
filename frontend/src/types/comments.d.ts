import type { Ticket } from "./tickets.ts";
import type { User } from "./user.ts";
export type TicketComment = {
    id: number;
    ticket: Ticket;
    user: User;
    message: string;
    created_at: string;
};
export type CommentCreatePayload = {
    message: string;
};
export type CommentUpdatePayload = {
    message?: string;
};
export type CommentsState = {
    comments: TicketComment[];
    isLoading: boolean;
    error: string | null;
};

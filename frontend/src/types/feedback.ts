import type { Ticket } from "./tickets.ts";
import type { User } from "./user.ts";


export type TicketFeedback = {
    id: number;
    ticket_id: number;
    student: User;
    rating: number;
    comments: string | null;
    created_at: string;
    updated_at: string;
}

export type FeedbackState = {
    feedbacks: TicketFeedback[];
    isLoading: boolean;
    error: string | null;
}


export type FeedbackCreatePayload = {
    rating: number;
    comments: string | null;
}


export type FeedbackUpdatePayload = {
    rating?: number;
    comments?: string | null;
}

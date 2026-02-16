import type { Ticket } from "../../types/tickets.ts";
import type { User } from "../../types/user.ts";
import { PUBLIC_API_URL } from "$env/static/public";


export type TicketFeedback = {
    id: number;
    ticket: Ticket;
    student: User;
    rating: number;
    comments: string | null;
    created_at: string;
    updated_at: string;
}

export type FeedbackCreatePayload = {
    rating: number;
    comments: string | null;
}

export type FeedbackUpdatePayload = {
    rating?: number;
    comments?: string | null;
}


export async function getFeedback(ticketId: number): Promise<TicketFeedback> {
    const res = await fetch(`${PUBLIC_API_URL}/tickets/${ticketId}/feedback`, {
        credentials: 'include',
    });
    if (!res.ok) {
        throw new Error(`Failed to fetch feedback: ${res.statusText}`);
    }
    return res.json() as Promise<TicketFeedback>;
}

export async function createFeedback(ticketId: number, payload: FeedbackCreatePayload): Promise<TicketFeedback> {
    const res = await fetch(`${PUBLIC_API_URL}/tickets/${ticketId}/feedback`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
        credentials: 'include',
    });
    if (!res.ok) {
        throw new Error(`Failed to create feedback: ${res.statusText}`);
    }
    return res.json() as Promise<TicketFeedback>;
}

export async function updateFeedback(ticketId: number, feedbackId: number, payload: FeedbackUpdatePayload): Promise<TicketFeedback> {
    const res = await fetch(`${PUBLIC_API_URL}/tickets/${ticketId}/feedback/${feedbackId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
        credentials: 'include',
    });
    if (!res.ok) {
        throw new Error(`Failed to update feedback: ${res.statusText}`);
    }
    return res.json() as Promise<TicketFeedback>;
}

export async function deleteFeedback(ticketId: number, feedbackId: number): Promise<void> {
    const res = await fetch(`${PUBLIC_API_URL}/tickets/${ticketId}/feedback/${feedbackId}`, {
        method: 'DELETE',
        credentials: 'include',
    }); 
    if (!res.ok) {
        throw new Error(`Failed to delete feedback: ${res.statusText}`);
    }
}
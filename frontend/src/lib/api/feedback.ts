import type { TicketFeedback, FeedbackCreatePayload, FeedbackUpdatePayload } from "../../types/feedback.ts";
import { PUBLIC_API_URL } from "$env/static/public";

const BASE = `${PUBLIC_API_URL}/tickets`;

async function handleRes<T>(res: Response): Promise<T> {
    if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        const detail = Array.isArray(body?.detail)
            ? body.detail.map((item: { msg?: string }) => item?.msg).filter(Boolean).join(", ")
            : body?.detail;
        throw new Error(body.message || detail || res.statusText);
    }

    return res.json() as Promise<T>;
}

export async function getFeedback(ticketId: number): Promise<TicketFeedback> {
    try {
        const res = await fetch(`${BASE}/${ticketId}/feedback/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        });

        return await handleRes<TicketFeedback>(res);
    } catch (error) {
        console.error(`Error fetching feedback for ticket ${ticketId}:`, error);
        throw error;
    }
}

export async function createFeedback(ticketId: number, payload: FeedbackCreatePayload): Promise<TicketFeedback> {
    try {
        const formData = new FormData();
        formData.append('rating', String(payload.rating));
        if (payload.comments !== null && payload.comments !== undefined) {
            formData.append('comments', payload.comments);
        }

        const res = await fetch(`${BASE}/${ticketId}/feedback/`, {
            method: 'POST',
            body: formData,
            credentials: 'include',
        });

        return await handleRes<TicketFeedback>(res);
    } catch (error) {
        console.error(`Error creating feedback for ticket ${ticketId}:`, error);
        throw error;
    }
}

export async function updateFeedback(ticketId: number, feedbackId: number, payload: FeedbackUpdatePayload): Promise<TicketFeedback> {
    try {
        const res = await fetch(`${BASE}/${ticketId}/feedback/${feedbackId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
            credentials: 'include',
        });

        return await handleRes<TicketFeedback>(res);
    } catch (error) {
        console.error(`Error updating feedback ${feedbackId} for ticket ${ticketId}:`, error);
        throw error;
    }
}

export async function deleteFeedback(ticketId: number, feedbackId: number): Promise<void> {
    try {
        const res = await fetch(`${BASE}/${ticketId}/feedback/${feedbackId}`, {
            method: 'DELETE',
            credentials: 'include',
        });

        if (!res.ok) {
            const body = await res.json().catch(() => ({}));
            throw new Error(body.message || body.detail || 'Failed to delete feedback');
        }
    } catch (error) {
        console.error(`Error deleting feedback ${feedbackId} for ticket ${ticketId}:`, error);
        throw error;
    }
}


import { PUBLIC_API_URL } from "$env/static/public";
import type { CommentCreatePayload, CommentUpdatePayload, TicketComment } from "../../types/comments.ts";

const BASE = `${PUBLIC_API_URL}/tickets`;

 async function handleRes<T>(res: Response): Promise<T> {
    if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.message || body.detail || res.statusText);
    }
    return res.json() as Promise<T>;
}

export async function createComment(
    ticketId: number,
    payload: CommentCreatePayload,
    attachment?: File
): Promise<TicketComment> {
    try {
        const formData = new FormData();
        formData.append("message", payload.message || "");

        if (attachment) {
            formData.append("attachment", attachment);
        }

        const res = await fetch(`${BASE}/${ticketId}/comments`, {
            method: "POST",
            body: formData,
            credentials: "include",
        });

        return await handleRes<TicketComment>(res);
    } catch (error) {
        console.error(`Error creating comment for ticket ${ticketId}:`, error);
        throw error;
    }
}

export async function editComment(
    ticketId: number,
    commentId: number,
    payload: CommentUpdatePayload
): Promise<TicketComment> {
    try {
        const res = await fetch(`${BASE}/${ticketId}/comments/${commentId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ ...payload }),
            credentials: "include",
        });

        return await handleRes<TicketComment>(res);
    } catch (error) {
        console.error(`Error editing comment ${commentId} for ticket ${ticketId}:`, error);
        throw error;
    }
}

export async function deleteComment(ticketId: number, commentId: number): Promise<void> {
    try {
        const res = await fetch(`${BASE}/${ticketId}/comments/${commentId}`, {
            method: "DELETE",
            credentials: "include",
        });

        if (!res.ok) {
            const body = await res.json().catch(() => ({}));
            throw new Error(body.message || body.detail || `Failed to delete comment ${commentId}.`);
        }
    } catch (error) {
        console.error(`Error deleting comment ${commentId} for ticket ${ticketId}:`, error);
        throw error;
    }
}


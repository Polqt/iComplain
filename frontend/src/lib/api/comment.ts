import { apiFetch, resolveApiAssetUrl } from "../../utils/api.ts";
import type {
	CommentCreatePayload,
	CommentUpdatePayload,
	TicketComment,
} from "../../types/comments.ts";

const BASE = "/tickets";

function normalizeCommentAvatar(comment: TicketComment): TicketComment {
	return {
		...comment,
		user: {
			...comment.user,
			avatar: resolveApiAssetUrl(comment.user?.avatar),
		},
	};
}

async function handleRes<T>(res: Response): Promise<T> {
	if (!res.ok) {
		const body = await res.json().catch(() => ({}));
		throw new Error(body.message || body.detail || res.statusText);
	}
	return res.json() as Promise<T>;
}

export async function fetchComments(
	ticketId: number,
): Promise<TicketComment[]> {
	try {
		const res = await apiFetch(`${BASE}/${ticketId}/comments`, {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
			},
		});
		const comments = await handleRes<TicketComment[]>(res);
		return comments.map(normalizeCommentAvatar);
	} catch (error) {
		console.error(`Error fetching comments for ticket ${ticketId}:`, error);
		throw error;
	}
}

export async function createComment(
	ticketId: number,
	payload: CommentCreatePayload,
): Promise<TicketComment> {
	try {
		const formData = new FormData();
		formData.append("message", payload.message || "");

		const res = await apiFetch(`${BASE}/${ticketId}/comments`, {
			method: "POST",
			body: formData,
		});

		const comment = await handleRes<TicketComment>(res);
		return normalizeCommentAvatar(comment);
	} catch (error) {
		console.error(`Error creating comment for ticket ${ticketId}:`, error);
		throw error;
	}
}

export async function editComment(
	ticketId: number,
	commentId: number,
	payload: CommentUpdatePayload,
): Promise<TicketComment> {
	try {
		const formData = new FormData();
		if (payload.message !== undefined) {
			formData.append("message", payload.message);
		}

		const res = await apiFetch(`${BASE}/${ticketId}/comments/${commentId}`, {
			method: "PUT",
			body: formData,
		});

		const comment = await handleRes<TicketComment>(res);
		return normalizeCommentAvatar(comment);
	} catch (error) {
		console.error(
			`Error editing comment ${commentId} for ticket ${ticketId}:`,
			error,
		);
		throw error;
	}
}

export async function deleteComment(
	ticketId: number,
	commentId: number,
): Promise<void> {
	try {
		const res = await apiFetch(`${BASE}/${ticketId}/comments/${commentId}`, {
			method: "DELETE",
		});

		if (!res.ok) {
			const body = await res.json().catch(() => ({}));
			throw new Error(
				body.message || body.detail || `Failed to delete comment ${commentId}.`,
			);
		}
	} catch (error) {
		console.error(
			`Error deleting comment ${commentId} for ticket ${ticketId}:`,
			error,
		);
		throw error;
	}
}

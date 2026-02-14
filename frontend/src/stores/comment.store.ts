import { PUBLIC_API_URL } from "$env/static/public";
import { get, writable, type Readable } from "svelte/store";
import { createComment as apiCreateComment, deleteComment as apiDeleteComment, editComment as apiEditComment } from "../lib/api/comment.ts";
import type { CommentCreatePayload, CommentsState, CommentUpdatePayload, TicketComment } from "../types/comments.ts";

interface CommentsStore extends Readable<CommentsState> {
    setComments: (comments: TicketComment[]) => void;
    setLoading: (isLoading: boolean) => void;
    setError: (error: string | null) => void;

    loadCommentsForTicket: (ticketId: number) => Promise<void>;
    createComment: (ticketId: number, payload: CommentCreatePayload, attachment?: File) => Promise<TicketComment | null>;
    updateComment: (ticketId: number, commentId: number, updates: CommentUpdatePayload) => Promise<TicketComment | null>;
    deleteComment: (ticketId: number, commentId: number) => Promise<boolean>;

    addCommentToStore: (comment: TicketComment) => void;
    updateCommentInStore: (commentId: number, updates: Partial<TicketComment>) => void;
    removeCommentFromStore: (commentId: number) => void;
    clearComments: () => void;
}

const BASE = `${PUBLIC_API_URL}/tickets`;

function createCommentsStore(): CommentsStore {
    const { subscribe, update, set } = writable<CommentsState>({
        comments: [],
        isLoading: false,
        error: null,
    });

    return {
        subscribe,

        setComments(comments: TicketComment[]) {
            set({ comments, isLoading: false, error: null });
        },

        setLoading(isLoading: boolean) {
            update((state) => ({ ...state, isLoading }));
        },

        setError(error: string | null) {
            update((state) => ({ ...state, error, isLoading: false }));
        },

        async loadCommentsForTicket(ticketId: number): Promise<void> {
            update((state) => ({ ...state, isLoading: true, error: null }));

            try {
                const res = await fetch(`${BASE}/${ticketId}/comments`, {
                    method: "GET",
                    credentials: "include",
                });

                if (!res.ok) {
                    const body = await res.json().catch(() => ({}));
                    throw new Error(body.message || body.detail || `Failed to load comments for ticket ${ticketId}`);
                }

                const comments = (await res.json()) as TicketComment[];

                update((state) => ({
                    ...state,
                    comments,
                    isLoading: false,
                    error: null,
                }));
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : "Unknown error";
                update((state) => ({
                    ...state,
                    isLoading: false,
                    error: `Failed to load comments: ${errorMessage}`,
                }));
            }
        },

        async createComment(ticketId: number, payload: CommentCreatePayload, attachment?: File): Promise<TicketComment | null> {
            update((state) => ({ ...state, isLoading: true, error: null }));

            try {
                const newComment = await apiCreateComment(ticketId, payload, attachment);

                if (newComment) {
                    update((state) => ({
                        ...state,
                        comments: [...state.comments, newComment],
                        isLoading: false,
                        error: null,
                    }));
                }

                return newComment;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : "Unknown error";
                update((state) => ({
                    ...state,
                    isLoading: false,
                    error: `Failed to create comment: ${errorMessage}`,
                }));
                return null;
            }
        },

        async updateComment(ticketId: number, commentId: number, updates: CommentUpdatePayload): Promise<TicketComment | null> {
            update((state) => ({ ...state, isLoading: true, error: null }));

            try {
                const updatedComment = await apiEditComment(ticketId, commentId, updates);

                if (updatedComment) {
                    update((state) => ({
                        ...state,
                        comments: state.comments.map((comment) => (comment.id === commentId ? updatedComment : comment)),
                        isLoading: false,
                        error: null,
                    }));
                }

                return updatedComment;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : "Unknown error";
                update((state) => ({
                    ...state,
                    isLoading: false,
                    error: `Failed to update comment: ${errorMessage}`,
                }));
                return null;
            }
        },

        async deleteComment(ticketId: number, commentId: number): Promise<boolean> {
            update((state) => ({ ...state, isLoading: true, error: null }));

            try {
                await apiDeleteComment(ticketId, commentId);

                update((state) => ({
                    ...state,
                    comments: state.comments.filter((comment) => comment.id !== commentId),
                    isLoading: false,
                    error: null,
                }));

                return true;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : `Failed to delete comment ${commentId}`;
                console.error(`Error deleting comment ${commentId}:`, error);
                update((state) => ({
                    ...state,
                    isLoading: false,
                    error: errorMessage,
                }));
                return false;
            }
        },

        addCommentToStore(comment: TicketComment) {
            update((state) => ({ ...state, comments: [...state.comments, comment] }));
        },

        updateCommentInStore(commentId: number, updates: Partial<TicketComment>) {
            update((state) => ({
                ...state,
                comments: state.comments.map((comment) => (comment.id === commentId ? { ...comment, ...updates } : comment)),
            }));
        },

        removeCommentFromStore(commentId: number) {
            update((state) => ({ ...state, comments: state.comments.filter((comment) => comment.id !== commentId) }));
        },

        clearComments() {
            update((state) => ({ ...state, comments: [], error: null }));
        },
    };
}

export const commentsStore = createCommentsStore();

export function getCommentsByTicketId(ticketId: number): TicketComment[] {
    const store = get(commentsStore);
    return store.comments.filter((comment) => comment.ticket.id === ticketId);
}

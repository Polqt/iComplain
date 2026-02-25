import { writable, type Readable } from "svelte/store";
import { fetchComments as apiGetComment, createComment as apiCreateComment, deleteComment as apiDeleteComment, editComment as apiEditComment } from "../lib/api/comment.ts";
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
                const comments = await apiGetComment(ticketId);
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
                    update((state) => {
                        const exists = state.comments.some((c) => c.id === newComment.id);
                        return {
                            ...state,
                            comments: exists ? state.comments : [...state.comments, newComment],
                            error: null,
                        };
                    });
                }

                return newComment;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : "Unknown error";
                update((state) => ({
                    ...state,
                    error: `Failed to create comment: ${errorMessage}`,
                }));
                return null;
            } finally {
                update((state) => ({ ...state, isLoading: false }));
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
                        error: null,
                    }));
                }

                return updatedComment;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : "Unknown error";
                update((state) => ({
                    ...state,
                    error: `Failed to update comment: ${errorMessage}`,
                }));
                return null;
            } finally {
                update((state) => ({ ...state, isLoading: false }));
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
            update((state) => {
                const exists = state.comments.some((c) => c.id === comment.id);
                if (exists) return state;
                return { ...state, comments: [...state.comments, comment] };
            });
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

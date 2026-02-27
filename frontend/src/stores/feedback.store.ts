import { writable, type Readable } from "svelte/store";
import type { FeedbackCreatePayload, FeedbackState, FeedbackUpdatePayload, TicketFeedback } from "../types/feedback.ts";
import * as feedbackAPI from "../lib/api/feedback.ts";

interface FeedbackStore extends Readable<FeedbackState> {
    setTicketFeedback: (feedback: TicketFeedback[]) => void;
    setLoading: (isLoading: boolean) => void;
    setError: (error: string | null) => void;

    loadFeedbackForTicket: (ticketId: number) => Promise<void>;
    createFeedback: (ticketId: number, payload: FeedbackCreatePayload) => Promise<TicketFeedback | null>;
    updateFeedback: (ticketId: number, feedbackId: number, updates: FeedbackUpdatePayload) => Promise<TicketFeedback | null>;
    deleteFeedback: (ticketId: number, feedbackId: number) => Promise<boolean>;
    clearFeedback: () => void;
}

function createFeedbackStore(): FeedbackStore {
    const { subscribe, update, set } = writable<FeedbackState>({
        feedbacks: [],
        isLoading: false,
        error: null,
    });

    return {
        subscribe,
        
        setTicketFeedback(feedbacks: TicketFeedback[]) {
            update(s => ({ ...s, feedbacks, isLoading: false, error: null }));
        },

        setLoading(isLoading: boolean) {
            update(s => ({ ...s, isLoading }));
        },

        setError(error: string | null) {
            update(s => ({ ...s, error, isLoading: false }));
        },

        async loadFeedbackForTicket(ticketId: number): Promise<void> {
            update(s => ({ ...s, isLoading: true, error: null }));
            
            try {
                const feedback = await feedbackAPI.getFeedback(ticketId);
                
                // Feedback endpoint returns single feedback, not array
                update(s => ({
                    ...s,
                    feedbacks: [feedback],
                    isLoading: false,
                    error: null
                }));
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : "Unknown error";
                
                // If 404, it means no feedback exists (not an error state)
                if (errorMessage.includes('404') || errorMessage.includes('No feedback')) {
                    update(s => ({
                        ...s,
                        feedbacks: [],
                        isLoading: false,
                        error: null  // Don't show error for missing feedback
                    }));
                } else {
                    update(s => ({
                        ...s,
                        isLoading: false,
                        error: `Failed to load feedback: ${errorMessage}`
                    }));
                }
            }
        },

        async createFeedback(ticketId: number, payload: FeedbackCreatePayload): Promise<TicketFeedback | null> {
            update(s => ({ ...s, isLoading: true, error: null }));
            
            try {
                const feedback = await feedbackAPI.createFeedback(ticketId, payload);
                
                update(s => ({
                    ...s,
                    feedbacks: [feedback],
                    isLoading: false,
                    error: null
                }));
                
                return feedback;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : "Unknown error";
                update(s => ({
                    ...s,
                    isLoading: false,
                    error: `Failed to create feedback: ${errorMessage}`
                }));
                return null;
            }
        },

        async updateFeedback(ticketId: number, feedbackId: number, updates: FeedbackUpdatePayload): Promise<TicketFeedback | null> {
            update(s => ({ ...s, isLoading: true, error: null }));
            
            try {
                const feedback = await feedbackAPI.updateFeedback(ticketId, feedbackId, updates);
                
                update(s => ({
                    ...s,
                    feedbacks: s.feedbacks.map(f => f.id === feedbackId ? feedback : f),
                    isLoading: false,
                    error: null
                }));
                
                return feedback;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : "Unknown error";
                update(s => ({
                    ...s,
                    isLoading: false,
                    error: `Failed to update feedback: ${errorMessage}`
                }));
                return null;
            }
        },

        async deleteFeedback(ticketId: number, feedbackId: number): Promise<boolean> {
            update(s => ({ ...s, isLoading: true, error: null }));
            
            try {
                await feedbackAPI.deleteFeedback(ticketId, feedbackId);
                
                update(s => ({
                    ...s,
                    feedbacks: s.feedbacks.filter(f => f.id !== feedbackId),
                    isLoading: false,
                    error: null
                }));
                
                return true;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : "Unknown error";
                update(s => ({
                    ...s,
                    isLoading: false,
                    error: `Failed to delete feedback: ${errorMessage}`
                }));
                return false;
            }
        },

        clearFeedback() {
            set({
                feedbacks: [],
                isLoading: false,
                error: null
            });
        }
    };
}

export const feedbackStore = createFeedbackStore();
import { get, writable, type Readable } from "svelte/store";
import type { RawTicket, Ticket, TicketCreatePayload, TicketsState, TicketUpdatePayload } from "../types/tickets.ts";
import { fetchTicketById, fetchTickets, createTicket as apiCreateTicket, updateTicket as apiUpdateTicket, deleteTicket as apiDeleteTicket, adminPatchTicket as apiAdminPatch, loadCommunityTickets as apiGetCommunity } from "../lib/api/ticket.ts";

interface TicketsStore extends Readable<TicketsState> {
    setTickets: (tickets: Ticket[]) => void;
    setLoading: (isLoading: boolean) => void;
    setError: (error: string | null) => void;

    loadTickets: () => Promise<void>;
    loadTicketById: (id: number) => Promise<Ticket | null>;
    createTicket: (ticketData: TicketCreatePayload, attachment?: File) => Promise<Ticket | null>;
    updateTicket: (id: number, updates: TicketUpdatePayload, attachment?: File | null) => Promise<Ticket | null>;
    deleteTicket: (id: number) => Promise<boolean>;
    adminPatchTicket: (id: number, patch: { status?: string; priority?: number }) => Promise<Ticket | null>;
    loadCommunityTickets: () => Promise<void>;

    addTicketToStore: (ticket: Ticket) => void;
    updateTicketInStore: (id: number, updates: Partial<Ticket>) => void;
    removeTicketFromStore: (id: number) => void;
}


function createTicketsStore(): TicketsStore {
    const { subscribe, update, set } = writable<TicketsState>({
        tickets: [],
        isLoading: false,
        error: null,
    });

    return {
        subscribe,
        setTickets(tickets: Ticket[]) {
            set({ tickets, isLoading: false, error: null });
        },

        setLoading(isLoading: boolean) {
            update((state) => ({ ...state, isLoading }));
        },

        setError(error: string | null) {
            update((State) => ({ ...State, error, isLoading: false }));
        },

        async loadCommunityTickets(): Promise<void> {
            update((state) => ({ ...state, isLoading: true, error: null }));

            try {
                const tickets: RawTicket[] = await apiGetCommunity();

                const mappedTickets = tickets.map((t) => ({
                    ...t,
                    category: t.category ?? { id: 0, name: "Unknown" },
                    priority: t.priority ?? { id: 0, name: "Unknown", level: 0, color_code: "#000" },
                }));

                update(s => ({ ...s, tickets: mappedTickets, isLoading: false, error: null }));
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : 'Unknown error';
                update(s => ({
                    ...s,
                    isLoading: false,
                    error: `Failed to load tickets: ${errorMessage}`,
                }))
            }
        },

        async loadTickets(): Promise<void> {
            update((state) => ({ ...state, isLoading: true, error: null }));

            try {
                const tickets: RawTicket[] =  await fetchTickets();
                
                const mappedTickets = tickets.map((t) => ({
                    ...t,
                    category: t.category ?? { id: 0, name: "Unknown" },
                    priority: t.priority ?? { id: 0, name: "Unknown", level: 0, color_code: "#000" },
                }));

                update(s => ({ ...s, tickets: mappedTickets, isLoading: false, error: null }));
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : 'Unknown error';
                update(s => ({
                    ...s,
                    isLoading: false,
                    error: `Failed to load tickets: ${errorMessage}`,
                }))
            }
        },

        async loadTicketById(id: number): Promise<Ticket | null> {
            update(s => ({ ...s, isLoading: true, error: null }));
            
            try {
                const ticket = await fetchTicketById(id);

                update(s => ({
                    ...s,
                    tickets: s.tickets.some((t) => t.id === id)
                        ? s.tickets.map((t) => (t.id === id ? ticket : t))
                        : [...s.tickets, ticket],
                    isLoading: false,
                    error: null,
                }))

                return ticket;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : 'Unknown error';
                update(s => ({
                    ...s,
                    isLoading: false,
                    error: `Failed to load tickets: ${errorMessage}`,
                }))
                return null;
            }
        },

        async createTicket(ticketData: TicketCreatePayload, attachment?: File): Promise<Ticket | null> {
            update(s => ({ ...s, isLoading: true, error: null }));

            try {
                const newTicket = await apiCreateTicket(ticketData, attachment);

                if (newTicket) {
                    update(s => ({
                        ...s,
                        tickets: [newTicket, ...s.tickets],
                        isLoading: false,
                        error: null,
                    }))
                }

                return newTicket
                
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : 'Unknown error';
                update(s => ({
                    ...s,
                    isLoading: false,
                    error: `Failed to load tickets: ${errorMessage}`,
                }))
                return null;
            }
        },

        async updateTicket(id: number, updates: TicketUpdatePayload, attachment?: File | null): Promise<Ticket | null> {
            update(s => ({ ...s, isLoading: true, error: null }));

            try {
                const updatedTicket = await apiUpdateTicket(id, updates, attachment ?? undefined);

                if (updatedTicket) {
                    update(s => ({
                        ...s,
                        tickets: s.tickets.map(t => t.id === id ? updatedTicket : t),
                        isLoading: false,
                        error: null,
                    }))
                }

                return updatedTicket;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : 'Unknown error';
                update(s => ({
                    ...s,
                    isLoading: false,
                    error: `Failed to update ticket: ${errorMessage}`,
                }))
                return null;
            }
        },

        async adminPatchTicket(id: number, patch: { status?: string; priority?: number }) {
            update(s => ({ ...s, isLoading: true, error: null }));
            try {
                const updated = await apiAdminPatch(id, patch);
                update(s => ({
                    ...s,
                    tickets: s.tickets.map(t => t.id === id ? updated : t),
                    isLoading: false,
                }));
                return updated;
            } catch (error) {
                const msg = error instanceof Error ? error.message : 'Update failed';
                update(s => ({ ...s, isLoading: false, error: msg }));
                return null;
            }
        },

        async deleteTicket(id: number): Promise<boolean> {
            update(s => ({ ...s, isLoading: true, error: null }));

            try {
                await apiDeleteTicket(id);

                update(s => ({
                    ...s,
                    tickets: s.tickets.filter(t => t.id !== id),
                    isLoading: false,
                    error: null,
                }))

                return true;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : `Failed to delete ticket ${id}`;
                console.error(`Error deleting ticket ${id}:`, error);
                update((state) => ({
                    ...state,
                    isLoading: false,
                    error: errorMessage,
                }));
                return false;
            }
        },

        addTicketToStore(ticket: Ticket) {
            update(s => ({ ...s, tickets: [ticket, ...s.tickets] }));
        },

        updateTicketInStore(id: number, updates: Partial<Ticket>) {
            update(s => ({ ...s, tickets: s.tickets.map(t => t.id === id ? { ...t, ...updates, updated_at: new Date().toISOString() } : t) }));
        },

        removeTicketFromStore(id: number) {
            update(s => ({ ...s, tickets: s.tickets.filter(t => t.id !== id) }));
        }
        
    };
}

export const ticketsStore = createTicketsStore();

export function getTicketsByStatus(status: string) {
    const store = get(ticketsStore);
    return store.tickets.filter(t => t.status === status);
}

export function getPendingTicketsCount() {
    const store = get(ticketsStore);
    return store.tickets.filter(t => t.status === 'pending').length;
}

export function searchTickets(query: string) {
    const store = get(ticketsStore);
    const lowerQuery= query.toLowerCase();
    return store.tickets.filter(
        t => 
            t.title.toLowerCase().includes(lowerQuery) ||
            t.description.toLowerCase().includes(lowerQuery) ||
            t.ticket_number.toLowerCase().includes(lowerQuery) ||
            t.building.toLowerCase().includes(lowerQuery) ||
            t.room_name.toLowerCase().includes(lowerQuery)
    )
}

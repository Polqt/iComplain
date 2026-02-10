import { writable, type Readable } from "svelte/store";
import type { Ticket, TicketPriority, TicketsState } from "../types/tickets.ts";

interface TicketsStore extends Readable<TicketsState> {
    setTickets: (tickets: Ticket[]) => void;
    addTicket: (ticket: Ticket) => void;
    updateTicket: (id: string, updates: Partial<Ticket>) => void;
    removeTicket: (id: string) => void;
}

// Temporary mock tickets – shared across student views.
const initialTickets: Ticket[] = [
    {
        id: "TKT-001",
        title: "Broken AC Unit in Room 301",
        description:
            "Air conditioning not working properly, temperature control issues...",
        student: {
            id: 1,
            email: "student@example.com",
            is_active: true,
            role: "student",
        },
        category: { id: 1, name: "Facilities" },
        priority: {
            id: 1,
            name: "Low",
            level: 1,
            color_code: "#6b7280",
        } as TicketPriority,
        building: "Main",
        room_name: "Room 301",
        status: "pending",
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        ticket_number: "TKT-001",
        attachments: "3/3",
        comments: 5,
    } as Ticket,
    {
        id: "TKT-002",
        title: "Leaking Faucet in Restroom",
        description: "Water dripping continuously from the main sink...",
        student: {
            id: 2,
            email: "student@example.com",
            is_active: true,
            role: "student",
        },
        category: { id: 2, name: "Plumbing" },
        priority: {
            id: 2,
            name: "Medium",
            level: 2,
            color_code: "#f59e0b",
        } as TicketPriority,
        building: "South",
        room_name: "Restroom A",
        status: "in_progress",
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        ticket_number: "TKT-002",
        attachments: "2/3",
        comments: 12,
    } as Ticket,
    {
        id: "TKT-003",
        title: "Flickering Hallway Lights",
        description:
            "Lights in 3F hallway flickering intermittently during evening hours...",
        student: {
            id: 3,
            email: "student@example.com",
            is_active: true,
            role: "student",
        },
        category: { id: 3, name: "Electrical" },
        priority: {
            id: 3,
            name: "High",
            level: 3,
            color_code: "#dc2626",
        } as TicketPriority,
        building: "North",
        room_name: "Hallway 3F",
        status: "in_progress",
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        ticket_number: "TKT-003",
        attachments: "2/3",
        comments: 8,
    } as Ticket,
    {
        id: "TKT-004",
        title: "Broken Projector Screen",
        description:
            "Projection screen won't retract properly in lecture hall...",
        student: {
            id: 4,
            email: "student@example.com",
            is_active: true,
            role: "student",
        },
        category: { id: 4, name: "AV" },
        priority: {
            id: 1,
            name: "Low",
            level: 1,
            color_code: "#6b7280",
        } as TicketPriority,
        building: "Main",
        room_name: "Lecture Hall A",
        status: "in_progress",
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        ticket_number: "TKT-004",
        attachments: "2/3",
        comments: 3,
    } as Ticket,
];

function createTicketsStore(): TicketsStore {
    const { subscribe, update, set } = writable<TicketsState>({
        tickets: initialTickets,
        isLoading: false,
        error: null,
    });

    return {
        subscribe,
        setTickets(tickets: Ticket[]) {
            set({ tickets, isLoading: false, error: null });
        },
        addTicket(ticket: Ticket) {
            update((state) => ({
                ...state,
                tickets: [...state.tickets, ticket],
            }));
        },
        updateTicket(id: string, updates: Partial<Ticket>) {
            update((state) => ({
                ...state,
                tickets: state.tickets.map((t: Ticket) =>
                    t.id === id ? ({ ...t, ...updates, updated_at: new Date().toISOString() } as Ticket) : t,
                ),
            }));
        },
        removeTicket(id: string) {
            update((state) => ({
                ...state,
                tickets: state.tickets.filter((t: Ticket) => t.id !== id),
            }));
        },
    };
}

export const ticketsStore = createTicketsStore();

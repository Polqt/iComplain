
import type { Ticket } from '../../types/tickets.ts';

const BASE = `${import.meta.env.VITE_API_URL}/tickets`;

async function handleRes<T>(res: Response): Promise<T> {
    if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.message || res.statusText);
    }
    return res.json() as Promise<T>;
}

// Fetch all tickets
export async function fetchTickets(): Promise<Ticket[]> { 
    // Change return type to Promise<Ticket[]>
    const res = await fetch(BASE);
    return handleRes(res);
}

// Fetch ticket by ID
export async function fetchTicketById(id: number): Promise<Ticket> { // Change return type to Promise<Ticket[]>
    const res = await fetch(`${BASE}/${id}`);
    return handleRes(res);
}

export async function createTicket(ticketData: Partial<Ticket>): Promise<Ticket> { // Change return type to Promise<Ticket[]>
    // TODO: Implement ticket creation logic
    const res = await fetch(BASE, {
        method: 'POST',
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(ticketData),
    });

    return handleRes(res);
}


export async function updateTicket(id: number, ticketData: Partial<Ticket>): Promise<Ticket> { 
    // Change return type to Promise<Ticket[]>
    const res = await fetch(`${BASE}/${id}`, {
        method: 'PUT',
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(ticketData),
    });

    return handleRes(res);
}

export async function deleteTicket(id: number): Promise<void> {
    const res = await fetch(`${BASE}/${id}`, {
        method: 'DELETE',
    });

    if (!res.ok) {
        throw new Error('Failed to delete ticket');
    }
}
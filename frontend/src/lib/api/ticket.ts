import { PUBLIC_API_URL } from '$env/static/public';
import type { Ticket } from '../../types/tickets.ts';

const BASE = `${PUBLIC_API_URL}/tickets`;

async function handleRes(res: Response) {
    if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.message || res.statusText);
    }
    return res.json();
}

// Fetch all tickets
export async function fetchTickets(): Promise<void> { // Change return type to Promise<Ticket[]>

}

// Fetch ticket by ID
export async function fetchTicketById(id: number): Promise<void> { // Change return type to Promise<Ticket[]>
    const res = await fetch(`${BASE}/${id}`);

}

export async function createTicket(ticketData: Partial<Ticket>): Promise<void> { // Change return type to Promise<Ticket[]>
    // TODO: Implement ticket creation logic
}

export async function updateTicket(id: number, ticketData: Partial<Ticket>): Promise<void> { // Change return type to Promise<Ticket[]>
    

}

export async function deleteTicket(id: number): Promise<void> {
}
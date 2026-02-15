import { PUBLIC_API_URL } from '$env/static/public';
import type { Category, Ticket, TicketCreatePayload, TicketPriority, TicketUpdatePayload } from '../../types/tickets.ts';

const BASE = `${PUBLIC_API_URL}/tickets`;

async function handleRes<T>(res: Response): Promise<T> {
    if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.message || res.statusText);
    }
    return res.json() as Promise<T>;
}

// Fetch all tickets
export async function fetchTickets(): Promise<Ticket[]> {
    try {
        const res = await fetch(`${BASE}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        })

        return await handleRes<Ticket[]>(res);
    } catch (error) {
        console.error('Error fetching tickets:', error);
        throw error;
    }
}

// Fetch ticket by ID
export async function fetchTicketById(id: number): Promise<Ticket> { 
    try {
        const res = await fetch(`${BASE}/${id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        });

        return await handleRes<Ticket>(res);
    } catch (error) {
        console.error(`Error fetching ticket with ID ${id}:`, error);
        throw error;
    }

}

export async function createTicket(ticketData: TicketCreatePayload, attachment?: File): Promise<Ticket> { 
    try {
        const formData = new FormData();
        formData.append('title', ticketData.title || '');
        formData.append('description', ticketData.description || '');
        formData.append('category', ticketData.category?.toString() || '');
        formData.append('building', ticketData.building || '');
        formData.append('room_name', ticketData.room_name || '');

        if (attachment) {
            formData.append('attachment', attachment);
        }

        const res = await fetch(`${BASE}/`, {
            method: 'POST',
            headers: {
            
            },
            body: formData,
            credentials: 'include',
        })

    return await handleRes<Ticket>(res);
    } catch (error) {
        console.error('Error creating ticket:', error);
        throw error;
    }
}

export async function updateTicket(id: number, ticketData: TicketUpdatePayload, attachment?: File | null): Promise<Ticket> { 
    try {
        const formData = new FormData();

        if (ticketData.title       !== undefined) formData.append('title',       ticketData.title);
        if (ticketData.description !== undefined) formData.append('description', ticketData.description);
        if (ticketData.building    !== undefined) formData.append('building',    ticketData.building);
        if (ticketData.room_name   !== undefined) formData.append('room_name',   ticketData.room_name);
        if (ticketData.category    !== undefined) formData.append('category',    ticketData.category.toString());
        if (ticketData.priority    !== undefined) formData.append('priority',    ticketData.priority.toString());
        if (ticketData.status      !== undefined) formData.append('status',      ticketData.status);

        if (attachment) {
            formData.append('attachment', attachment);
        }

        const res = await fetch(`${BASE}/${id}`, {
            method: 'PUT',
            body: formData,
            credentials: 'include',
        })

        return await handleRes<Ticket>(res);
    } catch (error) {
        console.error(`Error updating ticket with ID ${id}:`, error);
        throw error;
    }
}

export async function adminPatchTicket(id: number, patch: {status?: string; priority?: number }): Promise<Ticket> {
    try {
        const res = await fetch(`${BASE}/${id}/admin`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(patch),
            credentials: 'include',
        });

        return await handleRes<Ticket>(res);
    } catch (error) {
        console.error(`Error patching ticket with ID ${id}:`, error);
        throw error;
    }
}

export async function deleteTicket(id: number): Promise<void> {
    try {
        const res = await fetch(`${BASE}/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        })

        if (!res.ok) {
            const body = await res.json().catch(() => ({}));
            throw new Error(body.message || `Failed to delete ticket with ID ${id}.`);
        }
    } catch (error) {
        console.error('Error deleting ticket:', error);
        throw error;
    }
}

export async function fetchCategories(): Promise<Category[]> {
    const res = await fetch(`${BASE}/categories`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
    });
    if (!res.ok) throw new Error('Failed to fetch categories');
    return res.json() as Promise<Category[]>;
}

export async function fetchPriorities(): Promise<TicketPriority[]> {
    const res = await fetch(`${BASE}/priorities`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
    });
    if (!res.ok) throw new Error('Failed to fetch priorities');
    return res.json() as Promise<TicketPriority[]>;
}

export async function loadCommunityTickets(): Promise<Ticket[]> {
    try {
        const res = await fetch(`${BASE}/`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },

            credentials: 'include',
        });
        if (!res.ok) throw new Error('Failed to fetch community tickets');
        return res.json() as Promise<Ticket[]>;
    } catch (error) {
        console.error(`Error fetching community tickets:`, error);
        throw error;
    }
}
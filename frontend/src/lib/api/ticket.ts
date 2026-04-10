import { apiFetch, resolveApiAssetUrl } from "../../utils/api.ts";
import { parseApiResponse } from "./core.ts";
import type { DashboardStats } from "../../types/dashboard.ts";
import type {
	ActivityLogListResponse,
	Category,
	Ticket,
	TicketCreatePayload,
	TicketListResponse,
	TicketPriority,
	TicketUpdatePayload,
} from "../../types/tickets.ts";

const BASE = "/tickets";

function normalizeTicketAvatar(ticket: Ticket): Ticket {
	return {
		...ticket,
		student: {
			...ticket.student,
			avatar: resolveApiAssetUrl(ticket.student?.avatar),
		},
	};
}

function getFilenameFromDisposition(
	contentDisposition: string | null,
	fallback: string,
): string {
	if (!contentDisposition) return fallback;
	const match = contentDisposition.match(/filename="?([^"]+)"?/i);
	return match?.[1] || fallback;
}

async function downloadFile(
	url: string,
	fallbackFilename: string,
	contentType = "application/octet-stream",
): Promise<void> {
	const res = await apiFetch(url, {
		method: "GET",
	});

	if (!res.ok) {
		const body = await res.json().catch(() => ({}));
		throw new Error(body.message || body.detail || res.statusText);
	}

	const blob = await res.blob();
	const fileBlob = blob.type ? blob : new Blob([blob], { type: contentType });
	const filename = getFilenameFromDisposition(
		res.headers.get("content-disposition"),
		fallbackFilename,
	);

	saveBlob(fileBlob, filename);
}

function saveBlob(blob: Blob, filename: string): void {
	const downloadUrl = URL.createObjectURL(blob);
	const link = document.createElement("a");
	link.href = downloadUrl;
	link.download = filename;
	document.body.appendChild(link);
	link.click();
	link.remove();
	URL.revokeObjectURL(downloadUrl);
}

// Fetch tickets (paginated; defaults to first page of 20)
export async function fetchTickets(limit = 20, offset = 0): Promise<TicketListResponse> {
	try {
		const res = await apiFetch(`${BASE}/?limit=${limit}&offset=${offset}`, {
			method: "GET",
			headers: { "Content-Type": "application/json" },
		});
		const data = await parseApiResponse<TicketListResponse>(res);
		return { ...data, items: data.items.map(normalizeTicketAvatar) };
	} catch (error) {
		console.error("Error fetching tickets:", error);
		throw error;
	}
}

// Fetch ticket by ID
export async function fetchTicketById(id: number): Promise<Ticket> {
	try {
		const res = await apiFetch(`${BASE}/${id}`, {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
			},
		});

		return normalizeTicketAvatar(await parseApiResponse<Ticket>(res));
	} catch (error) {
		console.error(`Error fetching ticket with ID ${id}:`, error);
		throw error;
	}
}

export async function createTicket(ticketData: TicketCreatePayload, attachment?: File | File[] | null): Promise<Ticket> { 
    try {
        const formData = new FormData();
        formData.append('title', ticketData.title || '');
        formData.append('description', ticketData.description || '');
        formData.append('category', ticketData.category?.toString() || '');
        formData.append('building', ticketData.building || '');
        formData.append('room_name', ticketData.room_name || '');

        if (attachment) {
            if (Array.isArray(attachment)) {
                attachment.forEach((f) => formData.append('attachment', f));
            } else {
                formData.append('attachment', attachment);
            }
        }

        const res = await apiFetch(`${BASE}/`, {
            method: 'POST',
            headers: {
            
            },
            body: formData,
        })

	return normalizeTicketAvatar(await parseApiResponse<Ticket>(res));
    } catch (error) {
        console.error('Error creating ticket:', error);
        throw error;
    }
}

export async function updateTicket(id: number, ticketData: TicketUpdatePayload, attachment?: File | File[] | null): Promise<Ticket> { 
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
            if (Array.isArray(attachment)) {
                attachment.forEach((f) => formData.append('attachment', f));
            } else {
                formData.append('attachment', attachment);
            }
        }

        const res = await apiFetch(`${BASE}/${id}`, {
            method: 'PUT',
            body: formData,
        })

		return normalizeTicketAvatar(await parseApiResponse<Ticket>(res));
    } catch (error) {
        console.error(`Error updating ticket with ID ${id}:`, error);
        throw error;
    }
}

export async function adminPatchTicket(
	id: number,
	patch: { status?: string; priority?: number },
): Promise<Ticket> {
	try {
		const res = await apiFetch(`${BASE}/${id}/admin`, {
			method: "PATCH",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(patch),
		});

		return normalizeTicketAvatar(await parseApiResponse<Ticket>(res));
	} catch (error) {
		console.error(`Error patching ticket with ID ${id}:`, error);
		throw error;
	}
}

export async function deleteTicket(id: number): Promise<void> {
	try {
		const res = await apiFetch(`${BASE}/${id}`, {
			method: "DELETE",
			headers: {
				"Content-Type": "application/json",
			},
		});

		if (!res.ok) {
			const body = await res.json().catch(() => ({}));
			throw new Error(
				body.message || body.detail || `Failed to delete ticket with ID ${id}.`,
			);
		}
	} catch (error) {
		console.error("Error deleting ticket:", error);
		throw error;
	}
}

export async function fetchCategories(): Promise<Category[]> {
	const res = await apiFetch(`${BASE}/categories`, {
		method: "GET",
		headers: { "Content-Type": "application/json" },
	});
	if (!res.ok) throw new Error("Failed to fetch categories");
	return res.json() as Promise<Category[]>;
}

export async function fetchPriorities(): Promise<TicketPriority[]> {
	const res = await apiFetch(`${BASE}/priorities`, {
		method: "GET",
		headers: { "Content-Type": "application/json" },
	});
	if (!res.ok) throw new Error("Failed to fetch priorities");
	return res.json() as Promise<TicketPriority[]>;
}

export async function loadCommunityTickets(
	limit = 20,
	offset = 0,
): Promise<TicketListResponse> {
	try {
		const res = await apiFetch(
			`${BASE}/community?limit=${limit}&offset=${offset}`,
			{
				method: "GET",
				headers: { "Content-Type": "application/json" },
			},
		);
		const data = await parseApiResponse<TicketListResponse>(res);
		return { ...data, items: data.items.map(normalizeTicketAvatar) };
	} catch (error) {
		console.error(`Error fetching community tickets:`, error);
		throw error;
	}
}

export async function getDashboardStats(): Promise<DashboardStats> {
	try {
		const res = await apiFetch(`${BASE}/stats/dashboard`, {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
			},
		});

		return await parseApiResponse<DashboardStats>(res);
	} catch (error) {
		console.error("Error fetching dashboard stats:", error);
		throw error;
	}
}
export async function getActivityLogs(
	limit = 50,
	offset = 0,
	ticketId?: number,
): Promise<ActivityLogListResponse> {
	try {
		const params = new URLSearchParams({
			limit: limit.toString(),
			offset: offset.toString(),
		});

		if (ticketId !== undefined && ticketId !== null) {
			params.append("ticket_id", ticketId.toString());
		}

		const res = await apiFetch(`${BASE}/activity/?${params}`, {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
			},
		});

		return await parseApiResponse<ActivityLogListResponse>(res);
	} catch (error) {
		console.error("Error fetching activity logs:", error);
		throw error;
	}
}

type CsvExportParams = {
	startDate?: string;
	endDate?: string;
};

export async function exportDashboardCsv(params: CsvExportParams = {}): Promise<void> {
	try {
		const query = new URLSearchParams();
		if (params.startDate) query.set("start_date", params.startDate);
		if (params.endDate) query.set("end_date", params.endDate);
		const suffix = query.toString() ? `?${query}` : "";

		await downloadFile(
			`${BASE}/stats/dashboard/export-csv${suffix}`,
			`tickets-export-${new Date().toISOString().slice(0, 10)}.csv`,
			"text/csv;charset=utf-8",
		);
	} catch (error) {
		console.error("Error exporting dashboard CSV:", error);
		throw error;
	}
}

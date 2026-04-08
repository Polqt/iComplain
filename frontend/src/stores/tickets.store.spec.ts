import { get } from "svelte/store";
import { beforeEach, describe, expect, it, vi } from "vitest";

const {
	fetchTicketsMock,
	fetchTicketByIdMock,
	createTicketMock,
	updateTicketMock,
	deleteTicketMock,
	adminPatchMock,
	loadCommunityMock,
} = vi.hoisted(() => ({
	fetchTicketsMock: vi.fn(),
	fetchTicketByIdMock: vi.fn(),
	createTicketMock: vi.fn(),
	updateTicketMock: vi.fn(),
	deleteTicketMock: vi.fn(),
	adminPatchMock: vi.fn(),
	loadCommunityMock: vi.fn(),
}));

vi.mock("../lib/api/ticket.ts", () => ({
	fetchTickets: fetchTicketsMock,
	fetchTicketById: fetchTicketByIdMock,
	createTicket: createTicketMock,
	updateTicket: updateTicketMock,
	deleteTicket: deleteTicketMock,
	adminPatchTicket: adminPatchMock,
	loadCommunityTickets: loadCommunityMock,
}));

import { ticketsStore } from "./tickets.store.ts";

const ticket = {
	id: 1,
	ticket_number: "TKT-00001",
	title: "Broken chair",
	description: "Leg is loose",
	student: {
		id: 2,
		email: "student@usls.edu.ph",
		is_active: true,
		role: "student" as const,
	},
	category: { id: 1, name: "Facilities" },
	priority: { id: 2, name: "Medium", level: 2, color_code: "#f59e0b" },
	building: "Main",
	room_name: "M102",
	status: "pending" as const,
	created_at: new Date().toISOString(),
	updated_at: new Date().toISOString(),
	comments_count: 0,
};

describe("ticketsStore", () => {
	beforeEach(() => {
		fetchTicketsMock.mockReset();
		fetchTicketByIdMock.mockReset();
		createTicketMock.mockReset();
		updateTicketMock.mockReset();
		deleteTicketMock.mockReset();
		adminPatchMock.mockReset();
		loadCommunityMock.mockReset();
		ticketsStore.setTickets([]);
	});

	it("loadTickets stores API tickets", async () => {
		fetchTicketsMock.mockResolvedValue([ticket]);

		await ticketsStore.loadTickets();
		const state = get(ticketsStore);

		expect(state.currentView).toBe("personal");
		expect(state.tickets).toHaveLength(1);
		expect(state.tickets[0].ticket_number).toBe("TKT-00001");
	});

	it("loadCommunityTickets switches view and stores tickets", async () => {
		loadCommunityMock.mockResolvedValue([ticket]);

		await ticketsStore.loadCommunityTickets();
		const state = get(ticketsStore);

		expect(state.currentView).toBe("community");
		expect(state.tickets).toHaveLength(1);
	});

	it("createTicket prepends new ticket", async () => {
		createTicketMock.mockResolvedValue(ticket);

		const created = await ticketsStore.createTicket({
			title: ticket.title,
			description: ticket.description,
			category: ticket.category.id,
			building: ticket.building,
			room_name: ticket.room_name,
		});

		const state = get(ticketsStore);
		expect(created?.id).toBe(ticket.id);
		expect(state.tickets[0].id).toBe(ticket.id);
	});
});

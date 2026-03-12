import type { User } from "./user.ts";

export type RawTicket = Omit<Ticket, "category" | "priority"> & {
	category?: Category | null;
	priority?: TicketPriority | null;
};

export type Category = {
	id: number;
	name: string;
};

export type TicketStatus = "pending" | "in_progress" | "resolved" | "closed";

export type TicketPriority = {
	id: number;
	name: string;
	level: number;
	color_code: string;
};

export type Ticket = {
	id: number;
	ticket_number: string;
	title: string;
	description: string;
	student: User;
	category: Category;
	priority: TicketPriority;
	building: string;
	room_name: string;
	status: TicketStatus;
	attachment?: string;
	created_at: string;
	updated_at: string;
	comments_count?: number;
	has_feedback?: boolean;
	feedback_rating?: number | null;
};

export type TicketCreatePayload = {
	title: string;
	description: string;
	category: number;
	building: string;
	room_name: string;
};

export type TicketUpdatePayload = {
	title?: string;
	description?: string;
	category?: number;
	priority?: number;
	building?: string;
	room_name?: string;
	status?: TicketStatus;
};

export type TicketColumn = {
	id: TicketStatus;
	title: string;
	color: string;
	dotColor: string;
	reports: Ticket[];
};

export type Column = {
	id: TicketStatus;
	title: string;
	color: string;
	dotColor: string;
};

export type TicketsState = {
	tickets: Ticket[];
	isLoading: boolean;
	error: string | null;
	currentView: "personal" | "community";
};

export type PipelineStep = {
	id: TicketStatus;
	label: string;
	icon: string;
};

export type ViewMode = "grid" | "list";

export type ModalMode = "create" | "edit" | "delete" | null;

export type AdminTicketEdit = "status" | "priority" | null;

export type ActivityLog = {
	id: number;
	action:
		| "created"
		| "status_changed"
		| "priority_changed"
		| "assigned"
		| "commented"
		| "reopened"
		| "resolved"
		| "feedback";
	ticket_number: string;
	ticket_title: string;
	performed_by: {
		id: number;
		name: string | null;
		email: string;
		avatar: string | null;
	} | null;
	description: string;
	old_value: string | null;
	new_value: string | null;
	created_at: string;
};

export type ActivityLogListResponse = {
	items: ActivityLog[];
	total: number;
	limit: number;
	offset: number;
};

export type TicketListResponse = {
	items: Ticket[];
	total: number;
	limit: number;
	offset: number;
};

import { apiFetch } from "../../utils/api.ts";
import type { Notification } from "../../types/notifications.ts";
import { parseApiResponse } from "./core.ts";

const BASE = "/notifications";
const INAPP = `${BASE}/inapp`;

export async function fetchNotifications(
	limit: number = 50,
): Promise<Notification[]> {
	const res = await apiFetch(`${INAPP}/?limit=${limit}`, {
		method: "GET",
		headers: { Accept: "application/json" },
	});
	const data = await parseApiResponse<Notification[]>(res);
	return (data ?? []) as Notification[];
}

export async function markAsRead(id: string): Promise<Notification> {
	const res = await apiFetch(`${INAPP}/${id}/`, {
		method: "PATCH",
		headers: { "Content-Type": "application/json", Accept: "application/json" },
		body: JSON.stringify({ read: true }),
	});
	return parseApiResponse<Notification>(res);
}

export async function markAllAsRead(): Promise<{ marked: number }> {
	const res = await apiFetch(`${INAPP}/mark-all-read/`, {
		method: "POST",
		headers: { Accept: "application/json" },
	});
	return parseApiResponse<{ marked: number }>(res);
}

export async function deleteNotification(id: string): Promise<void> {
	const res = await apiFetch(`${INAPP}/${id}/`, {
		method: "DELETE",
		headers: { Accept: "application/json" },
	});
	if (!res.ok) await parseApiResponse<{ ok: true }>(res);
}

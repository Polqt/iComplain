import { PUBLIC_API_URL } from "$env/static/public";
import type { Notification } from "../../types/notifications.ts";

const BASE = `${PUBLIC_API_URL}/notifications`;
const INAPP = `${BASE}/inapp`;

async function handleRes(res: Response) {
    if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error((body as { detail?: string }).detail || res.statusText);
    }
    return res.json();
}

export async function fetchNotifications(limit: number = 50): Promise<Notification[]> {
    const res = await fetch(`${INAPP}/?limit=${limit}`, {
        method: "GET",
        credentials: "include",
        headers: { Accept: "application/json" },
    });
    const data = await handleRes(res);
    return (data ?? []) as Notification[];
}

export async function markAsRead(id: string): Promise<Notification> {
    const res = await fetch(`${INAPP}/${id}/`, {
        method: "PATCH",
        credentials: "include",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({ read: true }),
    });
    return handleRes(res) as Promise<Notification>;
}

export async function markAllAsRead(): Promise<{ marked: number }> {
    const res = await fetch(`${INAPP}/mark-all-read/`, {
        method: "POST",
        credentials: "include",
        headers: { Accept: "application/json" },
    });
    return handleRes(res) as Promise<{ marked: number }>;
}

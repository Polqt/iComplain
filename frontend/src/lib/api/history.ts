import { apiFetch } from "../../utils/api.ts";
import type { HistoryItem } from "../../types/history.ts";

const BASE = "/tickets";

export async function fetchTicketHistory(): Promise<HistoryItem[]> {
    const res = await apiFetch(`${BASE}/history`, {
        method: "GET",
        headers: { Accept: "application/json" },
    });
    if (!res.ok) {
        throw new Error(
            res.status === 401 ? "Unauthorized" : "Failed to load history",
        );
    }
    const data = await res.json();
    return (data ?? []) as HistoryItem[];
}

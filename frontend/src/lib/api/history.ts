import { PUBLIC_API_URL } from "$env/static/public";
import type { HistoryItem } from "../../types/history.ts";

const BASE = `${PUBLIC_API_URL}/tickets`;

export async function fetchTicketHistory(): Promise<HistoryItem[]> {
  const res = await fetch(`${BASE}/history`, {
    method: "GET",
    credentials: "include",
    headers: { Accept: "application/json" },
  });
  if (!res.ok) {
    throw new Error(res.status === 401 ? "Unauthorized" : "Failed to load history");
  }
  const data = await res.json();
  return (data ?? []) as HistoryItem[];
}

export async function fetchAdminTicketHistory(): Promise<HistoryItem[]> {
  const res = await fetch(`${BASE}/admin/history`, {
    method: "GET",
    credentials: "include",
    headers: { Accept: "application/json" },
  });
  if (!res.ok) {
    if (res.status === 403) {
      throw new Error("You do not have permission to view admin history");
    }
    throw new Error(res.status === 401 ? "Unauthorized" : "Failed to load admin history");
  }
  const data = await res.json();
  return (data ?? []) as HistoryItem[];
}

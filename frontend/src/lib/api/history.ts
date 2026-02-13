import { PUBLIC_API_URL } from "$env/static/public";
import type { HistoryItem } from "../../types/history.ts";


export async function fetchTicketHistory(): Promise<HistoryItem[]> {
  const res = await fetch(`${PUBLIC_API_URL}/tickets/history`, {
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

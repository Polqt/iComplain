import type { TicketStatus } from "../types/tickets.ts";

export const COMMUNITY_PAGE_SIZE = 10;

export const COMMUNITY_STATUSES: TicketStatus[] = [
  "pending",
  "in_progress",
  "resolved",
  "closed",
];

export function createInitialPageState(): Record<TicketStatus, number> {
  return {
    pending: 1,
    in_progress: 1,
    resolved: 1,
    closed: 1,
  };
}

export function getTotalPages(
  count: number,
  pageSize: number = COMMUNITY_PAGE_SIZE,
): number {
  return Math.max(1, Math.ceil(count / pageSize));
}

export function getPageSlice<T>(
  items: T[],
  page: number,
  pageSize: number = COMMUNITY_PAGE_SIZE,
): T[] {
  const safePage = page < 1 ? 1 : page;
  const start = (safePage - 1) * pageSize;
  return items.slice(start, start + pageSize);
}


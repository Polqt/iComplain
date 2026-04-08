import { get } from "svelte/store";
import { beforeEach, describe, expect, it, vi } from "vitest";

const { fetchNotificationsMock, markAsReadMock, markAllAsReadMock } = vi.hoisted(
	() => ({
		fetchNotificationsMock: vi.fn(),
		markAsReadMock: vi.fn(),
		markAllAsReadMock: vi.fn(),
	}),
);

vi.mock("../lib/api/notifications.ts", () => ({
	fetchNotifications: fetchNotificationsMock,
	markAsRead: markAsReadMock,
	markAllAsRead: markAllAsReadMock,
}));

import { notificationStore } from "./notification.store.ts";

const n1 = {
	id: "1",
	type: "info" as const,
	title: "Created",
	message: "Ticket created",
	timestamp: new Date().toISOString(),
	read: false,
};

const n2 = {
	id: "2",
	type: "success" as const,
	title: "Resolved",
	message: "Ticket resolved",
	timestamp: new Date().toISOString(),
	read: true,
};

describe("notificationStore", () => {
	beforeEach(() => {
		fetchNotificationsMock.mockReset();
		markAsReadMock.mockReset();
		markAllAsReadMock.mockReset();
		notificationStore.clear();
	});

	it("loadNotifications sets notifications and unread count", async () => {
		fetchNotificationsMock.mockResolvedValue([n1, n2]);

		await notificationStore.loadNotifications();
		const state = get(notificationStore);

		expect(state.notifications).toHaveLength(2);
		expect(state.unreadCount).toBe(1);
	});

	it("markAsRead updates unread count", async () => {
		fetchNotificationsMock.mockResolvedValue([n1]);
		markAsReadMock.mockResolvedValue({ ...n1, read: true });
		await notificationStore.loadNotifications();

		await notificationStore.markAsRead("1");
		const state = get(notificationStore);

		expect(state.unreadCount).toBe(0);
		expect(state.notifications[0].read).toBe(true);
	});

	it("markAllAsRead marks all local notifications as read", async () => {
		fetchNotificationsMock.mockResolvedValue([n1, { ...n1, id: "3", read: false }]);
		markAllAsReadMock.mockResolvedValue({ marked: 2 });
		await notificationStore.loadNotifications();

		await notificationStore.markAllAsRead();
		const state = get(notificationStore);

		expect(state.unreadCount).toBe(0);
		expect(state.notifications.every((n) => n.read)).toBe(true);
	});
});

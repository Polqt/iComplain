import { writable, get, type Readable } from "svelte/store";
import type { Notification, NotificationState } from "../types/notifications.ts";
import { fetchNotifications, markAsRead as apiMarkAsRead, markAllAsRead as apiMarkAllAsRead } from "../lib/api/notifications.ts";


interface NotificationStore extends Readable<NotificationState> {
    loadNotifications: (limit?: number) => Promise<void>;
    addNotification: (notification: Notification) => void;
    markAsRead: (id: string) => Promise<void>;
    markAllAsRead: () => Promise<void>;
    clear: () => void;
}

function createNotificationStore(): NotificationStore {
    const { subscribe, update, set } = writable<NotificationState>({
        notifications: [],
        unreadCount: 0,
        isLoading: false,
    });

    return {
        subscribe,

        async loadNotifications(limit: number = 50) {
            update((s) => ({ ...s, isLoading: true }));
            try {
                const list = await fetchNotifications(limit);
                const unreadCount = list.filter((n) => !n.read).length;
                update(() => ({ notifications: list, unreadCount, isLoading: false }));
            } catch (e) {
                console.error("Failed to load notifications:", e);
                update((s) => ({ ...s, isLoading: false }));
            }
        },

        addNotification(notification: Notification) {
            update((s) => ({
                notifications: [notification, ...s.notifications],
                unreadCount: s.unreadCount + (notification.read ? 0 : 1),
                isLoading: false,
            }));
        },

        async markAsRead(id: string) {
            try {
                await apiMarkAsRead(id);
                update((s) => {
                    const notifications = s.notifications.map((n) =>
                        n.id === id ? { ...n, read: true } : n,
                    );
                    return {
                        ...s,
                        notifications,
                        unreadCount: notifications.filter((n) => !n.read).length,
                    };
                });
            } catch (e) {
                console.error("Failed to mark notification as read:", e);
            }
        },

        async markAllAsRead() {
            try {
                await apiMarkAllAsRead();
                update((s) => ({
                    ...s,
                    notifications: s.notifications.map((n) => ({ ...n, read: true })),
                    unreadCount: 0,
                }));
            } catch (e) {
                console.error("Failed to mark all as read:", e);
            }
        },

        clear() {
            set({ notifications: [], unreadCount: 0, isLoading: false });
        },
    };
}

export const notificationStore = createNotificationStore();

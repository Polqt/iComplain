export type Notification = {
    id: string;
    type: "info" | "success" | "warning" | "error";
    title: string;
    message: string;
    timestamp: string;
    read: boolean;
    actionUrl?: string;
    actionLabel?: string;
}

export type NotificationState = {
    notifications: Notification[];
    unreadCount: number;
    isLoading: boolean;
}

export type NotificationFilter = "all" | "unread" | "read";

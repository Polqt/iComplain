<script lang="ts">
  import Icon from "@iconify/svelte";
  import type {
    NotificationFilter,
    Notification,
  } from "../../../types/notifications.ts";
  import { notificationConfig } from "../../../utils/notifications.ts";
  import StudentLayout from "../../layout/StudentLayout.svelte";

  let notifications: Notification[] = [
    {
      id: "1",
      type: "success",
      title: "Report Resolved",
      message:
        "Your report about the broken AC unit in Room 301 has been marked as resolved.",
      timestamp: "5 minutes ago",
      read: false,
      actionUrl: "/student/reports/1",
      actionLabel: "View Report",
    },
    {
      id: "2",
      type: "info",
      title: "Report Update",
      message:
        "Your leaking faucet report is now being reviewed by maintenance staff.",
      timestamp: "2 hours ago",
      read: false,
      actionUrl: "/student/reports/2",
      actionLabel: "View Details",
    },
    {
      id: "3",
      type: "warning",
      title: "Pending Review",
      message:
        "Your report needs additional information. Please update it with more details.",
      timestamp: "1 day ago",
      read: true,
      actionUrl: "/student/reports/3",
      actionLabel: "Update Report",
    },
    {
      id: "4",
      type: "info",
      title: "New Comment",
      message:
        "Admin responded to your question about the hallway lights issue.",
      timestamp: "2 days ago",
      read: true,
      actionUrl: "/student/reports/4",
      actionLabel: "Read Comment",
    },
    {
      id: "5",
      type: "success",
      title: "Report Approved",
      message:
        "Your facility report has been approved and forwarded to maintenance.",
      timestamp: "3 days ago",
      read: true,
    },
    {
      id: "6",
      type: "error",
      title: "Report Rejected",
      message:
        "Your report was rejected due to insufficient details. Please resubmit.",
      timestamp: "1 week ago",
      read: true,
      actionUrl: "/student/new-report",
      actionLabel: "Resubmit",
    },
  ];

  let activeFilter: NotificationFilter = "all";

  $: filteredNotifications = notifications.filter((n) => {
    if (activeFilter === "unread") return !n.read;
    if (activeFilter === "read") return n.read;
    return true;
  });

  $: unreadCount = notifications.filter((n) => !n.read).length;

  function markAsRead(notificationId: string) {
    notifications = notifications.map((n) =>
      n.id === notificationId ? { ...n, read: true } : n,
    );
    // TODO: Call API to mark as read
    // await api.markNotificationAsRead(notificationId);
  }

  function markAllAsRead() {
    notifications = notifications.map((n) => ({ ...n, read: true }));
    // TODO: Call API to mark all as read
    // await api.markAllNotificationsAsRead();
  }

  function deleteNotification(notificationId: string) {
    notifications = notifications.filter((n) => n.id !== notificationId);
    // TODO: Call API to delete notification
    // await api.deleteNotification(notificationId);
  }

  // TODO: Load notifications from API on mount
  // onMount(async () => {
  //   notifications = await api.getNotifications();
  // });
</script>

<StudentLayout>
  <div class="flex flex-col h-[calc(100vh-8rem)]">
    <div class="shrink-0 mb-6">
      <h1 class="text-2xl font-black text-base-content mb-1">Notifications</h1>
      <p class="text-sm text-base-content/60">
        Stay updated with the latest alerts and messages.
      </p>
    </div>

    <div class="flex items-center justify-between mb-6 shrink-0">
      <div class="tabs tabs-boxed bg-base-200 p-1">
        <button
          class="tab {activeFilter === 'all' ? 'tab-active' : ''}"
          onclick={() => (activeFilter = "all")}
        >
          All
          <span class="badge badge-sm ml-2">{notifications.length}</span>
        </button>
        <button
          class="tab {activeFilter === 'unread' ? 'tab-active' : ''}"
          onclick={() => (activeFilter = "unread")}
        >
          Unread
          {#if unreadCount > 0}
            <span class="badge badge-primary badge-sm ml-2">{unreadCount}</span>
          {/if}
        </button>
        <button
          class="tab {activeFilter === 'read' ? 'tab-active' : ''}"
          onclick={() => (activeFilter = "read")}
        >
          Read
        </button>
      </div>

      {#if unreadCount > 0}
        <button class="btn btn-sm btn-outline" onclick={markAllAsRead}>
          <Icon icon="mdi:check-all" width="16" height="16" />
          Mark All as Read
        </button>
      {/if}
    </div>

    {#if filteredNotifications.length > 0}
      <div class="mb-4 shrink-0">
        <p class="text-sm text-base-content/60">
          You have <span class="font-semibold text-primary"
            >{filteredNotifications.length}</span
          >
          {activeFilter === "all"
            ? "notifications"
            : activeFilter === "unread"
              ? "unread notifications"
              : "read notifications"}.
        </p>
      </div>
    {/if}

    <div class="flex-1 overflow-y-auto space-y-3 pr-2">
      {#if filteredNotifications.length === 0}
        <div
          class="flex flex-col items-center justify-center h-full text-center py-12"
        >
          <Icon
            icon="mdi:bell-outline"
            width="64"
            height="64"
            class="text-base-content/20 mb-4"
          />
          <h3 class="text-lg font-semibold text-base-content/80 mb-1">
            No notifications
          </h3>
          <p class="text-sm text-base-content/50">
            {activeFilter === "unread"
              ? "You're all caught up! No unread notifications."
              : activeFilter === "read"
                ? "No read notifications yet."
                : "You don't have any notifications at the moment."}
          </p>
        </div>
      {:else}
        {#each filteredNotifications as notification}
          <div
            class="card bg-base-100 border border-base-content/10 shadow-sm hover:shadow-md transition-all duration-200 {!notification.read
              ? 'border-l-4 ' +
                notificationConfig[notification.type].borderColor
              : ''}"
          >
            <div class="card-body p-4">
              <div class="flex items-start gap-4">
                <div class="shrink-0">
                  <div
                    class="w-10 h-10 rounded-full {notificationConfig[
                      notification.type
                    ].bgColor} flex items-center justify-center"
                  >
                    <Icon
                      icon={notificationConfig[notification.type].icon}
                      width="20"
                      height="20"
                      class={notificationConfig[notification.type].iconColor}
                    />
                  </div>
                </div>

                <div class="flex-1 min-w-0">
                  <div class="flex items-start justify-between gap-2 mb-2">
                    <h3 class="font-semibold text-base text-base-content">
                      {notification.title}
                    </h3>
                    {#if !notification.read}
                      <div
                        class="w-2 h-2 rounded-full bg-primary shrink-0 mt-2"
                      ></div>
                    {/if}
                  </div>

                  <p class="text-sm text-base-content/70 mb-3">
                    {notification.message}
                  </p>

                  <div class="flex items-center justify-between">
                    <div class="flex items-center gap-3">
                      <span class="text-xs text-base-content/50">
                        <Icon
                          icon="mdi:clock-outline"
                          width="12"
                          height="12"
                          class="inline mr-1"
                        />
                        {notification.timestamp}
                      </span>

                      {#if notification.actionUrl}
                        <a
                          href={notification.actionUrl}
                          class="text-xs text-primary hover:underline font-medium"
                        >
                          {notification.actionLabel || "View"}
                          <Icon
                            icon="mdi:arrow-right"
                            width="12"
                            height="12"
                            class="inline ml-1"
                          />
                        </a>
                      {/if}
                    </div>

                    <div class="flex items-center gap-1">
                      {#if !notification.read}
                        <button
                          class="btn btn-ghost btn-xs"
                          onclick={() => markAsRead(notification.id)}
                          title="Mark as read"
                        >
                          <Icon icon="mdi:check" width="14" height="14" />
                        </button>
                      {/if}
                      <button
                        class="btn btn-ghost btn-xs"
                        onclick={() => deleteNotification(notification.id)}
                        title="Delete"
                      >
                        <Icon
                          icon="mdi:delete-outline"
                          width="14"
                          height="14"
                        />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        {/each}
      {/if}
    </div>
  </div>
</StudentLayout>

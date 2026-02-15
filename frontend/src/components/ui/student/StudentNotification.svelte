<script lang="ts">
  import { onMount } from "svelte";
  import Icon from "@iconify/svelte";
  import type {
    NotificationFilter,
    Notification,
  } from "../../../types/notifications.ts";
  import {
    notificationConfig,
    formatNotificationTimestamp,
  } from "../../../utils/notificationConfig.ts";
  import StudentLayout from "../../layout/StudentLayout.svelte";
  import {
    fetchNotifications,
    markAsRead as apiMarkAsRead,
    markAllAsRead as apiMarkAllAsRead,
    deleteNotification as apiDeleteNotification,
  } from "../../../lib/api/notifications.ts";

  let notifications: Notification[] = [];
  let loading = true;
  let activeFilter: NotificationFilter = "all";
  let markError = "";
  let deleteError = "";
  let fetchError = "";

  $: filteredNotifications = notifications.filter((n) => {
    if (activeFilter === "unread") return !n.read;
    if (activeFilter === "read") return n.read;
    return true;
  });

  $: unreadCount = notifications.filter((n) => !n.read).length;

  async function markAsRead(notificationId: string) {
    markError = "";
    try {
      await apiMarkAsRead(notificationId);
      notifications = notifications.map((n) =>
        n.id === notificationId ? { ...n, read: true } : n,
      );
    } catch (e) {
      console.error("Failed to mark notification as read", e);
      markError = "Could not update read status.";
      setTimeout(() => (markError = ""), 3000);
    }
  }

  async function markAllAsRead() {
    markError = "";
    try {
      await apiMarkAllAsRead();
      notifications = notifications.map((n) => ({ ...n, read: true }));
    } catch (e) {
      console.error("Failed to mark all as read", e);
      markError = "Could not update read status.";
      setTimeout(() => (markError = ""), 3000);
    }
  }

  async function deleteNotification(notificationId: string) {
    deleteError = "";
    try {
      await apiDeleteNotification(notificationId);
      notifications = notifications.filter((n) => n.id !== notificationId);
    } catch (e) {
      console.error("Failed to delete notification", e);
      deleteError = "Could not delete notification. Please try again.";
      setTimeout(() => (deleteError = ""), 4000);
    }
  }

  async function loadNotifications() {
    try {
      loading = true;
      fetchError = "";
      const list = await fetchNotifications();
      notifications = list.map((n) => ({
        ...n,
        timestamp: formatNotificationTimestamp(n.timestamp),
      }));
    } catch (e) {
      console.error("Failed to load notifications", e);
      fetchError = "Could not load notifications. Please try again.";
    } finally {
      loading = false;
    }
  }

  onMount(() => {
    loadNotifications();
  });
</script>

<svelte:head>
  <title>Student Notifications - iComplain</title>
</svelte:head>

<StudentLayout>
  <div class="flex flex-col h-[calc(100vh-8rem)]">
    <div class="shrink-0 mb-6">
      <h1 class="text-2xl font-black text-base-content mb-1">Notifications</h1>
      <p class="text-sm text-base-content/60">
        Stay updated with the latest alerts and messages.
      </p>
    </div>

    {#if markError}
      <div class="alert alert-warning mb-4 shrink-0" role="alert">
        <span>{markError}</span>
      </div>
    {/if}
    {#if deleteError}
      <div class="toast toast-top toast-end z-9999">
        <div class="alert alert-error shadow-lg rounded-xl gap-2 text-sm">
          <span>{deleteError}</span>
          <button
            type="button"
            class="btn btn-ghost btn-xs rounded-lg ml-1"
            onclick={() => (deleteError = '')}
            aria-label="Dismiss"
          >✕</button>
        </div>
      </div>
    {/if}
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
      {#if loading}
        <div class="flex flex-col items-center justify-center py-12 text-base-content/60">
          Loading notifications…
        </div>
      {:else if fetchError}
        <div
          class="flex flex-col items-center justify-center h-full text-center py-12"
        >
          <div class="alert alert-error shadow-lg max-w-md">
            <Icon icon="mdi:alert-circle-outline" width="24" height="24" />
            <div class="flex flex-col gap-2 items-center">
              <span>{fetchError}</span>
              <button
                type="button"
                class="btn btn-sm btn-primary"
                onclick={loadNotifications}
              >
                Retry
              </button>
            </div>
          </div>
        </div>
      {:else if filteredNotifications.length === 0}
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

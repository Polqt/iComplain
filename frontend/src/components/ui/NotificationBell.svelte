<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { goto } from "$app/navigation";
  import type { Notification } from "../../types/notifications.ts";
  import Icon from "@iconify/svelte";

  export let notifications: Notification[] = [];
  export let unreadCount: number = 0;
  export let viewAllHref: string = "/notifications";

  export let notificationsConfig: Record<
    string,
    { icon: string; bgColor: string; iconColor: string }
  >;

  const dispatch = createEventDispatcher<{
    markAsRead: { id: string };
    notificationClick: { notification: Notification };
    viewAll: void;
  }>();

  function handleMarkAsRead(id: string, event: Event) {
    event.stopPropagation();
    dispatch("markAsRead", { id });
  }

  function handleNotificationClick(notification: Notification) {
    if (!notification.read) {
      dispatch("markAsRead", { id: notification.id });
    }
    dispatch("notificationClick", { notification });
    if (notification.actionUrl) {
      goto(notification.actionUrl);
    }
  }

  function handleViewAll() {
    dispatch("viewAll");
  }

  $: previewNotifications = notifications.slice(0, 5);
</script>

<div class="dropdown dropdown-end">
  <button
    type="button"
    tabindex="0"
    class="btn btn-ghost btn-circle hover:scale-105 transition-transform relative"
    aria-label="Notifications"
  >
    <Icon icon="lucide:bell" width="20" height="20" />
    {#if unreadCount > 0}
      <span class="absolute top-1 right-1 flex w-5 h-5">
        <span
          class="animate-ping absolute inline-flex w-full h-full rounded-full bg-primary opacity-75"
        ></span>
        <span
          class="relative inline-flex items-center justify-center rounded-full w-5 h-5 bg-primary text-primary-content text-xs font-bold"
        >
          {unreadCount > 9 ? "9+" : unreadCount}
        </span>
      </span>
    {/if}
  </button>

  <div
    class="dropdown-content menu bg-base-100 rounded-box w-96 p-0 shadow-xl border border-base-content/10 z-100 mt-3"
  >
    <div
      class="flex items-center justify-between px-4 py-3 border-b border-base-content/10"
    >
      <h3 class="font-bold text-base">Notifications</h3>
      {#if unreadCount > 0}
        <span class="badge badge-primary badge-sm">{unreadCount} new</span>
      {/if}
    </div>

    <div class="max-h-96 overflow-y-auto">
      {#if previewNotifications.length === 0}
        <div
          class="flex flex-col items-center justify-center py-12 px-4 text-center"
        >
          <Icon
            icon="mdi:bell-outline"
            width="48"
            height="48"
            class="text-base-content/20 mb-2"
          />
          <p class="text-sm text-base-content/60">No notifications yet</p>
        </div>
      {:else}
        {#each previewNotifications as notification}
          <button
            type="button"
            class="w-full flex items-start gap-3 px-4 py-3 hover:bg-base-200 transition-colors border-b border-base-content/5 last:border-b-0 text-left {!notification.read
              ? 'bg-primary/5'
              : ''}"
            onclick={() => handleNotificationClick(notification)}
          >
            <div class="shrink-0 mt-0.5">
              <div
                class="w-8 h-8 rounded-full {notificationsConfig[
                  notification.type
                ].bgColor} flex items-center justify-center"
              >
                <Icon
                  icon={notificationsConfig[notification.type].icon}
                  width="16"
                  height="16"
                  class={notificationsConfig[notification.type].iconColor}
                />
              </div>
            </div>

            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2 mb-1">
                <p class="font-semibold text-sm text-base-content line-clamp-1">
                  {notification.title}
                </p>
                {#if !notification.read}
                  <div
                    class="w-2 h-2 rounded-full bg-primary shrink-0 mt-1.5"
                  ></div>
                {/if}
              </div>
              <p class="text-xs text-base-content/70 line-clamp-2 mb-1">
                {notification.message}
              </p>
              <div class="flex items-center justify-between">
                <span class="text-xs text-base-content/50"
                  >{notification.timestamp}</span
                >
                {#if !notification.read}
                  <span
                    role="button"
                    tabindex="0"
                    class="text-xs text-primary hover:underline cursor-pointer"
                    onclick={(e) => handleMarkAsRead(notification.id, e)}
                    onkeydown={(e) =>
                      e.key === "Enter" && handleMarkAsRead(notification.id, e)}
                    aria-label="Mark as read"
                  >
                    Mark as read
                  </span>
                {/if}
              </div>
            </div>
          </button>
        {/each}
      {/if}
    </div>

    {#if notifications.length > 0}
      <div class="border-t border-base-content/10">
        <a
          href={viewAllHref}
          class="block text-center py-3 text-sm font-medium text-primary hover:bg-base-200 transition-colors"
          onclick={handleViewAll}
        >
          View All Notifications
          <Icon
            icon="mdi:arrow-right"
            width="14"
            height="14"
            class="inline ml-1"
          />
        </a>
      </div>
    {/if}
  </div>
</div>

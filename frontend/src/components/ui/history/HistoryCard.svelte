<script lang="ts">
  import { browser } from "$app/environment";
  import { onDestroy } from "svelte";
  import Icon from "@iconify/svelte";
  import type { HistoryItem } from "../../../types/history.ts";
  import { historyConfig, statusConfig, priorityConfig } from "../../../utils/historyConfig.ts";

  export let item: HistoryItem;
  /** Base path for "View Ticket" link; item.ticketPk is appended (e.g. "/tickets"). */
  export let ticketUrlPrefix: string = "/tickets";

  let menuOpen = false;
  let menuButtonEl: HTMLButtonElement;

  function handleToggleMenu() {
    menuOpen = !menuOpen;
  }

  function handleMenuKeydown(e: KeyboardEvent) {
    if (e.key === "Escape") menuOpen = false;
  }

  $: menuId = `history-card-menu-${item.id}`;

  function formatRelativeTime(isoOrDate: string): string {
    const d = new Date(isoOrDate);
    if (Number.isNaN(d.getTime())) return item.date;
    const now = new Date();
    const sec = Math.floor((now.getTime() - d.getTime()) / 1000);
    if (sec < 60) return "just now";
    const mins = Math.floor(sec / 60);
    if (sec < 3600) return mins === 1 ? "1 min ago" : `${mins} mins ago`;
    const hours = Math.floor(sec / 3600);
    if (sec < 86400) return hours === 1 ? "1 hour ago" : `${hours} hours ago`;
    const days = Math.floor(sec / 86400);
    if (sec < 604800) return days === 1 ? "1 day ago" : `${days} days ago`;
    return item.date;
  }

  $: timeLabel = formatRelativeTime(item.timestamp);

  function handleClickOutside(e: MouseEvent) {
    const target = e.target as Node;
    if (menuOpen && menuButtonEl && !menuButtonEl.contains(target)) {
      const menuEl = document.getElementById(menuId);
      if (menuEl && !menuEl.contains(target)) menuOpen = false;
    }
  }

  $: if (browser) {
    if (menuOpen) {
      document.addEventListener("click", handleClickOutside);
    } else {
      document.removeEventListener("click", handleClickOutside);
    }
  }

  onDestroy(() => {
    if (browser) document.removeEventListener("click", handleClickOutside);
  });
</script>

<svelte:window on:keydown={handleMenuKeydown} />

<div
  class="card bg-base-100 shadow-sm hover:shadow-md transition-all duration-200 border border-base-content/5"
>
  <div class="card-body p-4">
    <div class="flex items-start justify-between gap-3 mb-3">
      <div class="flex-1 min-w-0">
        <div class="flex items-center gap-2 mb-2">
          <span
            class="badge badge-sm {historyConfig[item.action].color} {historyConfig[item.action].bgColor} border-0"
          >
            {historyConfig[item.action].label}
          </span>
          <span class="text-xs text-base-content/50">
            {item.ticketId}
          </span>
        </div>
        <h3 class="font-semibold text-base text-base-content mb-1">
          {item.title}
        </h3>
        <p class="text-sm text-base-content/70">
          {item.description}
        </p>
      </div>
      <div class="relative shrink-0">
        <button
          type="button"
          class="btn btn-ghost btn-xs btn-circle"
          aria-haspopup="menu"
          aria-expanded={menuOpen}
          aria-controls={menuId}
          aria-label="Open actions menu"
          bind:this={menuButtonEl}
          on:click={handleToggleMenu}
        >
          <Icon icon="mdi:dots-horizontal" width="16" height="16" />
        </button>
        {#if menuOpen}
          <ul
            id={menuId}
            role="menu"
            class="absolute right-0 top-full mt-1 menu bg-base-100 rounded-box w-40 p-2 shadow-lg border border-base-content/10 z-10"
          >
            <li role="none">
              <a
                role="menuitem"
                href={`${ticketUrlPrefix}/${item.ticketPk}`}
                class="gap-2"
              >
                <Icon icon="mdi:eye-outline" width="16" height="16" />
                View Ticket
              </a>
            </li>
          </ul>
        {/if}
      </div>
    </div>

    <div class="flex items-center justify-between pt-3 border-t border-base-content/5">
      <div class="flex items-center gap-3 text-xs text-base-content/60">
        <div class="flex items-center gap-1">
          <Icon icon="mdi:clock-outline" width="14" height="14" />
          <span>{timeLabel}</span>
        </div>
        <div class="flex items-center gap-1">
          <Icon icon="mdi:calendar-outline" width="14" height="14" />
          <span>{item.date}</span>
        </div>
        {#if item.category}
          <div class="flex items-center gap-1">
            <Icon icon="mdi:tag-outline" width="14" height="14" />
            <span>{item.category}</span>
          </div>
        {/if}
      </div>

      <div class="flex items-center gap-2">
        <div class="badge {statusConfig[item.status].color} badge-sm">
          {statusConfig[item.status].label}
        </div>
        <div class="badge {priorityConfig[item.priority].color} badge-sm">
          {priorityConfig[item.priority].label}
        </div>
      </div>
    </div>

    <div class="mt-3">
      <a
        href={`${ticketUrlPrefix}/${item.ticketPk}`}
        class="btn btn-sm btn-outline btn-primary w-full sm:w-auto"
      >
        <Icon icon="mdi:eye-outline" width="16" height="16" />
        View Ticket
      </a>
    </div>
  </div>
</div>

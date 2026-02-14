<script lang="ts">
  import { browser } from "$app/environment";
  import { onDestroy } from "svelte";
  import Icon from "@iconify/svelte";
  import type { HistoryItem } from "../../../types/history.ts";
  import {
    historyConfig,
    statusConfig,
    priorityConfig,
    formatRelativeTime,
  } from "../../../utils/historyConfig.ts";
  import { goto } from "$app/navigation";

  export let item: HistoryItem;

  function navigate() {
    goto(`tickets/${item.ticketId}`);
  }

  let menuOpen = false;

  function handleMenuKeydown(e: KeyboardEvent) {
    if (e.key === "Escape") menuOpen = false;
  }

  $: menuId = `history-card-menu-${item.id}`;
  $: timeLabel = formatRelativeTime(item.timestamp, item.date);

  function handleClickOutside(e: MouseEvent) {
    const target = e.target as Node;
    if (menuOpen) {
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
  role="button"
  tabindex="0"
  aria-label="View ticket {item.ticketId}"
  onclick={navigate}
  onkeydown={(e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      navigate();
    }
  }}
  class="card bg-base-100 shadow-sm hover:shadow-md transition-all duration-200 border border-base-content/5 cursor-pointer hover:border-primary/20 hover:shadow-primary/5 active:scale-[0.995]"
>
  <div class="card-body p-4">
    <div class="flex items-start justify-between gap-3 mb-3">
      <div class="flex-1 min-w-0">
        <div class="flex items-center gap-2 mb-2">
          <span
            class="badge badge-sm {historyConfig[item.action]
              .color} {historyConfig[item.action].bgColor} border-0"
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
    </div>

    <div
      class="flex items-center justify-between pt-3 border-t border-base-content/5"
    >
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
  </div>
</div>

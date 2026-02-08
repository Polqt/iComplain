<script lang="ts">
  import Icon from "@iconify/svelte";
  import type { HistoryItem } from "../../../types/history.js";
  import { historyConfig, statusConfig, priorityConfig } from "../../../utils/history.js";

  export let item: HistoryItem;
  /** Base URL for "View Ticket" link, e.g. "/student/tickets". Item.ticketId is appended. */
  export let ticketUrlPrefix: string = "/student/tickets";
</script>

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
      <button type="button" class="btn btn-ghost btn-xs btn-circle shrink-0">
        <Icon icon="mdi:dots-horizontal" width="16" height="16" />
      </button>
    </div>

    <div class="flex items-center justify-between pt-3 border-t border-base-content/5">
      <div class="flex items-center gap-3 text-xs text-base-content/60">
        <div class="flex items-center gap-1">
          <Icon icon="mdi:clock-outline" width="14" height="14" />
          <span>{item.timestamp}</span>
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
        href="{ticketUrlPrefix}/{item.ticketId}"
        class="btn btn-sm btn-outline btn-primary w-full sm:w-auto"
      >
        <Icon icon="mdi:eye-outline" width="16" height="16" />
        View Ticket
      </a>
    </div>
  </div>
</div>

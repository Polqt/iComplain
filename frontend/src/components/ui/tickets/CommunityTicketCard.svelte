<script lang="ts">
  import Icon from "@iconify/svelte";
  import type { Ticket } from "../../../types/tickets.ts";
  import {
    columns,
    getPriorityKey,
    priorityDot,
  } from "../../../utils/ticketConfig.ts";
  import { formatDate } from "../../../utils/date.ts";
  import { goto } from "$app/navigation";

  export let ticket: Ticket;

  function navigateToTicket() {
    goto(`/tickets/${ticket.ticket_number}`);
  }

  $: commentCount = (ticket as any).comments_count ?? 0;

  $: priorityKey = getPriorityKey(ticket.priority);
  $: priorityColor = priorityDot[priorityKey] ?? priorityDot.low;

  $: statusConfig = columns.find((c) => c.id === ticket.status);
  $: statusColor = statusConfig?.dot ?? "bg-base-content/25";
</script>

<div
  class="card bg-base-100 border border-base-300 hover:border-primary/30
         transition-all duration-200 cursor-pointer hover:shadow-md"
  role="button"
  tabindex="0"
  aria-label={`Open ticket ${ticket.title}`}
  onclick={navigateToTicket}
  onkeydown={(e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      navigateToTicket();
    }
  }}
>
  <div class="card-body p-4">
    <div class="flex items-start gap-4">
      <div class="w-1 h-full rounded-full shrink-0 {priorityColor}"></div>

      <div class="flex-1 min-w-0">
        <div class="flex items-center gap-2 mb-2 flex-wrap">
          <span class="text-xs font-mono text-base-content/60 font-medium">
            {ticket.ticket_number}
          </span>
          <span class="badge badge-sm badge-outline">
            {ticket.category.name}
          </span>
        </div>

        <h3 class="font-semibold text-base mb-2 text-base-content line-clamp-2">
          {ticket.title}
        </h3>

        <div
          class="flex items-center gap-4 text-sm text-base-content/60 flex-wrap"
        >
          <div class="flex items-center gap-1.5">
            <Icon icon="mdi:map-marker" width="16" height="16" />
            <span class="text-xs">{ticket.building} - {ticket.room_name}</span>
          </div>

          <div class="flex items-center gap-1.5">
            <Icon icon="mdi:account-circle" width="16" height="16" />
            <span class="text-xs">{ticket.student.name || "Anonymous"}</span>
          </div>

          <div class="flex items-center gap-1.5">
            <Icon icon="mdi:comment-outline" width="16" height="16" />
            <span class="text-xs font-medium">{commentCount}</span>
          </div>
        </div>
      </div>

      <div class="text-right shrink-0 flex flex-col items-end gap-2">
        <div class="text-xs text-base-content/60">
          {formatDate(ticket.created_at)}
        </div>
        <div
          class="badge badge-sm gap-1.5 border-0"
          style="background-color: {statusColor.replace('bg-', '')}20; 
                 color: {statusColor.replace('bg-', '')}"
        >
          <span class="w-1.5 h-1.5 rounded-full {statusColor}"></span>
          <span class="text-[10px] font-bold uppercase tracking-wide">
            {statusConfig?.label ?? ticket.status}
          </span>
        </div>
      </div>
    </div>
  </div>
</div>

<script lang="ts">
  import Icon from "@iconify/svelte";
  import {
    baseColumns,
    getPriorityKey,
    priorityConfig,
  } from "../../../utils/ticketConfig.ts";
  import type { Ticket, TicketColumn } from "../../../types/tickets.ts";
  import { ticketsStore } from "../../../stores/tickets.store.ts";
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";
  import { authStore } from "../../../stores/auth.store.ts";
  import { formatDate } from "../../../utils/date.ts";

  let expandedTicketId: number | null = null;

  $: ({ tickets, isLoading } = $ticketsStore);
  $: ({ role } = $authStore);

  onMount(async () => {
    if ($ticketsStore.tickets.length === 0) {
      await ticketsStore.loadTickets();
    }
  });

  $: columns = baseColumns.map(
    (col): TicketColumn => ({
      ...col,
      reports: tickets.filter((t) => t.status === col.id),
    }),
  );

  function toggleExpand(ticketId: number) {
    if (expandedTicketId === ticketId) {
      expandedTicketId = null;
    } else {
      expandedTicketId = ticketId;
    }
  }

  function navigateToFullView(ticket: Ticket) {
    if (role === "admin") {
      goto(`/admin/tickets/${ticket.id}`);
    } else {
      goto(`/tickets/${ticket.ticket_number}`);
    }
  }
</script>

<div class="mb-6 shrink-0">
  <h1 class="text-2xl font-black text-base-content mb-1">
    Ticket Status Board
  </h1>
  <p class="text-sm text-base-content/60">Click any ticket to expand details</p>
</div>

{#if isLoading}
  <div class="grid grid-cols-4 gap-4">
    {#each [1, 2, 3, 4] as _}
      <div class="flex flex-col gap-3">
        <div class="skeleton h-12 rounded-xl"></div>
        <div class="skeleton h-20 rounded-xl"></div>
        <div class="skeleton h-20 rounded-xl"></div>
      </div>
    {/each}
  </div>
{:else if tickets.length === 0}
  <div
    class="flex flex-col items-center justify-center gap-3 py-16 text-base-content/40"
  >
    <Icon icon="mdi:ticket-outline" width="48" height="48" />
    <p class="text-sm font-medium">No tickets yet</p>
  </div>
{:else}
  <div class="grid grid-cols-4 gap-4 h-full min-h-0">
    {#each columns as column}
      <div class="flex flex-col min-h-0 h-full">
        <div
          class="flex items-center justify-between px-4 py-3 mb-3 rounded-xl
                 bg-base-200/60 border border-base-content/8 shrink-0"
        >
          <div class="flex items-center gap-2 min-w-0">
            <div class="w-2 h-2 rounded-full {column.dotColor} shrink-0"></div>
            <h2
              class="font-bold text-xs uppercase tracking-wider {column.color} truncate"
            >
              {column.title}
            </h2>
          </div>
          <div class="badge badge-sm badge-ghost font-mono">
            {column.reports.length}
          </div>
        </div>

        <div class="flex flex-col gap-2 overflow-y-auto flex-1 min-h-0 pr-1">
          {#each column.reports as ticket (ticket.id)}
            {@const isExpanded = expandedTicketId === ticket.id}
            {@const priorityKey = getPriorityKey(ticket.priority)}

            <div
              class="bg-base-100 rounded-xl border border-base-content/8
                     hover:border-base-content/15 transition-all duration-200
                     overflow-hidden {isExpanded ? 'shadow-md' : 'shadow-sm'}"
            >
              <button
                type="button"
                class="w-full text-left p-3 hover:bg-base-200/50 transition-colors duration-150"
                onclick={() => toggleExpand(ticket.id)}
              >
                <div class="flex items-start justify-between gap-2 mb-2">
                  <h3
                    class="font-semibold text-sm text-base-content line-clamp-2 flex-1"
                  >
                    {ticket.title}
                  </h3>
                  <Icon
                    icon={isExpanded ? "mdi:chevron-up" : "mdi:chevron-down"}
                    width="16"
                    height="16"
                    class="text-base-content/40 shrink-0 mt-0.5 transition-transform duration-200"
                  />
                </div>

                <div class="flex items-center gap-2 flex-wrap">
                  <span
                    class="text-[10px] font-mono text-base-content/40 tracking-wide"
                  >
                    {ticket.ticket_number}
                  </span>
                  <div
                    class="badge badge-xs {priorityConfig[priorityKey].color}"
                  >
                    {priorityConfig[priorityKey].label}
                  </div>
                </div>
              </button>

              {#if isExpanded}
                <div
                  class="border-t border-base-content/8 bg-base-200/30 p-4 space-y-3
                         animate-accordion-down"
                >
                  <!-- Description -->
                  <div>
                    <p class="text-xs text-base-content/50 mb-1 font-semibold">
                      Description
                    </p>
                    <p class="text-sm text-base-content/70 leading-relaxed">
                      {ticket.description}
                    </p>
                  </div>

                  <!-- Location -->
                  <div class="flex items-start gap-2">
                    <Icon
                      icon="mdi:map-marker"
                      width="14"
                      height="14"
                      class="text-base-content/40 mt-0.5 shrink-0"
                    />
                    <div class="min-w-0">
                      <p class="text-xs font-medium text-base-content/70">
                        {ticket.building}
                      </p>
                      <p class="text-[11px] text-base-content/50">
                        {ticket.room_name}
                      </p>
                    </div>
                  </div>

                  <!-- Student -->
                  <div class="flex items-center gap-2">
                    <Icon
                      icon="mdi:account"
                      width="14"
                      height="14"
                      class="text-base-content/40 shrink-0"
                    />
                    <p class="text-xs text-base-content/60 truncate">
                      {ticket.student.name || ticket.student.email}
                    </p>
                  </div>

                  <!-- Category & Date -->
                  <div class="flex items-center gap-3 text-xs">
                    <div class="flex items-center gap-1.5">
                      <Icon
                        icon="mdi:tag"
                        width="12"
                        height="12"
                        class="text-base-content/40"
                      />
                      <span class="text-base-content/60"
                        >{ticket.category.name}</span
                      >
                    </div>
                    <div class="flex items-center gap-1.5">
                      <Icon
                        icon="mdi:calendar"
                        width="12"
                        height="12"
                        class="text-base-content/40"
                      />
                      <span class="text-base-content/50"
                        >{formatDate(ticket.created_at)}</span
                      >
                    </div>
                  </div>

                  <!-- Comments Count -->
                  {#if (ticket.comments_count ?? 0) > 0}
                    <div class="flex items-center gap-1.5 text-xs">
                      <Icon
                        icon="mdi:comment-outline"
                        width="12"
                        height="12"
                        class="text-base-content/40"
                      />
                      <span class="text-base-content/50"
                        >{ticket.comments_count ?? 0} comment{(ticket.comments_count ??
                          0) !== 1
                          ? "s"
                          : ""}</span
                      >
                    </div>
                  {/if}

                  <!-- Action Button -->
                  <button
                    type="button"
                    class="btn btn-primary btn-sm w-full gap-1.5 mt-2"
                    onclick={() => navigateToFullView(ticket)}
                  >
                    <Icon icon="mdi:open-in-new" width="14" height="14" />
                    View Full Details
                  </button>
                </div>
              {/if}
            </div>
          {/each}

          {#if column.reports.length === 0}
            <div
              class="flex flex-col items-center justify-center py-8 text-center
                     border-2 border-dashed border-base-content/8 rounded-xl"
            >
              <Icon
                icon="mdi:inbox-outline"
                width="24"
                height="24"
                class="text-base-content/15 mb-2"
              />
              <p class="text-xs text-base-content/30 font-medium">No tickets</p>
            </div>
          {/if}
        </div>
      </div>
    {/each}
  </div>
{/if}

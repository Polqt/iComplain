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
    goto(`/tickets/${ticket.id}`);
  }

  function getAgingDays(createdAt: string): number {
    const created = new Date(createdAt);
    const now = new Date();
    return Math.floor((now.getTime() - created.getTime()) / (1000 * 60 * 60 * 24));
  }

  function getAgingLabel(days: number): string {
    if (days === 0) return "Today";
    if (days === 1) return "1 day ago";
    if (days < 7) return `${days}d ago`;
    if (days < 30) return `${Math.floor(days / 7)}w ago`;
    return `${Math.floor(days / 30)}mo ago`;
  }

  function getAgingColor(days: number): string {
    if (days > 14) return "text-error bg-error/10"; // Critical: Over 2 weeks
    if (days > 7) return "text-warning bg-warning/10"; // Warning: Over 1 week
    return "text-info bg-info/10"; // Normal
  }

  function getPriorityBgColor(priorityKey: string): string {
    switch (priorityKey) {
      case "high":
      case "urgent":
        return "bg-red-50 border-red-200 dark:bg-red-950/40 dark:border-red-700";
      case "medium":
        return "bg-amber-50 border-amber-200 dark:bg-amber-950/40 dark:border-amber-700";
      case "low":
        return "bg-blue-50 border-blue-200 dark:bg-blue-950/40 dark:border-blue-700";
      default:
        return "bg-base-100 border-base-content/5";
    }
  }

  function getPriorityBadgeColor(priorityKey: string): string {
    const config = priorityConfig[priorityKey as keyof typeof priorityConfig];
    if (!config) return "badge-ghost";
    
    // Return semantic badge color with better dark mode support
    switch (priorityKey) {
      case "high":
      case "urgent":
        return "bg-red-600 dark:bg-red-700 text-white font-bold";
      case "medium":
        return "bg-amber-500 dark:bg-amber-600 text-white dark:text-black font-bold";
      case "low":
        return "bg-blue-600 dark:bg-blue-700 text-white font-bold";
      default:
        return "badge-ghost";
    }
  }
</script>

<div class="space-y-4 shrink-0 mb-6">
  <div class="flex items-center justify-between">
    <div>
      <h2 class="text-2xl font-black text-base-content mb-1">Ticket Status Board</h2>
      <p class="text-sm text-base-content/60 font-medium">Kanban view - Click any ticket to expand</p>
    </div>
    <div class="flex items-center gap-3 text-xs text-base-content/50">
      <span class="inline-flex items-center gap-1.5">
        <div class="w-2 h-2 rounded-full bg-red-600 dark:bg-red-500"></div>
        High Priority
      </span>
      <span class="inline-flex items-center gap-1.5">
        <div class="w-2 h-2 rounded-full bg-amber-500 dark:bg-amber-400"></div>
        Medium
      </span>
      <span class="inline-flex items-center gap-1.5">
        <div class="w-2 h-2 rounded-full bg-blue-600 dark:bg-blue-500"></div>
        Low
      </span>
    </div>
  </div>
</div>

{#if isLoading}
  <div class="grid grid-cols-4 gap-4">
    {#each [1, 2, 3, 4] as _}
      <div class="flex flex-col gap-3">
        <div class="skeleton h-12 rounded-xl"></div>
        <div class="skeleton h-24 rounded-xl"></div>
        <div class="skeleton h-24 rounded-xl"></div>
        <div class="skeleton h-24 rounded-xl"></div>
      </div>
    {/each}
  </div>
{:else if tickets.length === 0}
  <div
    class="flex flex-col items-center justify-center gap-3 py-24 text-base-content/40"
  >
    <Icon icon="mdi:ticket-outline" width="56" height="56" class="opacity-50" />
    <p class="text-sm font-semibold">No tickets yet</p>
  </div>
{:else}
  <div class="grid grid-cols-4 gap-4 h-full min-h-0">
    {#each columns as column}
      <div class="flex flex-col min-h-0 h-full bg-base-200/20 rounded-2xl overflow-hidden border border-base-content/5">
        <!-- Column Header -->
        <div class="flex items-center justify-between px-4 py-4 border-b border-base-content/10 shrink-0 bg-gradient-to-r from-base-100/50 to-transparent">
          <div class="flex items-center gap-2 min-w-0">
            <div class="w-2.5 h-2.5 rounded-full {column.dotColor} shrink-0"></div>
            <h3 class="font-bold text-sm text-base-content truncate">
              {column.title}
            </h3>
          </div>
          <div class="badge badge-sm badge-ghost font-bold text-xs flex-shrink-0">
            {column.reports.length}
          </div>
        </div>

        <!-- Cards Container -->
        <div class="flex flex-col gap-3 overflow-y-auto flex-1 min-h-0 p-3">
          {#each column.reports as ticket (ticket.id)}
            {@const isExpanded = expandedTicketId === ticket.id}
            {@const priorityKey = getPriorityKey(ticket.priority)}
            {@const agingDays = getAgingDays(ticket.created_at)}
            {@const showAgingWarning = agingDays > 7}

            <div
              class="rounded-lg border-2 transition-all duration-200 overflow-hidden
                     {isExpanded ? 'shadow-md ring-1 ring-primary/30' : 'shadow-sm hover:shadow-md hover:border-base-content/15'}
                     {getPriorityBgColor(priorityKey)}"
            >
              <!-- Card Header (Always Visible) -->
              <button
                type="button"
                class="w-full text-left p-3 focus:outline-none transition-colors duration-150 hover:bg-black/5 dark:hover:bg-white/5"
                onclick={() => toggleExpand(ticket.id)}
              >
                <!-- Title Row -->
                <div class="flex items-start justify-between gap-2 mb-2">
                  <h4 class="font-bold text-sm text-base-content line-clamp-2 flex-1 leading-snug">
                    {ticket.title}
                  </h4>
                  <Icon
                    icon={isExpanded ? "mdi:chevron-up" : "mdi:chevron-down"}
                    width="18"
                    height="18"
                    class="text-base-content/40 shrink-0 transition-transform duration-200"
                  />
                </div>

                <!-- Ticket Number & Priority Badge -->
                <div class="flex items-center gap-2 mb-2">
                  <span class="text-xs font-mono font-semibold text-base-content/60">
                    {ticket.ticket_number}
                  </span>
                  <span class="inline-flex items-center px-2 py-1 rounded text-xs font-bold {getPriorityBadgeColor(priorityKey)}">
                    {priorityConfig[priorityKey].label}
                  </span>
                </div>

                <!-- Aging & Metadata Row -->
                <div class="flex items-center gap-2 text-xs">
                  <div class="inline-flex items-center gap-1 px-2 py-1 rounded-full {getAgingColor(agingDays)}">
                    <Icon icon="mdi:clock-outline" width="12" height="12" />
                    <span class="font-semibold">{getAgingLabel(agingDays)}</span>
                  </div>
                  {#if (ticket.comments_count ?? 0) > 0}
                    <div class="inline-flex items-center gap-1 text-base-content/60">
                      <Icon icon="mdi:comment-outline" width="12" height="12" />
                      <span>{ticket.comments_count}</span>
                    </div>
                  {/if}
                </div>
              </button>

              <!-- Expanded Details -->
              {#if isExpanded}
                <div
                  class="border-t border-black/10 dark:border-white/10 bg-gradient-to-br from-base-100/60 to-transparent p-4 space-y-3 animate-accordion-down"
                >
                  <!-- Location -->
                  <div class="flex items-start gap-2">
                    <Icon
                      icon="mdi:map-marker"
                      width="14"
                      height="14"
                      class="text-base-content/40 mt-0.5 flex-shrink-0"
                    />
                    <div class="min-w-0">
                      <p class="text-xs font-semibold text-base-content/80">
                        {ticket.building}
                      </p>
                      <p class="text-xs text-base-content/50">
                        {ticket.room_name}
                      </p>
                    </div>
                  </div>

                  <!-- Category -->
                  {#if ticket.category?.name}
                    <div class="flex items-center gap-2 text-xs">
                      <Icon
                        icon="mdi:tag"
                        width="12"
                        height="12"
                        class="text-base-content/40 flex-shrink-0"
                      />
                      <span class="px-2 py-1 rounded-full bg-base-content/5 text-base-content/70 font-medium">
                        {ticket.category.name}
                      </span>
                    </div>
                  {/if}

                  <!-- Student -->
                  <div class="flex items-center gap-2 text-xs">
                    <Icon
                      icon="mdi:account-circle"
                      width="14"
                      height="14"
                      class="text-base-content/40 flex-shrink-0"
                    />
                    <p class="text-base-content/70 truncate">
                      {ticket.student.name || ticket.student.email}
                    </p>
                  </div>

                  <!-- Description -->
                  <div>
                    <p class="text-xs text-base-content/50 mb-1 font-semibold uppercase tracking-wide">
                      Description
                    </p>
                    <p class="text-xs text-base-content/70 leading-relaxed line-clamp-3">
                      {ticket.description}
                    </p>
                  </div>

                  <!-- Action Button -->
                  <button
                    type="button"
                    class="btn btn-primary btn-sm w-full gap-1.5 mt-2 font-bold"
                    onclick={() => navigateToFullView(ticket)}
                  >
                    <Icon icon="mdi:open-in-new" width="14" height="14" />
                    Open Details
                  </button>
                </div>
              {/if}
            </div>
          {/each}

          <!-- Empty State -->
          {#if column.reports.length === 0}
            <div
              class="flex flex-col items-center justify-center py-12 text-center text-base-content/30"
            >
              <Icon
                icon="mdi:inbox-outline"
                width="32"
                height="32"
                class="mb-2 opacity-40"
              />
              <p class="text-xs font-medium">No tickets</p>
            </div>
          {/if}
        </div>
      </div>
    {/each}
  </div>
{/if}

<style>
  :global(.animate-accordion-down) {
    animation: accordion-down 0.2s ease-out;
  }

  @keyframes accordion-down {
    from {
      opacity: 0;
      transform: translateY(-4px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
</style>

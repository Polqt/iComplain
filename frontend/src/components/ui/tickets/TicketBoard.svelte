<script lang="ts">
  import Icon from "@iconify/svelte";
  import {
    baseColumns,
    getPriorityKey,
    priorityConfig,
    statusConfig,
  } from "../../../utils/ticketConfig.ts";
  import type {
    Ticket,
    TicketColumn,
    ViewMode,
  } from "../../../types/tickets.ts";
  import { ticketsStore } from "../../../stores/tickets.store.ts";
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";
  
  let viewMode: ViewMode = "grid";

  $: ({ tickets, isLoading } = $ticketsStore);

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

  function navigate(t: Ticket) {
    goto(`/tickets/${t.ticket_number}`);
  }
</script>

<div class="flex items-center justify-between mb-6 shrink-0">
  <h1 class="text-2xl font-black text-base-content">Ticket Status Board</h1>

  <div class="flex items-center gap-2 bg-base-200 p-1 rounded-lg">
    <button
      class="btn btn-sm {viewMode === 'list' ? 'btn-primary' : 'btn-ghost'}"
      onclick={() => (viewMode = "list")}
    >
      <Icon icon="mdi:format-list-bulleted" width="18" height="18" />
      List
    </button>
    <button
      class="btn btn-sm {viewMode === 'grid' ? 'btn-primary' : 'btn-ghost'}"
      onclick={() => (viewMode = "grid")}
    >
      <Icon icon="mdi:view-grid-outline" width="18" height="18" />
      Board
    </button>
  </div>
</div>

{#if isLoading}
  <div class="flex gap-6 pb-4 flex-1 overflow-x-auto overyflow-y-hidden">
    {#each [1, 2, 3, 4] as _}
      <div
        class="flex flex-col shrink-0 w-80 bg-base-100 shadow-sm rounded-lg h-64"
      >
        <div class="p-4 border-b border-base-content/5">
          <div class="skeleton w-28 h-4 rounded"></div>
        </div>
        <div class="flex flex-col gap-3 p-4">
          <div class="skeleton h-20 rounded-xl"></div>
          <div class="skeleton h-20 rounded-xl"></div>
        </div>
      </div>
    {/each}
  </div>
{:else if tickets.length === 0}
  <div
    class="flex-1 flex flex-col items-center justify-center gap-3 text-base-content/40"
  >
    <Icon icon="mdi:ticket-outline" width="48" height="48" />
    <p class="text-sm font-medium">No tickets yet</p>
  </div>
{:else if viewMode === "grid"}
  <div class="flex gap-6 pb-4 flex-1 overflow-x-auto overflow-y-hidden">
    {#each columns as column}
      <div
        class="flex flex-col shrink-0 w-80 bg-base-100 dark:bg-base-100 shadow rounded-lg h-full"
      >
        <div
          class="flex items-center justify-between p-4 border-b border-base-content/5 shrink-0"
        >
          <div class="flex items-center gap-2">
            <div class="w-2 h-2 rounded-full {column.dotColor}"></div>
            <h2 class="font-semibold text-sm {column.color}">
              {column.title}
            </h2>
            <div class="badge badge-sm badge-ghost">
              {column.reports.length}
            </div>
          </div>
        </div>

        <div class="flex flex-col gap-3 p-4 overflow-y-auto flex-1 max-h-130">
          {#each column.reports as report}
            <div
              role="button"
              tabindex="0"
              aria-label={`Open ticket ${report.title}`}
              onclick={() => navigate(report)}
              onkeydown={(e) => {
                if (e.key === "Enter" || e.key === " ") {
                  e.preventDefault();
                  navigate(report);
                }
              }}
              class="card bg-base-200 dark:bg-base-300 shadow-sm hover:shadow-md transition-all duration-200 border border-base-content/5 shrink-0 cursor-pointer"
            >
              <div class="card-body p-4">
                <div class="flex items-center justify-between mb-3">
                  <div
                    class="badge badge-sm {statusConfig[report.status].color}"
                  >
                    {statusConfig[report.status].label}
                  </div>
                </div>

                <h3
                  class="font-semibold text-base text-base-content mb-2 line-clamp-2"
                >
                  {report.title}
                </h3>

                <p class="text-sm text-base-content/60 mb-3 line-clamp-2">
                  {report.description}
                </p>
              </div>
            </div>
          {/each}
        </div>
      </div>
    {/each}
  </div>
{:else}
  <div class="flex-1 overflow-y-auto space-y-2 pr-2">
    {#each columns as column}
      {#each column.reports as report}
        <div
          role="button"
          tabindex="0"
          aria-label={`Open ticket ${report.title}`}
          onclick={() => navigate(report)}
          onkeydown={(e) => {
            if (e.key === "Enter" || e.key === " ") {
              e.preventDefault();
              navigate(report);
            }
          }}
          class="card bg-base-100 shadow-sm hover:shadow-md transition-all duration-200 border border-base-content/5 cursor-pointer hover:border-primary/20"
        >
          <div class="card-body p-4">
            <div class="flex items-center gap-4">
              <div
                class="badge badge-sm whitespace-nowrap {statusConfig[
                  report.status
                ].color}"
              >
                {statusConfig[report.status].label}
              </div>

              <div class="flex-1 min-w-0">
                <h3
                  class="font-semibold text-sm text-base-content truncate mb-1"
                >
                  {report.title}
                </h3>
                <p class="text-xs text-base-content/60">{report.description}</p>
              </div>

              <span class="text-[10px] font-mono text-base-content/30 shrink-0"
                >{report.ticket_number}</span
              >

              <div
                class="badge badge-sm {priorityConfig[
                  getPriorityKey(report.priority)
                ].color}"
              >
                {priorityConfig[getPriorityKey(report.priority)].label}
              </div>
            </div>
          </div>
        </div>
      {/each}
    {/each}
  </div>
{/if}

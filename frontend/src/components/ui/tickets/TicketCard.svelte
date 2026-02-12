<script lang="ts">
  import Icon from "@iconify/svelte";
  import type { ModalMode, Ticket, ViewMode } from "../../../types/tickets.ts";
  import {
    columnConfigs,
    getPriorityKey,
    priorityConfig,
    statusConfig,
  } from "../../../utils/ticketConfig.ts";
  import { ticketsStore } from "../../../stores/tickets.store.ts";
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";

  let viewMode: ViewMode = "grid";
  let modalMode: ModalMode = null;
  let selectedReport: Ticket | null = null;
  let formData: Partial<Ticket> = {};

  $: ({ tickets } = $ticketsStore);

  $: columns = columnConfigs.map((config) => ({
    ...config,
    reports: tickets.filter((t) => t.status === config.id),
  }));

  // Load tickets when component mounts
  onMount(async () => {
    await ticketsStore.loadTickets();
  });

  function openModal(mode: ModalMode, report: Ticket | null = null) {
    modalMode = mode;
    selectedReport = report;
    formData = mode === "edit" && report ? { ...report } : {};
  }

  function navigateToTicket(reportId: number) {
    goto(`/tickets/${reportId}`);
  }
</script>

{#if viewMode === "grid"}
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
        <div class="flex flex-col gap-3 p-4 overflow-y-auto flex-1">
          {#each column.reports as report}
            <div class="relative">
              <button
                type="button"
                aria-label={`Open ticket ${report.title}`}
                class="card bg-base-200 dark:bg-base-300 shadow-sm hover:shadow-md transition-all duration-200 border border-base-content/5 shrink-0 cursor-pointer text-left w-full"
                style="padding-right:2.5rem;"
                onclick={() => navigateToTicket(report.id)}
              >
                <div class="card-body p-4">
                  <div class="flex items-center justify-between mb-3">
                    <div
                      class="badge badge-sm {statusConfig[report.status].color}"
                    >
                      {statusConfig[report.status].label}
                    </div>
                    <span class="text-xs text-base-content/40 font-mono"
                      >{report.ticket_number}</span
                    >
                  </div>

                  <h3
                    class="font-semibold text-base text-base-content mb-2 line-clamp-2"
                  >
                    {report.title}
                  </h3>

                  <p class="text-sm text-base-content/60 mb-1 line-clamp-2">
                    {report.description}
                  </p>
                  <p
                    class="text-xs text-base-content/70 mb-3 flex items-center gap-1"
                  >
                    <Icon
                      icon="mdi:office-building-outline"
                      width="14"
                      height="14"
                    />
                    <span class="truncate">
                      {report.building} • {report.room_name}
                    </span>
                  </p>

                  <div class="flex items-center justify-between mb-3">
                    <span class="badge badge-ghost badge-sm">
                      {report.category.name}
                    </span>
                    <div
                      class="badge badge-sm {priorityConfig[
                        getPriorityKey(report.priority)
                      ].color}"
                    >
                      {priorityConfig[getPriorityKey(report.priority)].label}
                    </div>
                  </div>

                  <div
                    class="flex items-center gap-4 text-xs text-base-content/50"
                  >
                    <div class="flex items-center gap-1">
                      <span
                        >{new Date(
                          report.created_at,
                        ).toLocaleDateString()}</span
                      >
                    </div>
                  </div>
                  <!-- Later adding comments -->
                </div>
              </button>
              <div class="absolute top-4 right-4 z-10">
                <div class="dropdown dropdown-end">
                  <button
                    type="button"
                    aria-haspopup="menu"
                    aria-expanded="false"
                    class="btn btn-ghost btn-xs btn-circle cursor-pointer"
                    onclick={(e) => e.stopPropagation()}
                  >
                    <Icon icon="mdi:dots-horizontal" width="14" height="14" />
                  </button>
                  <ul
                    tabindex="-1"
                    role="menu"
                    class="dropdown-content menu bg-base-100 rounded-box z-1 w-40 p-2 shadow-lg border border-base-content/5"
                  >
                    {#if report.status === "pending"}
                      <li>
                        <button
                          type="button"
                          role="menuitem"
                          class="gap-2"
                          onclick={(e) => {
                            e.stopPropagation();
                            openModal("edit", report);
                          }}
                        >
                          <Icon
                            icon="mdi:pencil-outline"
                            width="16"
                            height="16"
                          />
                          Edit
                        </button>
                      </li>
                      <li>
                        <button
                          type="button"
                          role="menuitem"
                          class="gap-2 text-error hover:bg-error/10 focus:bg-error/10 focus:text-error"
                          onclick={(e) => {
                            e.stopPropagation();
                            openModal("delete", report);
                          }}
                        >
                          <Icon
                            icon="mdi:delete-outline"
                            width="16"
                            height="16"
                          />
                          Delete
                        </button>
                      </li>
                    {:else}
                      <li>
                        <button
                          type="button"
                          role="menuitem"
                          class="gap-2 btn-disabled"
                          onclick={(e) => {
                            e.stopPropagation();
                            openModal("edit", report);
                          }}
                        >
                          <Icon icon="mdi:eye-outline" width="16" height="16" />
                          Edit
                        </button>
                      </li>
                    {/if}
                  </ul>
                </div>
              </div>
            </div>
          {/each}

          {#if column.reports.length === 0}
            <div
              class="flex flex-col items-center justify-center py-8 text-center"
            >
              <Icon
                icon="mdi:inbox-outline"
                width="32"
                height="32"
                class="text-base-content/20 mb-2"
              />
              <p class="text-xs text-base-content/40">No tickets</p>
            </div>
          {/if}
        </div>
      </div>
    {/each}
  </div>
{:else}
  <div class="flex-1 overflow-y-auto space-y-2 pr-2">
    {#each columns as column}
      {#each column.reports as report}
        <div
          class="card bg-base-100 shadow-sm hover:shadow-md transition-all duration-200 border border-base-content/5 text-left w-full relative"
        >
          <button
            type="button"
            class="card-body p-4 text-left w-full cursor-pointer"
            aria-label={`Open ticket ${report.title}`}
            onclick={() => navigateToTicket(report.id)}
          >
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
                <p class="text-xs text-base-content/60 truncate">
                  {report.description}
                </p>
                <p class="text-[11px] text-base-content/70 truncate mt-0.5">
                  {report.building} • {report.room_name}
                </p>
              </div>

              <span class="badge badge-ghost badge-sm hidden sm:flex">
                {report.category.name}
              </span>

              <div
                class="badge badge-sm {priorityConfig[
                  getPriorityKey(report.priority)
                ].color}"
              >
                {priorityConfig[getPriorityKey(report.priority)].label}
              </div>

              <span class="text-xs text-base-content/40 font-mono hidden"
                >{report.ticket_number}</span
              >

              <div
                class="flex items-center gap-1 text-xs text-base-content/50 whitespace-nowrap lg:flex"
              >
                <span>{new Date(report.created_at).toLocaleDateString()}</span>
              </div>
            </div>
          </button>

          <div class="absolute top-4 right-4 z-10">
            <div class="dropdown dropdown-end">
              <button
                type="button"
                class="btn btn-ghost btn-xs btn-circle cursor-pointer"
                onclick={(e) => e.stopPropagation()}
              >
                <Icon icon="mdi:dots-horizontal" width="16" height="16" />
              </button>
              <ul
                class="dropdown-content menu bg-base-100 rounded-box z-1 w-40 p-2 shadow-lg border border-base-content/5"
              >
                {#if report.status === "pending"}
                  <li>
                    <button
                      type="button"
                      class="gap-2"
                      onclick={(e) => {
                        e.stopPropagation();
                        openModal("edit", report);
                      }}
                    >
                      <Icon icon="mdi:pencil-outline" width="16" height="16" />
                      Edit
                    </button>
                  </li>
                  <li>
                    <button
                      type="button"
                      class="gap-2 text-error hover:bg-error/10 focus:bg-error/10 focus:text-error"
                      onclick={(e) => {
                        e.stopPropagation();
                        openModal("delete", report);
                      }}
                    >
                      <Icon icon="mdi:delete-outline" width="16" height="16" />
                      Delete
                    </button>
                  </li>
                {:else}
                  <li>
                    <button
                      type="button"
                      class="gap-2 btn-disabled"
                      onclick={(e) => {
                        e.stopPropagation();
                        openModal("edit", report);
                      }}
                    >
                      <Icon icon="mdi:pencil-outline" width="16" height="16" />
                      Edit
                    </button>
                  </li>
                {/if}
              </ul>
            </div>
          </div>
        </div>
      {/each}
    {/each}
  </div>
{/if}

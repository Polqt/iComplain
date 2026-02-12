<script lang="ts">
  import Icon from "@iconify/svelte";
  import StudentLayout from "../../../components/layout/StudentLayout.svelte";
  import { goto } from "$app/navigation";
  import type {
    ModalMode,
    Ticket,
    TicketCreatePayload,
    TicketUpdatePayload,
    ViewMode,
  } from "../../../types/tickets.ts";
  import {
    statusConfig,
    priorityConfig,
    getPriorityKey,
    columnConfigs,
  } from "../../../utils/ticketConfig.ts";
  import TicketDeleteModal from "../../../components/ui/tickets/TicketDeleteModal.svelte";
  import TicketCreateModal from "../../../components/ui/tickets/TicketCreateModal.svelte";
  import { ticketsStore } from "../../../stores/tickets.store.ts";
  import { onMount } from "svelte";

  let viewMode: ViewMode = "grid";
  let modalMode: ModalMode = null;
  let selectedReport: Ticket | null = null;
  let formData: Partial<Ticket> = {};

  // Reactive statement to update local variables when the store changes
  $: ({ tickets, isLoading, error } = $ticketsStore);

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

  function closeModal() {
    modalMode = null;
    selectedReport = null;
    formData = {};
    ticketsStore.setError(null);
  }

  async function handleSubmit(data: Partial<Ticket>, file?: File | null) {
    if (modalMode === "create") {
      const categoryId =
        typeof data.category === "number"
          ? data.category
          : (data.category?.id ?? 1);

      const payload: TicketCreatePayload = {
        title: data.title!,
        description: data.description!,
        category: categoryId,
        building: data.building!,
        room_name: data.room_name!,
      };
    } else if (modalMode === "edit" && selectedReport) {
      const categoryId =
        typeof data.category === "number" ? data.category : data.category?.id;

      const payload: TicketUpdatePayload = {
        title: data.title!,
        description: data.description!,
        building: data.building!,
        room_name: data.room_name!,
        category: categoryId!,
      };

      const updated = await ticketsStore.updateTicket(
        selectedReport.id,
        payload,
      );

      if (updated) {
        closeModal();
      }
    }
  }

  async function handleDelete() {
    if (!selectedReport) return;

    const success = await ticketsStore.deleteTicket(selectedReport.id);
    if (success) {
      closeModal();
    }
  }

  function navigateToTicket(reportId: number) {
    goto(`/student/tickets/${reportId}`);
  }
</script>

<StudentLayout>
  <div class="flex flex-col h-[calc(100vh-8rem)]">
    {#if tickets.length > 0}
      <div class="flex items-center justify-between mb-6 shrink-0">
        <div>
          <h1 class="text-2xl font-black text-base-content">My Tickets</h1>
          {#if !isLoading}
            <p class="text-sm text-base-content/50">
              {tickets.length} ticket{tickets.length !== 1 ? "s" : ""} total
            </p>
          {/if}
        </div>

        <div class="flex items-center gap-3">
          <button
            class="btn btn-primary btn-sm gap-2"
            onclick={() => openModal("create")}
            disabled={isLoading}
          >
            <Icon icon="mdi:plus" width="18" height="18" />
            Create Ticket
          </button>

          <div class="flex items-center gap-2 bg-base-200 p-1 rounded-lg">
            <button
              class="btn btn-sm"
              class:btn-primary={viewMode === "list"}
              class:btn-ghost={viewMode !== "list"}
              onclick={() => (viewMode = "list")}
            >
              <Icon icon="mdi:format-list-bulleted" width="18" height="18" />
              List
            </button>
            <button
              class="btn btn-sm"
              class:btn-primary={viewMode === "grid"}
              class:btn-ghost={viewMode !== "grid"}
              onclick={() => (viewMode = "grid")}
            >
              <Icon icon="mdi:view-grid-outline" width="18" height="18" />
              Board
            </button>
          </div>
        </div>
      </div>
    {/if}

    {#if error}
      <div class="toast toast-top toast-end z-9999">
        <div class="alert alert-error">
          <Icon icon="mdi-alert-circle-outline" width="20" height="20" />
          <span>{error}</span>
          <button
            class="btn btn-ghost btn-xs ml-auto"
            onclick={() => ticketsStore.setError(null)}
          >
            Dismiss
          </button>
        </div>
      </div>
    {/if}

    {#if isLoading}
      <div class="flex gap-6 flex-1">
        {#each columnConfigs as _}
          <div
            class="flex flex-col shrink-0 w-80 bg-base-100 rounded-lg p-4 gap-3"
          >
            <div class="skeleton w-28 h-5 rounded mb-2">
              {#each [1, 2] as _}
                <div class="skeleton h-37 w-full rounded-lg"></div>
              {/each}
            </div>
          </div>
        {/each}
      </div>
    {:else if tickets.length === 0}
      <div class="flex flex-col items-center justify-center flex-1 gap-4">
        <div class="p-6 bg-base-200 rounded-full">
          <Icon
            icon="mdi:ticket-outline"
            width="48"
            height="48"
            class="text-base-content/30"
          />
        </div>
        <div class="text-center">
          <h3 class="font-semibold text-base-content/70 mb-1">
            No tickets yet
          </h3>
          <p class="text-sm text-base-content/50">
            Create your first ticket to report a facility issue.
          </p>
        </div>
        <button
          class="btn btn-primary btn-sm gap-2"
          onclick={() => openModal("create")}
        >
          <Icon icon="mdi:plus" width="18" height="18" />
          Create Ticket
        </button>
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
                          class="badge badge-sm {statusConfig[report.status]
                            .color}"
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
                          {priorityConfig[getPriorityKey(report.priority)]
                            .label}
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
                        <Icon
                          icon="mdi:dots-horizontal"
                          width="14"
                          height="14"
                        />
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
                              <Icon
                                icon="mdi:eye-outline"
                                width="16"
                                height="16"
                              />
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
                    <span
                      >{new Date(report.created_at).toLocaleDateString()}</span
                    >
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
                          class="gap-2 btn-disabled"
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
                    {/if}
                  </ul>
                </div>
              </div>
            </div>
          {/each}
        {/each}
      </div>
    {/if}
  </div>

  <TicketCreateModal
    open={modalMode === "create" || modalMode === "edit"}
    mode={modalMode === "create" ? "create" : "edit"}
    {formData}
    {isLoading}
    onclose={closeModal}
    onsubmit={handleSubmit}
  />
  <TicketDeleteModal
    open={modalMode === "delete"}
    ticket={selectedReport}
    {isLoading}
    onclose={closeModal}
    onconfirm={handleDelete}
  />
</StudentLayout>

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
    columnAccent,
  } from "../../../utils/ticketConfig.ts";
  import TicketDeleteModal from "../../../components/ui/tickets/TicketDeleteModal.svelte";
  import TicketCreateModal from "../../../components/ui/tickets/TicketCreateModal.svelte";
  import TicketCard from "../../../components/ui/tickets/TicketCard.svelte";
  import { ticketsStore } from "../../../stores/tickets.store.ts";
  import { onMount } from "svelte";

  let viewMode: ViewMode = "grid";
  let modalMode: ModalMode = null;
  let selectedReport: Ticket | null = null;
  let formData: Partial<Ticket> = {};

  $: ({ tickets, isLoading, error } = $ticketsStore);

  $: columns = columnConfigs.map((config) => ({
    ...config,
    reports: tickets.filter((t) => t.status === config.id),
  }));

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
      const created = await ticketsStore.createTicket(
        payload,
        file || undefined,
      );
      if (created) closeModal();
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
      if (updated) closeModal();
    }
  }

  async function handleDelete() {
    if (!selectedReport) return;
    const success = await ticketsStore.deleteTicket(selectedReport.id);
    if (success) closeModal();
  }

  function navigateToTicket(ticketnumber: string) {
    goto(`/tickets/${ticketnumber}`);
  }
</script>

<StudentLayout>
  <div class="flex flex-col h-[calc(100vh-8rem)]">
    <div class="flex items-center justify-between mb-5 shrink-0">
      <div>
        <h1 class="text-xl font-bold text-base-content tracking-tight">
          My Tickets
        </h1>
        {#if !isLoading}
          <p class="text-xs text-base-content/40 mt-0.5">
            {tickets.length} ticket{tickets.length !== 1 ? "s" : ""}
          </p>
        {/if}
      </div>

      <div class="flex items-center gap-2">
        <div class="flex items-center bg-base-200 rounded-lg p-0.5 gap-0.5">
          <button
            class="btn btn-xs rounded-md transition-all duration-150
                   {viewMode === 'list'
              ? 'btn-primary shadow-sm'
              : 'btn-ghost text-base-content/50'}"
            onclick={() => (viewMode = "list")}
            aria-label="List view"
          >
            <Icon icon="mdi:format-list-bulleted" width="15" height="15" />
          </button>
          <button
            class="btn btn-xs rounded-md transition-all duration-150
                   {viewMode === 'grid'
              ? 'btn-primary shadow-sm'
              : 'btn-ghost text-base-content/50'}"
            onclick={() => (viewMode = "grid")}
            aria-label="Board view"
          >
            <Icon icon="mdi:view-column-outline" width="15" height="15" />
          </button>
        </div>

        <button
          class="btn btn-primary btn-sm gap-1.5 rounded-lg font-semibold text-xs"
          onclick={() => openModal("create")}
          disabled={isLoading}
        >
          <Icon icon="mdi:plus" width="16" height="16" />
          New Ticket
        </button>
      </div>
    </div>

    {#if error}
      <div class="toast toast-top toast-end z-9999">
        <div class="alert alert-error shadow-lg rounded-xl gap-2 text-sm">
          <Icon icon="mdi:alert-circle-outline" width="18" height="18" />
          <span>{error}</span>
          <button
            class="btn btn-ghost btn-xs rounded-lg ml-1"
            onclick={() => ticketsStore.setError(null)}>✕</button
          >
        </div>
      </div>
    {/if}

    {#if isLoading}
      <div class="grid grid-cols-4 gap-3 flex-1">
        {#each columnConfigs as _, i}
          <div class="flex flex-col gap-3">
            <div class="skeleton h-11 w-full rounded-xl"></div>
            {#each Array(i % 2 === 0 ? 2 : 1) as _}
              <div class="skeleton h-44 w-full rounded-xl"></div>
            {/each}
          </div>
        {/each}
      </div>

    {:else if tickets.length === 0}
      <div class="flex flex-col items-center justify-center flex-1 gap-5">
        <div class="relative">
          <div
            class="w-20 h-20 rounded-2xl bg-base-200 flex items-center justify-center"
          >
            <Icon
              icon="mdi:ticket-outline"
              width="36"
              height="36"
              class="text-base-content/25"
            />
          </div>
          <div
            class="absolute -bottom-1 -right-1 w-7 h-7 rounded-full bg-primary
                      flex items-center justify-center shadow-md"
          >
            <Icon
              icon="mdi:plus"
              width="16"
              height="16"
              class="text-primary-content"
            />
          </div>
        </div>
        <div class="text-center">
          <p class="font-semibold text-base-content/70 text-sm">
            No tickets yet
          </p>
          <p class="text-xs text-base-content/40 mt-1 max-w-50 leading-relaxed">
            Report a facility issue and we'll get it sorted.
          </p>
        </div>
        <button
          class="btn btn-primary btn-sm gap-1.5 rounded-lg font-semibold text-xs"
          onclick={() => openModal("create")}
        >
          <Icon icon="mdi:plus" width="16" height="16" />
          Create your first ticket
        </button>
      </div>
    {:else if viewMode === "grid"}
      <div class="grid grid-cols-4 gap-3 flex-1 overflow-y-hidden pb-2 min-h-0">
        {#each columns as column}
          <div class="flex flex-col min-h-0">
            <div
              class="flex items-center justify-between px-4 py-2.5 mb-2.5 shrink-0
                        bg-base-200/60 rounded-xl border border-base-content/8
                        border-l-[3px] {columnAccent[column.id]}"
            >
              <div class="flex items-center gap-2 min-w-0">
                <span class="w-2 h-2 rounded-full {column.dotColor} shrink-0"
                ></span>
                <span
                  class="text-xs font-bold {column.color} tracking-widest uppercase truncate"
                >
                  {column.title}
                </span>
                <span
                  class="text-xs font-mono text-base-content/35 shrink-0 ml-0.5"
                >
                  {column.reports.length}
                </span>
              </div>
              {#if column.id === "pending"}
                <button
                  class="btn btn-ghost btn-xs btn-circle shrink-0
                         text-base-content/30 hover:text-primary hover:bg-primary/10"
                  onclick={() => openModal("create")}
                  aria-label="Add ticket"
                >
                  <Icon icon="mdi:plus" width="14" height="14" />
                </button>
              {/if}
            </div>

            <div class="flex flex-col gap-2.5 overflow-y-auto flex-1 min-h-0">
              {#each column.reports as report (report.id)}
                <TicketCard
                  {report}
                  onEdit={(r) => openModal("edit", r)}
                  onDelete={(r) => openModal("delete", r)}
                />
              {/each}

              {#if column.reports.length === 0}
                <div
                  class="flex flex-col items-center justify-center gap-2.5 flex-1
                            border-2 border-dashed border-base-content/8 rounded-xl py-10"
                >
                  <Icon
                    icon="mdi:inbox-outline"
                    width="26"
                    height="26"
                    class="text-base-content/15"
                  />
                  <p class="text-xs text-base-content/25 font-medium">
                    No tickets
                  </p>
                </div>
              {/if}
            </div>
          </div>
        {/each}
      </div>
    {:else}
      <div class="flex-1 overflow-y-auto min-h-0">
        <div
          class="grid grid-cols-[1fr_130px_110px_90px_100px] gap-4
                    px-4 py-2 mb-1 border-b border-base-content/8
                    text-[10px] font-bold uppercase tracking-widest text-base-content/35"
        >
          <span>Ticket</span>
          <span class="text-center">Category</span>
          <span class="text-center">Status</span>
          <span class="text-center">Priority</span>
          <span class="text-right">Date</span>
        </div>

        <div class="space-y-1.5">
          {#each columns as column}
            {#each column.reports as report (report.id)}
              <div
                class="group relative bg-base-100 rounded-xl border border-base-content/6
                       hover:border-base-content/18 hover:shadow-sm
                       transition-all duration-150 cursor-pointer"
                role="button"
                tabindex="0"
                aria-label={`Open ticket ${report.title}`}
                onclick={() => navigateToTicket(report.ticket_number)}
                onkeydown={(e) => {
                  if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    navigateToTicket(report.ticket_number);
                  }
                }}
              >
                <div
                  class="grid grid-cols-[1fr_130px_110px_90px_100px] gap-4 items-center px-4 py-3 pr-10"
                >
                  <div class="min-w-0">
                    <span
                      class="text-[10px] font-mono text-base-content/30 block mb-0.5"
                      >{report.ticket_number}</span
                    >
                    <p class="font-semibold text-sm text-base-content truncate">
                      {report.title}
                    </p>
                    <p class="text-[11px] text-base-content/45 truncate mt-0.5">
                      {report.building} · {report.room_name}
                    </p>
                  </div>
                  <div class="flex justify-center">
                    <span
                      class="text-[11px] bg-base-200 text-base-content/55 rounded-full px-2.5 py-0.5 truncate max-w-30"
                    >
                      {report.category.name}
                    </span>
                  </div>
                  <div class="flex justify-center">
                    <span
                      class="badge badge-xs {statusConfig[report.status]
                        .color} font-semibold"
                    >
                      {statusConfig[report.status].label}
                    </span>
                  </div>
                  <div class="flex justify-center">
                    <span
                      class="badge badge-xs {priorityConfig[
                        getPriorityKey(report.priority)
                      ].color} font-semibold"
                    >
                      {priorityConfig[getPriorityKey(report.priority)].label}
                    </span>
                  </div>
                  <div class="text-right">
                    <span class="text-[11px] text-base-content/40">
                      {new Date(report.created_at).toLocaleDateString("en-US", {
                        month: "short",
                        day: "numeric",
                      })}
                    </span>
                  </div>
                </div>

                <div
                  class="absolute top-1/2 -translate-y-1/2 right-3
                         opacity-0 group-hover:opacity-100 transition-opacity duration-150"
                  onclick={(e) => e.stopPropagation()}
                  role="none"
                >
                  <div class="dropdown dropdown-end">
                    <button
                      type="button"
                      tabindex="0"
                      class="btn btn-ghost btn-xs btn-circle text-base-content/40 hover:text-base-content"
                    >
                      <Icon icon="mdi:dots-horizontal" width="15" height="15" />
                    </button>
                    <ul
                      tabindex="-1"
                      role="menu"
                      class="dropdown-content menu bg-base-100 border border-base-content/10
                             rounded-xl shadow-xl z-50 w-40 p-1.5 text-sm"
                    >
                      {#if report.status === "pending"}
                        <li>
                          <button
                            type="button"
                            class="flex items-center gap-2 rounded-lg px-3 py-2 hover:bg-base-200"
                            onclick={(e) => {
                              e.stopPropagation();
                              openModal("edit", report);
                            }}
                          >
                            <Icon
                              icon="mdi:pencil-outline"
                              width="14"
                              height="14"
                            /> Edit
                          </button>
                        </li>
                        <li>
                          <button
                            type="button"
                            class="flex items-center gap-2 rounded-lg px-3 py-2 text-error hover:bg-error/10"
                            onclick={(e) => {
                              e.stopPropagation();
                              openModal("delete", report);
                            }}
                          >
                            <Icon
                              icon="mdi:delete-outline"
                              width="14"
                              height="14"
                            /> Delete
                          </button>
                        </li>
                      {:else}
                        <li>
                          <button
                            type="button"
                            class="flex items-center gap-2 rounded-lg px-3 py-2 text-error hover:bg-error/10 btn-disabled cursor-not-allowed"
                            onclick={(e) => {
                              e.stopPropagation();
                              openModal("delete", report);
                            }}
                          >
                            <Icon
                              icon="mdi:delete-outline"
                              width="14"
                              height="14"
                            /> Delete
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

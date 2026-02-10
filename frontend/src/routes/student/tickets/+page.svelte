<script lang="ts">
  import Icon from "@iconify/svelte";
  import StudentLayout from "../../../components/layout/StudentLayout.svelte";
  import { goto } from "$app/navigation";
  import type {
    Column,
    ModalMode,
    Ticket,
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

  let viewMode: ViewMode = "grid";
  let modalMode: ModalMode = null;
  let selectedReport: Ticket | null = null;
  let formData: Partial<Ticket> = {};

  $: ({ tickets } = $ticketsStore);

  function openModal(mode: ModalMode, report: Ticket | null = null) {
    modalMode = mode;
    selectedReport = report;
    if (mode === "create") {
      formData = {
        title: "",
        description: "",
        status: "pending",
        priority: { id: 1, name: "Low", level: 1, color_code: "#6b7280" },
        comments: 0,
        attachments: "0/3",
        student: {
          id: 0,
          email: "student@example.com",
          is_active: true,
          role: "student",
        },
      };
    } else if (mode === "edit" && report) {
      formData = { ...report };
    }
  }

  function closeModal() {
    modalMode = null;
    selectedReport = null;
    formData = {};
  }

  function handleSubmit(data: Partial<Ticket>) {
    if (modalMode === "create" && data) {
      // Fill all required Ticket fields with defaults if missing
      const newTicket: Ticket = {
        id: `TKT-${String(Date.now()).slice(-6)}`,
        title: data.title ?? "",
        description: data.description ?? "",
        status: data.status ?? "pending",
        priority:
          data.priority ?? {
            id: 1,
            name: "Low",
            level: 1,
            color_code: "#6b7280",
          },
        student:
          data.student ?? {
            id: 0,
            email: "student@example.com",
            is_active: true,
            role: "student",
          },
        category: data.category ?? { id: 1, name: "General" },
        building: data.building ?? "Building A",
        room_name: data.room_name ?? "Room 101",
        created_at: data.created_at ?? new Date().toISOString(),
        updated_at: data.updated_at ?? new Date().toISOString(),
        ticket_number:
          data.ticket_number ?? `TKT-${String(Date.now()).slice(-6)}`,
        attachments: data.attachments ?? "0/3",
        comments: data.comments ?? 0,
      };
      ticketsStore.addTicket(newTicket);
    } else if (modalMode === "edit" && selectedReport && data) {
      ticketsStore.updateTicket(selectedReport.id, data);
    }
    closeModal();
  }

  function handleDelete() {
    if (selectedReport) {
      ticketsStore.removeTicket(selectedReport.id);
    }
    closeModal();
  }

  function navigateToTicket(reportId: string) {
    goto(`/student/tickets/${reportId}`);
  }

  $: columns = columnConfigs.map((config) => ({
    ...config,
    reports: tickets.filter((t) => t.status === config.id),
  }));
</script>

<StudentLayout>
  <div class="flex flex-col h-[calc(100vh-8rem)]">
    <div class="flex items-center justify-between mb-6 shrink-0">
      <h1 class="text-2xl font-black text-base-content">My Tickets</h1>

      <div class="flex items-center gap-3">
        <button
          class="btn btn-primary btn-sm gap-2"
          onclick={() => openModal("create")}
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

              <div class="flex items-center gap-1">
                <button class="btn btn-ghost btn-xs btn-circle">
                  <Icon icon="mdi:dots-horizontal" width="16" height="16" />
                </button>
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
                    onkeydown={(e) => {
                      if (
                        e.key === "Enter" ||
                        e.key === " " ||
                        e.code === "Space"
                      ) {
                        e.preventDefault();
                        navigateToTicket(report.id);
                      }
                    }}
                  >
                    <div class="card-body p-4">
                      <div class="flex items-center justify-between mb-3">
                        <div
                          class="badge badge-sm {statusConfig[report.status]
                            .color}"
                        >
                          {statusConfig[report.status].label}
                        </div>
                      </div>
                      <!-- end card action row -->
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
                        class="flex items-center gap-4 text-xs text-base-content/50 pt-3 border-t border-base-content/5"
                      >
                        <div class="flex items-center gap-1">
                          <Icon
                            icon="mdi:message-outline"
                            width="14"
                            height="14"
                          />
                          <span>{report.comments}</span>
                        </div>
                        <div class="flex items-center gap-1">
                          <Icon icon="mdi:paperclip" width="14" height="14" />
                          <span>{report.attachments}</span>
                        </div>
                      </div>
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
                      </ul>
                    </div>
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
              class="card bg-base-100 shadow-sm hover:shadow-md transition-all duration-200 border border-base-content/5 text-left w-full relative"
            >
              <button
                type="button"
                class="card-body p-4 text-left w-full cursor-pointer"
                aria-label={`Open ticket ${report.title}`}
                onclick={() => navigateToTicket(report.id)}
                onkeydown={(e) => {
                  if (
                    e.key === "Enter" ||
                    e.key === " " ||
                    e.code === "Space"
                  ) {
                    e.preventDefault();
                    navigateToTicket(report.id);
                  }
                }}
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

                  <div
                    class="badge badge-sm {priorityConfig[
                      getPriorityKey(report.priority)
                    ].color}"
                  >
                    {priorityConfig[getPriorityKey(report.priority)].label}
                  </div>

                  <div
                    class="flex items-center gap-3 text-xs text-base-content/50"
                  >
                    <div class="flex items-center gap-1">
                      <Icon icon="mdi:message-outline" width="14" height="14" />
                      <span>{report.comments}</span>
                    </div>
                    <div class="flex items-center gap-1">
                      <Icon icon="mdi:paperclip" width="14" height="14" />
                      <span>{report.attachments}</span>
                    </div>
                  </div>
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
                    <Icon icon="mdi:dots-horizontal" width="16" height="16" />
                  </button>
                  <ul
                    class="dropdown-content menu bg-base-100 rounded-box z-1 w-40 p-2 shadow-lg border border-base-content/5"
                  >
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
    onclose={closeModal}
    onsubmit={handleSubmit}
  />
  <TicketDeleteModal
    open={modalMode === "delete"}
    ticket={selectedReport}
    onclose={closeModal}
    onconfirm={handleDelete}
  />
</StudentLayout>

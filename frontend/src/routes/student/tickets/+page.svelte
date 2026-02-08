<script lang="ts">
  import Icon from "@iconify/svelte";
  import StudentLayout from "../../../components/layout/StudentLayout.svelte";
  import { goto } from "$app/navigation";
  import {
    type Ticket,
    statusConfig,
    priorityConfig,
    TicketCreateModal,
    TicketDeleteModal,
  } from "../../../components/ui/tickets";

  interface Column {
    id: string;
    title: string;
    color: string;
    dotColor: string;
    reports: Ticket[];
  }

  type ViewMode = "grid" | "list";
  type ModalMode = "create" | "edit" | "delete" | null;

  let viewMode: ViewMode = "grid";
  let modalMode: ModalMode = null;
  let selectedReport: Ticket | null = null;
  let formData: Partial<Ticket> = {};

  function openModal(mode: ModalMode, report: Ticket | null = null) {
    modalMode = mode;
    selectedReport = report;
    if (mode === "create") {
      formData = {
        title: "",
        description: "",
        status: "not-started",
        priority: "low",
        assignees: [],
        date: new Date().toLocaleDateString("en-US", {
          day: "2-digit",
          month: "short",
          year: "numeric",
        }),
        comments: 0,
        links: 0,
        attachments: "0/3",
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
    if (modalMode === "create") {
      console.log("Creating ticket:", data);
    } else if (modalMode === "edit") {
      console.log("Updating ticket:", data);
    }
    closeModal();
  }

  function handleDelete() {
    if (selectedReport) {
      console.log("Deleting ticket:", selectedReport.id);
    }
    closeModal();
  }

  function navigateToTicket(reportId: string) {
    goto(`/student/tickets/${reportId}`);
  }

  const columns: Column[] = [
    {
      id: "pending",
      title: "Pending",
      color: "text-yellow-300",
      dotColor: "bg-yellow-300",
      reports: [
        {
          id: "TKT-001",
          title: "Broken AC Unit in Room 301",
          description:
            "Air conditioning not working properly, temperature control issues...",
          status: "not-started",
          priority: "low",
          assignees: ["JD", "AS"],
          date: "25 Mar 2023",
          comments: 5,
          links: 2,
          attachments: "3/3",
        },
        {
          id: "TKT-002",
          title: "Leaking Faucet in Restroom",
          description: "Water dripping continuously from the main sink...",
          status: "in-research",
          priority: "medium",
          assignees: ["MJ"],
          date: "28 Mar 2023",
          comments: 12,
          links: 1,
          attachments: "2/3",
        },
      ],
    },
    {
      id: "in-progress",
      title: "In Progress",
      color: "text-info",
      dotColor: "bg-info",
      reports: [
        {
          id: "TKT-003",
          title: "Flickering Hallway Lights",
          description:
            "Lights in 3F hallway flickering intermittently during evening hours...",
          status: "in-research",
          priority: "high",
          assignees: ["AS", "JD"],
          date: "30 Mar 2023",
          comments: 8,
          links: 1,
          attachments: "2/3",
        },
        {
          id: "TKT-004",
          title: "Broken Projector Screen",
          description:
            "Projection screen won't retract properly in lecture hall...",
          status: "on-track",
          priority: "low",
          assignees: ["MJ"],
          date: "02 Apr 2023",
          comments: 3,
          links: 0,
          attachments: "2/3",
        },
      ],
    },
    {
      id: "resolved",
      title: "Resolved",
      color: "text-green-300",
      dotColor: "bg-green-300",
      reports: [
        {
          id: "TKT-005",
          title: "Door Lock Malfunction",
          description:
            "Main entrance lock mechanism was jammed and needed repair...",
          status: "complete",
          priority: "high",
          assignees: ["AS"],
          date: "07 Apr 2023",
          comments: 6,
          links: 0,
          attachments: "1/3",
        },
        {
          id: "TKT-006",
          title: "Missing Whiteboard Markers",
          description:
            "Classroom 205 needed new dry-erase markers for teaching...",
          status: "not-started",
          priority: "low",
          assignees: ["JD", "MJ"],
          date: "10 Apr 2023",
          comments: 4,
          links: 2,
          attachments: "0/3",
        },
      ],
    },
    {
      id: "closed",
      title: "Closed",
      color: "text-gray-300",
      dotColor: "bg-gray-300",
      reports: [],
    },
  ];
</script>

<StudentLayout>
  <div class="flex flex-col h-[calc(100vh-8rem)]">
    <div class="flex items-center justify-between mb-6 shrink-0">
  <h1 class="text-2xl font-black text-base-content">My Tickets</h1>

  <div class="flex items-center gap-3">
    <!-- Create Ticket Button -->
    <button class="btn btn-primary btn-sm gap-2" onclick={() => openModal("create")}>
      <Icon icon="mdi:plus" width="18" height="18" />
      Create Ticket
    </button>

    <div class="flex items-center gap-2 bg-base-200 p-1 rounded-lg">
      <button
        class="btn btn-sm"
        class:btn-primary={viewMode === 'list'}
        class:btn-ghost={viewMode !== 'list'}
        onclick={() => (viewMode = "list")}
      >
        <Icon icon="mdi:format-list-bulleted" width="18" height="18" />
        List
      </button>
      <button
        class="btn btn-sm"
        class:btn-primary={viewMode === 'grid'}
        class:btn-ghost={viewMode !== 'grid'}
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
                <div
                  class="card bg-base-200 dark:bg-base-300 shadow-sm hover:shadow-md transition-all duration-200 border border-base-content/5 shrink-0 cursor-pointer"
                  onclick={() => navigateToTicket(report.id)}
                >
                  <div class="card-body p-4">
                    <div class="flex items-center justify-between mb-3">
                      <div
                        class="badge badge-sm {statusConfig[report.status].color}"
                      >
                        {statusConfig[report.status].label}
                      </div>
                      <div
                        class="dropdown dropdown-end"
                        onclick={(e) => e.stopPropagation()}
                      >
                        <label tabindex="0" class="btn btn-ghost btn-xs btn-circle cursor-pointer">
                          <Icon
                            icon="mdi:dots-horizontal"
                            width="14"
                            height="14"
                          />
                        </label>
                        <ul
                          tabindex="0"
                          class="dropdown-content menu bg-base-100 rounded-box z-[1] w-40 p-2 shadow-lg border border-base-content/5"
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
                        </ul>
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

                    <div class="flex items-center justify-between mb-3">
                      <div class="flex items-center gap-2">
                        <span class="text-xs text-base-content/50"
                          >Assignees:</span
                        >
                        <div class="avatar-group -space-x-3">
                          {#each report.assignees as assignee}
                            <div class="avatar placeholder">
                              <div
                                class="bg-primary text-primary-content w-6 rounded-full"
                              >
                                <span class="text-xs">{assignee}</span>
                              </div>
                            </div>
                          {/each}
                        </div>
                      </div>
                    </div>

                    <div class="flex items-center justify-between mb-3">
                      <div
                        class="flex items-center gap-1 text-xs text-base-content/60"
                      >
                        <Icon
                          icon="mdi:calendar-outline"
                          width="14"
                          height="14"
                        />
                        <span>{report.date}</span>
                      </div>
                      <div
                        class="badge badge-sm {priorityConfig[report.priority].color}"
                      >
                        {priorityConfig[report.priority].label}
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
                        <Icon icon="mdi:link-variant" width="14" height="14" />
                        <span>{report.links}</span>
                      </div>
                      <div class="flex items-center gap-1">
                        <Icon icon="mdi:paperclip" width="14" height="14" />
                        <span>{report.attachments}</span>
                      </div>
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
              class="card bg-base-100 shadow-sm hover:shadow-md transition-all duration-200 border border-base-content/5 cursor-pointer"
              onclick={() => navigateToTicket(report.id)}
            >
              <div class="card-body p-4">
                <div class="flex items-center gap-4">
                  <div
                    class="badge badge-sm whitespace-nowrap {statusConfig[report.status].color}"
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
                  </div>

                  <div class="avatar-group -space-x-3">
                    {#each report.assignees as assignee}
                      <div class="avatar placeholder">
                        <div
                          class="bg-primary text-primary-content w-6 rounded-full"
                        >
                          <span class="text-xs">{assignee}</span>
                        </div>
                      </div>
                    {/each}
                  </div>

                  <div
                    class="flex items-center gap-1 text-xs text-base-content/60 whitespace-nowrap"
                  >
                    <Icon icon="mdi:calendar-outline" width="14" height="14" />
                    <span>{report.date}</span>
                  </div>

                  <div
                    class="badge badge-sm {priorityConfig[report.priority].color}"
                  >
                    {priorityConfig[report.priority].label}
                  </div>

                  <div
                    class="flex items-center gap-3 text-xs text-base-content/50"
                  >
                    <div class="flex items-center gap-1">
                      <Icon icon="mdi:message-outline" width="14" height="14" />
                      <span>{report.comments}</span>
                    </div>
                    <div class="flex items-center gap-1">
                      <Icon icon="mdi:link-variant" width="14" height="14" />
                      <span>{report.links}</span>
                    </div>
                    <div class="flex items-center gap-1">
                      <Icon icon="mdi:paperclip" width="14" height="14" />
                      <span>{report.attachments}</span>
                    </div>
                  </div>

                  <div
                    class="dropdown dropdown-end"
                    onclick={(e) => e.stopPropagation()}
                  >
                    <label
                      tabindex="0"
                      class="btn btn-ghost btn-xs btn-circle cursor-pointer"
                    >
                      <Icon icon="mdi:dots-horizontal" width="16" height="16" />
                    </label>
                    <ul
                      tabindex="0"
                      class="dropdown-content menu bg-base-100 rounded-box z-[1] w-40 p-2 shadow-lg border border-base-content/5"
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
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          {/each}
        {/each}
      </div>
    {/if}
  </div>

  <!-- Modals (from ui/tickets) -->
  <TicketCreateModal
    open={modalMode === "create" || modalMode === "edit"}
    mode={modalMode === "create" ? "create" : "edit"}
    formData={formData}
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

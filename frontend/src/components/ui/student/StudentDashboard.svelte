<script lang="ts">
  import Icon from "@iconify/svelte";
  import StudentLayout from "../../../components/layout/StudentLayout.svelte";
  import type {
    TicketColumn,
    ViewMode,
    Ticket,
    TicketPriority,
  } from "../../../types/tickets.ts";
  import {
    priorityConfig,
    getPriorityKey,
    statusConfig,
  } from "../../../utils/ticketConfig.ts";

  let viewMode: ViewMode = "grid";

  const columns: TicketColumn[] = [
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
          student: { name: "Alice", avatar: "", email: "alice@example.com" },
          category: { id: 1, name: "Facilities" },
          priority: {
            id: 1,
            name: "Low",
            level: 1,
            color_code: "#6b7280",
          } as TicketPriority,
          building: "Main",
          room_name: "Room 301",
          status: "pending",
          created_at: "2023-03-25T09:00:00Z",
          updated_at: "2023-03-25T09:00:00Z",
          ticket_number: "TKT-001",
          attachments: "3/3",
          comments: 5,
        } as Ticket,
        {
          id: "TKT-002",
          title: "Leaking Faucet in Restroom",
          description: "Water dripping continuously from the main sink...",
          student: { name: "Bob", avatar: "", email: "bob@example.com" },
          category: { id: 2, name: "Plumbing" },
          priority: {
            id: 2,
            name: "Medium",
            level: 2,
            color_code: "#f59e0b",
          } as TicketPriority,
          building: "South",
          room_name: "Restroom A",
          status: "in_progress",
          created_at: "2023-03-28T10:30:00Z",
          updated_at: "2023-03-28T11:00:00Z",
          ticket_number: "TKT-002",
          attachments: "2/3",
          comments: 12,
        } as Ticket,
      ],
    },
    {
      id: "in_progress",
      title: "In Progress",
      color: "text-info",
      dotColor: "bg-info",
      reports: [
        {
          id: "TKT-003",
          title: "Flickering Hallway Lights",
          description:
            "Lights in 3F hallway flickering intermittently during evening hours...",
          student: { name: "Carol", avatar: "", email: "carol@example.com" },
          category: { id: 3, name: "Electrical" },
          priority: {
            id: 3,
            name: "High",
            level: 3,
            color_code: "#dc2626",
          } as TicketPriority,
          building: "North",
          room_name: "Hallway 3F",
          status: "in_progress",
          created_at: "2023-03-30T19:00:00Z",
          updated_at: "2023-03-30T19:10:00Z",
          ticket_number: "TKT-003",
          attachments: "2/3",
          comments: 8,
        } as Ticket,
        {
          id: "TKT-004",
          title: "Broken Projector Screen",
          description:
            "Projection screen won't retract properly in lecture hall...",
          student: { name: "Dan", avatar: "", email: "dan@example.com" },
          category: { id: 4, name: "AV" },
          priority: {
            id: 1,
            name: "Low",
            level: 1,
            color_code: "#6b7280",
          } as TicketPriority,
          building: "Main",
          room_name: "Lecture Hall A",
          status: "in_progress",
          created_at: "2023-04-02T14:20:00Z",
          updated_at: "2023-04-02T14:45:00Z",
          ticket_number: "TKT-004",
          attachments: "2/3",
          comments: 3,
        } as Ticket,
      ],
    },
    {
      id: "resolved",
      title: "Resolved",
      color: "text-green-300",
      dotColor: "bg-green-300",
      reports: [],
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
                <div class="{column.dotColor} w-2 h-2 rounded-full"></div>
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
                <div
                  class="card bg-base-200 dark:bg-base-300 shadow-sm hover:shadow-md transition-all duration-200 border border-base-content/5 shrink-0"
                >
                  <div class="card-body p-4">
                    <div class="flex items-center justify-between mb-3">
                      <div
                        class="badge {statusConfig[report.status]
                          .color} badge-sm"
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

                    <div class="flex items-center justify-between mb-3">
                      <div
                        class="badge {priorityConfig[
                          getPriorityKey(report.priority)
                        ].color} badge-sm"
                      >
                        {priorityConfig[getPriorityKey(report.priority)].label}
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
              class="card bg-base-100 shadow-sm hover:shadow-md transition-all duration-200 border border-base-content/5"
            >
              <div class="card-body p-4">
                <div class="flex items-center gap-4">
                  <div
                    class="badge {statusConfig[report.status]
                      .color} badge-sm whitespace-nowrap"
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

                  <div
                    class="badge {priorityConfig[
                      getPriorityKey(report.priority)
                    ].color} badge-sm"
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
              </div>
            </div>
          {/each}
        {/each}
      </div>
    {/if}
  </div>
</StudentLayout>

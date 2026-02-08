<script lang="ts">
  import Icon from "@iconify/svelte";
  import StudentLayout from "../../../components/layout/StudentLayout.svelte";

  interface Report {
    id: string;
    title: string;
    description: string;
    status: "not-started" | "in-research" | "on-track" | "complete";
    priority: "low" | "medium" | "high";
    assignees: string[];
    date: string;
    comments: number;
    links: number;
    attachments: string;
  }

  interface Column {
    id: string;
    title: string;
    color: string;
    dotColor: string;
    reports: Report[];
  }

  type ViewMode = "grid" | "list";

  let viewMode: ViewMode = "grid";

  const statusConfig = {
    "not-started": { label: "Not Started", color: "badge-primary" },
    "in-research": { label: "In Research", color: "badge-warning" },
    "on-track": { label: "On Track", color: "badge-secondary" },
    complete: { label: "Complete", color: "badge-success" },
  };

  const priorityConfig = {
    low: { label: "Low", color: "badge-info" },
    medium: { label: "Medium", color: "badge-warning" },
    high: { label: "High", color: "badge-error" },
  };

  const columns: Column[] = [
    {
      id: "pending",
      title: "Pending",
      color: "text-yellow-300",
      dotColor: "bg-yellow-300",
      reports: [
        {
          id: "1",
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
          id: "2",
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
          id: "3",
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
          id: "4",
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
          id: "5",
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
          id: "6",
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
    <button class="btn btn-primary btn-sm gap-2">
      <Icon icon="mdi:plus" width="18" height="18" />
      Create Ticket
    </button>

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
              <div class="flex items-center gap-1">
                <button class="btn btn-ghost btn-xs btn-circle">
                  <Icon icon="mdi:dots-horizontal" width="16" height="16" />
                </button>
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
                      <button class="btn btn-ghost btn-xs btn-circle">
                        <Icon
                          icon="mdi:dots-horizontal"
                          width="14"
                          height="14"
                        />
                      </button>
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
                        class="badge {priorityConfig[report.priority]
                          .color} badge-sm"
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
                    class="badge {priorityConfig[report.priority]
                      .color} badge-sm"
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

                  <button class="btn btn-ghost btn-xs btn-circle">
                    <Icon icon="mdi:dots-horizontal" width="16" height="16" />
                  </button>
                </div>
              </div>
            </div>
          {/each}
        {/each}
      </div>
    {/if}
  </div>
</StudentLayout>

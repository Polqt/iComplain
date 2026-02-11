<script lang="ts">
  import Icon from "@iconify/svelte";
  import AdminLayout from "../../layout/AdminLayout.svelte";
  import { priorityConfig, statusConfig, getPriorityKey } from "../../../utils/ticketConfig.ts";
  import type { TicketStatus, ViewMode } from "../../../types/tickets.ts";
  import type { PriorityKey } from "../../../utils/ticketConfig.ts";

  let viewMode: ViewMode = "grid";

  const metrics = [
    {
      title: "Total Tickets",
      value: "245",
      change: "+12%",
      subtitle: "vs last month",
      trend: "text-success",
    },
    {
      title: "Resolved Tickets",
      value: "180",
      change: "+15%",
      subtitle: "Last Month 56",
      trend: "text-success",
    },
    {
      title: "Pending Tickets",
      value: "45",
      change: "-12%",
      subtitle: "Last Month 49",
      trend: "text-error",
    },
    {
      title: "Response Time",
      value: "2.4 hrs",
      change: "10x faster",
      subtitle: "Last Month 2.4 hrs",
      trend: "text-success",
    },
  ];

  const volume = [
    { day: "S", value: 14 },
    { day: "M", value: 24 },
    { day: "T", value: 18 },
    { day: "W", value: 30 },
    { day: "T", value: 22 },
    { day: "F", value: 26 },
    { day: "S", value: 16 },
  ];

  const activities = [
    {
      id: "#4021",
      title: "Login Issue",
      status: "resolved" as TicketStatus,
      description: "Reset credentials and confirmed access restored.",
      tags: ["Urgent", "Technical"],
      assignee: "N. Flores",
      time: "2 hours ago",
    },
    {
      id: "#3987",
      title: "Billing Error",
      status: "pending" as TicketStatus,
      description: "Awaiting invoice verification from finance.",
      tags: ["Finance", "Follow-up"],
      assignee: "R. Santos",
      time: "Yesterday",
    },
    {
      id: "#3964",
      title: "Access Request",
      status: "in_progress" as TicketStatus,
      description: "New faculty access request pending approval.",
      tags: ["Account", "New"],
      assignee: "M. Tan",
      time: "2 days ago",
    },
  ];

  const statusBadge = (status: TicketStatus) => statusConfig[status].color;

  const columnConfigs = [
    { id: "pending", title: "Pending", color: "text-warning", dotColor: "bg-warning" },
    { id: "in_progress", title: "In Progress", color: "text-info", dotColor: "bg-info" },
    { id: "resolved", title: "Resolved", color: "text-success", dotColor: "bg-success" },
    { id: "closed", title: "Closed", color: "text-base-content/50", dotColor: "bg-base-300" },
  ];

  let mockTickets = [
    {
      id: "TC-0004",
      title: "System Login Failure",
      description: "Cannot access the portal after password reset.",
      status: "pending" as TicketStatus,
      priority: "high" as PriorityKey,
      assignees: ["AV", "KD"],
      date: "Feb 08, 2026",
      comments: 3,
      links: 1,
      attachments: "2/3",
    },
    {
      id: "TC-0001",
      title: "Request for Additional Storage",
      description: "Need more storage for project submission files.",
      status: "in_progress" as TicketStatus,
      priority: "medium" as PriorityKey,
      assignees: ["RS"],
      date: "Feb 07, 2026",
      comments: 2,
      links: 0,
      attachments: "1/3",
    },
    {
      id: "TC-0003",
      title: "Unable to Access Report",
      description: "Reports page returns a blank screen on load.",
      status: "in_progress" as TicketStatus,
      priority: "medium" as PriorityKey,
      assignees: ["NT"],
      date: "Feb 07, 2026",
      comments: 4,
      links: 1,
      attachments: "0/3",
    },
    {
      id: "TC-0008",
      title: "Unexpected App Crash",
      description: "Mobile app crashes after login on Android.",
      status: "resolved" as TicketStatus,
      priority: "high" as PriorityKey,
      assignees: ["JD", "AS"],
      date: "Feb 06, 2026",
      comments: 1,
      links: 0,
      attachments: "1/3",
    },
    {
      id: "TC-0007",
      title: "File Upload Error",
      description: "Submission fails with file size validation.",
      status: "pending" as TicketStatus,
      priority: "low" as PriorityKey,
      assignees: ["MJ"],
      date: "Feb 06, 2026",
      comments: 2,
      links: 0,
      attachments: "0/3",
    },
    {
      id: "TC-0010",
      title: "Email Notifications Delay",
      description: "Notifications arrive late outside business hours.",
      status: "closed" as TicketStatus,
      priority: "low" as PriorityKey,
      assignees: ["AV"],
      date: "Jan 31, 2026",
      comments: 0,
      links: 0,
      attachments: "0/3",
    },
  ];

  $: columns = columnConfigs.map((config) => ({
    ...config,
    reports: mockTickets.filter((t) => t.status === config.id),
  }));
</script>

<AdminLayout>
  <div class="flex flex-col h-[calc(100vh-8rem)]">
    <div class="flex flex-wrap items-center justify-between gap-4 mb-6 shrink-0">
      <div class="flex items-center gap-2">
        <div class="w-9 h-9 rounded-xl bg-primary/10 flex items-center justify-center">
          <Icon icon="mdi:view-dashboard-outline" width="20" height="20" />
        </div>
        <div>
          <h1 class="text-2xl font-black text-base-content">Dashboard Overview</h1>
          <p class="text-sm text-base-content/60">
            Track performance, workload, and support activity
          </p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <button class="btn btn-sm btn-primary gap-2">
          <Icon icon="mdi:chart-bar" width="18" height="18" />
          Generate Report
        </button>
        <button class="btn btn-sm btn-outline gap-2">
          <Icon icon="mdi:download" width="18" height="18" />
          Export CSV
        </button>
      </div>
    </div>

    <div class="flex-1 overflow-y-auto pr-2 space-y-6">
      <section class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        {#each metrics as metric}
          <div class="card bg-base-100 dark:bg-base-100 shadow-sm border border-base-content/5 rounded-lg">
            <div class="card-body p-4">
              <div class="flex items-center justify-between mb-3">
                <p class="text-xs text-base-content/60">{metric.title}</p>
                <button class="btn btn-ghost btn-xs btn-circle">
                  <Icon icon="mdi:dots-horizontal" width="16" height="16" />
                </button>
              </div>
              <div class="flex items-end justify-between">
                <div>
                  <p class="text-2xl font-bold leading-none">{metric.value}</p>
                  <p class="text-xs text-base-content/50 mt-1">{metric.subtitle}</p>
                </div>
                <span class="text-xs font-semibold {metric.trend}">{metric.change}</span>
              </div>
            </div>
          </div>
        {/each}
      </section>

      <section class="grid grid-cols-1 xl:grid-cols-3 gap-4">
        <div class="card bg-base-100 dark:bg-base-100 shadow-sm border border-base-content/5 rounded-lg xl:col-span-2">
          <div class="card-body p-4">
            <div class="flex items-center justify-between mb-4">
              <div>
                <h2 class="text-base font-semibold">Ticket Volume Tracker</h2>
                <p class="text-xs text-base-content/60">
                  Track daily ticket flow and monitor workload trends
                </p>
              </div>
              <select class="select select-bordered select-sm">
                <option>Weekly</option>
                <option>Monthly</option>
                <option>Quarterly</option>
              </select>
            </div>

            <div class="flex items-end justify-between gap-3 h-40">
              {#each volume as bar}
                <div class="flex flex-col items-center gap-2 flex-1">
                  <div
                    class="w-8 rounded-lg bg-primary/20 relative overflow-hidden"
                    style={`height: ${bar.value * 3}px`}
                  >
                    <div class="absolute bottom-0 inset-x-0 h-full bg-primary/60"></div>
                  </div>
                  <span class="text-xs text-base-content/60">{bar.day}</span>
                </div>
              {/each}
            </div>

            <div class="mt-4 text-sm text-base-content/60">
              <span class="text-success font-semibold">+18%</span>
              This week's ticket volume is higher than last week's
            </div>
          </div>
        </div>

        <div class="card bg-base-100 dark:bg-base-100 shadow-sm border border-base-content/5 rounded-lg">
          <div class="card-body p-4">
            <div class="flex items-center justify-between mb-3">
              <div>
                <h2 class="text-base font-semibold">Recent Support Activity</h2>
                <p class="text-xs text-base-content/60">
                  Latest updates from the support team
                </p>
              </div>
              <a href="/admin/activities" class="text-xs text-primary">
                See all activities
              </a>
            </div>

            <div class="space-y-3">
              {#each activities as activity}
                <div class="card bg-base-200 dark:bg-base-300 border border-base-content/5">
                  <div class="card-body p-3">
                    <div class="flex items-center justify-between">
                      <div class="flex items-center gap-2">
                        <span class="text-xs font-semibold">{activity.id}</span>
                        <span class="text-sm font-medium">{activity.title}</span>
                      </div>
                      <span class="badge badge-sm {statusBadge(activity.status)}">
                        {activity.status}
                      </span>
                    </div>
                    <p class="text-xs text-base-content/70 mt-2">
                      {activity.description}
                    </p>
                    <div class="flex flex-wrap gap-2 mt-2">
                      {#each activity.tags as tag}
                        <span class="badge badge-ghost badge-sm">{tag}</span>
                      {/each}
                    </div>
                    <div class="flex items-center justify-between text-xs text-base-content/50 mt-2">
                      <span>Assigned to {activity.assignee}</span>
                      <span>{activity.time}</span>
                    </div>
                  </div>
                </div>
              {/each}
            </div>
          </div>
        </div>
      </section>

      <section class="flex items-center justify-between">
        <h2 class="text-lg font-semibold">Ticket Status Board</h2>
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
      </section>

      {#if viewMode === "grid"}
        <div class="flex gap-6 pb-4 flex-1 overflow-x-auto overflow-y-hidden">
          {#each columns as column}
            <div class="flex flex-col shrink-0 w-80 bg-base-100 dark:bg-base-100 shadow rounded-lg h-full">
              <div class="flex items-center justify-between p-4 border-b border-base-content/5 shrink-0">
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

              <div class="flex flex-col gap-3 p-4 overflow-y-auto flex-1 max-h-130">
                {#each column.reports as report}
                  <div class="card bg-base-200 dark:bg-base-300 shadow-sm hover:shadow-md transition-all duration-200 border border-base-content/5 shrink-0 cursor-pointer">
                    <div class="card-body p-4">
                      <div class="flex items-center justify-between mb-3">
                        <div class="badge badge-sm {statusConfig[report.status].color}">
                          {statusConfig[report.status].label}
                        </div>
                        <div class="dropdown dropdown-end">
                          <label class="btn btn-ghost btn-xs btn-circle cursor-pointer">
                            <Icon icon="mdi:dots-horizontal" width="14" height="14" />
                          </label>
                          <ul
                            class="dropdown-content menu bg-base-100 rounded-box z-1 w-40 p-2 shadow-lg border border-base-content/5"
                          >
                            <li>
                              <button type="button" class="gap-2">
                                <Icon icon="mdi:eye-outline" width="16" height="16" />
                                View
                              </button>
                            </li>
                            <li>
                              <button type="button" class="gap-2">
                                <Icon icon="mdi:pencil-outline" width="16" height="16" />
                                Update
                              </button>
                            </li>
                          </ul>
                        </div>
                      </div>

                      <h3 class="font-semibold text-base text-base-content mb-2 line-clamp-2">
                        {report.title}
                      </h3>

                      <p class="text-sm text-base-content/60 mb-3 line-clamp-2">
                        {report.description}
                      </p>

                      <div class="flex items-center justify-between mb-3">
                        <div class="flex items-center gap-2">
                          <span class="text-xs text-base-content/50">Assignees:</span>
                          <div class="avatar-group -space-x-3">
                            {#each report.assignees as assignee}
                              <div class="avatar placeholder">
                                <div class="bg-primary text-primary-content w-6 rounded-full">
                                  <span class="text-xs">{assignee}</span>
                                </div>
                              </div>
                            {/each}
                          </div>
                        </div>
                      </div>

                      <div class="flex items-center justify-between mb-3">
                        <div class="flex items-center gap-1 text-xs text-base-content/60">
                          <Icon icon="mdi:calendar-outline" width="14" height="14" />
                          <span>{report.date}</span>
                        </div>
                        <div class="badge badge-sm {priorityConfig[getPriorityKey(report.priority)].color}">
                          {priorityConfig[getPriorityKey(report.priority)].label}
                        </div>
                      </div>

                      <div class="flex items-center gap-4 text-xs text-base-content/50 pt-3 border-t border-base-content/5">
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
              <div class="card bg-base-100 shadow-sm hover:shadow-md transition-all duration-200 border border-base-content/5">
                <div class="card-body p-4">
                  <div class="flex items-center gap-4">
                    <div class="badge badge-sm whitespace-nowrap {statusConfig[report.status].color}">
                      {statusConfig[report.status].label}
                    </div>

                    <div class="flex-1 min-w-0">
                      <h3 class="font-semibold text-sm text-base-content truncate mb-1">
                        {report.title}
                      </h3>
                      <p class="text-xs text-base-content/60 truncate">
                        {report.description}
                      </p>
                    </div>

                    <div class="avatar-group -space-x-3">
                      {#each report.assignees as assignee}
                        <div class="avatar placeholder">
                          <div class="bg-primary text-primary-content w-6 rounded-full">
                            <span class="text-xs">{assignee}</span>
                          </div>
                        </div>
                      {/each}
                    </div>

                    <div class="flex items-center gap-1 text-xs text-base-content/60 whitespace-nowrap">
                      <Icon icon="mdi:calendar-outline" width="14" height="14" />
                      <span>{report.date}</span>
                    </div>

                    <div class="badge badge-sm {priorityConfig[getPriorityKey(report.priority)].color}">
                      {priorityConfig[getPriorityKey(report.priority)].label}
                    </div>

                    <div class="flex items-center gap-3 text-xs text-base-content/50">
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
                  </div>
                </div>
              </div>
            {/each}
          {/each}
        </div>
      {/if}
    </div>
  </div>
</AdminLayout>

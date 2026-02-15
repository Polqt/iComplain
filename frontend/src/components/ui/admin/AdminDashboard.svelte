<script lang="ts">
  import Icon from "@iconify/svelte";
  import AdminLayout from "../../layout/AdminLayout.svelte";
  import { statusConfig } from "../../../utils/ticketConfig.ts";
  import type { TicketStatus, ViewMode } from "../../../types/tickets.ts";
  import TicketBoard from "../tickets/TicketBoard.svelte";

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
</script>

<AdminLayout>
  <div class="flex flex-col h-[calc(100vh-8rem)]">
    <div
      class="flex flex-wrap items-center justify-between gap-4 mb-6 shrink-0"
    >
      <div class="flex items-center gap-2">
        <div
          class="w-9 h-9 rounded-xl bg-primary/10 flex items-center justify-center"
        >
          <Icon icon="mdi:view-dashboard-outline" width="20" height="20" />
        </div>
        <div>
          <h1 class="text-2xl font-black text-base-content">
            Dashboard Overview
          </h1>
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
          <div
            class="card bg-base-100 dark:bg-base-100 shadow-sm border border-base-content/5 rounded-lg"
          >
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
                  <p class="text-xs text-base-content/50 mt-1">
                    {metric.subtitle}
                  </p>
                </div>
                <span class="text-xs font-semibold {metric.trend}"
                  >{metric.change}</span
                >
              </div>
            </div>
          </div>
        {/each}
      </section>

      <section class="grid grid-cols-1 xl:grid-cols-3 gap-4">
        <div
          class="card bg-base-100 dark:bg-base-100 shadow-sm border border-base-content/5 rounded-lg xl:col-span-2"
        >
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
                    <div
                      class="absolute bottom-0 inset-x-0 h-full bg-primary/60"
                    ></div>
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

        <div
          class="card bg-base-100 dark:bg-base-100 shadow-sm border border-base-content/5 rounded-lg"
        >
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
                <div
                  class="card bg-base-200 dark:bg-base-300 border border-base-content/5"
                >
                  <div class="card-body p-3">
                    <div class="flex items-center justify-between">
                      <div class="flex items-center gap-2">
                        <span class="text-xs font-semibold">{activity.id}</span>
                        <span class="text-sm font-medium">{activity.title}</span
                        >
                      </div>
                      <span
                        class="badge badge-sm {statusBadge(activity.status)}"
                      >
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
                    <div
                      class="flex items-center justify-between text-xs text-base-content/50 mt-2"
                    >
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

      <TicketBoard />
    </div>
  </div>
</AdminLayout>

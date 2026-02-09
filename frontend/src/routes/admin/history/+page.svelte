<script lang="ts">
  import Icon from "@iconify/svelte";
  import AdminLayout from "../../../components/layout/AdminLayout.svelte";

  type HistoryItem = {
    id: string;
    ticketId: string;
    title: string;
    action: string;
    by: string;
    time: string;
    status: "Resolved" | "Pending" | "Open" | "Closed";
    priority: "Low" | "Medium" | "High";
  };

  const statusConfig = {
    Resolved: "badge-success",
    Pending: "badge-warning",
    Open: "badge-info",
    Closed: "badge-ghost",
  };

  const priorityConfig = {
    Low: "badge-info",
    Medium: "badge-warning",
    High: "badge-error",
  };

  let query = "";
  let statusFilter: "all" | HistoryItem["status"] = "all";

  let history: HistoryItem[] = [
    {
      id: "H-201",
      ticketId: "TC-0004",
      title: "System Login Failure",
      action: "Status changed to Resolved",
      by: "Admin — J. Cruz",
      time: "Today, 09:52 AM",
      status: "Resolved",
      priority: "High",
    },
    {
      id: "H-202",
      ticketId: "TC-0001",
      title: "Request for Additional Storage",
      action: "Priority updated to Medium",
      by: "Admin — R. Sy",
      time: "Yesterday, 03:40 PM",
      status: "Pending",
      priority: "Medium",
    },
    {
      id: "H-203",
      ticketId: "TC-0003",
      title: "Unable to Access Report",
      action: "Assigned to IT Support",
      by: "Admin — L. Tan",
      time: "Feb 07, 2026",
      status: "Open",
      priority: "Medium",
    },
    {
      id: "H-204",
      ticketId: "TC-0008",
      title: "Unexpected App Crash",
      action: "Ticket closed after resolution confirmation",
      by: "Admin — M. Santos",
      time: "Feb 05, 2026",
      status: "Closed",
      priority: "High",
    },
  ];

  $: filtered = history.filter((item) => {
    const q = query.trim().toLowerCase();
    const matchesQuery =
      !q ||
      item.ticketId.toLowerCase().includes(q) ||
      item.title.toLowerCase().includes(q) ||
      item.action.toLowerCase().includes(q);
    const matchesStatus = statusFilter === "all" || item.status === statusFilter;
    return matchesQuery && matchesStatus;
  });
</script>

<AdminLayout>
  <div class="flex flex-col h-[calc(100vh-8rem)]">
    <div class="flex flex-wrap items-center justify-between gap-4 mb-6 shrink-0">
      <div>
        <h1 class="text-2xl font-black text-base-content">Ticket History</h1>
        <p class="text-sm text-base-content/60">
          Review updates and audit changes across tickets.
        </p>
      </div>
      <button class="btn btn-sm btn-outline gap-2">
        <Icon icon="mdi:download" width="18" height="18" />
        Export History
      </button>
    </div>

    <div class="flex-1 overflow-y-auto pr-2 space-y-4">
      <section class="card bg-base-100 dark:bg-base-100 shadow-sm border border-base-content/5 rounded-lg">
        <div class="card-body p-4">
          <div class="flex flex-wrap items-center gap-3">
            <label class="input input-bordered flex items-center gap-2 flex-1 min-w-[220px]">
              <Icon icon="mdi:magnify" width="16" height="16" />
              <input
                type="search"
                placeholder="Search by ticket, action, or title..."
                class="grow"
                bind:value={query}
              />
            </label>
            <select class="select select-bordered" bind:value={statusFilter}>
              <option value="all">All Status</option>
              <option value="Open">Open</option>
              <option value="Pending">Pending</option>
              <option value="Resolved">Resolved</option>
              <option value="Closed">Closed</option>
            </select>
          </div>
        </div>
      </section>

      <section class="space-y-3">
        {#each filtered as item}
          <div class="card bg-base-100 dark:bg-base-100 shadow-sm border border-base-content/5 rounded-lg">
            <div class="card-body p-4">
              <div class="flex flex-wrap items-start justify-between gap-4">
                <div class="space-y-1">
                  <div class="flex items-center gap-2">
                    <span class="text-xs font-semibold">{item.ticketId}</span>
                    <span class="text-sm font-medium">{item.title}</span>
                  </div>
                  <p class="text-sm text-base-content/70">{item.action}</p>
                  <p class="text-xs text-base-content/50">{item.by}</p>
                </div>
                <div class="flex items-center gap-2">
                  <span class="badge badge-sm {statusConfig[item.status]}">
                    {item.status}
                  </span>
                  <span class="badge badge-sm {priorityConfig[item.priority]}">
                    {item.priority}
                  </span>
                </div>
              </div>
              <div class="flex items-center justify-between text-xs text-base-content/50 mt-3">
                <span>{item.time}</span>
                <button class="btn btn-xs btn-ghost">View Ticket</button>
              </div>
            </div>
          </div>
        {/each}

        {#if filtered.length === 0}
          <div class="text-sm text-base-content/60 text-center py-10">
            No history records found.
          </div>
        {/if}
      </section>
    </div>
  </div>
</AdminLayout>

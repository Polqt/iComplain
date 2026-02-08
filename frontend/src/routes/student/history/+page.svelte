<script lang="ts">
  import Icon from "@iconify/svelte";
  import StudentLayout from "../../../components/layout/StudentLayout.svelte";
  import type { HistoryItem, HistoryFilterType, HistorySortType } from "../../../types/history.ts";
  import { 
    historyConfig, 
    statusConfig, 
    priorityConfig,
    filterAndSortHistory 
  } from "../../../utils/history.ts";

  let activeFilter: HistoryFilterType = "all";
  let sortBy: HistorySortType = "newest";
  let searchQuery: string = "";

  const historyItems: HistoryItem[] = [
    {
      id: "1",
      ticketId: "TKT-001",
      title: "Broken AC Unit in Room 301",
      action: "resolved",
      description: "Ticket was marked as resolved by maintenance team",
      timestamp: "2 hours ago",
      date: "08 Feb 2026",
      status: "resolved",
      priority: "high",
      category: "Facilities",
    },
    {
      id: "2",
      ticketId: "TKT-002",
      title: "Leaking Faucet in Restroom",
      action: "updated",
      description: "Status changed from Pending to In Progress",
      timestamp: "5 hours ago",
      date: "08 Feb 2026",
      status: "in-progress",
      priority: "medium",
      category: "Plumbing",
    },
    {
      id: "3",
      ticketId: "TKT-003",
      title: "Flickering Hallway Lights",
      action: "commented",
      description: "Admin added a comment: 'Electrician scheduled for tomorrow'",
      timestamp: "1 day ago",
      date: "07 Feb 2026",
      status: "in-progress",
      priority: "high",
      category: "Electrical",
    },
    {
      id: "4",
      ticketId: "TKT-004",
      title: "Broken Projector Screen",
      action: "created",
      description: "New ticket created for projector screen issue",
      timestamp: "2 days ago",
      date: "06 Feb 2026",
      status: "pending",
      priority: "low",
      category: "Equipment",
    },
    {
      id: "5",
      ticketId: "TKT-005",
      title: "Door Lock Malfunction",
      action: "closed",
      description: "Ticket closed after successful repair verification",
      timestamp: "3 days ago",
      date: "05 Feb 2026",
      status: "closed",
      priority: "high",
      category: "Security",
    },
    {
      id: "6",
      ticketId: "TKT-006",
      title: "Missing Whiteboard Markers",
      action: "resolved",
      description: "Markers delivered and ticket marked as resolved",
      timestamp: "4 days ago",
      date: "04 Feb 2026",
      status: "resolved",
      priority: "low",
      category: "Supplies",
    },
    {
      id: "7",
      ticketId: "TKT-007",
      title: "Noisy Ventilation System",
      action: "reopened",
      description: "Ticket reopened due to recurring issue",
      timestamp: "5 days ago",
      date: "03 Feb 2026",
      status: "in-progress",
      priority: "medium",
      category: "Facilities",
    },
    {
      id: "8",
      ticketId: "TKT-008",
      title: "Broken Window in Classroom 205",
      action: "updated",
      description: "Priority changed from Low to High",
      timestamp: "1 week ago",
      date: "01 Feb 2026",
      status: "pending",
      priority: "high",
      category: "Facilities",
    },
  ];

  $: filteredItems = filterAndSortHistory(
    historyItems,
    activeFilter,
    searchQuery,
    sortBy
  );

  function clearFilters() {
    activeFilter = "all";
    searchQuery = "";
    sortBy = "newest";
  }
</script>

<StudentLayout>
  <div class="flex flex-col h-[calc(100vh-8rem)]">
    <!-- Header Section -->
    <div class="shrink-0 mb-6">
      <h1 class="text-2xl font-black text-base-content mb-1">Ticket History</h1>
      <p class="text-sm text-base-content/60">
        View all your ticket activities and status changes.
      </p>
    </div>

    <!-- Filters and Search Section -->
    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6 shrink-0">
      <!-- Filter Tabs -->
      <div class="tabs tabs-boxed bg-base-200 p-1">
        <button
          class="tab {activeFilter === 'all' ? 'tab-active' : ''}"
          onclick={() => (activeFilter = "all")}
        >
          All
          <span class="badge badge-sm ml-2">{historyItems.length}</span>
        </button>
        <button
          class="tab {activeFilter === 'created' ? 'tab-active' : ''}"
          onclick={() => (activeFilter = "created")}
        >
          Created
        </button>
        <button
          class="tab {activeFilter === 'updated' ? 'tab-active' : ''}"
          onclick={() => (activeFilter = "updated")}
        >
          Updated
        </button>
        <button
          class="tab {activeFilter === 'resolved' ? 'tab-active' : ''}"
          onclick={() => (activeFilter = "resolved")}
        >
          Resolved
        </button>
        <button
          class="tab {activeFilter === 'closed' ? 'tab-active' : ''}"
          onclick={() => (activeFilter = "closed")}
        >
          Closed
        </button>
      </div>

      <!-- Sort and Search Controls -->
      <div class="flex items-center gap-3">
        <!-- Search Input -->
        <div class="form-control">
          <div class="input-group">
            <input
              type="text"
              placeholder="Search history..."
              class="input input-bordered input-sm w-48"
              bind:value={searchQuery}
            />
            {#if searchQuery}
              <button
                class="btn btn-square btn-sm"
                onclick={() => (searchQuery = "")}
              >
                <Icon icon="mdi:close" width="16" height="16" />
              </button>
            {/if}
          </div>
        </div>

        <!-- Sort Dropdown -->
        <div class="dropdown dropdown-end">
          <button tabindex={0} class="btn btn-sm btn-outline gap-2">
            <Icon icon="mdi:sort" width="16" height="16" />
            {sortBy === "newest" ? "Newest" : "Oldest"}
          </button>
          <ul class="dropdown-content menu p-2 shadow bg-base-100 rounded-box w-40 mt-2">
            <li>
              <button onclick={() => (sortBy = "newest")}>
                <Icon icon="mdi:sort-descending" width="16" height="16" />
                Newest First
              </button>
            </li>
            <li>
              <button onclick={() => (sortBy = "oldest")}>
                <Icon icon="mdi:sort-ascending" width="16" height="16" />
                Oldest First
              </button>
            </li>
          </ul>
        </div>

        <!-- Clear Filters -->
        {#if activeFilter !== "all" || searchQuery || sortBy !== "newest"}
          <button class="btn btn-sm btn-ghost" onclick={clearFilters}>
            <Icon icon="mdi:filter-off" width="16" height="16" />
            Clear
          </button>
        {/if}
      </div>
    </div>

    <!-- Results Count -->
    {#if filteredItems.length > 0}
      <div class="mb-4 shrink-0">
        <p class="text-sm text-base-content/60">
          Showing <span class="font-semibold text-primary">{filteredItems.length}</span>
          {filteredItems.length === 1 ? "activity" : "activities"}
          {#if activeFilter !== "all"}
            in <span class="font-semibold">{historyConfig[activeFilter].label}</span>
          {/if}
        </p>
      </div>
    {/if}

    <!-- History Timeline -->
    <div class="flex-1 overflow-y-auto pr-2">
      {#if filteredItems.length === 0}
        <!-- Empty State -->
        <div class="flex flex-col items-center justify-center h-full text-center py-12">
          <Icon
            icon="mdi:history"
            width="64"
            height="64"
            class="text-base-content/20 mb-4"
          />
          <h3 class="text-lg font-semibold text-base-content/80 mb-1">
            No history found
          </h3>
          <p class="text-sm text-base-content/50 mb-4">
            {searchQuery
              ? "No activities match your search criteria."
              : "You don't have any ticket history yet."}
          </p>
          {#if searchQuery || activeFilter !== "all"}
            <button class="btn btn-sm btn-primary" onclick={clearFilters}>
              Clear Filters
            </button>
          {/if}
        </div>
      {:else}
        <!-- Timeline Items -->
        <div class="space-y-4">
          {#each filteredItems as item, index}
            <div class="flex gap-4">
              <!-- Timeline Line -->
              <div class="flex flex-col items-center">
                <div
                  class="w-10 h-10 rounded-full {historyConfig[item.action].bgColor} flex items-center justify-center shrink-0"
                >
                  <Icon
                    icon={historyConfig[item.action].icon}
                    width="20"
                    height="20"
                    class={historyConfig[item.action].color}
                  />
                </div>
                {#if index < filteredItems.length - 1}
                  <div class="w-0.5 h-full bg-base-content/10 mt-2"></div>
                {/if}
              </div>

              <!-- Content Card -->
              <div class="flex-1 pb-4">
                <div
                  class="card bg-base-100 shadow-sm hover:shadow-md transition-all duration-200 border border-base-content/5"
                >
                  <div class="card-body p-4">
                    <!-- Header -->
                    <div class="flex items-start justify-between gap-3 mb-3">
                      <div class="flex-1 min-w-0">
                        <div class="flex items-center gap-2 mb-2">
                          <span
                            class="badge badge-sm {historyConfig[item.action].color} {historyConfig[item.action].bgColor} border-0"
                          >
                            {historyConfig[item.action].label}
                          </span>
                          <span class="text-xs text-base-content/50">
                            {item.ticketId}
                          </span>
                        </div>
                        <h3 class="font-semibold text-base text-base-content mb-1">
                          {item.title}
                        </h3>
                        <p class="text-sm text-base-content/70">
                          {item.description}
                        </p>
                      </div>
                      <button class="btn btn-ghost btn-xs btn-circle shrink-0">
                        <Icon icon="mdi:dots-horizontal" width="16" height="16" />
                      </button>
                    </div>

                    <!-- Footer -->
                    <div class="flex items-center justify-between pt-3 border-t border-base-content/5">
                      <div class="flex items-center gap-3 text-xs text-base-content/60">
                        <div class="flex items-center gap-1">
                          <Icon icon="mdi:clock-outline" width="14" height="14" />
                          <span>{item.timestamp}</span>
                        </div>
                        <div class="flex items-center gap-1">
                          <Icon icon="mdi:calendar-outline" width="14" height="14" />
                          <span>{item.date}</span>
                        </div>
                        {#if item.category}
                          <div class="flex items-center gap-1">
                            <Icon icon="mdi:tag-outline" width="14" height="14" />
                            <span>{item.category}</span>
                          </div>
                        {/if}
                      </div>

                      <div class="flex items-center gap-2">
                        <div class="badge {statusConfig[item.status].color} badge-sm">
                          {statusConfig[item.status].label}
                        </div>
                        <div class="badge {priorityConfig[item.priority].color} badge-sm">
                          {priorityConfig[item.priority].label}
                        </div>
                      </div>
                    </div>

                    <!-- Action Button -->
                    <div class="mt-3">
                      <a
                        href="/student/tickets/{item.ticketId}"
                        class="btn btn-sm btn-outline btn-primary w-full sm:w-auto"
                      >
                        <Icon icon="mdi:eye-outline" width="16" height="16" />
                        View Ticket
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          {/each}
        </div>
      {/if}
    </div>
  </div>
</StudentLayout>

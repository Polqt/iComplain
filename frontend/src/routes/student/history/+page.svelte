<script lang="ts">
  import StudentLayout from "../../../components/layout/StudentLayout.svelte";
  import {
    type HistoryItem,
    type HistoryFilterType,
    type HistorySortType,
    historyConfig,
    filterAndSortHistory,
    HistoryFilters,
    HistoryTimeline,
  } from "../../../components/ui/history";

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
      id: "TKT-004",
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
      id: "TKT-005",
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
      id: "TKT-006",
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
    <div class="shrink-0 mb-6">
      <h1 class="text-2xl font-black text-base-content mb-1">Ticket History</h1>
      <p class="text-sm text-base-content/60">
        View all your ticket activities and status changes.
      </p>
    </div>

    <div class="mb-6 shrink-0">
      <HistoryFilters
        bind:activeFilter
        bind:sortBy
        bind:searchQuery
        totalCount={historyItems.length}
        onclear={clearFilters}
      />
    </div>

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

    <div class="flex-1 overflow-y-auto pr-2">
      <HistoryTimeline
        items={filteredItems}
        {activeFilter}
        {searchQuery}
        ticketUrlPrefix="/student/tickets"
        onclearfilters={clearFilters}
      />
    </div>
  </div>
</StudentLayout>

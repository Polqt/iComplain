<script lang="ts">
  import StudentLayout from "../../components/layout/StudentLayout.svelte";
  import { ticketsStore } from "../../stores/tickets.store.ts";
  import { onMount } from "svelte";
  import type { TicketStatus } from "../../types/tickets.ts";
  import { columns, getPriorityKey } from "../../utils/ticketConfig.ts";
  import TicketFilters from "../../components/ui/tickets/TicketFilters.svelte";
  import KanbanColumn from "../../components/ui/tickets/KanbanColumn.svelte";
  import KanbanSkeleton from "../../components/ui/tickets/KanbanSkeleton.svelte";
  import ErrorState from "../../components/ui/ErrorState.svelte";
  import { COMMUNITY_STATUSES } from "../../utils/paginationConfig.ts";

  $: ({ tickets, isLoading, error } = $ticketsStore);

  onMount(async () => {
    await ticketsStore.loadCommunityTickets();
  });

  let search = "";
  let activeStatus: TicketStatus | "all" = "all";
  let priorityFilter = "all";
  let currentPage = 1;
  const pageSize = 10;

  $: filtered = tickets.filter((t) => {
    const q = search.trim().toLowerCase();
    const matchSearch =
      !q ||
      t.title.toLowerCase().includes(q) ||
      t.building.toLowerCase().includes(q) ||
      t.room_name.toLowerCase().includes(q) ||
      t.category.name.toLowerCase().includes(q) ||
      t.ticket_number.toLowerCase().includes(q);
    const matchStatus = activeStatus === "all" || t.status === activeStatus;
    const matchPriority =
      priorityFilter === "all" || getPriorityKey(t.priority) === priorityFilter;
    return matchSearch && matchStatus && matchPriority;
  });

  $: ticketsByStatus = COMMUNITY_STATUSES.reduce(
    (acc, status) => {
      acc[status] = filtered.filter((t) => t.status === status);
      return acc;
    },
    {} as Record<TicketStatus, typeof filtered>,
  );

  $: statusCounts = {
    all: filtered.length,
    ...COMMUNITY_STATUSES.reduce(
      (acc, status) => {
        acc[status] = ticketsByStatus[status]?.length ?? 0;
        return acc;
      },
      {} as Record<TicketStatus, number>,
    ),
  };

  $: totalPages = Math.ceil(filtered.length / pageSize);
  $: {
    if (currentPage > totalPages && totalPages > 0) {
      currentPage = totalPages;
    }
  }
  $: paginatedTickets = filtered.slice(
    (currentPage - 1) * pageSize,
    currentPage * pageSize,
  );

  function handleFilterChange<T>(setter: (value: T) => void) {
    return (value: T) => {
      setter(value);
      currentPage = 1;
    };
  }

  function handlePageChange(page: number) {
    currentPage = page;
  }

  function handleClearFilters() {
    search = "";
    activeStatus = "all";
    priorityFilter = "all";
    currentPage = 1;
  }

  function handleStatusClick(status: TicketStatus) {
    activeStatus = status;
    currentPage = 1;
  }
</script>

<StudentLayout>
  <div class="flex flex-col h-[calc(100vh-8rem)]">
    <div class="shrink-0 mb-6">
      <h1 class="text-2xl font-black text-base-content mb-1">
        Community Board
      </h1>
      <p class="text-sm text-base-content/60">
        Campus-wide issues — see what's reported and being fixed
      </p>
    </div>

    <div class="mb-4 shrink-0">
      <TicketFilters
        {search}
        {activeStatus}
        {priorityFilter}
        {statusCounts}
        totalCount={filtered.length}
        onSearchChange={handleFilterChange((v) => (search = v))}
        onStatusChange={handleFilterChange((v) => (activeStatus = v))}
        onPriorityChange={handleFilterChange((v) => (priorityFilter = v))}
        onClear={handleClearFilters}
      />
    </div>

    {#if isLoading}
      <KanbanSkeleton />
    {:else if error}
      <ErrorState {error} onRetry={() => ticketsStore.loadCommunityTickets()} />
    {:else}
      <div class="flex gap-6 flex-1 min-h-0">
        <KanbanColumn
          tickets={paginatedTickets}
          {totalPages}
          {currentPage}
          onPageChange={handlePageChange}
        />

        <div class="w-64 shrink-0">
          <div class="sticky top-0 space-y-2">
            {#each columns as col}
              {@const count = statusCounts[col.id] ?? 0}
              {@const percentage =
                statusCounts.all > 0 ? (count / statusCounts.all) * 100 : 0}
              <button
                on:click={() => handleStatusClick(col.id)}
                class="w-full card border hover:border-opacity-100 transition-all cursor-pointer
                       {col.headerTint.replace('bg-base-200', 'bg-base-100')}"
                class:ring-2={activeStatus === col.id}
                class:ring-offset-2={activeStatus === col.id}
                style="--tw-ring-color: {col.dot.replace('bg-', '')}"
              >
                <div class="card-body p-4">
                  <div class="flex items-center justify-between mb-2">
                    <span
                      class="text-sm font-bold uppercase tracking-wide {col.countText}"
                    >
                      {col.label}
                    </span>
                    <span class="text-2xl font-black {col.countText}">
                      {count}
                    </span>
                  </div>
                  <div class="w-full bg-base-200 rounded-full h-2">
                    <div
                      class="h-2 rounded-full transition-all duration-300 {col.dot}"
                      style="width: {percentage}%"
                    ></div>
                  </div>
                </div>
              </button>
            {/each}
          </div>
        </div>
      </div>
    {/if}
  </div>
</StudentLayout>

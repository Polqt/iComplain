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
  import {
    COMMUNITY_PAGE_SIZE,
    COMMUNITY_STATUSES,
    createInitialPageState,
    getPageSlice,
    getTotalPages,
  } from "../../utils/paginationConfig.ts";

  $: ({ tickets, isLoading, error } = $ticketsStore);

  onMount(async () => {
    await ticketsStore.loadCommunityTickets();
  });

  let search = "";
  let activeStatus: TicketStatus | "all" = "all";
  let priorityFilter = "all";
  let currentPageByStatus = createInitialPageState();

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

  $: totalPagesByStatus = COMMUNITY_STATUSES.reduce(
    (acc, status) => {
      acc[status] = getTotalPages(
        ticketsByStatus[status]?.length ?? 0,
        COMMUNITY_PAGE_SIZE,
      );
      return acc;
    },
    {} as Record<TicketStatus, number>,
  );

  $: {
    const updated = { ...currentPageByStatus };
    let changed = false;
    COMMUNITY_STATUSES.forEach((status) => {
      const max = totalPagesByStatus[status] ?? 1;
      if (updated[status] > max) {
        updated[status] = max;
        changed = true;
      }
    });
    if (changed) currentPageByStatus = updated;
  }

  function handleFilterChange<T>(setter: (value: T) => void) {
    return (value: T) => {
      setter(value);
      currentPageByStatus = createInitialPageState();
    };
  }

  function handlePageChange(status: TicketStatus, page: number) {
    currentPageByStatus = { ...currentPageByStatus, [status]: page };
  }

  function handleClearFilters() {
    search = "";
    activeStatus = "all";
    priorityFilter = "all";
    currentPageByStatus = createInitialPageState();
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
      <ErrorState
        error={error}
        onRetry={() => ticketsStore.loadCommunityTickets()}
      />
    {:else}
      <div class="grid grid-cols-4 gap-3 flex-1 min-h-0">
        {#each columns as col}
          {@const status = col.id}
          {@const allTickets = ticketsByStatus[status] ?? []}
          {@const currentPage = currentPageByStatus[status] ?? 1}
          {@const pageTickets = getPageSlice(
            allTickets,
            currentPage,
            COMMUNITY_PAGE_SIZE,
          )}
          {@const totalPages = totalPagesByStatus[status] ?? 1}

          <KanbanColumn
            column={col}
            {status}
            tickets={allTickets}
            {pageTickets}
            {totalPages}
            {currentPage}
            onPageChange={(page) => handlePageChange(status, page)}
          />
        {/each}
      </div>
    {/if}
  </div>
</StudentLayout>

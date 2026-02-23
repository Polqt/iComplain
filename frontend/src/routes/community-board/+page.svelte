<script lang="ts">
  import StudentLayout from "../../components/layout/StudentLayout.svelte";
  import { ticketsStore } from "../../stores/tickets.store.ts";
  import { onMount } from "svelte";
  import type { Ticket, TicketStatus } from "../../types/tickets.ts";
  import { getPriorityKey } from "../../utils/ticketConfig.ts";
  import TicketFilters from "../../components/ui/tickets/TicketFilters.svelte";
  import CommunityTicketCard from "../../components/ui/tickets/CommunityTicketCard.svelte";
  import KanbanSkeleton from "../../components/ui/tickets/KanbanSkeleton.svelte";
  import ErrorState from "../../components/ui/ErrorState.svelte";
  import { COMMUNITY_STATUSES } from "../../utils/paginationConfig.ts";
  import Icon from "@iconify/svelte";
  import CommentDrawer from "../../components/ui/comments/CommentDrawer.svelte";

  $: ({ tickets, isLoading, error } = $ticketsStore);

  onMount(async () => {
    await ticketsStore.loadCommunityTickets();
  });

  let search = "";
  let activeStatus: TicketStatus | "all" = "all";
  let priorityFilter = "all";
  let categoryFilter = "all";
  let selectedTicket: Ticket | null = null;

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
    const matchCategory =
      categoryFilter === "all" ||
      t.category.name.toLowerCase() === categoryFilter.toLowerCase();
    return matchSearch && matchStatus && matchPriority && matchCategory;
  });

  $: statusCounts = {
    all: filtered.length,
    ...COMMUNITY_STATUSES.reduce(
      (acc, status) => {
        acc[status] = filtered.filter((t) => t.status === status).length;
        return acc;
      },
      {} as Record<TicketStatus, number>,
    ),
  };

  function handleClearFilters() {
    search = "";
    activeStatus = "all";
    priorityFilter = "all";
    categoryFilter = "all";
  }

  function handleTicketClick(ticket: Ticket) {
    selectedTicket = ticket;
  }
</script>

<StudentLayout>
  <div class="flex flex-col h-[calc(100vh-8rem)]">
    <div class="flex items-center justify-between gap-4 mb-5 shrink-0">
      <div class="flex-1 min-w-0">
        <h1 class="text-2xl font-black text-base-content mb-1">
          Community Board
        </h1>
        <p class="text-sm text-base-content/60">
          Campus-wide issues — see what's reported and being fixed
        </p>
      </div>
    </div>

    <div class="mb-4 shrink-0">
      <TicketFilters
        bind:search
        bind:activeStatus
        bind:priorityFilter
        bind:categoryFilter
        {statusCounts}
        totalCount={filtered.length}
        onStatusChange={(v) => (activeStatus = v)}
        onPriorityChange={(v) => (priorityFilter = v)}
        onCategoryChange={(v) => (categoryFilter = v)}
        onClear={handleClearFilters}
      />
    </div>

    {#if isLoading}
      <KanbanSkeleton />
    {:else if error}
      <ErrorState {error} onRetry={() => ticketsStore.loadCommunityTickets()} />
    {:else}
      <div class="flex gap-4 flex-1 min-h-0">
        <div class="flex-1 overflow-y-auto pr-2">
          {#if filtered.length === 0}
            <div
              class="flex flex-col items-center justify-center h-full text-center py-12"
            >
              <Icon
                icon="mdi:ticket-outline"
                width="64"
                height="64"
                class="text-base-content/15 mb-4"
              />
              <h3 class="text-lg font-semibold text-base-content/60 mb-2">
                No tickets found
              </h3>
              <p class="text-sm text-base-content/40">
                Try adjusting your filters or search query
              </p>
            </div>
          {:else}
            <div class="grid gap-3">
              {#each filtered as ticket (ticket.id)}
                <CommunityTicketCard
                  {ticket}
                  isActive={selectedTicket?.id === ticket.id}
                  onClick={() => handleTicketClick(ticket)}
                />
              {/each}
            </div>
          {/if}
        </div>

        <CommentDrawer ticket={selectedTicket} />
      </div>
    {/if}
  </div>
</StudentLayout>

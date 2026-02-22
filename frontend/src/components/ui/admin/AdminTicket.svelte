<script lang="ts">
  import { onMount } from "svelte";
  import Icon from "@iconify/svelte";
  import AdminLayout from "../../../components/layout/AdminLayout.svelte";
  import { ticketsStore } from "../../../stores/tickets.store.ts";
  import { fetchCategories } from "../../../lib/api/ticket.ts";
  import type { TicketStatus, Category } from "../../../types/tickets.ts";
  import { statusConfig } from "../../../utils/ticketConfig.ts";

  $: ({ tickets, isLoading, error } = $ticketsStore);

  let categories: Category[] = [];
  let selectedTicketId: number | null = null;

  let searchQuery = "";
  let statusFilter: TicketStatus | "all" = "all";
  let priorityFilter = "all";
  let categoryFilter = "all";
  let locationFilter = "all";

  $: selectedTicket = tickets.find((t) => t.id === selectedTicketId) ?? null;

  $: locations = Array.from(
    new Set(tickets.map((t) => `${t.building} - ${t.room_name}`)),
  ).sort();

  $: filteredTickets = tickets.filter((ticket) => {
    const query = searchQuery.trim().toLowerCase();
    const matchesQuery =
      !query ||
      ticket.title.toLowerCase().includes(query) ||
      ticket.description.toLowerCase().includes(query) ||
      ticket.ticket_number.toLowerCase().includes(query) ||
      ticket.student.name?.toLowerCase().includes(query);

    const matchesStatus =
      statusFilter === "all" || ticket.status === statusFilter;
    const matchesPriority =
      priorityFilter === "all" ||
      ticket.priority.name.toLowerCase() === priorityFilter;
    const matchesCategory =
      categoryFilter === "all" || ticket.category.name === categoryFilter;

    const locationLabel = `${ticket.building} - ${ticket.room_name}`;
    const matchesLocation =
      locationFilter === "all" || locationLabel === locationFilter;

    return (
      matchesQuery &&
      matchesStatus &&
      matchesPriority &&
      matchesCategory &&
      matchesLocation
    );
  });

  onMount(async () => {
    await Promise.all([
      ticketsStore.loadTickets(),
      fetchCategories().then((cats) => (categories = cats)),
    ]);

    if (filteredTickets.length > 0) {
      selectedTicketId = filteredTickets[0].id;
    }
  });

  async function handleStatusChange(ticketId: number, newStatus: TicketStatus) {
    await ticketsStore.adminPatchTicket(ticketId, { status: newStatus });
  }

  async function handlePriorityChange(ticketId: number, newPriorityId: number) {
    await ticketsStore.adminPatchTicket(ticketId, { priority: newPriorityId });
  }
</script>

<AdminLayout>
  <div class="flex flex-col h-[calc(100vh-8rem)] gap-4">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-black text-base-content">Tickets</h1>
        <p class="text-sm text-base-content/60">
          View and manage support tickets in one place.
        </p>
      </div>
    </div>

    <section
      class="card bg-base-100 shadow-sm border border-base-content/5 rounded-lg"
    >
      <div class="card-body p-4">
        <div class="grid grid-cols-1 lg:grid-cols-6 gap-3">
          <label
            class="input input-bordered flex items-center gap-2 lg:col-span-2"
          >
            <Icon icon="mdi:magnify" width="16" height="16" />
            <input
              type="search"
              placeholder="Search tickets, students, IDs..."
              class="grow"
              bind:value={searchQuery}
            />
          </label>

          <select class="select select-bordered" bind:value={statusFilter}>
            <option value="all">All Status</option>
            <option value="pending">Pending</option>
            <option value="in_progress">In Progress</option>
            <option value="resolved">Resolved</option>
            <option value="closed">Closed</option>
          </select>

          <select class="select select-bordered" bind:value={priorityFilter}>
            <option value="all">All Priority</option>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
            <option value="urgent">Urgent</option>
          </select>

          <select class="select select-bordered" bind:value={locationFilter}>
            <option value="all">All Locations</option>
            {#each locations as location}
              <option value={location}>{location}</option>
            {/each}
          </select>

          <select class="select select-bordered" bind:value={categoryFilter}>
            <option value="all">All Categories</option>
            {#each categories as category}
              <option value={category.name}>{category.name}</option>
            {/each}
          </select>
        </div>
      </div>
    </section>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 flex-1 min-h-0">
      <section
        class="card bg-base-100 shadow-sm border border-base-content/5 rounded-lg overflow-hidden"
      >
        <div class="card-body p-0 h-full flex flex-col">
          <div class="p-4 border-b border-base-content/5 shrink-0">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <h2 class="text-sm font-semibold">Total tickets</h2>
                <span class="badge badge-sm badge-ghost"
                  >{filteredTickets.length}</span
                >
              </div>
            </div>
          </div>

          <div class="flex-1 overflow-y-auto">
            {#if isLoading}
              <div class="p-6 text-center">
                <span class="loading loading-spinner loading-md"></span>
              </div>
            {:else if filteredTickets.length === 0}
              <div class="p-6 text-center text-sm text-base-content/60">
                No tickets found.
              </div>
            {:else}
              {#each filteredTickets as ticket (ticket.id)}
                <button
                  type="button"
                  class="w-full text-left px-4 py-3 border-b border-base-content/5
                         hover:bg-base-200 transition-colors
                         {ticket.id === selectedTicketId ? 'bg-base-200' : ''}"
                  onclick={() => (selectedTicketId = ticket.id)}
                >
                  <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-semibold font-mono"
                      >{ticket.ticket_number}</span
                    >
                    <span class="text-xs text-base-content/50">
                      {new Date(ticket.updated_at).toLocaleDateString()}
                    </span>
                  </div>

                  <div class="flex items-center justify-between gap-2">
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-medium truncate">
                        {ticket.student.name || "Anonymous"}
                      </p>
                      <p class="text-xs text-base-content/60 line-clamp-1">
                        {ticket.title}
                      </p>
                    </div>

                    <!-- Unread Badge (if comments_count > 0) -->
                    {#if ticket.comments_count && ticket.comments_count > 0}
                      <span class="badge badge-primary badge-sm">
                        {ticket.comments_count}
                      </span>
                    {/if}
                  </div>
                </button>
              {/each}
            {/if}
          </div>
        </div>
      </section>

      <section
        class="card bg-base-100 shadow-sm border border-base-content/5 rounded-lg lg:col-span-2 overflow-hidden"
      >
        <div class="card-body p-4 h-full overflow-y-auto">
          {#if selectedTicket}
            <div class="flex flex-wrap items-center justify-between gap-3 mb-4">
              <div>
                <h2 class="text-lg font-semibold">{selectedTicket.title}</h2>
                <p class="text-xs text-base-content/60">
                  {selectedTicket.ticket_number} • {selectedTicket.student
                    .name || "Anonymous"}
                </p>
              </div>
              <div class="flex items-center gap-2">
                <span
                  class="badge badge-sm {statusConfig[selectedTicket.status]
                    .color}"
                >
                  {statusConfig[selectedTicket.status].label}
                </span>
                <span class="badge badge-sm badge-outline">
                  {selectedTicket.priority.name}
                </span>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div class="space-y-2">
                <p class="text-xs text-base-content/60 font-semibold">
                  Description
                </p>
                <p class="text-sm">{selectedTicket.description}</p>
              </div>
              <div class="space-y-3">
                <div>
                  <p class="text-xs text-base-content/60 font-semibold mb-2">
                    Location
                  </p>
                  <div class="flex flex-wrap gap-2">
                    <span class="badge badge-outline badge-sm">
                      {selectedTicket.building}
                    </span>
                    <span class="badge badge-outline badge-sm">
                      {selectedTicket.room_name}
                    </span>
                  </div>
                </div>
                <div>
                  <p class="text-xs text-base-content/60 font-semibold mb-2">
                    Category
                  </p>
                  <span class="badge badge-outline badge-sm">
                    {selectedTicket.category.name}
                  </span>
                </div>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-4">
              <div>
                <p class="text-xs text-base-content/60 font-semibold mb-1">
                  Status
                </p>
                <select
                  class="select select-bordered select-sm w-full"
                  value={selectedTicket.status}
                  onchange={(e) =>
                    handleStatusChange(
                      selectedTicket.id,
                      (e.target as HTMLSelectElement).value as TicketStatus,
                    )}
                >
                  <option value="pending">Pending</option>
                  <option value="in_progress">In Progress</option>
                  <option value="resolved">Resolved</option>
                  <option value="closed">Closed</option>
                </select>
              </div>

              <div>
                <p class="text-xs text-base-content/60 font-semibold mb-1">
                  Priority
                </p>
                <select
                  class="select select-bordered select-sm w-full"
                  value={selectedTicket.priority.id}
                  onchange={(e) =>
                    handlePriorityChange(
                      selectedTicket.id,
                      parseInt((e.target as HTMLSelectElement).value),
                    )}
                >
                  <option value="1">Low</option>
                  <option value="2">Medium</option>
                  <option value="3">High</option>
                  <option value="4">Urgent</option>
                </select>
              </div>

              <div>
                <p class="text-xs text-base-content/60 font-semibold mb-1">
                  Updated
                </p>
                <div
                  class="px-3 py-2 rounded-lg border border-base-content/10 bg-base-200 text-sm"
                >
                  {new Date(selectedTicket.updated_at).toLocaleString()}
                </div>
              </div>
            </div>

            <div class="flex flex-wrap items-center gap-2">
              <button
                type="button"
                class="btn btn-sm btn-outline gap-2"
                onclick={() =>
                  (window.location.href = `/history?ticket=${selectedTicket.id}`)}
              >
                <Icon icon="mdi:history" width="18" height="18" />
                View History
              </button>
            </div>
          {:else}
            <div
              class="flex flex-col items-center justify-center h-full text-base-content/60"
            >
              <Icon
                icon="mdi:ticket-outline"
                width="48"
                height="48"
                class="mb-3"
              />
              <p class="text-sm">Select a ticket to view details</p>
            </div>
          {/if}
        </div>
      </section>
    </div>
  </div>
</AdminLayout>

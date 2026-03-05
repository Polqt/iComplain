<script lang="ts">
  import { onDestroy, onMount, tick } from "svelte";
  import { page } from "$app/stores";
  import Icon from "@iconify/svelte";
  import AdminLayout from "../../../components/layout/AdminLayout.svelte";
  import { ticketsStore } from "../../../stores/tickets.store.ts";
  import { fetchCategories } from "../../../lib/api/ticket.ts";
  import type { TicketStatus, Category } from "../../../types/tickets.ts";
  import { statusConfig } from "../../../utils/ticketConfig.ts";
  import AttachmentModal from "./AttachmentModal.svelte";
  import CommentSection from "../comments/CommentSection.svelte";

  $: ({ tickets, isLoading } = $ticketsStore);

  let categories: Category[] = [];
  let selectedTicketId: number | null = null;

  let searchQuery = "";
  let statusFilter: TicketStatus | "all" = "all";
  let priorityFilter = "all";
  let categoryFilter = "all";
  let locationFilter = "all";
  let pendingStatus: TicketStatus | null = null;
  let pendingPriority: number | null = null;
  let isSaving = false;
  let highlightedTicketId: number | null = null;
  let handledQueryTicketId: number | null = null;
  let highlightTimer: ReturnType<typeof setTimeout> | null = null;
  const ticketRowElements = new Map<number, HTMLButtonElement>();

  $: selectedTicket = tickets.find((t) => t.id === selectedTicketId) ?? null;

  $: hasChanges =
    selectedTicket &&
    ((pendingStatus != null && pendingStatus !== selectedTicket.status) ||
      (pendingPriority != null &&
        pendingPriority !== selectedTicket.priority.id));

  $: if (selectedTicket) {
    pendingStatus = null;
    pendingPriority = null;
  }

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
  }).sort((a, b) => {
    const aTime = new Date(a.updated_at).getTime();
    const bTime = new Date(b.updated_at).getTime();
    return bTime - aTime || b.id - a.id;
  });

  $: queryTicketId = (() => {
    const raw = $page.url.searchParams.get("ticket");
    if (!raw) return null;
    const parsed = Number(raw);
    return Number.isInteger(parsed) && parsed > 0 ? parsed : null;
  })();

  $: {
    if (filteredTickets.length === 0) {
      selectedTicketId = null;
    } else if (
      selectedTicketId == null ||
      !filteredTickets.some((t) => t.id === selectedTicketId)
    ) {
      selectedTicketId = filteredTickets[0].id;
    }
  }

  $: if (
    !isLoading &&
    queryTicketId !== null &&
    handledQueryTicketId !== queryTicketId
  ) {
    searchQuery = "";
    statusFilter = "all";
    priorityFilter = "all";
    categoryFilter = "all";
    locationFilter = "all";

    const exists = tickets.some((ticket) => ticket.id === queryTicketId);
    if (exists) {
      selectedTicketId = queryTicketId;
      highlightTicket(queryTicketId);
    }
    handledQueryTicketId = queryTicketId;
  }

  onMount(async () => {
    await Promise.all([
      ticketsStore.loadTickets(),
      fetchCategories().then((cats) => (categories = cats)),
    ]);
  });

  onDestroy(() => {
    if (highlightTimer) clearTimeout(highlightTimer);
    ticketRowElements.clear();
  });

  function registerTicketRow(node: HTMLButtonElement, ticketId: number) {
    ticketRowElements.set(ticketId, node);
    return {
      update(nextTicketId: number) {
        ticketRowElements.delete(ticketId);
        ticketId = nextTicketId;
        ticketRowElements.set(ticketId, node);
      },
      destroy() {
        ticketRowElements.delete(ticketId);
      },
    };
  }

  async function highlightTicket(ticketId: number) {
    highlightedTicketId = ticketId;
    await tick();
    ticketRowElements.get(ticketId)?.scrollIntoView({
      block: "center",
      behavior: "smooth",
    });

    if (highlightTimer) clearTimeout(highlightTimer);
    highlightTimer = setTimeout(() => {
      highlightedTicketId = null;
      highlightTimer = null;
    }, 4500);
  }

  function getInitials(name?: string | null) {
    if (!name) return "AN";
    return name
      .split(" ")
      .map((n: string) => n[0])
      .join("")
      .slice(0, 2)
      .toUpperCase();
  }

  function handleStatusChange(newStatus: TicketStatus) {
    pendingStatus = newStatus;
  }

  function handlePriorityChange(newPriorityId: number) {
    pendingPriority = newPriorityId;
  }

  async function handleSaveChanges() {
    if (!selectedTicket) return;

    isSaving = true;
    try {
      const updates: { status?: TicketStatus; priority?: number } = {};

      if (pendingStatus != null && pendingStatus !== selectedTicket.status) {
        updates.status = pendingStatus;
      }

      if (
        pendingPriority != null &&
        pendingPriority !== selectedTicket.priority.id
      ) {
        updates.priority = pendingPriority;
      }

      if (Object.keys(updates).length > 0) {
        await ticketsStore.adminPatchTicket(selectedTicket.id, updates);
      }

      pendingStatus = null;
      pendingPriority = null;
    } catch (error) {
      console.error("Failed to save changes:", error);
    } finally {
      isSaving = false;
    }
  }

  function handleCancelChanges() {
    pendingStatus = null;
    pendingPriority = null;
  }
</script>

<AdminLayout>
  <div class="flex flex-col h-[calc(100vh-8rem)] gap-3">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-black text-base-content">Tickets</h1>
        <p class="text-sm text-base-content/60">
          Messenger-style ticket comments with retained ticket details.
        </p>
      </div>
    </div>

    <section
      class="card bg-base-100 shadow-sm border border-base-content/5 rounded-lg"
    >
      <div class="card-body p-3">
        <div class="grid grid-cols-1 lg:grid-cols-6 gap-2">
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

    <div
      class="grid grid-cols-1 xl:grid-cols-[320px_minmax(0,1fr)_350px] gap-3 flex-1 min-h-0"
    >
      <section
        class="card bg-base-100 shadow-sm border border-base-content/5 rounded-lg overflow-hidden"
      >
        <div class="card-body p-0 h-full flex flex-col">
          <div class="p-3 border-b border-base-content/5 shrink-0">
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
                  use:registerTicketRow={ticket.id}
                  class="w-full text-left px-3 py-3 border-b border-base-content/5 hover:bg-base-200 transition-colors
                         {ticket.id === selectedTicketId
                    ? 'bg-base-200 border-l-2 border-l-info'
                    : ''}
                         {ticket.id === highlightedTicketId
                    ? 'ring-2 ring-inset ring-info/60'
                    : ''}"
                  onclick={() => (selectedTicketId = ticket.id)}
                >
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-xs font-semibold font-mono">
                      {ticket.ticket_number}
                    </span>
                    <span class="text-[11px] text-base-content/50">
                      {new Date(ticket.updated_at).toLocaleDateString()}
                    </span>
                  </div>
                  <p class="text-sm font-semibold truncate">
                    {ticket.student.name || "Anonymous"}
                  </p>
                  <div class="flex items-center justify-between gap-2 mt-1">
                    <p class="text-xs text-base-content/55 truncate">
                      {ticket.title}
                    </p>
                    {#if ticket.comments_count && ticket.comments_count > 0}
                      <span class="badge badge-info badge-sm">
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
        class="card bg-base-100 shadow-sm border border-base-content/5 rounded-lg overflow-hidden"
      >
        {#if selectedTicket}
          <div class="h-full flex flex-col">
            <div
              class="px-4 py-3 border-b border-base-content/8 bg-base-200/70 flex items-center justify-between gap-3 shrink-0"
            >
              <div class="flex items-center gap-3 min-w-0">
                <div class="avatar placeholder shrink-0">
                  <div
                    class="w-10 h-10 rounded-full bg-info/15 ring-1 ring-info/20 text-info"
                  >
                    <span class="text-xs font-bold">
                      {getInitials(selectedTicket.student.name)}
                    </span>
                  </div>
                </div>
                <div class="min-w-0">
                  <p class="text-sm font-bold truncate">
                    {selectedTicket.student.name || "Anonymous"}
                  </p>
                  <p class="text-xs text-base-content/55 truncate">
                    {selectedTicket.ticket_number} - {selectedTicket.title}
                  </p>
                </div>
              </div>
              <div class="flex items-center gap-2 shrink-0">
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

            <div class="flex-1 min-h-0">
              {#key selectedTicket.id}
                <CommentSection
                  ticketId={selectedTicket.id}
                  ticketStatus={selectedTicket.status}
                  compact={true}
                  variant="messenger"
                />
              {/key}
            </div>
          </div>
        {:else}
          <div
            class="h-full flex flex-col items-center justify-center text-base-content/60"
          >
            <Icon
              icon="mdi:message-text-outline"
              width="48"
              height="48"
              class="mb-3"
            />
            <p class="text-sm">Select a ticket to open comments</p>
          </div>
        {/if}
      </section>

      <section
        class="card bg-base-100 shadow-sm border border-base-content/5 rounded-lg overflow-hidden"
      >
        <div class="card-body p-4 h-full overflow-y-auto">
          {#if selectedTicket}
            {#if hasChanges}
              <div class="alert alert-warning mb-3">
                <Icon icon="mdi:alert" width="18" height="18" />
                <span class="text-sm">You have unsaved changes</span>
              </div>
            {/if}

            <div class="space-y-4">
              <div>
                <h2 class="text-lg font-semibold">{selectedTicket.title}</h2>
                <p class="text-xs text-base-content/60">
                  {selectedTicket.ticket_number} - {selectedTicket.student.name ||
                    "Anonymous"}
                </p>
              </div>

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

              {#if selectedTicket.attachment}
                <div>
                  <p class="text-xs text-base-content/60 font-semibold mb-2">
                    Attachment
                  </p>
                  <AttachmentModal
                    attachment={selectedTicket.attachment}
                    ticketNumber={selectedTicket.ticket_number}
                  />
                </div>
              {/if}

              <div class="grid grid-cols-1 gap-3">
                <div>
                  <p class="text-xs text-base-content/60 font-semibold mb-1">
                    Status
                  </p>
                  <select
                    class="select select-bordered select-sm w-full"
                    value={pendingStatus ?? selectedTicket.status}
                    onchange={(e) =>
                      handleStatusChange(
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
                    value={pendingPriority ?? selectedTicket.priority.id}
                    onchange={(e) =>
                      handlePriorityChange(
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
                {#if hasChanges}
                  <button
                    type="button"
                    class="btn btn-sm btn-primary gap-2"
                    onclick={handleSaveChanges}
                    disabled={isSaving}
                  >
                    {#if isSaving}
                      <span class="loading loading-spinner loading-xs"></span>
                    {:else}
                      <Icon icon="mdi:content-save" width="18" height="18" />
                    {/if}
                    Save Changes
                  </button>
                  <button
                    type="button"
                    class="btn btn-sm btn-ghost gap-2"
                    onclick={handleCancelChanges}
                    disabled={isSaving}
                  >
                    <Icon icon="mdi:close" width="18" height="18" />
                    Cancel
                  </button>
                {/if}

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

<script lang="ts">
  import Icon from "@iconify/svelte";
  import AdminLayout from "../../../components/layout/AdminLayout.svelte";

  import {
    fetchTickets,
    fetchTicketById,
    createTicket,
    updateTicket as updateTicketAPI,
    deleteTicket,
  } from "../../../lib/api/ticket.js";

  import { onMount } from "svelte";

  type Status = "open" | "pending" | "resolved" | "closed";
  type Priority = "low" | "medium" | "high";

  type Ticket = {
    id: string;
    title: string;
    description: string;
    student: string;
    status: Status;
    priority: Priority;
    category: string;
    building: string;
    room: string;
    createdAt: string;
    updatedAt: string;
    unread: number;
  };

  const statusConfig: Record<Status, { label: string; color: string }> = {
    open: { label: "Open", color: "badge-info" },
    pending: { label: "Pending", color: "badge-warning" },
    resolved: { label: "Resolved", color: "badge-success" },
    closed: { label: "Closed", color: "badge-ghost" },
  };

  const priorityConfig: Record<Priority, { label: string; color: string }> = {
    low: { label: "Low", color: "badge-info" },
    medium: { label: "Medium", color: "badge-warning" },
    high: { label: "High", color: "badge-error" },
  };

  const categories = [
    "Facilities",
    "IT Support",
    "Safety",
    "Cleanliness",
    "Equipment",
  ];
  const locations = [
    "Building A - 1F",
    "Building A - 3F",
    "Building B - 2F",
    "Building C - 1F",
    "Gymnasium",
  ];

  let searchQuery = "";
  let statusFilter: "all" | Status = "all";
  let priorityFilter: "all" | Priority = "all";
  let categoryFilter = "all";
  let locationFilter = "all";

  let tickets: Ticket[] = [
    {
      id: "TC-0004",
      title: "System Login Failure",
      description: "Cannot access the portal after password reset.",
      student: "David Newman",
      status: "open",
      priority: "high",
      category: "IT Support",
      building: "Building B",
      room: "Library 2F",
      createdAt: "Feb 08, 2026",
      updatedAt: "09:46 AM",
      unread: 2,
    },
    {
      id: "TC-0001",
      title: "Request for Additional Storage",
      description: "Need more storage for project submission files.",
      student: "Emily Johnson",
      status: "pending",
      priority: "medium",
      category: "IT Support",
      building: "Building A",
      room: "301",
      createdAt: "Feb 07, 2026",
      updatedAt: "09:10 AM",
      unread: 0,
    },
    {
      id: "TC-0003",
      title: "Unable to Access Report",
      description: "Reports page returns a blank screen on load.",
      student: "Raihan Fikri",
      status: "open",
      priority: "medium",
      category: "IT Support",
      building: "Building A",
      room: "204",
      createdAt: "Feb 07, 2026",
      updatedAt: "09:36 AM",
      unread: 1,
    },
    {
      id: "TC-0007",
      title: "File Upload Error",
      description: "Submission fails with file size validation.",
      student: "Brooklyn Simmons",
      status: "pending",
      priority: "low",
      category: "Equipment",
      building: "Building C",
      room: "Cafeteria",
      createdAt: "Feb 06, 2026",
      updatedAt: "08:36 AM",
      unread: 1,
    },
    {
      id: "TC-0008",
      title: "Unexpected App Crash",
      description: "Mobile app crashes after login on Android.",
      student: "Guy Hawkins",
      status: "open",
      priority: "high",
      category: "IT Support",
      building: "Building B",
      room: "115",
      createdAt: "Feb 06, 2026",
      updatedAt: "08:10 AM",
      unread: 0,
    },
  ];

  let selectedId = tickets[0]?.id ?? "";

  function updateTicket(id: string, patch: Partial<Ticket>) {
    tickets = tickets.map((ticket) =>
      ticket.id === id ? { ...ticket, ...patch } : ticket,
    );
  }

  function handleStatusChange(id: string, e: Event) {
    const target = e.currentTarget as HTMLSelectElement | null;
    if (!target) return;
    updateTicket(id, { status: target.value as Status });
  }

  function handlePriorityChange(id: string, e: Event) {
    const target = e.currentTarget as HTMLSelectElement | null;
    if (!target) return;
    updateTicket(id, { priority: target.value as Priority });
  }

  $: filteredTickets = tickets.filter((ticket) => {
    const query = searchQuery.trim().toLowerCase();
    const matchesQuery =
      !query ||
      ticket.title.toLowerCase().includes(query) ||
      ticket.description.toLowerCase().includes(query) ||
      ticket.id.toLowerCase().includes(query) ||
      ticket.student.toLowerCase().includes(query);

    const matchesStatus =
      statusFilter === "all" || ticket.status === statusFilter;
    const matchesPriority =
      priorityFilter === "all" || ticket.priority === priorityFilter;
    const matchesCategory =
      categoryFilter === "all" || ticket.category === categoryFilter;
    const locationLabel = `${ticket.building} - ${ticket.room}`;
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

  $: selectedTicket =
    tickets.find((ticket) => ticket.id === selectedId) ?? null;
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
      <div class="flex items-center gap-2">
        <button class="btn btn-sm btn-outline gap-2">
          <Icon icon="mdi:refresh" width="18" height="18" />
          Refresh
        </button>
        <button class="btn btn-sm btn-primary gap-2">
          <Icon icon="mdi:export-variant" width="18" height="18" />
          Export
        </button>
      </div>
    </div>

    <section
      class="card bg-base-100 dark:bg-base-100 shadow-sm border border-base-content/5 rounded-lg"
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
            <option value="open">Open</option>
            <option value="pending">Pending</option>
            <option value="resolved">Resolved</option>
            <option value="closed">Closed</option>
          </select>
          <select class="select select-bordered" bind:value={priorityFilter}>
            <option value="all">All Priority</option>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
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
              <option value={category}>{category}</option>
            {/each}
          </select>
        </div>
      </div>
    </section>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 flex-1 min-h-0">
      <section
        class="card bg-base-100 dark:bg-base-100 shadow-sm border border-base-content/5 rounded-lg overflow-hidden"
      >
        <div class="card-body p-0 h-full">
          <div class="p-4 border-b border-base-content/5">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <h2 class="text-sm font-semibold">Total tickets</h2>
                <span class="badge badge-sm badge-ghost"
                  >{filteredTickets.length}</span
                >
              </div>
              <select class="select select-bordered select-sm">
                <option>Newest</option>
                <option>Oldest</option>
              </select>
            </div>
          </div>

          <div class="flex flex-col overflow-y-auto h-full">
            {#each filteredTickets as ticket}
              <button
                type="button"
                class="w-full text-left px-4 py-3 border-b border-base-content/5 hover:bg-base-200 transition-colors {ticket.id ===
                selectedId
                  ? 'bg-base-200'
                  : ''}"
                onclick={() => (selectedId = ticket.id)}
              >
                <div class="flex items-center justify-between mb-2">
                  <span class="text-xs font-semibold">{ticket.id}</span>
                  <span class="text-xs text-base-content/50"
                    >{ticket.updatedAt}</span
                  >
                </div>
                <div class="flex items-center justify-between gap-2">
                  <div>
                    <p class="text-sm font-medium">{ticket.student}</p>
                    <p class="text-xs text-base-content/60 line-clamp-1">
                      {ticket.title}
                    </p>
                  </div>
                  {#if ticket.unread > 0}
                    <span class="badge badge-error badge-sm"
                      >{ticket.unread}</span
                    >
                  {/if}
                </div>
              </button>
            {/each}
            {#if filteredTickets.length === 0}
              <div class="p-6 text-center text-sm text-base-content/60">
                No tickets found.
              </div>
            {/if}
          </div>
        </div>
      </section>

      <section
        class="card bg-base-100 dark:bg-base-100 shadow-sm border border-base-content/5 rounded-lg lg:col-span-2 overflow-hidden"
      >
        <div class="card-body p-4 h-full">
          {#if selectedTicket}
            <div class="flex flex-wrap items-center justify-between gap-3 mb-4">
              <div>
                <h2 class="text-lg font-semibold">{selectedTicket.title}</h2>
                <p class="text-xs text-base-content/60">
                  {selectedTicket.id} • {selectedTicket.student}
                </p>
              </div>
              <div class="flex items-center gap-2">
                <span
                  class="badge badge-sm {statusConfig[selectedTicket.status]
                    .color}"
                >
                  {statusConfig[selectedTicket.status].label}
                </span>
                <span
                  class="badge badge-sm {priorityConfig[selectedTicket.priority]
                    .color}"
                >
                  {priorityConfig[selectedTicket.priority].label}
                </span>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div class="space-y-2">
                <p class="text-xs text-base-content/60">Description</p>
                <p class="text-sm">{selectedTicket.description}</p>
              </div>
              <div class="space-y-3">
                <p class="text-xs text-base-content/60">Location</p>
                <div class="flex flex-wrap gap-2">
                  <span class="badge badge-outline badge-sm">
                    Building: {selectedTicket.building}
                  </span>
                  <span class="badge badge-outline badge-sm">
                    Room: {selectedTicket.room}
                  </span>
                </div>
                <p class="text-xs text-base-content/60">Category</p>
                <span class="badge badge-outline badge-sm">
                  {selectedTicket.category}
                </span>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-4">
              <div>
                <p class="text-xs text-base-content/60 mb-1">Status</p>
                <select
                  class="select select-bordered w-full"
                  value={selectedTicket.status}
                  onchange={(e) => handleStatusChange(selectedTicket.id, e)}
                >
                  <option value="open">Open</option>
                  <option value="pending">Pending</option>
                  <option value="resolved">Resolved</option>
                  <option value="closed">Closed</option>
                </select>
              </div>
              <div>
                <p class="text-xs text-base-content/60 mb-1">Priority</p>
                <select
                  class="select select-bordered w-full"
                  value={selectedTicket.priority}
                  onchange={(e) => handlePriorityChange(selectedTicket.id, e)}
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>
              <div>
                <p class="text-xs text-base-content/60 mb-1">Updated</p>
                <div class="input input-bordered w-full">
                  <span class="text-sm">{selectedTicket.updatedAt}</span>
                </div>
              </div>
            </div>

            <div class="flex flex-wrap items-center gap-2">
              <button class="btn btn-sm btn-primary gap-2">
                <Icon icon="mdi:check-circle-outline" width="18" height="18" />
                Save Changes
              </button>
              <button class="btn btn-sm btn-outline gap-2">
                <Icon icon="mdi:eye-outline" width="18" height="18" />
                View Ticket
              </button>
              <button class="btn btn-sm btn-ghost gap-2">
                <Icon icon="mdi:history" width="18" height="18" />
                View History
              </button>
            </div>
          {:else}
            <div
              class="flex flex-col items-center justify-center h-full text-base-content/60"
            >
              <Icon icon="mdi:ticket-outline" width="36" height="36" />
              <p class="mt-2">Select a ticket to view details.</p>
            </div>
          {/if}
        </div>
      </section>
    </div>
  </div>
</AdminLayout>

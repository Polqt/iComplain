<script lang="ts">
  import { page } from "$app/stores";
  import { goto } from "$app/navigation";
  import Icon from "@iconify/svelte";
  import StudentLayout from "../../../components/layout/StudentLayout.svelte";
  import {
    statusConfig,
    priorityConfig,
    getPriorityKey,
  } from "../../../utils/ticketConfig.ts";
  import type { Ticket } from "../../../types/tickets.ts";
  import TicketCreateModal from "../../../components/ui/tickets/TicketCreateModal.svelte";
  import TicketDeleteModal from "../../../components/ui/tickets/TicketDeleteModal.svelte";

  // Get ticket ID from URL
  $: ticketId = $page.params.id;

  let showEditModal = false;
  let showDeleteModal = false;
  let formData: Partial<Ticket> = {};

  // Mock data - replace with actual API call
  let mockTickets: Ticket[] = [
    {
      id: "TKT-001",
      title: "Broken AC Unit in Room 301",
      description:
        "Air conditioning not working properly, temperature control issues...",
      status: "pending",
      priority: { id: 1, name: "Low", level: 1, color_code: "#6b7280" },
      comments: 5,
      attachments: "3/3",
      student: {
        id: 1,
        email: "student@example.com",
        is_active: true, // TODO: replace with actual user data (avatar: "",)
        role: "student",
      },
      category: { id: 1, name: "General" },
      building: "Building A",
      room_name: "Room 301",
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      ticket_number: "TKT-001",
    },
    {
      id: "TKT-002",
      title: "Leaking Faucet in Restroom",
      description: "Water dripping continuously from the main sink...",
      status: "in_progress",
      priority: { id: 2, name: "Medium", level: 2, color_code: "#6b7280" },
      comments: 12,
      attachments: "2/3",
      student: {
        id: 2,
        email: "student@example.com",
        is_active: true, // TODO: replace with actual user data (avatar: "",)
        role: "student",
      },
      category: { id: 1, name: "General" },
      building: "Building B",
      room_name: "Restroom",
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      ticket_number: "TKT-002",
    },
    {
      id: "TKT-003",
      title: "Flickering Hallway Lights",
      description:
        "Lights in 3F hallway flickering intermittently during evening hours...",
      status: "in_progress",
      priority: { id: 3, name: "High", level: 3, color_code: "#6b7280" },
      comments: 8,
      attachments: "2/3",
      student: {
        id: 3,
        email: "student@example.com",
        is_active: true, // TODO: replace with actual user data (avatar: "",)
        role: "student",
      },
      category: { id: 1, name: "General" },
      building: "Building C",
      room_name: "Hallway",
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      ticket_number: "TKT-003",
    },
    {
      id: "TKT-004",
      title: "Broken Projector Screen",
      description:
        "Projection screen won't retract properly in lecture hall...",
      status: "in_progress",
      priority: { id: 1, name: "Low", level: 1, color_code: "#6b7280" },
      comments: 3,
      attachments: "2/3",
      student: {
        id: 4,
        email: "student@example.com",
        is_active: true, // TODO: replace with actual user data (avatar: "",)
        role: "student",
      },
      category: { id: 1, name: "General" },
      building: "Building D",
      room_name: "Lecture Hall",
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      ticket_number: "TKT-004",
    },
    {
      id: "TKT-005",
      title: "Door Lock Malfunction",
      description:
        "Main entrance lock mechanism was jammed and needed repair...",
      status: "resolved",
      priority: { id: 3, name: "High", level: 3, color_code: "#6b7280" },
      comments: 6,
      attachments: "1/3",
      student: {
        id: 5,
        email: "student@example.com",
        is_active: true, // TODO: replace with actual user data (avatar: "",)
        role: "student",
      },
      category: { id: 1, name: "General" },
      building: "Building E",
      room_name: "Entrance",
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      ticket_number: "TKT-005",
    },
    {
      id: "TKT-006",
      title: "Missing Whiteboard Markers",
      description: "Classroom 205 needed new dry-erase markers for teaching...",
      status: "pending",
      priority: { id: 1, name: "Low", level: 1, color_code: "#6b7280" },
      comments: 4,
      attachments: "0/3",
      student: {
        id: 6,
        email: "student@example.com",
        is_active: true, // TODO: replace with actual user data (avatar: "",)
        role: "student",
      },
      category: { id: 1, name: "General" },
      building: "Building F",
      room_name: "Classroom 205",
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      ticket_number: "TKT-006",
    },
  ];

  $: ticket = mockTickets.find((t) => t.id === ticketId);

  function goBack() {
    goto("/student/tickets");
  }

  function openEditModal() {
    if (ticket) {
      formData = { ...ticket };
      showEditModal = true;
    }
  }

  function closeEditModal() {
    showEditModal = false;
    formData = {};
  }

  function openDeleteModal() {
    showDeleteModal = true;
  }

  function closeDeleteModal() {
    showDeleteModal = false;
  }

  function confirmDelete() {
    if (!ticket) return;
    // TODO: call delete API when available
    mockTickets = mockTickets.filter((t) => t.id !== ticket.id);
    closeDeleteModal();
    goBack();
  }
</script>

<StudentLayout>
  {#if ticket}
    <div class="flex flex-col w-full min-h-[calc(100vh-8rem)]">
      <!-- Header -->
      <div class="flex items-center gap-2 sm:gap-4 mb-4 sm:mb-6 shrink-0">
        <button
          class="btn btn-ghost btn-sm btn-circle shrink-0"
          onclick={goBack}
        >
          <Icon icon="mdi:arrow-left" width="20" height="20" />
        </button>
        <h1 class="text-xl sm:text-2xl font-black text-base-content truncate">
          Ticket Details
        </h1>
      </div>

      <!-- Ticket Card -->
      <div
        class="card bg-base-100 shadow-lg w-full flex-1 flex flex-col min-h-0"
      >
        <div class="card-body flex-1 flex flex-col p-4 sm:p-6">
          <!-- Main content (scrolls if needed) -->
          <div class="flex-1 min-h-0">
            <!-- Title and Status -->
            <div
              class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3 mb-4"
            >
              <div class="min-w-0 flex-1">
                <h2
                  class="text-lg sm:text-2xl font-bold text-base-content mb-2 wrap-break-word"
                >
                  {ticket.title}
                </h2>
                <div class="flex flex-wrap items-center gap-2 sm:gap-3">
                  <div
                    class="badge badge-sm sm:badge-lg {statusConfig[
                      ticket.status
                    ].color}"
                  >
                    {statusConfig[ticket.status].label}
                  </div>
                  <div
                    class="badge badge-sm sm:badge-lg {priorityConfig[
                      getPriorityKey(ticket.priority)
                    ].color}"
                  >
                    {priorityConfig[getPriorityKey(ticket.priority)].label}
                  </div>
                </div>
              </div>
            </div>

            <div class="divider my-3 sm:my-4"></div>

            <div class="space-y-4">
              <div>
                <h3 class="text-sm font-semibold text-base-content/60 mb-2">
                  Description
                </h3>
                <p
                  class="text-sm sm:text-base text-base-content/80 wrap-break-word"
                >
                  {ticket.description}
                </p>
              </div>

              <div>
                <h3 class="text-sm font-semibold text-base-content/60 mb-2">
                  Location
                </h3>
                <p class="text-sm sm:text-base text-base-content/80">
                  {ticket.building} • {ticket.room_name}
                </p>
              </div>
            </div>
          </div>

          <!-- Bottom section: date, assignees, activity stats + actions (pinned to bottom) -->
          <div
            class="mt-auto pt-4 sm:pt-6 border-t border-base-content/10 shrink-0"
          >
            <!-- Activity Stats -->
            <div
              class="flex flex-wrap items-center gap-4 sm:gap-8 mb-4 sm:mb-6"
            >
              <div class="flex items-center gap-2">
                <Icon
                  icon="mdi:message-outline"
                  width="18"
                  height="18"
                  class="sm:w-5 sm:h-5 text-base-content/60 shrink-0"
                />
                <span class="text-sm sm:text-base"
                  >{ticket.comments} Comments</span
                >
              </div>
              <div class="flex items-center gap-2">
                <Icon
                  icon="mdi:paperclip"
                  width="18"
                  height="18"
                  class="sm:w-5 sm:h-5 text-base-content/60 shrink-0"
                />
                <span class="text-sm sm:text-base"
                  >{ticket.attachments} Attachments</span
                >
              </div>
            </div>

            <div
              class="flex flex-col sm:flex-row gap-2 sm:gap-3 sm:justify-end"
            >
              <button
                class="btn btn-ghost gap-2 w-full sm:w-auto"
                onclick={openEditModal}
              >
                <Icon icon="mdi:pencil-outline" width="18" height="18" />
                Edit
              </button>
              <button
                class="btn btn-error gap-2 w-full sm:w-auto"
                onclick={openDeleteModal}
              >
                <Icon icon="mdi:delete-outline" width="18" height="18" />
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  {:else}
    <div class="flex flex-col items-center justify-center min-h-[60vh]">
      <Icon
        icon="mdi:alert-circle-outline"
        width="64"
        height="64"
        class="text-error mb-4"
      />
      <h2 class="text-2xl font-bold mb-2">Ticket Not Found</h2>
      <p class="text-base-content/60 mb-6">
        The ticket you're looking for doesn't exist or has been removed.
      </p>
      <button class="btn btn-primary" onclick={goBack}>
        <Icon icon="mdi:arrow-left" width="18" height="18" />
        Back to Tickets
      </button>
    </div>
  {/if}

  <TicketCreateModal
    open={showEditModal && !!ticket}
    mode="edit"
    {formData}
    onclose={closeEditModal}
    onsubmit={(data) => {
      if (!ticketId || !data) return;
      mockTickets = mockTickets.map((t) =>
        t.id === ticketId ? ({ ...t, ...data } as Ticket) : t,
      );
      closeEditModal();
    }}
  />
  <TicketDeleteModal
    open={showDeleteModal}
    ticket={ticket ?? null}
    onclose={closeDeleteModal}
    onconfirm={confirmDelete}
  />
</StudentLayout>

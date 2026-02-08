<script lang="ts">
  import { page } from "$app/stores";
  import { goto } from "$app/navigation";
  import Icon from "@iconify/svelte";
  import StudentLayout from "../../../../components/layout/StudentLayout.svelte";
  import {
    type Ticket,
    statusConfig,
    priorityConfig,
    TicketCreateModal,
  } from "../../../../components/ui/tickets";

  // Get ticket ID from URL
  $: ticketId = $page.params.id;

  let showEditModal = false;
  let formData: Partial<Ticket> = {};

  // Mock data - replace with actual API call
  let mockTickets: Ticket[] = [
    {
      id: "TKT-001",
      title: "Broken AC Unit in Room 301",
      description:
        "Air conditioning not working properly, temperature control issues. The unit makes strange noises and doesn't cool the room effectively.",
      status: "not-started",
      priority: "low",
      assignees: ["JD", "AS"],
      date: "25 Mar 2023",
      comments: 5,
      links: 2,
      attachments: "3/3",
    },
    {
      id: "TKT-002",
      title: "Leaking Faucet in Restroom",
      description: "Water dripping continuously from the main sink. This is causing water wastage and potential damage to the floor.",
      status: "in-research",
      priority: "medium",
      assignees: ["MJ"],
      date: "28 Mar 2023",
      comments: 12,
      links: 1,
      attachments: "2/3",
    },
    {
      id: "TKT-003",
      title: "Flickering Hallway Lights",
      description:
        "Lights in 3F hallway flickering intermittently during evening hours. This creates safety concerns for students walking through the area.",
      status: "in-research",
      priority: "high",
      assignees: ["AS", "JD"],
      date: "30 Mar 2023",
      comments: 8,
      links: 1,
      attachments: "2/3",
    },
    {
      id: "TKT-005",
      title: "Door Lock Malfunction",
      description:
        "Main entrance lock mechanism was jammed and needed repair...",
      status: "complete",
      priority: "high",
      assignees: ["AS"],
      date: "07 Apr 2023",
      comments: 6,
      links: 0,
      attachments: "1/3",
      },
    {
      id: "TKT-006",
      title: "Missing Whiteboard Markers",
      description:
        "Classroom 205 needed new dry-erase markers for teaching...",
      status: "not-started",
      priority: "low",
      assignees: ["JD", "MJ"],
      date: "10 Apr 2023",
      comments: 4,
      links: 2,
      attachments: "0/3",
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
</script>

<StudentLayout>
  {#if ticket}
    <div class="flex flex-col w-full min-h-[calc(100vh-8rem)]">
      <!-- Header -->
      <div class="flex items-center gap-2 sm:gap-4 mb-4 sm:mb-6 shrink-0">
        <button class="btn btn-ghost btn-sm btn-circle shrink-0" onclick={goBack}>
          <Icon icon="mdi:arrow-left" width="20" height="20" />
        </button>
        <h1 class="text-xl sm:text-2xl font-black text-base-content truncate">Ticket Details</h1>
      </div>

      <!-- Ticket Card -->
      <div class="card bg-base-100 shadow-lg w-full flex-1 flex flex-col min-h-0">
        <div class="card-body flex-1 flex flex-col p-4 sm:p-6">
          <!-- Main content (scrolls if needed) -->
          <div class="flex-1 min-h-0">
            <!-- Title and Status -->
            <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3 mb-4">
              <div class="min-w-0 flex-1">
                <h2 class="text-lg sm:text-2xl font-bold text-base-content mb-2 break-words">
                  {ticket.title}
                </h2>
                <div class="flex flex-wrap items-center gap-2 sm:gap-3">
                  <div class="badge badge-sm sm:badge-lg {statusConfig[ticket.status].color}">
                    {statusConfig[ticket.status].label}
                  </div>
                  <div class="badge badge-sm sm:badge-lg {priorityConfig[ticket.priority].color}">
                    {priorityConfig[ticket.priority].label}
                  </div>
                </div>
              </div>
            </div>

            <div class="divider my-3 sm:my-4"></div>

            <!-- Description -->
            <div>
              <h3 class="text-sm font-semibold text-base-content/60 mb-2">
                Description
              </h3>
              <p class="text-sm sm:text-base text-base-content/80 break-words">{ticket.description}</p>
            </div>
          </div>

          <!-- Bottom section: date, assignees, activity stats + actions (pinned to bottom) -->
          <div class="mt-auto pt-4 sm:pt-6 border-t border-base-content/10 shrink-0">
            <!-- Date & Assignees -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6 mb-4 sm:mb-6">
              <div>
                <h3 class="text-sm font-semibold text-base-content/60 mb-2">
                  Date Created
                </h3>
                <div class="flex items-center gap-2">
                  <Icon icon="mdi:calendar-outline" width="18" height="18" class="shrink-0" />
                  <span class="text-sm sm:text-base">{ticket.date}</span>
                </div>
              </div>
              <div>
                <h3 class="text-sm font-semibold text-base-content/60 mb-2">
                  Assignees
                </h3>
                <div class="avatar-group -space-x-3 sm:-space-x-4">
                  {#each ticket.assignees as assignee}
                    <div class="avatar placeholder">
                      <div class="bg-primary text-primary-content w-8 h-8 sm:w-10 sm:h-10 rounded-full">
                        <span class="text-xs sm:text-sm">{assignee}</span>
                      </div>
                    </div>
                  {/each}
                </div>
              </div>
            </div>

            <!-- Activity Stats -->
            <div class="flex flex-wrap items-center gap-4 sm:gap-8 mb-4 sm:mb-6">
              <div class="flex items-center gap-2">
                <Icon icon="mdi:message-outline" width="18" height="18" class="sm:w-5 sm:h-5 text-base-content/60 shrink-0" />
                <span class="text-sm sm:text-base">{ticket.comments} Comments</span>
              </div>
              <div class="flex items-center gap-2">
                <Icon icon="mdi:link-variant" width="18" height="18" class="sm:w-5 sm:h-5 text-base-content/60 shrink-0" />
                <span class="text-sm sm:text-base">{ticket.links} Links</span>
              </div>
              <div class="flex items-center gap-2">
                <Icon icon="mdi:paperclip" width="18" height="18" class="sm:w-5 sm:h-5 text-base-content/60 shrink-0" />
                <span class="text-sm sm:text-base">{ticket.attachments} Attachments</span>
              </div>
            </div>

            <!-- Action Buttons (Edit first, then Delete) -->
            <div class="flex flex-col sm:flex-row gap-2 sm:gap-3 sm:justify-end">
              <button class="btn btn-ghost gap-2 w-full sm:w-auto" onclick={openEditModal}>
                <Icon icon="mdi:pencil-outline" width="18" height="18" />
                Edit
              </button>
              <button class="btn btn-error gap-2 w-full sm:w-auto">
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
      <Icon icon="mdi:alert-circle-outline" width="64" height="64" class="text-error mb-4" />
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
    formData={formData}
    onclose={closeEditModal}
    onsubmit={(data) => {
      if (!ticketId || !data) return;
      mockTickets = mockTickets.map((t) =>
        t.id === ticketId ? ({ ...t, ...data } as Ticket) : t
      );
      closeEditModal();
    }}
  />
</StudentLayout>

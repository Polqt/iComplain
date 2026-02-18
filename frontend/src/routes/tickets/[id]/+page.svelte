<script lang="ts">
  import { page } from "$app/stores";
  import { goto } from "$app/navigation";
  import Icon from "@iconify/svelte";
  import StudentLayout from "../../../components/layout/StudentLayout.svelte";
  import {
    statusConfig,
    priorityConfig,
    getPriorityKey,
    priorityAccent,
    priorityIcons,
    getStepState,
    pipelineSteps,
  } from "../../../utils/ticketConfig.ts";
  import TicketDeleteModal from "../../../components/ui/tickets/TicketDeleteModal.svelte";
  import { ticketsStore } from "../../../stores/tickets.store.ts";
  import { onMount } from "svelte";
  import { formatDate, formatDateTime } from "../../../utils/date.ts";
  import {
    getFileIcon,
    getFileName,
    isImage,
  } from "../../../utils/attachment.ts";
  import { authStore } from "../../../stores/auth.store.ts";
  import { deriveNameFromEmail } from "../../../utils/userConfig.ts";
  import AdminLayout from "../../../components/layout/AdminLayout.svelte";
  import AdminTicketControl from "../../../components/ui/tickets/AdminTicketControl.svelte";
  import TicketEdit from "../../../components/ui/tickets/TicketEdit.svelte";
  import CommentSection from "../../../components/ui/comments/CommentSection.svelte";

  $: idParam = $page.params.id;
  $: isNumericId = /^\d+$/.test(idParam ?? "");
  $: ({ tickets, isLoading, error } = $ticketsStore);
  $: ({ role, user } = $authStore);
  $: ticket = isNumericId
    ? (tickets.find((t) => t.id === Number(idParam)) ?? null)
    : (tickets.find((t) => t.ticket_number === idParam) ?? null);

  onMount(async () => {
    if (isNumericId) {
      const id = Number(idParam);
      const inStore = tickets.find((t) => t.id === id);
      if (!inStore) await ticketsStore.loadTicketById(id);
    } else {
      const inStore = tickets.find((t) => t.ticket_number === idParam);
      if (!inStore) await ticketsStore.loadTickets();
    }
  });

  let showEditModal = false;
  let showDeleteModal = false;

  async function handleDelete() {
    if (!ticket) return;
    const success = await ticketsStore.deleteTicket(ticket.id);
    if (success) goto("/tickets");
  }

  $: pKey = ticket ? getPriorityKey(ticket.priority) : "low";
  $: pAccent = priorityAccent[pKey] ?? "border-l-info";
  $: pIcon = priorityIcons[pKey] ?? "mdi:minus";
  $: timeline = ticket
    ? [
        {
          icon: "mdi:ticket-outline",
          color: "text-primary",
          bg: "bg-primary/10",
          label: "Ticket created",
          time: formatDateTime(ticket.created_at),
        },
        ...(ticket.status !== "pending"
          ? [
              {
                icon: "mdi:progress-clock",
                color: "text-info",
                bg: "bg-info/10",
                label: "Status changed to " + statusConfig[ticket.status].label,
                time: formatDateTime(ticket.updated_at),
              },
            ]
          : []),
      ]
    : [];

</script>

<svelte:component this={role === "admin" ? AdminLayout : StudentLayout}>
  {#if isLoading && !ticket}
  <div class="flex flex-col h-[calc(100vh-8rem)] gap-5">
      <div class="flex items-center gap-3 shrink-0">
        <div class="skeleton w-8 h-8 rounded-lg"></div>
        <div class="skeleton h-6 w-48 rounded-lg"></div>
      </div>
      <div class="grid grid-cols-[1fr_300px] gap-5 flex-1 min-h-0">
        <div class="skeleton rounded-2xl h-full"></div>
        <div class="skeleton rounded-2xl h-full"></div>
      </div>
    </div>
  {:else if !ticket}
    <div
      class="flex flex-col items-center justify-center h-[calc(100vh-8rem)] gap-4"
    >
      <div
        class="w-16 h-16 rounded-2xl bg-base-200 flex items-center justify-center"
      >
        <Icon
          icon="mdi:ticket-off-outline"
          width="32"
          height="32"
          class="text-base-content/25"
        />
      </div>
      <p class="font-semibold text-base-content/60">Ticket not found</p>
      <p class="text-xs text-base-content/40">
        It may have been deleted or the ID is wrong.
      </p>
      <button
        class="btn btn-primary btn-sm gap-2 mt-2"
        onclick={() => goto("/tickets")}
      >
        <Icon icon="mdi:arrow-left" width="15" height="15" />
        Back to tickets
      </button>
    </div>
  {:else}
    <div class="flex flex-col h-[calc(100vh-8rem)]">
      <div class="flex items-center justify-between mb-4 shrink-0">
        <div class="flex items-center gap-2">
          <button
            class="btn btn-ghost btn-sm btn-circle"
            onclick={() => goto("/tickets")}
            aria-label="Back"
          >
            <Icon icon="mdi:arrow-left" width="18" height="18" />
          </button>
          <div class="breadcrumbs text-xs text-base-content/40 p-0">
            <ul>
              <li><span>My Tickets</span></li>
              <li>
                <span class="font-mono text-base-content/60"
                  >{ticket.ticket_number}</span
                >
              </li>
            </ul>
          </div>
        </div>

        {#if ticket.status === "pending" && role === "student"}
          <div class="flex items-center gap-2">
            <button
              class="btn btn-ghost btn-sm gap-1.5 rounded-lg text-xs"
              onclick={() => (showEditModal = true)}
              disabled={isLoading}
            >
              <Icon icon="mdi:pencil-outline" width="14" height="14" />
              Edit
            </button>
            <button
              class="btn btn-error btn-outline btn-sm gap-1.5 rounded-lg text-xs"
              onclick={() => (showDeleteModal = true)}
              disabled={isLoading}
            >
              <Icon icon="mdi:delete-outline" width="14" height="14" />
              Delete
            </button>
          </div>
        {:else if role === "admin"}
          <AdminTicketControl {ticket} />
        {:else if ticket.status === "pending" && role === "student"}
          <div class="flex items-center gap-2">
            <button
              class="btn btn-ghost btn-sm gap-1.5 rounded-lg text-xs"
              onclick={() => (showEditModal = true)}
              disabled={isLoading}
            >
              <Icon icon="mdi:pencil-outline" width="14" height="14" /> Edit
            </button>
            <button
              class="btn btn-error btn-outline btn-sm gap-1.5 rounded-lg text-xs"
              onclick={() => (showDeleteModal = true)}
              disabled={isLoading}
            >
              <Icon icon="mdi:delete-outline" width="14" height="14" /> Delete
            </button>
          </div>
        {/if}
      </div>
      <div
        class="grid grid-cols-[1fr_272px] gap-4 flex-1 min-h-0 overflow-hidden"
      >
        <div class="flex flex-col gap-4 overflow-y-auto min-h-0 pr-0.5">
          <div
            class="bg-base-100 rounded-2xl border border-base-content/8 border-l-[3px] {pAccent} p-6"
          >
            <div class="flex gap-2 mb-2">
              <div
                class="text-2xl font-bold text-base-content leading-snug mb-3"
              >
                {ticket.title}
              </div>
              <span
                class="ml-auto text-[10px] font-mono text-base-content/25 tracking-widest"
              >
                {ticket.ticket_number}
              </span>
            </div>

            <p class="text-sm text-base-content/60 leading-relaxed">
              {ticket.description}
            </p>
          </div>

          {#if ticket.attachment}
            <div
              class="bg-base-100 rounded-2xl border border-base-content/8 p-5"
            >
              <h3
                class="text-[10px] font-bold uppercase tracking-widest text-base-content/35 mb-3"
              >
                Attachment
              </h3>

              {#if isImage(ticket.attachment)}
                <div
                  class="rounded-xl overflow-hidden border border-base-content/8 mb-2"
                >
                  <img
                    src={ticket.attachment}
                    alt="Ticket attachment"
                    class="w-full max-h-64 object-cover"
                  />
                </div>
                <a
                  href={ticket.attachment}
                  target="_blank"
                  rel="noopener noreferrer"
                  class="inline-flex items-center gap-1.5 text-xs text-primary hover:underline"
                >
                  <Icon icon="mdi:open-in-new" width="12" height="12" />
                  Open full image
                </a>
              {:else}
                <a
                  href={ticket.attachment}
                  target="_blank"
                  rel="noopener noreferrer"
                  class="flex items-center gap-3 p-3 rounded-xl border border-base-content/8
                         hover:border-primary/30 hover:bg-primary/5 transition-colors group"
                >
                  <div
                    class="w-9 h-9 rounded-lg bg-base-200 flex items-center justify-center shrink-0
                              group-hover:bg-primary/10 transition-colors"
                  >
                    <Icon
                      icon={getFileIcon(ticket.attachment)}
                      width="18"
                      height="18"
                      class="text-base-content/50 group-hover:text-primary transition-colors"
                    />
                  </div>
                  <div class="min-w-0 flex-1">
                    <p class="text-xs font-medium text-base-content truncate">
                      {getFileName(ticket.attachment)}
                    </p>
                    <p class="text-[10px] text-base-content/40 mt-0.5">
                      Click to download
                    </p>
                  </div>
                  <Icon
                    icon="mdi:download-outline"
                    width="15"
                    height="15"
                    class="text-base-content/30 group-hover:text-primary shrink-0 transition-colors"
                  />
                </a>
              {/if}
            </div>
          {/if}

          <!-- Activity timeline -->
          <div
            class="bg-base-100 rounded-2xl border border-base-content/8 p-5 flex-1"
          >
            <h3
              class="text-[10px] font-bold uppercase tracking-widest text-base-content/35 mb-4"
            >
              Activity
            </h3>

            <div class="relative">
              <div
                class="absolute left-3.75 top-2 bottom-2 w-px bg-base-content/8"
              ></div>
              <div class="flex flex-col gap-5">
                {#each timeline as event}
                  <div class="flex items-start gap-3">
                    <div
                      class="w-7.5 h-7.5 rounded-full {event.bg} shrink-0
                                flex items-center justify-center relative z-10"
                    >
                      <Icon
                        icon={event.icon}
                        width="14"
                        height="14"
                        class={event.color}
                      />
                    </div>
                    <div class="pt-0.5 min-w-0">
                      <p class="text-sm text-base-content/75 font-medium">
                        {event.label}
                      </p>
                      <p class="text-[11px] text-base-content/35 mt-0.5">
                        {event.time}
                      </p>
                    </div>
                  </div>
                {/each}
              </div>
            </div>
          </div>
          {#if ticket.id}
            <CommentSection ticketId={ticket.id} ticketStatus={ticket.status} />
          {/if}
        </div>

        <div class="flex flex-col gap-3 overflow-y-auto min-h-0">
          <div class="bg-base-100 rounded-2xl border border-base-content/8 p-4">
            <h3
              class="text-[10px] font-bold uppercase tracking-widest text-base-content/35 mb-3"
            >
              Details
            </h3>

            <div class="flex flex-col gap-2.5">
              <div class="flex items-center justify-between gap-3">
                <span class="text-xs text-base-content/45">Status</span>
                <div
                  class="badge badge-xs {statusConfig[ticket.status]
                    .color} font-semibold"
                >
                  {statusConfig[ticket.status].label}
                </div>
              </div>

              <div class="flex items-center justify-between gap-3">
                <span class="text-xs text-base-content/45">Priority</span>
                <div
                  class="badge badge-xs {priorityConfig[pKey]
                    .color} font-semibold gap-1"
                >
                  <Icon icon={pIcon} width="10" height="10" />
                  {priorityConfig[pKey].label}
                </div>
              </div>

              <div class="flex items-center justify-between gap-3">
                <span class="text-xs text-base-content/45 shrink-0"
                  >Category</span
                >
                <div
                  class="tooltip tooltip-left"
                  data-tip={ticket.category.name}
                >
                  <div
                    class="badge badge-ghost badge-xs font-medium max-w-30 truncate"
                  >
                    {ticket.category.name}
                  </div>
                </div>
              </div>

              <div class="divider my-0.5"></div>

              <div class="flex items-start gap-2">
                <Icon
                  icon="mdi:map-marker-outline"
                  width="13"
                  height="13"
                  class="text-base-content/35 shrink-0 mt-0.5"
                />
                <div class="min-w-0">
                  <p class="text-xs font-medium text-base-content/70 truncate">
                    {ticket.building}
                  </p>
                  <p class="text-[11px] text-base-content/40 truncate mt-0.5">
                    {ticket.room_name}
                  </p>
                </div>
              </div>

              <div class="divider my-0.5"></div>

              <div class="flex flex-col gap-2">
                <div class="flex flex-col gap-0.5">
                  <span
                    class="text-[10px] font-semibold uppercase tracking-wider text-base-content/30"
                  >
                    Created
                  </span>
                  <span class="text-xs text-base-content/55"
                    >{formatDate(ticket.created_at)}</span
                  >
                </div>
              </div>
            </div>
          </div>

          <div class="bg-base-100 rounded-2xl border border-base-content/8 p-4">
            <h3
              class="text-[10px] font-bold uppercase tracking-widest text-base-content/35 mb-3"
            >
              Reporter
            </h3>
            <div class="flex items-center gap-2.5">
              {#if user}
                {@const displayName =
                  user.name || deriveNameFromEmail(user.email) || "Student"}
                <div class="avatar placeholder shrink-0">
                  <div
                    class="w-8 h-8 rounded-full bg-primary/15 ring-1 ring-primary/20
                            flex items-center justify-center"
                  >
                    <img src={user.avatar} alt={displayName} />
                  </div>
                </div>
              {/if}
              <div class="min-w-0">
                <p class="text-xs font-semibold text-base-content truncate">
                  {ticket.student.email}
                </p>
                <p class="text-[10px] text-base-content/40 mt-0.5">Student</p>
              </div>
            </div>
          </div>

          <div class="bg-base-100 rounded-2xl border border-base-content/8 p-4">
            <h3
              class="text-[10px] font-bold uppercase tracking-widest text-base-content/35 mb-3"
            >
              Progress
            </h3>
            <ul class="steps steps-vertical w-full">
              {#each pipelineSteps as step}
                {@const state = getStepState(ticket.status, step.id)}
                <li
                  class="step text-left
                         {state === 'active' || state === 'past'
                    ? 'step-primary'
                    : ''}"
                  data-content={state === "past"
                    ? "✓"
                    : state === "active"
                      ? "●"
                      : "○"}
                >
                  <div class="flex items-center gap-1.5 ml-1">
                    <Icon
                      icon={step.icon}
                      width="12"
                      height="12"
                      class={state === "active"
                        ? "text-primary"
                        : state === "past"
                          ? "text-base-content/50"
                          : "text-base-content/20"}
                    />
                    <span
                      class="text-xs
                                 {state === 'active'
                        ? 'text-primary font-semibold'
                        : state === 'past'
                          ? 'text-base-content/50'
                          : 'text-base-content/25'}"
                    >
                      {step.label}
                    </span>
                    {#if state === "active"}
                      <span
                        class="w-1.5 h-1.5 rounded-full bg-primary animate-pulse ml-1"
                      ></span>
                    {/if}
                  </div>
                </li>
              {/each}
            </ul>
          </div>
        </div>
      </div>
    </div>
    {#if error}
      <div class="toast toast-top toast-end z-9999">
        <div class="alert alert-error shadow-lg rounded-xl gap-2 text-sm">
          <Icon icon="mdi:alert-circle-outline" width="18" height="18" />
          <span>{error}</span>
          <button
            class="btn btn-ghost btn-xs rounded-lg ml-1"
            onclick={() => ticketsStore.setError(null)}>✕</button
          >
        </div>
      </div>
    {/if}
  {/if}

  <TicketEdit
    {ticket}
    open={showEditModal}
    {isLoading}
    onclose={() => (showEditModal = false)}
  />
  <TicketDeleteModal
    open={showDeleteModal}
    {ticket}
    {isLoading}
    onclose={() => (showDeleteModal = false)}
    onconfirm={handleDelete}
  />
</svelte:component>

<script lang="ts">
  import { ticketsStore } from "../../../stores/tickets.store.ts";
  import type { AdminTicketEdit } from "../../../types/tickets.ts";
  import type { Ticket } from "../../../types/tickets.ts";
  import {
    getPriorityKey,
    priorities,
    priorityConfig,
    priorityIcons,
    priorityIdMap,
    statusConfig,
    statuses,
  } from "../../../utils/ticketConfig.ts";
  import Icon from "@iconify/svelte";

  export let ticket: Ticket;

  let editing: AdminTicketEdit = null;
  let saving: AdminTicketEdit = null;
  let saved: AdminTicketEdit = null;

  async function applyStatus(newStatus: string) {
    if (newStatus === ticket.status) {
      editing = null;
      return;
    }
    saving = "status";
    editing = null;

    const updated = await ticketsStore.adminPatchTicket(ticket.id, {
      status: newStatus,
    });

    if (updated) {
      await ticketsStore.loadTicketById(ticket.id);
      saved = "status";
      setTimeout(() => {
        saved = null;
      }, 2000);
      saving = null;
    }
  }

  async function applyPriority(newKey: string) {
    if (newKey === getPriorityKey(ticket.priority)) {
      editing = null;
      return;
    }
    saving = "priority";
    editing = null;

    const updated = await ticketsStore.adminPatchTicket(ticket.id, {
      priority: priorityIdMap[newKey],
    });

    if (updated) {
      await ticketsStore.loadTicketById(ticket.id);
      saved = "priority";
      setTimeout(() => {
        saved = null;
      }, 2000);
      saving = null;
    }
  }

  function clickOutside(node: HTMLElement, cb: () => void) {
    const handler = (e: MouseEvent) => {
      if (!node.contains(e.target as Node)) {
        cb();
      }
    };
    document.addEventListener("mousedown", handler);
    return {
      destroy: () => {
        document.removeEventListener("mousedown", handler);
      },
    };
  }

  $: pKey = getPriorityKey(ticket.priority);
</script>

<div class="flex items-center gap-2">
  <div
    class="relative group/status"
    use:clickOutside={() => {
      if (editing === "status") editing = null;
    }}
  >
    {#if editing === "status"}
      <div
        class="absolute right-0 top-full mt-1.5 z-50 bg-base-100 border border-base-content/10 rounded-xl shadow-2xl p-1 min-w-40 pop"
      >
        {#each statuses as s}
          <button
            class="w-full flex items-center gap-2.5 px-3 py-1.5 rounded-lg text-xs
                   hover:bg-base-200 transition-colors text-left
                   {s === ticket.status
              ? 'font-semibold text-primary bg-primary/5'
              : 'text-base-content/70'}"
            onclick={() => applyStatus(s)}
          >
            <span
              class="w-1.5 h-1.5 rounded-full shrink-0 {s === 'pending'
                ? 'bg-warning'
                : s === 'in_progress'
                  ? 'bg-info'
                  : s === 'resolved'
                    ? 'bg-success'
                    : 'bg-base-content/25'}"
            ></span>
            {statusConfig[s].label}
            {#if s === ticket.status}
              <Icon
                icon="mdi:check"
                width="10"
                height="10"
                class="ml-auto text-primary"
              />
            {/if}
          </button>
        {/each}
      </div>
    {/if}
    <button
      class="btn btn-ghost btn-sm gap-1.5 rounded-lg text-xs
             {saving === 'status' ? 'opacity-60 pointer-events-none' : ''}
             {saved === 'status' ? 'text-success' : ''}"
      onclick={() => (editing = editing === "status" ? null : "status")}
      disabled={!!saving}
      title="Change status"
    >
      {#if saving === "status"}
        <span class="loading loading-spinner loading-xs"></span>
      {:else if saved === "status"}
        <Icon icon="mdi:check-circle" width="14" height="14" />
      {:else}
        <Icon icon="mdi:flag-outline" width="14" height="14" />
      {/if}
      Status
      <Icon icon="mdi:chevron-down" width="12" height="12" class="opacity-50" />
    </button>
  </div>

  <div
    class="relative group/priority"
    use:clickOutside={() => {
      if (editing === "priority") editing = null;
    }}
  >
    {#if editing === "priority"}
      <div
        class="absolute right-0 top-full mt-1.5 z-50 bg-base-100 border border-base-content/10 rounded-xl shadow-2xl p-1 min-w-32"
      >
        {#each priorities as p}
          <button
            class="w-full flex items-center gap-2.5 px-3 py-1.5 rounded-lg text-xs
                   hover:bg-base-200 transition-colors text-left
                   {p === pKey
              ? 'font-semibold text-primary bg-primary/5'
              : 'text-base-content/70'}"
            onclick={() => applyPriority(p)}
          >
            <Icon
              icon={priorityIcons[p]}
              width="12"
              height="12"
              class={p === "high"
                ? "text-error"
                : p === "medium"
                  ? "text-warning"
                  : "text-info"}
            />
            {priorityConfig[p].label}
            {#if p === pKey}
              <Icon
                icon="mdi:check"
                width="10"
                height="10"
                class="ml-auto text-primary"
              />
            {/if}
          </button>
        {/each}
      </div>
    {/if}
    <button
      class="btn btn-ghost btn-sm gap-1.5 rounded-lg text-xs {saving ===
      'priority'
        ? 'opacity-60 pointer-events-none'
        : ''} {saved === 'priority' ? 'text-success' : ''}"
      onclick={() => (editing = editing === "priority" ? null : "priority")}
      disabled={!!saving}
      title="Change priority"
    >
      {#if saving === "priority"}
        <span class="loading loading-spinner loading-xs"></span>
      {:else if saved === "priority"}
        <Icon icon="mdi:check-circle" width="14" height="14" />
      {:else}
        <Icon icon="mdi:arrow-up-down" width="14" height="14" />
      {/if}
      Priority
      <Icon icon="mdi:chevron-down" width="12" height="12" class="opacity-50" />
    </button>
  </div>
</div>

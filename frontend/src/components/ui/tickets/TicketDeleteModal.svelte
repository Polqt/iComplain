<script lang="ts">
  import Icon from "@iconify/svelte";
  import type { Ticket } from "../../../types/tickets.ts";

  export let open = false;
  export let ticket: Ticket | null = null;
  export let isLoading = false;
  export let onclose: () => void = () => {};
  export let onconfirm: () => void = () => {};
</script>

{#if open && ticket}
  <dialog class="modal modal-open">
    <div class="modal-box">
      <div class="flex items-center gap-3 mb-4">
        <div class="p-2 bg-error/10 rounded-lg">
          <Icon
            icon="mdi:delete-alert-outline"
            width="22"
            height="22"
            class="text-error"
          />
        </div>
        <h3 class="font-bold text-lg">Delete Ticket</h3>
      </div>

      <div class="alert alert-warning mb-4">
        <Icon icon="mdi:alert-outline" width="20" height="20" />
        <span class="text-sm">
          This action cannot be undone. The ticket will be permanently removed.
        </span>
      </div>

      <div class="bg-base-200 p-4 rounded-lg mb-4">
        <div class="flex items-start gap-3">
          <div>
            <p class="text-xs text-base-content/50 font-mono mb-1">
              {ticket.ticket_number}
            </p>
            <h4 class="font-semibold text-sm mb-1">{ticket.title}</h4>
            <p class="text-xs text-base-content/60 line-clamp-2">
              {ticket.description}
            </p>
            <p class="text-xs text-base-content/50 mt-1">
              {ticket.building} · {ticket.room_name}
            </p>
          </div>
        </div>
      </div>

      <div class="modal-action">
        <button class="btn btn-ghost" onclick={onclose} disabled={isLoading}>
          Cancel
        </button>
        <button class="btn btn-error" onclick={onconfirm} disabled={isLoading}>
          {#if isLoading}
            <span class="loading loading-spinner loading-sm"></span>
            Deleting...
          {:else}
            <Icon icon="mdi:delete-outline" width="18" height="18" />
            Delete Ticket
          {/if}
        </button>
      </div>
    </div>

    <button
      type="button"
      class="modal-backdrop"
      onclick={onclose}
      aria-label="Close modal"
    ></button>
  </dialog>
{/if}

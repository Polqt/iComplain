<script lang="ts">
  import Icon from "@iconify/svelte";
  import type { Ticket } from "../../../types/tickets.js";

  export let open = false;
  export let ticket: Ticket | null = null;
  export let isLoading = false;
  export let onclose: () => void = () => {};
  export let onconfirm: () => void = () => {};
</script>

{#if open && ticket}
  <dialog class="modal modal-open">
    <div class="modal-box">
      <h3 class="font-bold text-lg mb-4">Delete Ticket</h3>

      <div class="alert alert-warning mb-4">
        <Icon icon="mdi:alert-outline" width="24" height="24" />
        <span
          >Are you sure you want to delete this ticket? This action cannot be
          undone.</span
        >
      </div>

      <div class="bg-base-200 p-4 rounded-lg mb-4">
        <h4 class="font-semibold text-sm mb-2">{ticket.title}</h4>
        <p class="text-xs text-base-content/60">{ticket.description}</p>
      </div>

      <div class="modal-action">
        <button class="btn btn-ghost" onclick={onclose}>Cancel</button>
        <button class="btn btn-error" onclick={onconfirm}>
          <Icon icon="mdi:delete-outline" width="18" height="18" />
          Delete Ticket
        </button>
      </div>
    </div>
    <form method="dialog" class="modal-backdrop" onclick={onclose}>
      <button>close</button>
    </form>
  </dialog>
{/if}

<script lang="ts">
  import Icon from "@iconify/svelte";
  import type { Ticket } from "../../../types/tickets.js";

  export let open = false;
  export let mode: "create" | "edit" = "create";
  export let formData: Partial<Ticket> = {};
  export let onclose: () => void = () => {};
  export let onsubmit: (data: Partial<Ticket>) => void = () => {};

  function handleSubmit(event: Event) {
    event.preventDefault();
    onsubmit(formData);
  }
</script>

{#if open}
  <dialog class="modal modal-open">
    <div class="modal-box max-w-2xl">
      <h3 class="font-bold text-lg mb-4">
        {mode === "create" ? "Create New Ticket" : "Edit Ticket"}
      </h3>

      <form onsubmit={handleSubmit} class="space-y-4">
        <!-- Title -->
        <div class="form-control">
          <label class="label">
            <span class="label-text font-semibold">Title</span>
          </label>
          <input
            type="text"
            bind:value={formData.title}
            placeholder="Enter ticket title"
            class="input input-bordered w-full"
            required
          />
        </div>

        <!-- Description -->
        <div class="form-control">
          <label class="label">
            <span class="label-text font-semibold">Description</span>
          </label>
          <textarea
            bind:value={formData.description}
            placeholder="Describe the issue in detail..."
            class="textarea textarea-bordered h-32"
            required
          ></textarea>
        </div>

        <!-- Priority and Status Row -->
        <div class="grid grid-cols-2 gap-4">
          <div class="form-control">
            <label class="label">
              <span class="label-text font-semibold">Priority</span>
            </label>
            <select bind:value={formData.priority} class="select select-bordered w-full">
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>
          <div class="form-control">
            <label class="label">
              <span class="label-text font-semibold">Status</span>
            </label>
            <select bind:value={formData.status} class="select select-bordered w-full">
              <option value="not-started">Not Started</option>
              <option value="in-research">In Research</option>
              <option value="on-track">On Track</option>
              <option value="complete">Complete</option>
            </select>
          </div>
        </div>

        <div class="modal-action">
          <button type="button" class="btn btn-ghost" onclick={onclose}>
            Cancel
          </button>
          <button type="submit" class="btn btn-primary">
            <Icon icon="mdi:check" width="18" height="18" />
            {mode === "create" ? "Create Ticket" : "Save Changes"}
          </button>
        </div>
      </form>
    </div>
    <form method="dialog" class="modal-backdrop" onclick={onclose}>
      <button>close</button>
    </form>
  </dialog>
{/if}

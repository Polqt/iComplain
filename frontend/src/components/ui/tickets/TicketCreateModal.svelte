<script lang="ts">
  import Icon from "@iconify/svelte";
  import type { Ticket } from "../../../types/tickets.js";
  import {
    statusConfig,
    priorityConfig,
    getPriorityKey,
  } from "../../../utils/ticketConfig.js";

  export let open = false;
  export let mode: "create" | "edit" = "create";
  /** When false (e.g. student), priority/status are hidden on create and read-only on edit. */
  export let canEditPriorityStatus = false;
  export let formData: Partial<Ticket> = {};
  export let onclose: () => void = () => {};
  export let onsubmit: (data: Partial<Ticket>) => void = () => {};

  function handleSubmit(event: Event) {
    event.preventDefault();
    // Students must not send priority/status; only admins can change them
    const data = canEditPriorityStatus
      ? formData
      : (({ priority, status, ...rest }) => rest)(formData);
    onsubmit(data);
  }
</script>

{#if open}
  <dialog class="modal modal-open">
    <div class="modal-box max-w-2xl">
      <h3 class="font-bold text-lg mb-4">
        {mode === "create" ? "Create New Ticket" : "Edit Ticket"}
      </h3>

      <form onsubmit={handleSubmit} class="space-y-4">
        <div class="form-control">
          <label for="title" class="label">
            <span class="label-text font-semibold">Title</span>
          </label>
          <input
            id="title"
            type="text"
            bind:value={formData.title}
            placeholder="Enter ticket title"
            class="input input-bordered w-full"
            required
          />
        </div>

        <div class="form-control">
          <label for="description" class="label">
            <span class="label-text font-semibold">Description</span>
          </label>
          <textarea
            bind:value={formData.description}
            placeholder="Describe the issue in detail..."
            class="textarea textarea-bordered w-full h-32"
            required
          ></textarea>
        </div>

        <div class="form-control">
          <label for="building" class="label">
            <span class="label-text font-semibold">Building</span>
          </label>
          <input
            id="building"
            type="text"
            bind:value={formData.building}
            placeholder="Enter building name"
            class="input input-bordered w-full"
            required
          />
        </div>
        <div class="form-control">
          <label for="room_name" class="label">
            <span class="label-text font-semibold">Room Name</span>
          </label>
          <input
            id="room_name"
            type="text"
            bind:value={formData.room_name}
            placeholder="Enter room name"
            class="input input-bordered w-full"
            required
          />
        </div>


        <!-- Priority and Status: editable only for admin (canEditPriorityStatus), else view-only in edit or hidden in create -->
        {#if canEditPriorityStatus}
          <div class="grid grid-cols-2 gap-4">
            <div class="form-control">
              <label for="priority" class="label">
                <span class="label-text font-semibold">Priority</span>
              </label>
              <select
                id="priority"
                bind:value={formData.priority}
                class="select select-bordered w-full"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
            <div class="form-control">
              <label for="status" class="label">
                <span class="label-text font-semibold">Status</span>
              </label>
              <select
                id="status"
                bind:value={formData.status}
                class="select select-bordered w-full"
              >
                <option value="pending">Pending</option>
                <option value="in_progress">In Progress</option>
                <option value="resolved">Resolved</option>
                <option value="closed">Closed</option>
              </select>
            </div>
          </div>
        {:else if mode === "edit" && formData.status && formData.priority}
          <div class="grid grid-cols-2 gap-4">
            <div class="form-control">
              <label for="status" class="label">
                <span class="label-text font-semibold">Status</span>
              </label>
              <div class="flex items-center gap-2 pt-2">
                <span class="badge {statusConfig[formData.status].color}">
                  {statusConfig[formData.status].label}
                </span>
              </div>
            </div>
            <div class="form-control">
              <label for="priority" class="label">
                <span class="label-text font-semibold">Priority</span>
              </label>
              <div class="flex items-center gap-2 pt-2">
                <span
                  class="badge {priorityConfig[
                    getPriorityKey(formData.priority)
                  ].color}"
                >
                  {priorityConfig[getPriorityKey(formData.priority)].label}
                </span>
              </div>
            </div>
          </div>
        {/if}

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
    <form method="dialog" class="modal-backdrop">
      <button
        type="submit"
        aria-label="Close dialog"
        class="w-full h-full absolute inset-0 cursor-pointer bg-transparent border-none p-0 m-0"
      ></button>
    </form>
  </dialog>
{/if}

<script lang="ts">
  import { writable } from "svelte/store";
  import type {
    Ticket,
    Category,
    TicketPriority,
  } from "../../../types/tickets.ts";
  import {
    statusConfig,
    priorityConfig,
    getPriorityKey,
  } from "../../../utils/ticketConfig.js";
  import Icon from "@iconify/svelte";
  import { onMount } from "svelte";
  import { fetchCategories, fetchPriorities } from "../../../lib/api/ticket.ts";

  export let open = false;
  export let mode: "create" | "edit" = "create";
  export let canEditPriorityStatus = false;
  export let formData: Partial<Ticket> = {};
  export let isLoading = false;
  export let onclose: () => void = () => {};
  export let onsubmit: (
    data: Partial<Ticket>,
    file?: File | null,
  ) => void = () => {};

  let selectedFile: File | null = null;

  export const categoriesStore = writable<Category[]>([]);
  export const prioritiesStore = writable<TicketPriority[]>([]);

  export async function loadCategories() {
    try {
      const cats = await fetchCategories();
      categoriesStore.set(cats);
    } catch (err) {
      console.error(err);
    }
  }

  export async function loadPriorities() {
    try {
      const prios = await fetchPriorities();
      prioritiesStore.set(prios);
    } catch (err) {
      console.error(err);
    }
  }

  onMount(() => {
    loadCategories();
    loadPriorities();
  });

  function handleSubmit(event: Event) {
    event.preventDefault();
    const data = canEditPriorityStatus
      ? formData
      : (({ priority, status, ...rest }) => rest)(formData);
    onsubmit(data, selectedFile);
    onclose();
  }

  function handleFileChange(event: Event) {
    const input = event.target as HTMLInputElement;
    selectedFile = input.files?.[0] ?? null;
  }
</script>

{#if open}
  <dialog class="modal modal-open">
    <div
      class="modal-box max-w-xl rounded-2xl p-0 overflow-hidden shadow-2xl border border-base-content/8"
    >
      <div
        class="flex items-center justify-between px-6 py-5 border-b border-base-content/6"
      >
        <div class="flex items-center gap-3">
          <div>
            <h3 class="font-bold text-sm text-base-content">
              {mode === "create" ? "New Ticket" : "Edit Ticket"}
            </h3>
            <p class="text-[11px] text-base-content/40 mt-0.5">
              {mode === "create"
                ? "Report a facility issue"
                : "Update ticket details"}
            </p>
          </div>
        </div>
        <button
          type="button"
          class="btn btn-ghost btn-sm btn-circle text-base-content/40 hover:text-base-content"
          onclick={onclose}
          disabled={isLoading}
          aria-label="Close"
        >
          <Icon icon="mdi:close" class="w-4 h-4" />
        </button>
      </div>

      <form onsubmit={handleSubmit} class="overflow-y-auto max-h-[70vh]">
        <div class="px-6 py-5 space-y-5">
          <div class="form-control gap-1.5">
            <label
              for="title"
              class="text-xs font-semibold text-base-content/70 uppercase tracking-wide"
            >
              Title <span class="text-error">*</span>
            </label>
            <input
              id="title"
              type="text"
              bind:value={formData.title}
              placeholder="Briefly describe the problem"
              class="input input-bordered w-full rounded-xl text-sm focus:border-primary focus:outline-none"
              required
              disabled={isLoading}
            />
          </div>

          <div class="form-control gap-1.5">
            <label
              for="description"
              class="text-xs font-semibold text-base-content/70 uppercase tracking-wide"
            >
              Description <span class="text-error">*</span>
            </label>
            <textarea
              id="description"
              bind:value={formData.description}
              placeholder="Describe the issue in detail..."
              class="textarea textarea-bordered w-full h-28 rounded-xl text-sm resize-none focus:border-primary focus:outline-none"
              required
              disabled={isLoading}
            ></textarea>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="form-control gap-1.5">
              <label
                for="category"
                class="text-xs font-semibold text-base-content/70 uppercase tracking-wide"
              >
                Category <span class="text-error">*</span>
              </label>
              <select
                id="category"
                bind:value={formData.category}
                class="select select-bordered w-full rounded-xl text-sm focus:border-primary focus:outline-none"
                disabled={isLoading}
              >
                {#each $categoriesStore as c}
                  <option value={c.id}>{c.name}</option>
                {/each}
              </select>
            </div>

            <div class="form-control gap-1.5">
              <label
                for="priority"
                class="text-xs font-semibold text-base-content/70 uppercase tracking-wide"
              >
                Priority
              </label>
              {#if mode === "create"}
                <select
                  id="priority"
                  bind:value={formData.priority}
                  class="select select-bordered w-full rounded-xl text-sm focus:border-primary focus:outline-none"
                  disabled={true}
                >
                  {#each $prioritiesStore as p}
                    <option value={p.id}>{p.name}</option>
                  {/each}
                </select>
              {:else if formData.priority}
                <div
                  class="flex items-center h-12 px-3 rounded-xl border border-base-content/15 bg-base-200/50"
                >
                  <span
                    class="badge badge-sm {priorityConfig[
                      getPriorityKey(formData.priority)
                    ].color}"
                  >
                    {priorityConfig[getPriorityKey(formData.priority)].label}
                  </span>
                  <span class="text-xs text-base-content/40 ml-2"
                    >set by admin</span
                  >
                </div>
              {/if}
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="form-control gap-1.5">
              <label
                for="building"
                class="text-xs font-semibold text-base-content/70 uppercase tracking-wide"
              >
                Building <span class="text-error">*</span>
              </label>
              <input
                id="building"
                type="text"
                bind:value={formData.building}
                placeholder="e.g. Main Building"
                class="input input-bordered w-full rounded-xl text-sm focus:border-primary focus:outline-none"
                required
                disabled={isLoading}
              />
            </div>
            <div class="form-control gap-1.5">
              <label
                for="room_name"
                class="text-xs font-semibold text-base-content/70 uppercase tracking-wide"
              >
                Room <span class="text-error">*</span>
              </label>
              <input
                id="room_name"
                type="text"
                bind:value={formData.room_name}
                placeholder="e.g. Room 301"
                class="input input-bordered w-full rounded-xl text-sm focus:border-primary focus:outline-none"
                required
                disabled={isLoading}
              />
            </div>
          </div>

          <div class="form-control gap-1">
            <label
              for="attachment"
              class="text-xs font-semibold text-base-content/60 uppercase tracking-wider"
            >
              Attachment <span
                class="text-base-content/35 font-normal normal-case tracking-normal ml-"
                >(optional)</span
              >
            </label>

            <label
              for="attachment"
              class="flex flex-col items-center justify-center gap-2 rounded-xl border-2 border-dashed border-base-content/15 hover:border-primary/40 hover:bg-primary/3 transition-colors cursor-pointer py-6 px-4 text-center"
              class:border-primary={!!selectedFile}
              class:bg-primary={!!selectedFile}
            >
              {#if selectedFile}
                <div class="flex items-center gap-2 text-primary">
                  <Icon icon="mdi:file" class="w-5 h-5" />
                  <span class="text-sm font-medium truncate max-w-xs"
                    >{selectedFile.name}</span
                  >
                </div>
                <span class="text-xs text-base-content/40"
                  >Click to change file</span
                >
              {:else}
                <Icon icon="mdi:upload" class="w-7 h-7 text-base-content/20" />
                <span class="text-xs text-base-content/40">
                  Drop a file or <span class="text-primary font-medium"
                    >browse</span
                  >
                </span>
                <span class="text-[10px] text-base-content/30"
                  >PNG, JPG, PDF · max 5 MB</span
                >
              {/if}
            </label>
            <input
              id="attachment"
              type="file"
              class="hidden"
              onchange={handleFileChange}
              accept="image/*"
            />
          </div>

          {#if canEditPriorityStatus}
            <div class="grid grid-cols-2 gap-4 pt-1">
              <div class="form-control gap-1.5">
                <label
                  for="priority-admin"
                  class="text-xs font-semibold text-base-content/70 uppercase tracking-wide"
                  >Priority</label
                >
                <select
                  id="priority-admin"
                  bind:value={formData.priority}
                  class="select select-bordered w-full rounded-xl text-sm"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>
              <div class="form-control gap-1.5">
                <label
                  for="status"
                  class="text-xs font-semibold text-base-content/70 uppercase tracking-wide"
                  >Status</label
                >
                <select
                  id="status"
                  bind:value={formData.status}
                  class="select select-bordered w-full rounded-xl text-sm"
                >
                  <option value="pending">Pending</option>
                  <option value="in_progress">In Progress</option>
                  <option value="resolved">Resolved</option>
                  <option value="closed">Closed</option>
                </select>
              </div>
            </div>
          {:else if mode === "edit" && formData.status && formData.priority}
            <div
              class="flex items-center gap-3 p-3 rounded-xl bg-base-200/60 border border-base-content/6"
            >
              <Icon
                icon="mdi:information-outline"
                class="w-4 h-4 text-base-content/30 shrink-0"
              />
              <div class="flex items-center gap-2 flex-wrap">
                <span class="text-xs text-base-content/50"
                  >Admin-controlled:</span
                >
                <span
                  class="badge badge-sm {statusConfig[formData.status].color}"
                  >{statusConfig[formData.status].label}</span
                >
                <span
                  class="badge badge-sm {priorityConfig[
                    getPriorityKey(formData.priority)
                  ].color}"
                  >{priorityConfig[getPriorityKey(formData.priority)]
                    .label}</span
                >
              </div>
            </div>
          {/if}
        </div>

        <div
          class="flex items-center justify-end gap-2 px-6 py-4 border-t border-base-content/6 bg-base-100"
        >
          <button
            type="button"
            class="btn btn-ghost btn-sm rounded-xl text-base-content/60"
            onclick={onclose}
            disabled={isLoading}
          >
            Cancel
          </button>
          <button
            type="submit"
            class="btn btn-primary btn-sm rounded-xl gap-2 min-w-28"
            disabled={isLoading}
          >
            {#if isLoading}
              <span class="loading loading-spinner loading-xs"></span>
              {mode === "create" ? "Creating…" : "Saving…"}
            {:else}
              {mode === "create" ? "Create Ticket" : "Save Changes"}
            {/if}
          </button>
        </div>
      </form>
    </div>

    <form method="dialog" class="modal-backdrop">
      <button
        type="submit"
        aria-label="Close dialog"
        class="w-full h-full absolute inset-0 cursor-default bg-transparent border-none"
      ></button>
    </form>
  </dialog>
{/if}

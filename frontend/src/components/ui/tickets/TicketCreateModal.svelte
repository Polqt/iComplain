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
  import { onMount } from "svelte";
  import { fetchCategories, fetchPriorities } from "../../../lib/api/ticket.ts";

  export let open = false;
  export let mode: "create" | "edit" = "create";
  /** When false (e.g. student), priority/status are hidden on create and read-only on edit. */
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
    <!-- Sheet -->
    <div
      class="modal-box max-w-xl rounded-2xl p-0 overflow-hidden shadow-2xl border border-base-content/8"
    >
      <!-- Modal header -->
      <div
        class="flex items-center justify-between px-6 py-5 border-b border-base-content/6"
      >
        <div class="flex items-center gap-3">
          <div
            class="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center shrink-0"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="w-4 h-4 text-primary"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2.2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              {#if mode === "create"}
                <path d="M12 5v14M5 12h14" />
              {:else}
                <path
                  d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"
                /><path
                  d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"
                />
              {/if}
            </svg>
          </div>
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
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="w-4 h-4"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2.5"
          >
            <path d="M18 6L6 18M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Scrollable form body -->
      <form onsubmit={handleSubmit} class="overflow-y-auto max-h-[70vh]">
        <div class="px-6 py-5 space-y-5">
          <!-- Title -->
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

          <!-- Description -->
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
              placeholder="Describe the issue in detail — include anything that helps us understand the problem…"
              class="textarea textarea-bordered w-full h-28 rounded-xl text-sm resize-none focus:border-primary focus:outline-none"
              required
              disabled={isLoading}
            ></textarea>
          </div>

          <!-- Category + Priority row -->
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
                  disabled={isLoading}
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

          <!-- Building + Room row -->
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

          <!-- Attachment -->
          <div class="form-control gap-1.5">
            <label
              for="attachment"
              class="text-xs font-semibold text-base-content/70 uppercase tracking-wide"
            >
              Attachment <span
                class="text-base-content/30 font-normal normal-case"
                >(optional)</span
              >
            </label>

            <!-- Custom file drop zone -->
            <label
              for="attachment"
              class="flex flex-col items-center justify-center gap-2 rounded-xl border-2 border-dashed border-base-content/15 hover:border-primary/40 hover:bg-primary/3 transition-colors cursor-pointer py-6 px-4 text-center"
              class:border-primary={!!selectedFile}
              class:bg-primary={!!selectedFile}
            >
              {#if selectedFile}
                <div class="flex items-center gap-2 text-primary">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="w-5 h-5"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                  >
                    <path
                      d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
                    /><polyline points="14 2 14 8 20 8" />
                  </svg>
                  <span class="text-sm font-medium truncate max-w-xs"
                    >{selectedFile.name}</span
                  >
                </div>
                <span class="text-xs text-base-content/40"
                  >Click to change file</span
                >
              {:else}
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="w-7 h-7 text-base-content/20"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.5"
                >
                  <polyline points="16 16 12 12 8 16" /><line
                    x1="12"
                    y1="12"
                    x2="12"
                    y2="21"
                  /><path
                    d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"
                  />
                </svg>
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
              accept="image/*,.pdf,.doc,.docx,.txt"
            />
          </div>

          <!-- Admin-only: status override -->
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
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="w-4 h-4 text-base-content/30 shrink-0"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <circle cx="12" cy="12" r="10" /><line
                  x1="12"
                  y1="8"
                  x2="12"
                  y2="12"
                /><line x1="12" y1="16" x2="12.01" y2="16" />
              </svg>
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

        <!-- Footer actions -->
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

    <!-- Backdrop -->
    <form method="dialog" class="modal-backdrop">
      <button
        type="submit"
        aria-label="Close dialog"
        class="w-full h-full absolute inset-0 cursor-default bg-transparent border-none"
      ></button>
    </form>
  </dialog>
{/if}

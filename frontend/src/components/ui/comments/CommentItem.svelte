<script lang="ts">
  import Icon from "@iconify/svelte";
  import { authStore } from "../../../stores/auth.store.ts";
  import type { TicketComment } from "../../../types/comments.ts";
  import { formatTime } from "../../../utils/date.ts";
  import { deriveNameFromEmail } from "../../../utils/userConfig.ts";

  export let comment: TicketComment;
  export let onUpdate: (commentId: number, message: string) => Promise<void>;
  export let onDelete: (commentId: number) => Promise<void>;
  export let disabled: boolean = false;

  $: ({ user } = $authStore);
  $: isOwner = user?.id === comment.user.id;
  $: displayName = comment.user.name || deriveNameFromEmail(comment.user.email);
  $: initials = displayName
    .split(" ")
    .map((n: string) => n[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

  let editing = false;
  let editText = "";
  let saving = false;

  function startEdit() {
    editText = comment.message;
    editing = true;
  }

  function cancelEdit() {
    editing = false;
    editText = "";
  }

  async function saveEdit() {
    if (!editText.trim() || editText.trim() === comment.message) {
      cancelEdit();
      return;
    }
    saving = true;
    await onUpdate(comment.id, editText.trim());
    saving = false;
    editing = false;
  }

  async function handleDelete() {
    await onDelete(comment.id);
  }
</script>

<div class="flex gap-3 group">
  <div class="avatar placeholder shrink-0 mt-0.5">
    <div
      class="w-7 h-7 rounded-full ring-1 ring-primary/20
             flex items-center justify-center bg-primary/15"
    >
      {#if comment.user.avatar}
        <img src={comment.user.avatar} alt={displayName} class="rounded-full" />
      {:else}
        <span class="text-[10px] font-bold text-primary">{initials}</span>
      {/if}
    </div>
  </div>

  <div class="flex-1 min-w-0">
    <div class="flex items-center gap-2 mb-0.5">
      <span class="text-xs font-semibold text-base-content truncate">
        {displayName}
      </span>
      <span class="text-[10px] text-base-content/30"
        >{formatTime(comment.created_at)}</span
      >

      {#if isOwner && !editing && !disabled}
        <div
          class="ml-auto flex items-center gap-0.5 opacity-0 group-hover:opacity-100 transition-opacity"
        >
          <button
            type="button"
            onclick={startEdit}
            class="btn btn-ghost btn-xs btn-circle"
            aria-label="Edit comment"
          >
            <Icon
              icon="mdi:pencil-outline"
              width="12"
              height="12"
              class="text-base-content/40"
            />
          </button>
          <button
            type="button"
            onclick={handleDelete}
            class="btn btn-ghost btn-xs btn-circle"
            aria-label="Delete comment"
          >
            <Icon
              icon="mdi:delete-outline"
              width="12"
              height="12"
              class="text-error/60"
            />
          </button>
        </div>
      {/if}
    </div>

    {#if editing}
      <div class="flex flex-col gap-2">
        <textarea
          bind:value={editText}
          class="textarea textarea-bordered textarea-xs w-full resize-none rounded-lg
                 text-sm leading-relaxed"
          rows="2"
          disabled={saving}
        ></textarea>
        <div class="flex items-center gap-1.5 justify-end">
          <button
            type="button"
            onclick={cancelEdit}
            class="btn btn-ghost btn-xs rounded-lg"
            disabled={saving}
          >
            Cancel
          </button>
          <button
            type="button"
            onclick={saveEdit}
            class="btn btn-primary btn-xs rounded-lg"
            disabled={saving || !editText.trim()}
          >
            {#if saving}
              <span class="loading loading-spinner loading-xs"></span>
            {:else}
              Save
            {/if}
          </button>
        </div>
      </div>
    {:else}
      <p
        class="text-sm text-base-content/70 leading-relaxed whitespace-pre-wrap wrap-break-word"
      >
        {comment.message}
      </p>
    {/if}
  </div>
</div>

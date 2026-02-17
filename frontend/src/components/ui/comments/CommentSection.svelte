<script lang="ts">
  import { onDestroy, onMount, tick } from "svelte";
  import { commentsStore } from "../../../stores/comment.store.ts";
  import { wsStore } from "../../../stores/websocket.store.ts";
  import Icon from "@iconify/svelte";
  import CommentItem from "./CommentItem.svelte";

  export let ticketId: number;
  export let ticketStatus: string = "pending";
  export let compact: boolean = false;

  $: ({ comments, isLoading, error } = $commentsStore);
  $: isClosed = ticketStatus === "closed";

  let newMessage = "";
  let sending = false;
  let scrollContainer: HTMLDivElement;

  onMount(async () => {
    wsStore.connect();
    await commentsStore.loadCommentsForTicket(ticketId);
    await tick();
    scrollToBottom();
  });

  onDestroy(() => {
    commentsStore.clearComments();
  });

  async function scrollToBottom() {
    await tick();
    if (scrollContainer) {
      scrollContainer.scrollTop = scrollContainer.scrollHeight;
    }
  }

  async function handleSend() {
    const msg = newMessage.trim();
    if (!msg || sending) return;

    sending = true;
    const result = await commentsStore.createComment(ticketId, {
      message: msg,
    });

    if (result) {
      newMessage = "";
      await scrollToBottom();
    }
    sending = false;
  }

  function handleKeyDown(e: KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  async function handleUpdate(commentId: number, message: string) {
    await commentsStore.updateComment(ticketId, commentId, { message });
  }

  async function handleDelete(commentId: number) {
    await commentsStore.deleteComment(ticketId, commentId);
  }
</script>

<div
  class="flex flex-col {compact
    ? 'h-full'
    : 'bg-base-100 rounded-2xl border border-base-content/8 p-5 flex-1'}"
>
  <div class="flex items-center justify-between mb-4">
    <h3
      class="text-[10px] font-bold uppercase tracking-widest text-base-content/35"
    >
      Comments
      {#if comments.length > 0}
        <span class="text-base-content/20 ml-1">({comments.length})</span>
      {/if}
    </h3>
    {#if $wsStore === "connected"}
      <div class="tooltip tooltip-left" data-tip="Live updates active">
        <span
          class="w-1.5 h-1.5 rounded-full bg-success inline-block animate-pulse"
        ></span>
      </div>
    {/if}
  </div>

  <div
    bind:this={scrollContainer}
    class="flex-1 overflow-y-auto min-h-0 {compact
      ? 'max-h-[calc(100vh-16rem)]'
      : 'max-h-80'} pr-1"
  >
    {#if isLoading && comments.length === 0}
      <div class="flex flex-col gap-3 py-4">
        {#each [1, 2, 3] as _}
          <div class="flex gap-3">
            <div class="skeleton w-7 h-7 rounded-full shrink-0"></div>
            <div class="flex-1 space-y-1.5">
              <div class="skeleton w-24 h-3 rounded"></div>
              <div class="skeleton w-full h-3 rounded"></div>
            </div>
          </div>
        {/each}
      </div>
    {:else if error}
      <div class="flex flex-col items-center gap-2 py-8 text-center">
        <Icon
          icon="mdi:alert-circle-outline"
          width="20"
          height="20"
          class="text-error/50"
        />
        <p class="text-xs text-error/70">{error}</p>
        <button
          type="button"
          class="btn btn-ghost btn-sm rounded-lg"
          onclick={() => commentsStore.loadCommentsForTicket(ticketId)}
        >
          Retry
        </button>
      </div>
    {:else if comments.length === 0}
      <div class="flex flex-col items-center gap-2 py-8 text-center">
        <Icon
          icon="mdi:chat-outline"
          width="24"
          height="24"
          class="text-base-content/15"
        />
        <p class="text-xs text-base-content/30">
          No comments yet. Start the conversation
        </p>
      </div>
    {:else}
      <div class="flex flex-col gap-4">
        {#each comments as comment (comment.id)}
          <CommentItem
            {comment}
            onUpdate={handleUpdate}
            onDelete={handleDelete}
            disabled={isClosed}
          />
        {/each}
      </div>
    {/if}
  </div>

  {#if !isClosed}
    <div class="border-t border-base-content/8 pt-3 mt-3">
      <div class="flex items-end gap-2">
        <textarea
          name="newMessage"
          id="newMessage"
          bind:value={newMessage}
          onkeydown={handleKeyDown}
          rows="1"
          placeholder="Say something about this ticket…"
          class="textarea textarea-bordered flex-1 resize-none rounded-xl text-sm
                 leading-relaxed min-h-10 max-h-24"
          disabled={isLoading || sending}
        ></textarea>

        <button
          type="button"
          onclick={handleSend}
          disabled={sending || !newMessage.trim() || isLoading}
          class="btn btn-primary btn-sm btn-circle shrink-0"
          aria-label="Send comment"
        >
          {#if sending}
            <span class="loading loading-spinner loading-xs"></span>
          {:else}
            <Icon icon="mdi:send" width="16" height="16" />
          {/if}
        </button>
      </div>
    </div>
  {:else}
    <div class="border-t border-base-content/8 mt-3 pt-3">
      <p class="text-xs text-base-content/30 text-center italic">
        This ticket is closed. No new comments.
      </p>
    </div>
  {/if}
</div>

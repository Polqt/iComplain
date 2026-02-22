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
  {#if $wsStore === "connected"}
    <div class="flex items-center gap-1.5 px-5 pt-4 pb-0 shrink-0">
      <span
        class="w-1.5 h-1.5 rounded-full bg-success inline-block animate-pulse"
      ></span>
      <span class="text-[10px] text-base-content/30 font-medium">Live</span>
    </div>
  {/if}

  <div
    bind:this={scrollContainer}
    class="flex-1 overflow-y-auto min-h-0 px-5 py-4
           {compact ? 'max-h-[calc(100vh-18rem)]' : 'max-h-80'}"
  >
    {#if isLoading && comments.length === 0}
      <div class="flex flex-col gap-4">
        {#each [1, 2, 3] as _}
          <div class="flex gap-3 items-start">
            <div class="skeleton w-8 h-8 rounded-full shrink-0"></div>
            <div class="flex-1 space-y-2 pt-0.5">
              <div class="skeleton w-28 h-3 rounded-full"></div>
              <div class="skeleton w-full h-3 rounded-full"></div>
              <div class="skeleton w-3/4 h-3 rounded-full"></div>
            </div>
          </div>
        {/each}
      </div>
    {:else if error}
      <div class="flex flex-col items-center gap-3 py-10 text-center">
        <div
          class="w-9 h-9 rounded-xl bg-error/10 flex items-center justify-center"
        >
          <Icon
            icon="mdi:alert-circle-outline"
            width="18"
            height="18"
            class="text-error/60"
          />
        </div>
        <p class="text-xs text-base-content/50">{error}</p>
        <button
          type="button"
          class="btn btn-ghost btn-xs rounded-lg text-xs"
          onclick={() => commentsStore.loadCommentsForTicket(ticketId)}
        >
          Try again
        </button>
      </div>
    {:else if comments.length === 0}
      <div class="flex flex-col items-center gap-2 py-10 text-center">
        <div
          class="w-9 h-9 rounded-xl bg-base-200 flex items-center justify-center"
        >
          <Icon
            icon="mdi:chat-outline"
            width="18"
            height="18"
            class="text-base-content/25"
          />
        </div>
        <p class="text-xs text-base-content/35">No comments yet</p>
      </div>
    {:else}
      <div class="flex flex-col gap-5">
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

  <div class="shrink-0 px-4 py-3 border-t border-base-content/8">
    {#if !isClosed}
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
    {:else}
      <p class="text-xs text-base-content/30 text-center py-1">
        This ticket is closed — no new comments.
      </p>
    {/if}
  </div>
</div>

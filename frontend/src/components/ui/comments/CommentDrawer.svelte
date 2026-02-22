<script lang="ts">
  import Icon from "@iconify/svelte";
  import type { Ticket } from "../../../types/tickets.ts";
  import CommentSection from "./CommentSection.svelte";
  import { commentsStore } from "../../../stores/comment.store.ts";

  export let ticket: Ticket | null = null;

  $: if (ticket) {
    commentsStore.clearComments();
  }
</script>

<div
  class="w-[380px] shrink-0 bg-base-100 border-l border-base-content/8 flex flex-col"
>
  {#if ticket}
    {#key ticket.id}
      <div class="flex flex-col h-full">
        <!-- Header -->
        <div class="px-5 pt-5 pb-4 border-b border-base-content/8 shrink-0">
          <p
            class="text-[10px] font-semibold uppercase tracking-widest text-base-content/30 mb-2"
          >
            Discussion
          </p>
          <h3
            class="font-semibold text-sm text-base-content leading-snug truncate mb-1.5"
          >
            {ticket.title}
          </h3>
          <div class="flex items-center gap-1.5">
            <span
              class="inline-flex items-center rounded-md bg-base-200 px-2 py-0.5 text-[10px] font-mono text-base-content/50"
            >
              {ticket.ticket_number}
            </span>
            <span class="text-base-content/25 text-xs">·</span>
            <span class="text-[11px] text-base-content/40 truncate">
              {ticket.building} · {ticket.room_name}
            </span>
          </div>
        </div>

        <!-- Comment section -->
        <div class="flex-1 min-h-0">
          <CommentSection
            ticketId={ticket.id}
            ticketStatus={ticket.status}
            compact={true}
          />
        </div>
      </div>
    {/key}
  {:else}
    <!-- Empty state -->
    <div
      class="flex flex-col items-center justify-center h-full text-center px-8 gap-3"
    >
      <div
        class="w-12 h-12 rounded-xl bg-base-200 flex items-center justify-center"
      >
        <Icon
          icon="mdi:chat-outline"
          width="22"
          height="22"
          class="text-base-content/25"
        />
      </div>
      <div>
        <p class="text-sm font-semibold text-base-content/50 mb-1">
          No ticket selected
        </p>
        <p class="text-xs text-base-content/30 leading-relaxed">
          Select a ticket to view its discussion
        </p>
      </div>
    </div>
  {/if}
</div>

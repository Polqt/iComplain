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
  class="w-115 shrink-0 bg-base-100 border-l border-base-content/10 flex flex-col"
>
  {#if ticket}
    {#key ticket.id}
      <div class="flex flex-col h-full">
        <div class="px-4 py-3 border-b border-base-content/10 shrink-0">
          <div class="flex items-start gap-2">
            <Icon
              icon="mdi:chat-outline"
              width="18"
              height="18"
              class="text-base-content/60 shrink-0 mt-0.5"
            />
            <div class="flex-1 min-w-0">
              <h3
                class="font-semibold text-sm text-base-content truncate mb-0.5"
              >
                {ticket.title}
              </h3>
              <div
                class="flex items-center gap-2 text-[10px] text-base-content/40"
              >
                <span class="font-mono">{ticket.ticket_number}</span>
                <span>·</span>
                <span class="truncate"
                  >{ticket.building} · {ticket.room_name}</span
                >
              </div>
            </div>
          </div>
        </div>
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
    <div
      class="flex flex-col items-center justify-center h-full text-center px-6"
    >
      <div
        class="w-16 h-16 rounded-2xl bg-base-200 flex items-center justify-center mb-4"
      >
        <Icon
          icon="mdi:chat-outline"
          width="32"
          height="32"
          class="text-base-content/30"
        />
      </div>
      <h3 class="text-base font-semibold text-base-content/60 mb-2">
        No ticket selected
      </h3>
      <p class="text-sm text-base-content/40 leading-relaxed">
        Click any ticket to view and participate in its discussion
      </p>
    </div>
  {/if}
</div>

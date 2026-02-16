<script lang="ts">
  import type { TicketStatus, Ticket } from "../../../types/tickets.ts";
  import CommunityTicketCard from "./CommunityTicketCard.svelte";
  import Icon from "@iconify/svelte";
  export let column: any;
  export let status: TicketStatus;
  export let tickets: Ticket[] = [];
  export let pageTickets: Ticket[] = [];
  export let totalPages: number = 1;
  export let currentPage: number = 1;
  export let onPageChange: (page: number) => void = () => {};
</script>

<div class="flex flex-col min-h-0 gap-2">
  <div
    class="flex items-center justify-between px-3 py-2 rounded-xl
           border {column.headerTint} shrink-0"
  >
    <div class="flex items-center gap-2">
      <span class="w-2 h-2 rounded-full shrink-0 {column.dot}"></span>
      <span
        class="text-[10px] font-bold uppercase tracking-widest text-base-content/60"
      >
        {column.label}
      </span>
    </div>
    <span
      class="text-[10px] font-semibold rounded-full px-1.5 py-0.5
             min-w-5 text-center {column.countBg}"
    >
      {tickets.length}
    </span>
  </div>

  <div class="flex flex-col gap-1.5 flex-1 min-h-0 relative">
    <div class="flex flex-col gap-1.5 overflow-y-auto flex-1 min-h-0 pr-0.5">
      {#if tickets.length > 0}
        {#each pageTickets as ticket (ticket.id)}
          <CommunityTicketCard {ticket} />
        {/each}
      {:else}
        <div
          class="flex flex-col items-center justify-center gap-2 flex-1
                 rounded-xl min-h-20 border-2 border-dashed border-base-content/7"
        >
          <Icon
            icon={column.icon}
            width="18"
            height="18"
            class="text-base-content/20"
          />
          <p class="text-[10px] text-base-content/25 font-medium">
            {column.emptyText}
          </p>
        </div>
      {/if}
    </div>

    {#if tickets.length > 0 && totalPages > 1}
      <div class="flex justify-center mt-1.5">
        <div class="join">
          {#each Array(totalPages) as _, index}
            {@const pageNum = index + 1}
            <input
              class="join-item btn btn-xs btn-square"
              type="radio"
              name={`page-${status}`}
              aria-label={String(pageNum)}
              checked={pageNum === currentPage}
              onclick={() => onPageChange(pageNum)}
            />
          {/each}
        </div>
      </div>
    {/if}
  </div>
</div>


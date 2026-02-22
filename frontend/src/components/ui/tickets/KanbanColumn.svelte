<script lang="ts">
  import type { Ticket } from "../../../types/tickets.ts";
  import CommunityTicketCard from "./CommunityTicketCard.svelte";
  import Icon from "@iconify/svelte";

  export let tickets: Ticket[] = [];
  export let totalPages: number = 1;
  export let currentPage: number = 1;
  export let onPageChange: (page: number) => void = () => {};
</script>

<div class="flex flex-col flex-1 min-h-0">
  <div class="flex-1 overflow-y-auto space-y-3 pr-1">
    {#if tickets.length === 0}
      <div
        class="flex flex-col items-center justify-center h-full text-base-content/60"
      >
        <Icon
          icon="mdi:inbox-outline"
          width="64"
          height="64"
          class="text-base-content/20 mb-4"
        />
        <p class="text-lg font-medium">No tickets found</p>
        <p class="text-sm mt-1">Try adjusting your filters</p>
      </div>
    {:else}
      {#each tickets as ticket (ticket.id)}
        <CommunityTicketCard {ticket} />
      {/each}
    {/if}
  </div>

  <!-- Pagination -->
  {#if totalPages > 1 && tickets.length > 0}
    <div class="shrink-0 mt-4 flex justify-center">
      <div class="join">
        <button
          class="join-item btn btn-sm"
          disabled={currentPage === 1}
          on:click={() => onPageChange(currentPage - 1)}
        >
          «
        </button>
        {#each Array.from({ length: totalPages }, (_, i) => i + 1) as page}
          {#if page === 1 || page === totalPages || (page >= currentPage - 1 && page <= currentPage + 1)}
            <button
              class="join-item btn btn-sm"
              class:btn-active={page === currentPage}
              on:click={() => onPageChange(page)}
            >
              {page}
            </button>
          {:else if page === currentPage - 2 || page === currentPage + 2}
            <button class="join-item btn btn-sm btn-disabled">...</button>
          {/if}
        {/each}
        <button
          class="join-item btn btn-sm"
          disabled={currentPage === totalPages}
          on:click={() => onPageChange(currentPage + 1)}
        >
          »
        </button>
      </div>
    </div>
  {/if}
</div>

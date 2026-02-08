<script lang="ts">
  import Icon from "@iconify/svelte";

  export let searchQuery: string = "";
  export let hasActiveFilter: boolean = false;
  export let onclear: () => void = () => {};
</script>

<div class="flex flex-col items-center justify-center h-full text-center py-12">
  <Icon
    icon="mdi:history"
    width="64"
    height="64"
    class="text-base-content/20 mb-4"
  />
  <h3 class="text-lg font-semibold text-base-content/80 mb-1">
    No history found
  </h3>
  <p class="text-sm text-base-content/50 mb-4">
    {searchQuery
      ? "No activities match your search criteria."
      : "You don't have any ticket history yet."}
  </p>
  {#if searchQuery || hasActiveFilter}
    <button type="button" class="btn btn-sm btn-primary" on:click={onclear}>
      Clear Filters
    </button>
  {/if}
</div>

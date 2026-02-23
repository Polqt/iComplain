<script lang="ts">
  export let rating: number | null = null;
  export let size: 'sm' | 'md' = 'sm';
</script>

{#if rating !== null}
  <div class={"badge badge-ghost " + (size === 'sm' ? 'badge-sm' : 'badge-md')}>
    <span class="font-semibold">{rating}</span>
    <span class="text-xs text-base-content/40 ml-2">rating</span>
  </div>
{:else}
  <div class="badge badge-ghost badge-sm text-base-content/40">No rating</div>
{/if}

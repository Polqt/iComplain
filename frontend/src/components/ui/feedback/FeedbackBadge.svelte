<script lang="ts">
import Icon from "@iconify/svelte";

export let rating: number | null = null;
export let size: "sm" | "md" = "sm";

$: badgeClass = size === "sm" ? "badge-sm" : "badge-md";
$: starSize = size === "sm" ? 12 : 14;
</script>

{#if rating !== null}
  <div class="badge badge-ghost gap-1 {badgeClass}">
    <div class="flex items-center gap-0.5">
      {#each Array(5) as _, i}
        <Icon
          icon={i < rating ? "mdi:star" : "mdi:star-outline"}
          width={starSize}
          height={starSize}
          class={i < rating ? "text-warning" : "text-base-content/20"}
        />
      {/each}
    </div>
    <span class="font-semibold ml-1">{rating}/5</span>
  </div>
{:else}
  <div class="badge badge-ghost {badgeClass} text-base-content/40">
    <Icon icon="mdi:star-off" width={starSize} height={starSize} class="mr-1" />
    No rating
  </div>
{/if}

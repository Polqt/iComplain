<script lang="ts">
import Icon from "@iconify/svelte";

export let rating: number | null = null;
export let size: "sm" | "md" = "sm";
export let compact = false;
export let showValue = true;

$: badgeClass = size === "sm" ? "badge-sm" : "badge-md";
$: starSize = size === "sm" ? 12 : 16;
$: compactTextClass = size === "sm" ? "text-xs" : "text-sm";
</script>

{#if rating !== null}
  {#if compact}
    <div class="flex items-center gap-1.5">
      <div class="flex items-center gap-0.5">
        {#each Array(5) as _, i}
          <Icon
            icon={i < rating ? "mdi:star" : "mdi:star-outline"}
            width={starSize}
            height={starSize}
            class={i < rating ? "text-warning" : "text-base-content/25"}
          />
        {/each}
      </div>
      {#if showValue}
        <span class="{compactTextClass} font-semibold text-base-content/85"
          >{rating}/5</span
        >
      {/if}
    </div>
  {:else}
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
      {#if showValue}
        <span class="font-semibold ml-1">{rating}/5</span>
      {/if}
    </div>
  {/if}
{:else}
  <div class="badge badge-ghost {badgeClass} text-base-content/40">
    <Icon icon="mdi:star-off" width={starSize} height={starSize} class="mr-1" />
    No rating
  </div>
{/if}

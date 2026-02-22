<script lang="ts">
  import FeedbackItem from "./FeedbackItem.svelte";
  import type { TicketFeedback } from "../../../types/feedback.ts";

  export let feedbacks: TicketFeedback[] = [];
  export let emptyMessage: string = "No feedback yet.";
</script>

{#if feedbacks?.length}
  <div class="flex flex-col gap-3">
    {#each feedbacks as f}
      <FeedbackItem feedback={f} />
    {/each}
  </div>
{:else}
  <div class="text-sm text-base-content/40">{emptyMessage}</div>
{/if}

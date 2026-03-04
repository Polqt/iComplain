<script lang="ts">
import Icon from "@iconify/svelte";
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
  <div class="flex flex-col items-center justify-center py-8 text-center">
    <Icon
      icon="mdi:comment-off-outline"
      width="32"
      height="32"
      class="text-base-content/20 mb-2"
    />
    <p class="text-sm text-base-content/40">{emptyMessage}</p>
  </div>
{/if}

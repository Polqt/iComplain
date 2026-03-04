<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import Icon from "@iconify/svelte";
  import type {
    FeedbackCreatePayload,
    FeedbackUpdatePayload,
    TicketFeedback,
  } from "../../../types/feedback.ts";
  import { createFeedback, updateFeedback } from "../../../lib/api/feedback.ts";

  export let ticketId: number;
  export let existing: TicketFeedback | null = null;
  export let disabled: boolean = false;

  const dispatch = createEventDispatcher();

  let rating: number = existing?.rating ?? 5;
  let comments: string = existing?.comments ?? "";
  let saving = false;
  let error: string | null = null;
  let hoveredStar: number | null = null;

  async function handleSubmit(e: Event) {
    e.preventDefault();
    if (disabled || saving) return;
    saving = true;
    error = null;

    try {
      const payload: FeedbackCreatePayload | FeedbackUpdatePayload = {
        rating,
        comments: comments || null,
      };

      let result: TicketFeedback;
      if (existing) {
        result = await updateFeedback(
          ticketId,
          existing.id,
          payload as FeedbackUpdatePayload,
        );
      } else {
        result = await createFeedback(
          ticketId,
          payload as FeedbackCreatePayload,
        );
      }

      dispatch("saved", { feedback: result });
    } catch (err) {
      error = err instanceof Error ? err.message : String(err);
      dispatch("error", { error });
    } finally {
      saving = false;
    }
  }

  function setRating(value: number) {
    if (!disabled) {
      rating = value;
    }
  }

  $: displayRating = hoveredStar !== null ? hoveredStar : rating;
</script>

<form class="space-y-4" onsubmit={handleSubmit}>
  <div class="space-y-2">
    <label for="rating" class="text-sm font-semibold text-base-content"
      >How would you rate your experience?</label
    >
    <div class="flex items-center gap-1" id="rating">
      {#each [1, 2, 3, 4, 5] as star}
        <button
          type="button"
          class="btn btn-ghost btn-sm p-1 h-auto min-h-0 transition-all duration-200
                 hover:scale-110 {disabled
            ? 'cursor-not-allowed opacity-50'
            : ''}"
          onclick={() => setRating(star)}
          onmouseenter={() => !disabled && (hoveredStar = star)}
          onmouseleave={() => (hoveredStar = null)}
          {disabled}
        >
          <Icon
            icon={displayRating >= star ? "mdi:star" : "mdi:star-outline"}
            width="28"
            height="28"
            class={displayRating >= star
              ? "text-warning"
              : "text-base-content/20"}
          />
        </button>
      {/each}
      <span class="ml-2 text-sm font-medium text-base-content/60">
        {rating}/5
      </span>
    </div>
    <p class="text-xs text-base-content/40">1 = Poor, 5 = Excellent</p>
  </div>

  <!-- Comments -->
  <div class="space-y-2">
    <label for="comments" class="text-sm font-semibold text-base-content">
      Additional Comments
      <span class="text-xs font-normal text-base-content/40">(Optional)</span>
    </label>
    <textarea
      id="comments"
      class="textarea textarea-bordered w-full resize-none focus:textarea-primary transition-colors"
      rows={4}
      placeholder="Share your experience with us..."
      bind:value={comments}
      {disabled}
    ></textarea>
  </div>

  <!-- Error Message -->
  {#if error}
    <div class="alert alert-error shadow-sm">
      <Icon icon="mdi:alert-circle" width="20" height="20" />
      <span class="text-sm">{error}</span>
    </div>
  {/if}

  <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-2">
    <button
      type="submit"
      class="btn btn-primary gap-2 flex-1 sm:flex-initial"
      disabled={saving || disabled}
    >
      {#if saving}
        <span class="loading loading-spinner loading-sm"></span>
        Saving...
      {:else}
        <Icon icon="mdi:send" width="18" height="18" />
        {existing ? "Update Feedback" : "Submit Feedback"}
      {/if}
    </button>
    <button
      type="button"
      class="btn btn-ghost gap-2"
      onclick={() => dispatch("cancel")}
      disabled={saving}
    >
      <Icon icon="mdi:close" width="18" height="18" />
      Cancel
    </button>
  </div>
</form>

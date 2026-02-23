<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import type { FeedbackCreatePayload, FeedbackUpdatePayload, TicketFeedback } from "../../../types/feedback.ts";
  import { createFeedback, updateFeedback } from "../../../lib/api/feedback.ts";

  export let ticketId: number;
  export let existing: TicketFeedback | null = null;
  export let disabled: boolean = false;

  const dispatch = createEventDispatcher();

  let rating: number = existing?.rating ?? 5;
  let comments: string = existing?.comments ?? "";
  let saving = false;
  let error: string | null = null;

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
        result = await updateFeedback(ticketId, existing.id, payload as FeedbackUpdatePayload);
      } else {
        result = await createFeedback(ticketId, payload as FeedbackCreatePayload);
      }

      dispatch("saved", { feedback: result });
    } catch (err) {
      error = err instanceof Error ? err.message : String(err);
      dispatch("error", { error });
    } finally {
      saving = false;
    }
  }
</script>

<form class="space-y-3" on:submit|preventDefault={handleSubmit}>
  <div class="flex items-center gap-3">
    <label for="rating" class="text-xs text-base-content/60">Rating</label>
    <select class="input input-sm max-w-[84px]" bind:value={rating} disabled={disabled}>
      <option value={5}>5</option>
      <option value={4}>4</option>
      <option value={3}>3</option>
      <option value={2}>2</option>
      <option value={1}>1</option>
    </select>
    <span class="text-xs text-base-content/40">(1 = lowest, 5 = highest)</span>
  </div>

  <div>
    <label for="comments" class="text-xs text-base-content/60">Comments (optional)</label>
    <textarea class="textarea textarea-sm w-full mt-1" rows={3} bind:value={comments} disabled={disabled}></textarea>
  </div>

  {#if error}
    <div class="text-sm text-error">{error}</div>
  {/if}

  <div class="flex items-center gap-2">
    <button type="submit" class="btn btn-primary btn-sm" disabled={saving || disabled}>
      {#if saving}Saving...{:else}{existing ? 'Update Feedback' : 'Submit Feedback'}{/if}
    </button>
    <button type="button" class="btn btn-ghost btn-sm" on:click={() => dispatch('cancel')}>Cancel</button>
  </div>
</form>

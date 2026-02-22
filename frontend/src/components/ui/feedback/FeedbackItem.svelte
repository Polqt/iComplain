<script lang="ts">
  import type { TicketFeedback } from "../../../types/feedback.ts";
  import { formatDate } from "../../../utils/date.ts";

  export let feedback: TicketFeedback;
  export let compact: boolean = false;
</script>

<div class="bg-base-100 rounded-lg border border-base-content/8 p-3">
  <div class="flex items-start gap-3">
    <div class="flex-1 min-w-0">
      <div class="flex items-center gap-2">
        <div class="text-sm font-semibold">Rating: <span class="ml-1">{feedback.rating}</span></div>
        <div class="text-xs text-base-content/40 ml-auto">{formatDate(feedback.created_at)}</div>
      </div>

      {#if feedback.comments}
        <p class="text-sm text-base-content/60 mt-2">{feedback.comments}</p>
      {/if}

      {#if !compact}
        <div class="text-[11px] text-base-content/40 mt-2">By {feedback.student?.name ?? feedback.student?.email}</div>
      {/if}
    </div>
  </div>
</div>

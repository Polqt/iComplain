<script lang="ts">
  import Icon from "@iconify/svelte";
  import type { Ticket } from "../../../types/tickets.ts";
  import { getPriorityKey, priorityConfig, priorityDot } from "../../../utils/ticketConfig.ts";
  import { formatDate } from "../../../utils/date.ts";

  export let ticket: Ticket;

  $: pKey = getPriorityKey(ticket.priority);
</script>

<div
  class="group bg-base-100 rounded-xl border border-base-content/7
         hover:border-base-content/16
         hover:shadow-[0_2px_16px_rgba(0,0,0,0.07)]
         transition-all duration-150"
>
  <div class="p-3.5">
    <div class="flex items-center justify-between gap-2 mb-2">
      <div class="flex items-center gap-1.5 min-w-0">
        <span
          class="w-2 h-2 rounded-full shrink-0
                 {priorityDot[pKey] ?? 'bg-base-content/15'}"
          title="{priorityConfig[pKey]?.label} priority"
        ></span>
        <span
          class="text-[10px] text-base-content/45 bg-base-200
                 rounded-full px-2 py-0.5 truncate max-w-32 font-medium"
        >
          {ticket.category.name}
        </span>
      </div>
      <span class="text-[10px] font-mono text-base-content/20 shrink-0">
        {ticket.ticket_number}
      </span>
    </div>

    <p
      class="text-[13px] font-semibold text-base-content
               leading-snug line-clamp-2 mb-1.5"
    >
      {ticket.title}
    </p>

    <p
      class="text-[11px] text-base-content/40 leading-relaxed
               line-clamp-2 mb-2.5"
    >
      {ticket.description}
    </p>

    <div class="flex items-center gap-1 mb-3">
      <Icon
        icon="mdi:map-marker-outline"
        width="10"
        height="10"
        class="text-base-content/25 shrink-0"
      />
      <span class="text-[10px] text-base-content/35 truncate">
        {ticket.building} · {ticket.room_name}
      </span>
    </div>

    <div
      class="flex items-center justify-between gap-2
             pt-2.5 border-t border-base-content/6"
    >
      <div class="flex items-center gap-1.5 min-w-0">
        <div
          class="w-5 h-5 rounded-full bg-primary/10 shrink-0
                 flex items-center justify-center
                 text-[9px] font-bold text-primary uppercase"
        >
          {ticket.student.email[0]}
        </div>
        <span
          class="text-[10px] text-base-content/35 truncate max-w-20"
        >
          {ticket.student.email.split("@")[0]}
        </span>
      </div>

      <div class="flex items-center gap-2 shrink-0">
        <span class="text-[10px] text-base-content/25">
          {formatDate(ticket.created_at)}
        </span>
        <button
          class="flex items-center gap-0.5 text-base-content/25
                 hover:text-primary transition-colors"
          title="Comments — coming soon"
          type="button"
        >
          <Icon
            icon="mdi:comment-outline"
            width="12"
            height="12"
          />
          <span class="text-[10px] font-mono">0</span>
        </button>
        <button
          class="text-base-content/25 hover:text-primary transition-colors"
          title="Support — coming soon"
          type="button"
        >
          <Icon
            icon="mdi:arrow-up-bold-outline"
            width="12"
            height="12"
          />
        </button>
      </div>
    </div>
  </div>
</div>


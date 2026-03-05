<script lang="ts">
  import Icon from "@iconify/svelte";
  import type { Ticket } from "../../../types/tickets.ts";
  import { goto } from "$app/navigation";
  import { formatTime } from "../../../utils/date.ts";

  export let ticket: Ticket;
  export let onClick: () => void = () => {};
  export let onCommentClick: (ticket: Ticket) => void = () => {};
  export let onUpvoteToggle: (ticket: Ticket) => void = () => {};
  export let upvoteCount = 0;
  export let isUpvoted = false;
  export let isActive = false;

  let clickTimer: NodeJS.Timeout | null = null;
  let clickCount = 0;
  let isImageModalOpen = false;

  function handleCardClick() {
    clickCount++;

    if (clickCount === 1) {
      clickTimer = setTimeout(() => {
        onClick();
        clickCount = 0;
      }, 250);
    } else if (clickCount === 2) {
      if (clickTimer) clearTimeout(clickTimer);
      goto(`/tickets/${ticket.ticket_number}`);
      clickCount = 0;
    }
  }

  function getInitials(name?: string | null) {
    if (!name) return "AN";
    const parts = name
      .trim()
      .split(/\s+/)
      .slice(0, 2)
      .map((part) => part[0]?.toUpperCase() ?? "")
      .join("");
    return parts || "AN";
  }

  $: commentCount = ticket.comments_count ?? 0;
  $: hasAttachment = !!ticket.attachment;
  $: authorName = ticket.student?.name || "Anonymous";
</script>

<div
  role="button"
  tabindex="0"
  class="w-full text-left rounded-2xl border border-base-content/10 bg-base-100/90 backdrop-blur-sm transition-all duration-200
    {isActive
    ? 'ring-1 ring-base-content/20 border-base-content/20'
    : 'hover:bg-base-100 hover:border-base-content/20'}"
  aria-label="Ticket: {ticket.title}"
  aria-current={isActive ? "true" : undefined}
  onclick={handleCardClick}
  onkeydown={(e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      handleCardClick();
    }
  }}
>
  <article class="p-4 md:p-5">
    <div class="flex items-start gap-3">
      <div class="avatar placeholder shrink-0">
        {#if ticket.student?.avatar}
          <img
            src={ticket.student.avatar}
            alt={authorName}
            class="w-10 h-10 rounded-full object-cover border border-base-content/15"
            loading="lazy"
          />
        {:else}
          <div
            class="w-10 rounded-full bg-base-200 text-base-content/70 border border-base-content/10"
          >
            <span class="text-xs font-semibold">{getInitials(authorName)}</span>
          </div>
        {/if}
      </div>

      <div class="flex-1 min-w-0">
        <div class="flex items-start justify-between gap-3 mb-2">
          <div class="min-w-0">
            <div class="flex items-center gap-2 min-w-0">
              <p class="text-sm font-semibold text-base-content truncate">
                {authorName}
              </p>
              <span class="text-xs text-base-content/45 shrink-0"
                >{formatTime(ticket.created_at)}</span
              >
            </div>
            <div
              class="mt-1 flex items-center gap-2 text-[11px] text-base-content/50 flex-wrap"
            >
              <span class="font-mono">{ticket.ticket_number}</span>
              <span
                class="px-2 py-0.5 rounded-full border border-base-content/20 bg-base-200/60"
              >
                {ticket.category.name}
              </span>
            </div>
          </div>

          <button
            type="button"
            class="btn btn-ghost btn-xs btn-circle text-base-content/45 hover:text-base-content"
            onclick={(e) => e.stopPropagation()}
            aria-label="More options"
          >
            <Icon icon="mdi:dots-horizontal" width="18" height="18" />
          </button>
        </div>

        <h3
          class="text-base md:text-lg font-medium text-base-content leading-snug mb-1.5 line-clamp-2"
        >
          {ticket.title}
        </h3>

        <p
          class="text-sm text-base-content/75 leading-relaxed mb-2 line-clamp-3"
        >
          {ticket.description}
        </p>

        <p class="text-xs text-base-content/50 mb-3">
          {ticket.building} - {ticket.room_name}
        </p>

        {#if hasAttachment}
          <button
            type="button"
            class="mb-3 overflow-hidden rounded-xl border border-base-content/10 bg-base-200/40 max-w-xl w-full text-left block"
            onclick={(e) => {
              e.stopPropagation();
              isImageModalOpen = true;
            }}
            aria-label="View attachment"
          >
            <img
              src={ticket.attachment}
              alt={`Attachment for ${ticket.title}`}
              class="w-full h-56 object-cover"
              loading="lazy"
            />
          </button>
        {/if}

        <div class="flex items-center gap-4 text-base-content/65">
          <button
            type="button"
            class="inline-flex items-center gap-1.5 transition-colors {isUpvoted
              ? 'text-primary'
              : 'hover:text-base-content'}"
            onclick={(e) => {
              e.stopPropagation();
              onUpvoteToggle(ticket);
            }}
            aria-label="Upvote ticket"
            aria-pressed={isUpvoted ? "true" : "false"}
          >
            <Icon
              icon={isUpvoted
                ? "mdi:arrow-up-bold-circle"
                : "mdi:arrow-up-bold-circle-outline"}
              width="20"
              height="20"
            />
            <span class="text-xs font-medium">{upvoteCount}</span>
          </button>

          <button
            type="button"
            class="inline-flex items-center gap-1.5 hover:text-base-content transition-colors"
            onclick={(e) => {
              e.stopPropagation();
              onCommentClick(ticket);
            }}
            aria-label="Open comments"
          >
            <Icon icon="mdi:comment-outline" width="20" height="20" />
            <span class="text-xs font-medium">{commentCount}</span>
          </button>
        </div>
      </div>
    </div>
  </article>
</div>

{#if isImageModalOpen && ticket.attachment}
  <dialog class="modal modal-open" onclick={() => (isImageModalOpen = false)}>
    <div
      class="modal-box max-w-5xl p-0 bg-base-100 border border-base-content/10"
      role="dialog"
      tabindex="0"
      onclick={(e) => e.stopPropagation()}
      onkeydown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          e.stopPropagation();
        }
      }}
    >
      <div
        class="flex items-center justify-between px-4 py-3 border-b border-base-content/10"
      >
        <p class="text-sm font-medium text-base-content truncate pr-3">
          {ticket.title}
        </p>
        <button
          type="button"
          class="btn btn-ghost btn-sm btn-circle"
          onclick={() => (isImageModalOpen = false)}
          aria-label="Close image preview"
        >
          <Icon icon="mdi:close" width="18" height="18" />
        </button>
      </div>
      <img
        src={ticket.attachment}
        alt={`Attachment for ${ticket.title}`}
        class="w-full max-h-[78vh] object-contain bg-black/90"
      />
    </div>
  </dialog>
{/if}

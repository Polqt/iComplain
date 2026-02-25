<script lang="ts">
  import Icon from "@iconify/svelte";
  import { getFileName, isImageFile } from "../../../utils/attachment.ts";

  export let attachment: string | null = null;
  export let ticketNumber: string = "";

  let isOpen = false;

  function open() {
    if (attachment) isOpen = true;
  }

  function close() {
    isOpen = false;
  }

  function handleBackdropClick(e: MouseEvent) {
    if (e.target === e.currentTarget) close();
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === "Escape") close();
  }
</script>

<svelte:window on:keydown={handleKeydown} />

{#if attachment}
  <button type="button" class="btn btn-sm btn-outline gap-2" onclick={open}>
    <Icon icon="mdi:paperclip" width="16" height="16" />
    View Attachment
  </button>
{/if}

{#if isOpen && attachment}
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm"
    onclick={handleBackdropClick}
  >
    <div
      class="card bg-base-100 shadow-2xl w-full max-w-lg mx-4 max-h-[85vh] flex flex-col rounded-2xl overflow-hidden"
    >
      <div
        class="flex items-center justify-between px-5 py-4 border-b border-base-content/8 shrink-0"
      >
        <div class="flex items-center gap-2 min-w-0">
          <Icon
            icon="mdi:paperclip"
            width="18"
            height="18"
            class="text-base-content/50 shrink-0"
          />
          <div class="min-w-0">
            <h3 class="text-sm font-semibold truncate">Attachment</h3>
            <p class="text-xs text-base-content/50 truncate">{ticketNumber}</p>
          </div>
        </div>
        <button
          type="button"
          class="btn btn-sm btn-ghost btn-circle"
          onclick={close}
          aria-label="Close"
        >
          <Icon icon="mdi:close" width="18" height="18" />
        </button>
      </div>

      <div class="flex-1 overflow-y-auto p-5">
        {#if isImageFile(attachment)}
          <figure
            class="rounded-xl overflow-hidden bg-base-200 border border-base-content/5 mb-4"
          >
            <img
              src={attachment}
              alt="Ticket attachment"
              class="w-full max-h-96 object-contain"
            />
          </figure>
        {/if}

        <div
          class="flex items-center justify-between gap-3 p-3 rounded-lg bg-base-200 border border-base-content/5"
        >
          <div class="flex items-center gap-2 flex-1 min-w-0">
            <Icon
              icon={isImageFile(attachment) ? "mdi:image" : "mdi:file-document"}
              width="20"
              height="20"
              class="text-base-content/60 shrink-0"
            />
            <span class="text-sm font-medium truncate">
              {getFileName(attachment)}
            </span>
          </div>
          <a
            href={attachment}
            target="_blank"
            rel="noopener noreferrer"
            class="btn btn-sm btn-primary gap-1"
          >
            <Icon icon="mdi:download" width="16" height="16" />
            Download
          </a>
        </div>
      </div>
    </div>
  </div>
{/if}

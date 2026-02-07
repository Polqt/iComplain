<script lang="ts">
  import Icon from "@iconify/svelte";
  import { createEventDispatcher } from "svelte";

  export let placeholder: string = "Start searching here...";
  export let mobilePlaceholder: string = "Search...";
  export let showShortcutBadge: boolean = true;
  export let isMobile: boolean = false;

  const dispatch = createEventDispatcher<{
    openModal: void;
    focus: void;
  }>();

  function handleClick() {
    dispatch("openModal");
  }

  function handleFocus() {
    dispatch("focus");
  }
</script>

<div class="flex-1 min-w-0">
  <button
    type="button"
    class="flex items-center gap-2 bg-base-100 dark:bg-base-100 rounded-lg shadow px-2 sm:px-4 py-2 w-full hover:shadow-md transition-shadow"
    onclick={handleClick}
    onfocus={handleFocus}
  >
    <Icon
      icon="lucide:search"
      width="20"
      height="20"
      class="text-base-content/50 shrink-0"
    />
    <span class="flex-1 text-left text-base-content/50 text-sm sm:text-base"
      >{isMobile ? mobilePlaceholder : placeholder}</span
    >
    {#if showShortcutBadge}
      <kbd class="kbd kbd-sm hidden sm:inline-flex lg:kbd-md">⌘ K</kbd>
    {/if}
  </button>
</div>

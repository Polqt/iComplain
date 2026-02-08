<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import { goto } from "$app/navigation";
  import Icon from "@iconify/svelte";

  import { createEventDispatcher } from "svelte";
  import { searchStore } from "../../stores/search.store.ts";
  import type { SearchResult } from "../../types/search.ts";

  export let isOpen: boolean = false;

  const dispatch = createEventDispatcher<{
    close: void;
    select: SearchResult;
  }>();

  let inputElement: HTMLInputElement;

  // Subscribe to search store
  $: query = $searchStore.query;
  $: results = $searchStore.results;
  $: recentSearches = $searchStore.recentSearches;
  $: isSearching = $searchStore.isSearching;
  $: selectedIndex = $searchStore.selectedIndex;

  // Result type icons
  const typeIcons = {
    report: "mdi:file-document-outline",
    notification: "mdi:bell-outline",
    page: "mdi:view-dashboard-outline",
  };

  // Result type colors
  const typeColors = {
    report: "text-primary",
    notification: "text-warning",
    page: "text-info",
  };

  // Global keyboard shortcut handler (Cmd+K to open modal)
  function handleKeyDown(event: KeyboardEvent) {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
      event.preventDefault();
      if (!isOpen) {
        isOpen = true;
      }
    }
  }

  // Input keyboard handler - THIS HANDLES ARROW KEYS AND ENTER
  function handleInputKeyDown(event: KeyboardEvent) {
    switch (event.key) {
      case "ArrowDown":
        event.preventDefault();
        searchStore.selectNext();
        break;
      case "ArrowUp":
        event.preventDefault();
        searchStore.selectPrevious();
        break;
      case "Enter":
        event.preventDefault();
        const selected = searchStore.getSelectedResult();
        if (selected) {
          handleSelectResult(selected);
        }
        break;
      case "Escape":
        event.preventDefault();
        closeModal();
        break;
    }
  }

  function handleInputChange(event: Event) {
    const target = event.target as HTMLInputElement;
    searchStore.search(target.value);
  }

  function handleSelectResult(result: SearchResult) {
    searchStore.addRecentSearch(query);
    dispatch("select", result);
    goto(result.url);
    closeModal();
  }

  function handleRecentSearch(recentQuery: string) {
    searchStore.search(recentQuery);
    if (inputElement) {
      inputElement.focus();
    }
  }

  function closeModal() {
    isOpen = false;
    searchStore.clear();
    dispatch("close");
  }

  $: if (isOpen && inputElement) {
    setTimeout(() => inputElement.focus(), 100);
  }

  onMount(() => {
    searchStore.loadRecentSearches();
    window.addEventListener("keydown", handleKeyDown);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  });

  onDestroy(() => {
    searchStore.clear();
  });
</script>

{#if isOpen}
  <div
    class="fixed inset-0 z-50 flex items-start justify-center bg-black/40 backdrop-blur-sm pt-20"
    role="button"
    tabindex="0"
    onclick={closeModal}
    onkeydown={(e) => {
      if (e.key === "Escape") closeModal();
    }}
  >
    <div
      class="bg-base-100 rounded-lg shadow-2xl w-full max-w-2xl mx-4 overflow-hidden"
      role="presentation"
      onclick={(e) => e.stopPropagation()}
    >
      <div class="flex items-center gap-3 p-4 border-b border-base-content/10">
        <Icon
          icon="lucide:search"
          width="20"
          height="20"
          class="text-base-content/50"
        />
        <input
          aria-label="Search input"
          bind:this={inputElement}
          type="text"
          placeholder="Search reports, notifications, pages..."
          class="flex-1 bg-transparent outline-none border-none focus:ring-0 text-base"
          value={query}
          oninput={handleInputChange}
          onkeydown={handleInputKeyDown}
        />
        {#if isSearching}
          <span class="loading loading-spinner loading-sm text-base-content/40"
          ></span>
        {/if}
        <button
          class="btn btn-ghost btn-sm btn-circle"
          onclick={closeModal}
          title="Close (Esc)"
        >
          <Icon icon="lucide:x" width="16" height="16" />
        </button>
      </div>

      <div class="max-h-96 overflow-y-auto">
        {#if query && results.length > 0}
          <div class="p-2">
            <div class="px-3 py-2">
              <span
                class="text-xs font-semibold text-base-content/50 uppercase tracking-wider"
              >
                Results
              </span>
            </div>
            {#each results as result, index}
              <button
                class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-base-200 transition-colors text-left {selectedIndex ===
                index
                  ? 'bg-base-200'
                  : ''}"
                onclick={() => handleSelectResult(result)}
              >
                <div class="shrink-0">
                  <div
                    class="w-8 h-8 rounded-lg bg-base-200 flex items-center justify-center {selectedIndex ===
                    index
                      ? 'bg-base-300'
                      : ''}"
                  >
                    <Icon
                      icon={result.icon || typeIcons[result.type]}
                      width="18"
                      height="18"
                      class={typeColors[result.type]}
                    />
                  </div>
                </div>

                <div class="flex-1 min-w-0">
                  <div class="font-medium text-sm text-base-content truncate">
                    {result.title}
                  </div>
                  {#if result.description}
                    <div class="text-xs text-base-content/60 truncate">
                      {result.description}
                    </div>
                  {/if}
                </div>
                {#if result.meta}
                  <div class="shrink-0">
                    <span class="text-xs text-base-content/50">
                      {result.meta}
                    </span>
                  </div>
                {/if}

                {#if selectedIndex === index}
                  <Icon
                    icon="lucide:corner-down-left"
                    width="14"
                    height="14"
                    class="text-base-content/40"
                  />
                {/if}
              </button>
            {/each}
          </div>
        {:else if query && !isSearching}
          <div
            class="flex flex-col items-center justify-center py-12 text-center"
          >
            <Icon
              icon="mdi:magnify"
              width="48"
              height="48"
              class="text-base-content/20 mb-3"
            />
            <p class="text-sm font-medium text-base-content/80 mb-1">
              No results found
            </p>
            <p class="text-xs text-base-content/50">Try different keywords</p>
          </div>
        {:else if !query && recentSearches.length > 0}
          <div class="p-2">
            <div class="px-3 py-2 flex items-center justify-between">
              <span
                class="text-xs font-semibold text-base-content/50 uppercase tracking-wider"
              >
                Recent Searches
              </span>
              <button
                class="text-xs text-base-content/50 hover:text-base-content/80"
                onclick={() => searchStore.clearRecentSearches()}
              >
                Clear
              </button>
            </div>
            {#each recentSearches as recent}
              <button
                class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-base-200 transition-colors text-left"
                onclick={() => handleRecentSearch(recent)}
              >
                <Icon
                  icon="lucide:clock"
                  width="16"
                  height="16"
                  class="text-base-content/40"
                />
                <span class="flex-1 text-sm text-base-content/80">{recent}</span
                >
                <Icon
                  icon="lucide:arrow-up-left"
                  width="14"
                  height="14"
                  class="text-base-content/30"
                />
              </button>
            {/each}
          </div>
        {:else}
          <div
            class="flex flex-col items-center justify-center py-12 text-center"
          >
            <Icon
              icon="mdi:magnify"
              width="48"
              height="48"
              class="text-base-content/20 mb-3"
            />
            <p class="text-sm font-medium text-base-content/80 mb-1">
              Search anything
            </p>
            <p class="text-xs text-base-content/50">
              Reports, notifications, pages, and more
            </p>
          </div>
        {/if}
      </div>

      <div
        class="flex items-center justify-between px-4 py-3 border-t border-base-content/10 bg-base-200/50"
      >
        <div class="flex items-center gap-4 text-xs text-base-content/50">
          <div class="flex items-center gap-1">
            <kbd class="kbd kbd-xs">↑</kbd>
            <kbd class="kbd kbd-xs">↓</kbd>
            <span>Navigate</span>
          </div>
          <div class="flex items-center gap-1">
            <kbd class="kbd kbd-xs">↵</kbd>
            <span>Select</span>
          </div>
          <div class="flex items-center gap-1">
            <kbd class="kbd kbd-xs">esc</kbd>
            <span>Close</span>
          </div>
        </div>
      </div>
    </div>
  </div>
{/if}

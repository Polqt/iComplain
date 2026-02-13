<script lang="ts">
  import { onMount } from "svelte";
  import HistoryFilters from "./HistoryFilters.svelte";
  import HistoryTimeline from "./HistoryTimeline.svelte";
  import type {
    HistoryFilterType,
    HistoryItem,
    HistorySortType,
  } from "../../../types/history.ts";
  import {
    filterAndSortHistory,
    historyConfig,
  } from "../../../utils/historyConfig.ts";

  /** Called on mount to load history items. */
  export let fetchItems: () => Promise<HistoryItem[]> = async () => [];

  export let title: string = "Ticket History";
  export let description: string =
    "View all your ticket activities and status changes.";
  export let ticketUrlPrefix: string = "/tickets";

  let activeFilter: HistoryFilterType = "all";
  let sortBy: HistorySortType = "newest";
  let searchQuery: string = "";
  let historyItems: HistoryItem[] = [];
  let loading = true;
  let error: string | null = null;

  onMount(async () => {
    try {
      loading = true;
      error = null;
      historyItems = await fetchItems();
    } catch (e) {
      error = e instanceof Error ? e.message : "Failed to load history";
      historyItems = [];
    } finally {
      loading = false;
    }
  });

  $: filteredItems = filterAndSortHistory(
    historyItems,
    activeFilter,
    searchQuery,
    sortBy,
  );

  function clearFilters() {
    activeFilter = "all";
    searchQuery = "";
    sortBy = "newest";
  }
</script>

<div class="flex flex-col h-[calc(100vh-8rem)]">
  <div class="shrink-0 mb-6">
    <h1 class="text-2xl font-black text-base-content mb-1">{title}</h1>
    <p class="text-sm text-base-content/60">
      {description}
    </p>
  </div>

  <div class="mb-6 shrink-0">
    <HistoryFilters
      bind:activeFilter
      bind:sortBy
      bind:searchQuery
      totalCount={historyItems.length}
      onclear={clearFilters}
    />
  </div>

  {#if loading}
    <div class="flex-1 flex items-center justify-center text-base-content/60">
      Loading history…
    </div>
  {:else if error}
    <div class="flex-1 flex items-center justify-center text-error">
      {error}
    </div>
  {:else if filteredItems.length > 0}
    <div class="mb-4 shrink-0">
      <p class="text-sm text-base-content/60">
        Showing <span class="font-semibold text-primary"
          >{filteredItems.length}</span
        >
        {filteredItems.length === 1 ? "activity" : "activities"}
        {#if activeFilter !== "all"}
          in <span class="font-semibold"
            >{historyConfig[activeFilter].label}</span
          >
        {/if}
      </p>
    </div>
  {/if}

  <div class="flex-1 overflow-y-auto pr-2">
    <HistoryTimeline
      items={filteredItems}
      {activeFilter}
      {searchQuery}
      sortBy={sortBy}
      {ticketUrlPrefix}
      onclearfilters={clearFilters}
    />
  </div>
</div>

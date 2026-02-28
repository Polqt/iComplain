<script lang="ts">
  import { onMount } from "svelte";
  import HistoryFilters from "./HistoryFilters.svelte";
  import HistoryTimeline from "./HistoryTimeline.svelte";
  import AdminHistoryTimeline from "./AdminHistoryTimeline.svelte";
  import type {
    HistoryFilterType,
    HistoryItem,
    HistorySortType,
  } from "../../../types/history.ts";
  import {
    filterAndSortHistory,
    getActivityLabel,
    historyConfig,
  } from "../../../utils/historyConfig.ts";
  import { authStore } from "../../../stores/auth.store.ts";

  export let fetchItems: () => Promise<HistoryItem[]> = async () => [];

  let activeFilter: HistoryFilterType = "all";
  let sortBy: HistorySortType = "newest";
  let searchQuery: string = "";
  let historyItems: HistoryItem[] = [];
  let loading = true;
  let error: string | null = null;

  $: ({ role } = $authStore);

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

{#if role === "student"}
  <div class="flex flex-col h-[calc(100vh-8rem)]">
    <div class="shrink-0 mb-6">
      <h1 class="text-2xl font-black text-base-content mb-1">Ticket History</h1>
      <p class="text-sm text-base-content/60">
        View all your ticket activities and status changes.
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
    {:else}
      {#if filteredItems.length > 0}
        <div class="mb-4 shrink-0">
          <p class="text-sm text-base-content/60">
            Showing <span class="font-semibold text-primary"
              >{filteredItems.length}</span
            >
            {getActivityLabel(filteredItems.length)}
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
          {sortBy}
          onclearfilters={clearFilters}
        />
      </div>
    {/if}
  </div>
{:else if role === "admin"}
  <div class="flex flex-col h-[calc(100vh-8rem)]">
    <div class="shrink-0 mb-6">
      <h1 class="text-2xl font-black text-base-content mb-1">Admin History</h1>
      <p class="text-sm text-base-content/60">
        View all ticket activities across the system. Track status changes, priority updates, and admin actions for accountability.
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
    {:else}
      {#if filteredItems.length > 0}
        <div class="mb-4 shrink-0">
          <p class="text-sm text-base-content/60">
            Showing <span class="font-semibold text-primary"
              >{filteredItems.length}</span
            >
            {getActivityLabel(filteredItems.length)}
            {#if activeFilter !== "all"}
              in <span class="font-semibold"
                >{historyConfig[activeFilter].label}</span
              >
            {/if}
          </p>
        </div>
      {/if}

      <div class="flex-1 overflow-y-auto pr-2">
        <AdminHistoryTimeline
          items={filteredItems}
          {activeFilter}
          {searchQuery}
          {sortBy}
          onclearfilters={clearFilters}
        />
      </div>
    {/if}
  </div>
{/if}

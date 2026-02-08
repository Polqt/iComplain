<script lang="ts">
  import Icon from "@iconify/svelte";
  import type { HistoryFilterType, HistorySortType } from "../../../types/history.js";

  export let activeFilter: HistoryFilterType = "all";
  export let sortBy: HistorySortType = "newest";
  export let searchQuery: string = "";
  export let totalCount: number = 0;

  export let onclear: () => void = () => {};

  $: hasActiveFilters = activeFilter !== "all" || searchQuery.length > 0 || sortBy !== "newest";
</script>

<div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
  <!-- Filter Tabs -->
  <div class="tabs tabs-boxed bg-base-200 p-1">
    <button
      type="button"
      class="tab {activeFilter === 'all' ? 'tab-active' : ''}"
      on:click={() => (activeFilter = "all")}
    >
      All
      <span class="badge badge-sm ml-2">{totalCount}</span>
    </button>
    <button
      type="button"
      class="tab {activeFilter === 'created' ? 'tab-active' : ''}"
      on:click={() => (activeFilter = "created")}
    >
      Created
    </button>
    <button
      type="button"
      class="tab {activeFilter === 'updated' ? 'tab-active' : ''}"
      on:click={() => (activeFilter = "updated")}
    >
      Updated
    </button>
    <button
      type="button"
      class="tab {activeFilter === 'resolved' ? 'tab-active' : ''}"
      on:click={() => (activeFilter = "resolved")}
    >
      Resolved
    </button>
    <button
      type="button"
      class="tab {activeFilter === 'closed' ? 'tab-active' : ''}"
      on:click={() => (activeFilter = "closed")}
    >
      Closed
    </button>
    <button
      type="button"
      class="tab {activeFilter === 'commented' ? 'tab-active' : ''}"
      on:click={() => (activeFilter = "commented")}
    >
      Commented
    </button>
    <button
      type="button"
      class="tab {activeFilter === 'reopened' ? 'tab-active' : ''}"
      on:click={() => (activeFilter = "reopened")}
    >
      Reopened
    </button>
  </div>

  <!-- Sort and Search Controls -->
  <div class="flex items-center gap-3">
    <div class="form-control">
      <div class="input-group">
        <input
          type="text"
          placeholder="Search history..."
          class="input input-bordered input-sm w-48"
          bind:value={searchQuery}
        />
        {#if searchQuery}
          <button
            type="button"
            class="btn btn-square btn-sm"
            on:click={() => (searchQuery = "")}
          >
            <Icon icon="mdi:close" width="16" height="16" />
          </button>
        {/if}
      </div>
    </div>

    <div class="dropdown dropdown-end">
      <button type="button" tabindex={0} class="btn btn-sm btn-outline gap-2">
        <Icon icon="mdi:sort" width="16" height="16" />
        {sortBy === "newest" ? "Newest" : "Oldest"}
      </button>
      <ul class="dropdown-content menu p-2 shadow bg-base-100 rounded-box w-40 mt-2">
        <li>
          <button type="button" on:click={() => (sortBy = "newest")}>
            <Icon icon="mdi:sort-descending" width="16" height="16" />
            Newest First
          </button>
        </li>
        <li>
          <button type="button" on:click={() => (sortBy = "oldest")}>
            <Icon icon="mdi:sort-ascending" width="16" height="16" />
            Oldest First
          </button>
        </li>
      </ul>
    </div>

    {#if hasActiveFilters}
      <button type="button" class="btn btn-sm btn-ghost" on:click={onclear}>
        <Icon icon="mdi:filter-off" width="16" height="16" />
        Clear
      </button>
    {/if}
  </div>
</div>

<script lang="ts">
  import Icon from "@iconify/svelte";
  import type { TicketStatus } from "../../../types/tickets.ts";
  import {
    priorityFilters,
    statusFilters,
  } from "../../../utils/ticketConfig.ts";

  export let search = "";
  export let activeStatus: TicketStatus | "all" = "all";
  export let priorityFilter: string = "all";
  export let totalCount = 0;
  export let statusCounts: Record<TicketStatus | "all", number>;

  export let onSearchChange: (value: string) => void = () => {};
  export let onStatusChange: (value: TicketStatus | "all") => void = () => {};
  export let onPriorityChange: (value: string) => void = () => {};
  export let onClear: () => void = () => {};

  $: hasActiveFilters =
    search || activeStatus != "all" || priorityFilter !== "all";

  function clearAll() {
    onSearchChange("");
    onStatusChange("all");
    onPriorityChange("all");
    onClear();
  }
</script>

<div class="flex items-center gap-2 flex-wrap shrink-0">
  <label
    for="search"
    class="flex items-center gap-2 px-3 h-8 rounded-lg flex-1 min-w-44
           bg-base-200/70 border border-base-content/8
           focus-within:border-base-content/22 focus-within:bg-base-100
           transition-all duration-150"
  >
    <Icon
      icon="mdi:magnify"
      width="13"
      height="13"
      class="text-base-content/30"
    />
    <input
      type="text"
      placeholder="Search issues..."
      class="grow text-xs bg-transparent outline-none
            text-base-content placeholder:text-base-content/30"
      value={search}
      oninput={(e) => onSearchChange((e.target as HTMLInputElement).value)}
    />
    {#if search}
      <button
        onclick={() => onSearchChange("")}
        class="text-base-content/25 hover:text-base-content/60 transition-colors"
      >
        <Icon icon="mdi:close" width="11" height="11" />
      </button>
    {/if}
  </label>

  <div
    class="flex items-center bg-base-200/70 border border-base-content/8
              rounded-lg h-8 px-0.5 gap-0.5"
  >
    {#each statusFilters as f}
      <button
        class="flex items-center gap-1.5 px-2.5 h-7 rounded-md text-[11px] font-medium
               transition-all duration-100
               {activeStatus === f.id
          ? 'bg-base-100 shadow-sm text-base-content'
          : 'text-base-content/40 hover:text-base-content/65'}"
        onclick={() => onStatusChange(f.id)}
      >
        <span class="w-1.5 h-1.5 rounded-full shrink-0 {f.dot}"></span>
        {f.label}
        <span class="font-mono text-[10px] opacity-50">
          {statusCounts[f.id] ?? 0}
        </span>
      </button>
    {/each}
  </div>

  <div
    class="flex items-center bg-base-200/70 border border-base-content/8
              rounded-lg h-8 px-0.5 gap-0.5"
  >
    {#each priorityFilters as pf}
      <button
        class="flex items-center gap-1 px-2.5 h-7 rounded-md text-[11px] font-medium
               transition-all duration-100
               {priorityFilter === pf.id
          ? 'bg-base-100 shadow-sm text-base-content'
          : 'text-base-content/40 hover:text-base-content/65'}"
        onclick={() => onPriorityChange(pf.id)}
      >
        {#if pf.id !== "all"}
          <span
            class="w-1.5 h-1.5 rounded-full shrink-0
                   {pf.id === 'high'
              ? 'bg-orange-400'
              : pf.id === 'medium'
                ? 'bg-yellow-400'
                : 'bg-base-content/20'}"
          ></span>
        {/if}
        {pf.label}
      </button>
    {/each}
  </div>

  <div
    class="flex items-center gap-1.5 h-8 px-3 rounded-lg
              bg-base-200/70 border border-base-content/8
              text-[11px] text-base-content/45 font-mono shrink-0"
  >
    <Icon icon="mdi:ticket-outline" width="12" height="12" />
    {totalCount}

    {#if hasActiveFilters}
      <button
        class="ml-1 text-base-content/30 hover:text-primary transition-colors"
        onclick={clearAll}
        title="Clear all filters"
      >
        <Icon icon="mdi:filter-remove-outline" width="12" height="12" />
      </button>
    {/if}
  </div>
</div>

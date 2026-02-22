<script lang="ts">
  import Icon from "@iconify/svelte";
  import type { TicketStatus } from "../../../types/tickets.ts";
  import {
    statusFilters,
    priorityFilters,
    categoriesFilters,
  } from "../../../utils/ticketConfig.ts";

  export let activeStatus: TicketStatus | "all" = "all";
  export let priorityFilter: string = "all";
  export let categoryFilter: string = "all";
  export let totalCount = 0;
  export let statusCounts: Record<TicketStatus | "all", number> = {
    all: 0,
    pending: 0,
    in_progress: 0,
    resolved: 0,
    closed: 0,
  };

  let search = "";

  export let onStatusChange: (value: TicketStatus | "all") => void = () => {};
  export let onPriorityChange: (value: string) => void = () => {};
  export let onCategoryChange: (value: string) => void = () => {};
  export let onClear: () => void = () => {};

  $: hasActiveFilters =
    activeStatus !== "all" ||
    priorityFilter !== "all" ||
    categoryFilter !== "all";

  $: activeStatusLabel =
    statusFilters.find((f) => f.id === activeStatus)?.label ?? "All";
  $: activeStatusDot =
    statusFilters.find((f) => f.id === activeStatus)?.dot ??
    "bg-base-content/30";

  $: activePriorityLabel =
    priorityFilters.find((p) => p.id === priorityFilter)?.label ?? "All";
  $: activePriorityDot =
    priorityFilter === "urgent"
      ? "bg-red-500"
      : priorityFilter === "high"
        ? "bg-orange-400"
        : priorityFilter === "medium"
          ? "bg-yellow-400"
          : priorityFilter === "low"
            ? "bg-base-content/20"
            : null;

  $: activeCategoryLabel =
    categoriesFilters.find((c) => c.id === categoryFilter)?.name ?? "All";

  function closeDropdown() {
    (document.activeElement as HTMLElement)?.blur();
  }

  function clearAll() {
    onStatusChange("all");
    onPriorityChange("all");
    onCategoryChange("all");
    onClear();
  }
</script>

<div class="flex items-center gap-2 shrink-0">
  <label
    class="input input-sm flex items-center gap-2 w-80 rounded-lg
               bg-base-200/60 border-base-content/10 focus-within:border-base-content/25
               focus-within:bg-base-100 transition-all duration-150"
  >
    <Icon
      icon="mdi:magnify"
      width="14"
      height="14"
      class="text-base-content/35 shrink-0"
    />
    <input
      type="text"
      placeholder="Search tickets…"
      class="grow text-sm bg-transparent outline-none
                 text-base-content placeholder:text-base-content/30"
      bind:value={search}
    />
    {#if search}
      <button
        type="button"
        onclick={() => (search = "")}
        class="text-base-content/30 hover:text-base-content/60 transition-colors shrink-0"
        aria-label="Clear search"
      >
        <Icon icon="mdi:close" width="12" height="12" />
      </button>
    {/if}
  </label>
  <div class="dropdown dropdown-bottom dropdown-end">
    <button
      tabindex="0"
      class="btn btn-sm btn-ghost border border-base-content/10 rounded-lg h-8 min-h-8
             gap-1.5 font-medium text-xs px-3
             hover:border-base-content/20 hover:bg-base-200
             {activeStatus !== 'all'
        ? 'text-primary border-primary/25 bg-primary/5 hover:bg-primary/8'
        : 'text-base-content/60'}"
    >
      <span class="w-1.5 h-1.5 rounded-full shrink-0 {activeStatusDot}"></span>
      {activeStatusLabel}
      {#if activeStatus !== "all"}
        <span class="font-mono text-[10px] opacity-60"
          >{statusCounts[activeStatus] ?? 0}</span
        >
      {/if}
      <Icon icon="mdi:chevron-down" width="11" height="11" class="opacity-40" />
    </button>

    <div
      class="dropdown-content z-50 mt-1 w-48 bg-base-100
                border border-base-content/10 rounded-xl shadow-xl p-1"
    >
      {#each statusFilters as f}
        <button
          role="menuitem"
          class="w-full flex items-center gap-2.5 px-3 py-1.5 rounded-lg
                 text-xs text-left transition-colors
                 {activeStatus === f.id
            ? 'bg-primary/8 text-primary font-semibold'
            : 'text-base-content/65 hover:bg-base-200'}"
          onclick={() => {
            onStatusChange(f.id);
            closeDropdown();
          }}
        >
          <span class="w-1.5 h-1.5 rounded-full shrink-0 {f.dot}"></span>
          <span class="flex-1">{f.label}</span>
          <span class="font-mono text-[10px] opacity-40"
            >{statusCounts[f.id] ?? 0}</span
          >
          {#if activeStatus === f.id}
            <Icon
              icon="mdi:check"
              width="10"
              height="10"
              class="text-primary shrink-0"
            />
          {/if}
        </button>
      {/each}
    </div>
  </div>

  <div class="dropdown dropdown-bottom dropdown-end">
    <button
      tabindex="0"
      class="btn btn-sm btn-ghost border border-base-content/10 rounded-lg h-8 min-h-8
             gap-1.5 font-medium text-xs px-3
             hover:border-base-content/20 hover:bg-base-200
             {priorityFilter !== 'all'
        ? 'text-primary border-primary/25 bg-primary/5 hover:bg-primary/8'
        : 'text-base-content/60'}"
    >
      {#if activePriorityDot}
        <span class="w-1.5 h-1.5 rounded-full shrink-0 {activePriorityDot}"
        ></span>
      {:else}
        <Icon
          icon="mdi:flag-outline"
          width="11"
          height="11"
          class="opacity-40"
        />
      {/if}
      {activePriorityLabel}
      <Icon icon="mdi:chevron-down" width="11" height="11" class="opacity-40" />
    </button>

    <div
      class="dropdown-content z-50 mt-1 w-36 bg-base-100
                border border-base-content/10 rounded-xl shadow-xl p-1"
    >
      {#each priorityFilters as pf}
        <button
          role="menuitem"
          class="w-full flex items-center gap-2.5 px-3 py-1.5 rounded-lg
                 text-xs text-left transition-colors
                 {priorityFilter === pf.id
            ? 'bg-primary/8 text-primary font-semibold'
            : 'text-base-content/65 hover:bg-base-200'}"
          onclick={() => {
            onPriorityChange(pf.id);
            closeDropdown();
          }}
        >
          {#if pf.id === "all"}
            <Icon
              icon="mdi:flag-outline"
              width="10"
              height="10"
              class="opacity-35 shrink-0"
            />
          {:else}
            <span
              class="w-1.5 h-1.5 rounded-full shrink-0
                     {pf.id === 'urgent'
                ? 'bg-red-500'
                : pf.id === 'high'
                  ? 'bg-orange-400'
                  : pf.id === 'medium'
                    ? 'bg-yellow-400'
                    : 'bg-base-content/20'}"
            ></span>
          {/if}
          <span class="flex-1">{pf.label}</span>
          {#if priorityFilter === pf.id}
            <Icon
              icon="mdi:check"
              width="10"
              height="10"
              class="text-primary shrink-0"
            />
          {/if}
        </button>
      {/each}
    </div>
  </div>

  <div class="dropdown dropdown-bottom dropdown-end">
    <button
      tabindex="0"
      class="btn btn-sm btn-ghost border border-base-content/10 rounded-lg h-8 min-h-8
             gap-1.5 font-medium text-xs px-3
             hover:border-base-content/20 hover:bg-base-200
             {categoryFilter !== 'all'
        ? 'text-primary border-primary/25 bg-primary/5 hover:bg-primary/8'
        : 'text-base-content/60'}"
    >
      <Icon icon="mdi:tag-outline" width="11" height="11" class="opacity-40" />
      {activeCategoryLabel}
      <Icon icon="mdi:chevron-down" width="11" height="11" class="opacity-40" />
    </button>

    <div
      class="dropdown-content z-50 mt-1 w-64 bg-base-100
                border border-base-content/10 rounded-xl shadow-xl p-1
                max-h-72 overflow-y-auto"
    >
      {#each categoriesFilters as cf}
        <button
          role="menuitem"
          class="w-full flex items-center gap-2.5 px-3 py-1.5 rounded-lg
                 text-xs text-left transition-colors
                 {categoryFilter === cf.id
            ? 'bg-primary/8 text-primary font-semibold'
            : 'text-base-content/65 hover:bg-base-200'}"
          onclick={() => {
            onCategoryChange(cf.id);
            closeDropdown();
          }}
        >
          <span class="flex-1 truncate">{cf.name}</span>
          {#if categoryFilter === cf.id}
            <Icon
              icon="mdi:check"
              width="10"
              height="10"
              class="text-primary shrink-0"
            />
          {/if}
        </button>
      {/each}
    </div>
  </div>

  <div
    class="flex items-center gap-1 h-8 px-2.5 rounded-lg border border-base-content/10
              bg-base-200/60 text-[11px] text-base-content/40 font-mono shrink-0"
  >
    <Icon icon="mdi:ticket-outline" width="11" height="11" />
    {totalCount}
    {#if hasActiveFilters}
      <button
        type="button"
        onclick={clearAll}
        class="ml-0.5 text-base-content/30 hover:text-error transition-colors"
        title="Clear all filters"
        aria-label="Clear all filters"
      >
        <Icon icon="mdi:close-circle-outline" width="12" height="12" />
      </button>
    {/if}
  </div>
</div>

<script lang="ts">
  import Icon from "@iconify/svelte";
  import type {
    HistoryItem,
    HistoryFilterType,
    HistorySortType,
  } from "../../../types/history.ts";
  import { historyConfig } from "../../../utils/historyConfig.ts";
  import HistoryCard from "./HistoryCard.svelte";
  import HistoryEmptyState from "./HistoryEmptyState.svelte";

  export let items: HistoryItem[] = [];
  export let activeFilter: HistoryFilterType = "all";
  export let searchQuery: string = "";
  export let sortBy: HistorySortType = "newest";
  export let ticketUrlPrefix: string = "/tickets";
  export let onclearfilters: () => void = () => {};

  $: hasAnyFilter =
    activeFilter !== "all" ||
    searchQuery.length > 0 ||
    sortBy !== "newest";
</script>

{#if items.length === 0}
  <HistoryEmptyState
    searchQuery={searchQuery}
    hasActiveFilter={hasAnyFilter}
    onclear={onclearfilters}
  />
{:else}
  <div class="space-y-4">
    {#each items as item, index}
      <div class="flex gap-4">
        <div class="flex flex-col items-center">
          <div
            class="w-10 h-10 rounded-full {historyConfig[item.action].bgColor} flex items-center justify-center shrink-0"
          >
            <Icon
              icon={historyConfig[item.action].icon}
              width="20"
              height="20"
              class={historyConfig[item.action].color}
            />
          </div>
          {#if index < items.length - 1}
            <div class="w-0.5 h-full bg-base-content/10 mt-2"></div>
          {/if}
        </div>

        <div class="flex-1 pb-4">
          <HistoryCard {item} {ticketUrlPrefix} />
        </div>
      </div>
    {/each}
  </div>
{/if}

<script lang="ts">
  import Icon from "@iconify/svelte";
  import type {
    HistoryItem,
    HistoryFilterType,
    HistorySortType,
  } from "../../../types/history.ts";
  import { historyConfig, formatRelativeTime } from "../../../utils/historyConfig.ts";
  import { goto } from "$app/navigation";

  export let items: HistoryItem[] = [];
  export let activeFilter: HistoryFilterType = "all";
  export let searchQuery: string = "";
  export let sortBy: HistorySortType = "newest";
  export let onclearfilters: () => void = () => {};

  function navigate(ticketId: string) {
    goto(`tickets/${ticketId}`);
  }

  $: hasAnyFilter =
    activeFilter !== "all" ||
    searchQuery.length > 0 ||
    sortBy !== "newest";
</script>

{#if items.length === 0}
  <div class="text-center py-12">
    <div class="text-base-content/40 mb-2">
      <svg
        class="w-12 h-12 mx-auto opacity-50"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M12 8v.01M12 12v.01M12 16v.01"
        />
      </svg>
    </div>
    <p class="text-base-content/60 mb-2">No activities found</p>
    {#if hasAnyFilter}
      <button
        class="text-sm text-primary hover:underline"
        onclick={onclearfilters}
      >
        Clear filters to see all activities
      </button>
    {/if}
  </div>
{:else}
  <div class="space-y-3">
    {#each items as item, index (item.id)}
      <div
        role="button"
        tabindex="0"
        aria-label="View ticket {item.ticketId}"
        onclick={() => navigate(item.ticketId)}
        onkeydown={(e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            navigate(item.ticketId);
          }
        }}
        class="card bg-base-100 shadow-sm hover:shadow-md transition-all duration-200 border border-base-content/5 cursor-pointer hover:border-primary/20 hover:shadow-primary/5 active:scale-[0.995]"
      >
        <div class="card-body p-4">
          <div class="flex items-start justify-between gap-4">
            <!-- Icon -->
            <div class="flex-shrink-0 mt-0.5">
              <div
                class="w-10 h-10 rounded-lg {historyConfig[item.action]
                  .bgColor} flex items-center justify-center"
              >
                <Icon
                  icon={historyConfig[item.action].icon}
                  width="20"
                  height="20"
                  class={historyConfig[item.action].color}
                />
              </div>
            </div>

            <!-- Main Content -->
            <div class="flex-1 min-w-0">
              <!-- Badge and Ticket ID -->
              <div class="flex items-center gap-2 mb-2 flex-wrap">
                <span
                  class="badge badge-sm {historyConfig[item.action]
                    .color} {historyConfig[item.action]
                    .bgColor} border-0"
                >
                  {historyConfig[item.action].label}
                </span>
                <span class="text-xs font-medium text-base-content/70">
                  Ticket #{item.ticketId}
                </span>
              </div>

              <!-- Ticket Title -->
              <h3 class="font-semibold text-base text-base-content mb-2">
                {item.title}
              </h3>

              <!-- Activity Description -->
              <p class="text-sm text-base-content/70 mb-3">
                {item.description}
              </p>

              <!-- Admin Info and Timestamps -->
              <div class="flex items-center justify-between pt-3 border-t border-base-content/5">
                <div class="flex items-center gap-4 flex-wrap text-xs text-base-content/60">
                  <!-- Admin who made the change -->
                  {#if item.performedBy}
                    <div class="flex items-center gap-1">
                      <Icon icon="mdi:account" width="14" height="14" />
                      <span class="font-medium">
                        {item.performedBy}
                      </span>
                    </div>
                  {/if}

                  <!-- Time -->
                  <div class="flex items-center gap-1">
                    <Icon icon="mdi:clock-outline" width="14" height="14" />
                    <span>{formatRelativeTime(item.timestamp, item.date)}</span>
                  </div>

                  <!-- Date -->
                  <div class="flex items-center gap-1">
                    <Icon icon="mdi:calendar-outline" width="14" height="14" />
                    <span>{item.date}</span>
                  </div>
                </div>

                <!-- Category Badge -->
                {#if item.category}
                  <div class="flex-shrink-0">
                    <span class="badge badge-outline badge-sm">
                      {item.category}
                    </span>
                  </div>
                {/if}
              </div>
            </div>
          </div>
        </div>
      </div>
    {/each}
  </div>
{/if}

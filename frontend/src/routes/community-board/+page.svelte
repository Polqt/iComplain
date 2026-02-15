<script lang="ts">
  import StudentLayout from "../../components/layout/StudentLayout.svelte";
  import { ticketsStore } from "../../stores/tickets.store.ts";
  import { onMount } from "svelte";
  import type { TicketStatus } from "../../types/tickets.ts";
  import {
    columns,
    getPriorityKey,
    priorityConfig,
    priorityDot,
  } from "../../utils/ticketConfig.ts";
  import TicketFilters from "../../components/ui/tickets/TicketFilters.svelte";
  import Icon from "@iconify/svelte";
  import { formatDate } from "../../utils/date.ts";

  $: ({ tickets, isLoading, error } = $ticketsStore);

  onMount(async () => {
    await ticketsStore.loadCommunityTickets();
  });

  let search = "";
  let activeStatus: TicketStatus | "all" = "all";
  let priorityFilter = "all";

  $: filtered = tickets.filter((t) => {
    const q = search.trim().toLowerCase();
    const matchSearch =
      !q ||
      t.title.toLowerCase().includes(q) ||
      t.building.toLowerCase().includes(q) ||
      t.room_name.toLowerCase().includes(q) ||
      t.category.name.toLowerCase().includes(q) ||
      t.ticket_number.toLowerCase().includes(q);

    const matchStatus = activeStatus === "all" || t.status === activeStatus;
    const matchPriority =
      priorityFilter === "all" || getPriorityKey(t.priority) === priorityFilter;
    return matchSearch && matchStatus && matchPriority;
  });

  $: statusCounts = {
    all: filtered.length,
    pending: filtered.filter((t) => t.status === "pending").length,
    in_progress: filtered.filter((t) => t.status === "in_progress").length,
    resolved: filtered.filter((t) => t.status === "resolved").length,
    closed: filtered.filter((t) => t.status === "closed").length,
  };

  function getColumnTickets(status: TicketStatus) {
    return filtered.filter((t) => t.status === status);
  }
</script>

<StudentLayout>
  <div class="flex flex-col h-[calc(100vh-8rem)]">
    <div class="shrink-0 mb-6">
      <h1 class="text-2xl font-black text-base-content mb-1">
        Community Board
      </h1>
      <p class="text-sm text-base-content/60">
        Campus-wide issues — see what's reported and being fixed
      </p>
    </div>

    <div class="mb-4 shrink-0">
      <TicketFilters
        {search}
        {activeStatus}
        {priorityFilter}
        {statusCounts}
        totalCount={filtered.length}
        onSearchChange={(v) => (search = v)}
        onStatusChange={(v) => (activeStatus = v)}
        onPriorityChange={(v) => (priorityFilter = v)}
        onClear={() => {
          search = "";
          activeStatus = "all";
          priorityFilter = "all";
        }}
      />
    </div>

    {#if isLoading}
      <div class="grid grid-cols-4 gap-3 flex-1">
        {#each columns as _, i}
          <div class="flex flex-col gap-2">
            <div class="skeleton h-9 w-full rounded-xl"></div>
            {#each Array(i === 0 ? 3 : i === 1 ? 2 : 1) as _}
              <div class="skeleton h-32 w-full rounded-xl"></div>
            {/each}
          </div>
        {/each}
      </div>
    {:else if error}
      <div class="flex flex-col items-center justify-center flex-1 gap-3">
        <div
          class="w-12 h-12 rounded-2xl bg-error/8 flex items-center justify-center"
        >
          <Icon
            icon="mdi:alert-circle-outline"
            width="22"
            height="22"
            class="text-error/50"
          />
        </div>
        <div class="text-sm text-base-content/50">{error}</div>
        <button
          class="btn btn-ghost btn-xs rounded-lg gap-1.5"
          onclick={() => ticketsStore.loadCommunityTickets()}
        >
          <Icon icon="mdi:refresh" width="13" height="13" />
        </button>
      </div>
    {:else}
      <div class="grid grid-cols-4 gap-3 flex-1 min-h-0">
        {#each columns as col}
          {@const colTickets = getColumnTickets(col.id)}

          <div class="flex flex-col min-h-0 gap-2">
            <div
              class="flex items-center justify-between px-3 py-2 rounded-xl
                     border {col.headerTint} shrink-0"
            >
              <div class="flex items-center gap-2">
                <span class="w-2 h-2 rounded-full shrink-0 {col.dot}"></span>
                <span
                  class="text-[10px] font-bold uppercase tracking-widest text-base-content/60"
                >
                  {col.label}
                </span>
              </div>
              <span
                class="text-[10px] font-semibold rounded-full px-1.5 py-0.5
                       min-w-5 text-center {col.countBg}"
              >
                {colTickets.length}
              </span>
            </div>

            <div class="flex flex-col gap-1.5 overflow-y-auto flex-1 min-h-0">
              {#each colTickets as ticket (ticket.id)}
                {@const pKey = getPriorityKey(ticket.priority)}

                <div
                  class="group bg-base-100 rounded-xl border border-base-content/7
                         hover:border-base-content/16
                         hover:shadow-[0_2px_16px_rgba(0,0,0,0.07)]
                         transition-all duration-150"
                >
                  <div class="p-3.5">
                    <div class="flex items-center justify-between gap-2 mb-2">
                      <div class="flex items-center gap-1.5 min-w-0">
                        <span
                          class="w-2 h-2 rounded-full shrink-0
                                 {priorityDot[pKey] ?? 'bg-base-content/15'}"
                          title="{priorityConfig[pKey]?.label} priority"
                        ></span>
                        <span
                          class="text-[10px] text-base-content/45 bg-base-200
                                 rounded-full px-2 py-0.5 truncate max-w-32 font-medium"
                        >
                          {ticket.category.name}
                        </span>
                      </div>
                      <span
                        class="text-[10px] font-mono text-base-content/20 shrink-0"
                      >
                        {ticket.ticket_number}
                      </span>
                    </div>

                    <p
                      class="text-[13px] font-semibold text-base-content
                               leading-snug line-clamp-2 mb-1.5"
                    >
                      {ticket.title}
                    </p>

                    <p
                      class="text-[11px] text-base-content/40 leading-relaxed
                               line-clamp-2 mb-2.5"
                    >
                      {ticket.description}
                    </p>

                    <div class="flex items-center gap-1 mb-3">
                      <Icon
                        icon="mdi:map-marker-outline"
                        width="10"
                        height="10"
                        class="text-base-content/25 shrink-0"
                      />
                      <span class="text-[10px] text-base-content/35 truncate">
                        {ticket.building} · {ticket.room_name}
                      </span>
                    </div>

                    <div
                      class="flex items-center justify-between gap-2
                             pt-2.5 border-t border-base-content/6"
                    >
                      <div class="flex items-center gap-1.5 min-w-0">
                        <div
                          class="w-5 h-5 rounded-full bg-primary/10 shrink-0
                                 flex items-center justify-center
                                 text-[9px] font-bold text-primary uppercase"
                        >
                          {ticket.student.email[0]}
                        </div>
                        <span
                          class="text-[10px] text-base-content/35 truncate max-w-20"
                        >
                          {ticket.student.email.split("@")[0]}
                        </span>
                      </div>

                      <div class="flex items-center gap-2 shrink-0">
                        <span class="text-[10px] text-base-content/25">
                          {formatDate(ticket.created_at)}
                        </span>
                        <button
                          class="flex items-center gap-0.5 text-base-content/25
                                 hover:text-primary transition-colors"
                          title="Comments — coming soon"
                        >
                          <Icon
                            icon="mdi:comment-outline"
                            width="12"
                            height="12"
                          />
                          <span class="text-[10px] font-mono">0</span>
                        </button>
                        <button
                          class="text-base-content/25 hover:text-primary transition-colors"
                          title="Support — coming soon"
                        >
                          <Icon
                            icon="mdi:arrow-up-bold-outline"
                            width="12"
                            height="12"
                          />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              {/each}

              {#if colTickets.length === 0}
                <div
                  class="flex flex-col items-center justify-center gap-2 flex-1
                         rounded-xl min-h-20 border-2 border-dashed border-base-content/7"
                >
                  <Icon
                    icon={col.icon}
                    width="18"
                    height="18"
                    class="text-base-content/20"
                  />
                  <p class="text-[10px] text-base-content/25 font-medium">
                    {col.emptyText}
                  </p>
                </div>
              {/if}
            </div>
          </div>
        {/each}
      </div>
    {/if}
  </div>
</StudentLayout>

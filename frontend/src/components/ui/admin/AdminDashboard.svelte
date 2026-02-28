<script lang="ts">
  import Icon from "@iconify/svelte";
  import { onMount } from "svelte";
  import AdminLayout from "../../layout/AdminLayout.svelte";
  import TicketBoard from "../tickets/TicketBoard.svelte";
  import type { DashboardStats } from "../../../types/dashboard.ts";
  import { getDashboardStats } from "../../../lib/api/ticket.ts";

  let stats: DashboardStats | null = null;
  let isLoading = true;
  let error: string | null = null;

  onMount(async () => {
    try {
      stats = await getDashboardStats();
    } catch (err) {
      error = err instanceof Error ? err.message : "Failed to load stats";
      console.error("Dashboard stats error:", err);
    } finally {
      isLoading = false;
    }
  });

  $: metrics = stats?.metrics ?? [];
  $: volume = stats?.volume ?? [];
</script>

<AdminLayout>
  <div class="flex flex-col h-[calc(100vh-8rem)]">
    <div
      class="flex flex-wrap items-center justify-between gap-4 mb-6 shrink-0"
    >
      <div class="flex items-center gap-2">
        <div
          class="w-9 h-9 rounded-xl bg-primary/10 flex items-center justify-center"
        >
          <Icon icon="mdi:view-dashboard-outline" width="20" height="20" />
        </div>
        <div>
          <h1 class="text-2xl font-black text-base-content">
            Dashboard Overview
          </h1>
          <p class="text-sm text-base-content/60">
            Track performance, workload, and support activity
          </p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <button class="btn btn-sm btn-primary gap-2">
          <Icon icon="mdi:chart-bar" width="18" height="18" />
          Generate Report
        </button>
        <button class="btn btn-sm btn-outline gap-2">
          <Icon icon="mdi:download" width="18" height="18" />
          Export CSV
        </button>
      </div>
    </div>

    <div class="flex-1 overflow-y-auto pr-2 space-y-6 min-h-0">
      {#if isLoading}
        <div class="flex items-center justify-center py-12">
          <span class="loading loading-spinner loading-lg"></span>
        </div>
      {:else if error}
        <div class="alert alert-error">
          <Icon icon="mdi:alert-circle" width="20" height="20" />
          <span>{error}</span>
          <button
            class="btn btn-sm btn-ghost"
            onclick={() => window.location.reload()}
          >
            Retry
          </button>
        </div>
      {:else}
        <section class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
          {#each metrics as metric}
            <div
              class="card bg-base-100 dark:bg-base-100 shadow-sm border border-base-content/5 rounded-lg"
            >
              <div class="card-body p-4">
                <div class="flex items-center justify-between mb-3">
                  <p class="text-xs text-base-content/60">{metric.title}</p>
                  <button class="btn btn-ghost btn-xs btn-circle">
                    <Icon icon="mdi:dots-horizontal" width="16" height="16" />
                  </button>
                </div>
                <div class="flex items-end justify-between">
                  <div>
                    <p class="text-2xl font-bold leading-none">
                      {metric.value}
                    </p>
                    <p class="text-xs text-base-content/50 mt-1">
                      {metric.subtitle}
                    </p>
                  </div>
                  <span
                    class="text-xs font-semibold {metric.trend === 'success'
                      ? 'text-success'
                      : 'text-error'}"
                  >
                    {metric.change}
                  </span>
                </div>
              </div>
            </div>
          {/each}
        </section>

        <section class="grid grid-cols-1 xl:grid-cols-3 gap-4">
          <div
            class="card bg-base-100 dark:bg-base-100 shadow-sm border border-base-content/5 rounded-lg xl:col-span-2"
          >
            <div class="card-body p-4">
              <div class="flex items-center justify-between mb-4">
                <div>
                  <h2 class="text-base font-semibold">Ticket Volume Tracker</h2>
                  <p class="text-xs text-base-content/60">
                    Track daily ticket flow and monitor workload trends
                  </p>
                </div>
                <select class="select select-bordered select-sm">
                  <option>Weekly</option>
                  <option>Monthly</option>
                  <option>Quarterly</option>
                </select>
              </div>

              {#if volume.length > 0}
                <div class="flex items-end justify-between gap-3 h-40">
                  {#each volume as bar, i}
                    {@const height = Math.max(bar.value * 3, 10)}
                    <div class="flex flex-col items-center gap-2 flex-1">
                      <div
                        class="w-8 rounded-lg bg-primary/20 relative overflow-hidden transition-all duration-300"
                        class:h-2={height === 10}
                        class:h-4={height > 10 && height <= 20}
                        class:h-8={height > 20 && height <= 30}
                        class:h-12={height > 30 && height <= 40}
                        class:h-16={height > 40 && height <= 50}
                        class:h-20={height > 50 && height <= 60}
                        class:h-24={height > 60 && height <= 80}
                        class:h-32={height > 80 && height <= 100}
                        class:h-40={height > 100}
                      >
                        <div
                          class="absolute bottom-0 inset-x-0 h-full bg-primary/60"
                        ></div>
                      </div>
                      <span class="text-xs text-base-content/60">{bar.day}</span
                      >
                    </div>
                  {/each}
                </div>

                <div class="mt-4 text-sm text-base-content/60">
                  Last 7 days ticket volume
                </div>
              {:else}
                <div
                  class="flex items-center justify-center h-40 text-base-content/40"
                >
                  No volume data available
                </div>
              {/if}
            </div>
          </div>

          <!-- Recent Activity -->
          <div
            class="card bg-base-100 dark:bg-base-100 shadow-sm border border-base-content/5 rounded-lg"
          >
            <div class="card-body p-4">
              <div class="flex items-center justify-between mb-3">
                <div>
                  <h2 class="text-base font-semibold">
                    Recent Support Activity
                  </h2>
                  <p class="text-xs text-base-content/60">
                    Latest updates from the support team
                  </p>
                </div>
                <a href="/admin/tickets" class="text-xs text-primary">
                  See all
                </a>
              </div>
            </div>
          </div>
        </section>

        <section class="h-150 min-h-0">
          <TicketBoard />
        </section>
      {/if}
    </div>
  </div>
</AdminLayout>

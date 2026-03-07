<script lang="ts">
import Icon from "@iconify/svelte";
import { onMount } from "svelte";
import AdminLayout from "../../layout/AdminLayout.svelte";
import TicketBoard from "../tickets/TicketBoard.svelte";
import ActivityFeed from "./ActivityFeed.svelte";
import type {
	DashboardStats,
	DashboardMetric,
} from "../../../types/dashboard.ts";
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
$: pendingMetric = metrics[0]; // Now first due to backend reorder
$: secondaryMetrics = metrics.slice(1);

function getTrendIcon(metric: DashboardMetric) {
	if (metric.is_increasing) return "mdi:trending-up";
	return "mdi:trending-down";
}

function getTrendColor(metric: DashboardMetric) {
	if (metric.is_critical) {
		return metric.is_increasing ? "text-error" : "text-success";
	}
	return metric.trend === "success" ? "text-success" : "text-error";
}
</script>

<AdminLayout>
  <div class="flex flex-col h-[calc(100vh-8rem)]">
    <div class="flex flex-wrap items-center justify-between gap-4 mb-8 shrink-0">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-2xl bg-linear-to-br from-primary/20 to-primary/5 flex items-center justify-center border border-primary/10">
          <Icon icon="mdi:view-dashboard-outline" width="24" height="24" class="text-primary" />
        </div>
        <div>
          <h1 class="text-3xl font-black text-base-content">Dashboard</h1>
          <p class="text-sm text-base-content/50 font-medium">
            Real-time facility management overview
          </p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <button class="btn btn-sm btn-primary gap-2 font-semibold shadow-lg hover:shadow-xl transition-shadow">
          <Icon icon="mdi:chart-bar" width="18" height="18" />
          Generate Report
        </button>
        <button class="btn btn-sm btn-outline gap-2">
          <Icon icon="mdi:download" width="18" height="18" />
          Export CSV
        </button>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="flex-1 overflow-y-auto pr-2 space-y-8 min-h-0">
      {#if isLoading}
        <div class="flex items-center justify-center py-16">
          <span class="loading loading-spinner loading-lg text-primary"></span>
        </div>
      {:else if error}
        <div class="alert alert-error shadow-lg">
          <Icon icon="mdi:alert-circle" width="20" height="20" />
          <span class="font-semibold">{error}</span>
          <button
            class="btn btn-sm btn-ghost"
            onclick={() => window.location.reload()}
          >
            Retry
          </button>
        </div>
      {:else}
        {#if pendingMetric}
          <section>
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
              <div class="lg:col-span-2 bg-linear-to-br from-base-100 to-base-100/50 rounded-2xl border {pendingMetric.is_critical ? 'border-error/20 shadow-lg shadow-error/10' : 'border-base-content/5 shadow-md'} overflow-hidden hover:shadow-xl transition-all duration-300">
                <div class="p-8 flex flex-col h-full">
                  <div class="flex items-start justify-between mb-6">
                    <div class="flex-1">
                      <p class="text-sm font-semibold text-base-content/60 uppercase tracking-wider mb-2">
                        {pendingMetric.title}
                      </p>
                      <h2 class="text-5xl xl:text-6xl font-black text-base-content leading-tight mb-4">
                        {pendingMetric.value}
                      </h2>
                      <p class="text-sm text-base-content/50 font-medium">
                        {pendingMetric.subtitle}
                      </p>
                    </div>
                  </div>

                  <!-- Trend Indicator -->
                  <div class="flex items-center gap-3 mt-auto pt-6 border-t border-base-content/5">
                    <div class="flex items-center gap-2 px-3 py-2 rounded-lg {pendingMetric.is_critical && pendingMetric.is_increasing ? 'bg-error/10' : 'bg-success/10'}">
                      <Icon 
                        icon={getTrendIcon(pendingMetric)} 
                        width="18" 
                        height="18" 
                        class="{getTrendColor(pendingMetric)}"
                      />
                      <span class="text-sm font-bold {getTrendColor(pendingMetric)}">
                        {pendingMetric.change}
                      </span>
                    </div>
                    <span class="text-xs text-base-content/40">vs last month</span>
                  </div>
                </div>
              </div>

              <!-- Secondary Metrics Grid in Sidebar -->
              <div class="flex flex-col gap-4">
                {#each secondaryMetrics as metric}
                  <div class="bg-base-100/50 border border-base-content/5 rounded-xl p-5 hover:border-base-content/10 hover:shadow-md transition-all duration-200">
                    <p class="text-xs font-semibold text-base-content/60 uppercase tracking-wide mb-3">
                      {metric.title}
                    </p>
                    <div class="flex items-end justify-between gap-3">
                      <div>
                        <p class="text-3xl font-black text-base-content leading-none">
                          {metric.value}
                        </p>
                        <p class="text-xs text-base-content/40 mt-1 font-medium">
                          {metric.subtitle}
                        </p>
                      </div>
                      <div class="inline-flex items-center gap-1 px-2 py-1 rounded-lg {metric.trend === 'success' ? 'bg-success/10' : 'bg-error/10'}">
                        <Icon 
                          icon={getTrendIcon(metric)} 
                          width="14" 
                          height="14" 
                          class="shrink-0 {getTrendColor(metric)}"
                        />
                        <span class="text-xs font-bold {getTrendColor(metric)}">
                          {metric.change}
                        </span>
                      </div>
                    </div>
                  </div>
                {/each}
              </div>
            </div>
          </section>
        {/if}

        <section class="grid grid-cols-1 xl:grid-cols-3 gap-6">
          <div class="xl:col-span-2 bg-base-100/50 border border-base-content/5 rounded-2xl shadow-md hover:shadow-lg transition-all duration-200 overflow-hidden">
            <div class="p-6">
              <div class="flex items-center justify-between mb-6">
                <div>
                  <h3 class="text-lg font-bold text-base-content mb-1">Ticket Volume</h3>
                  <p class="text-xs text-base-content/50 font-medium">
                    Daily ticket submissions - Last 7 days
                  </p>
                </div>
                <select class="select select-bordered select-sm text-xs">
                  <option selected>Weekly</option>
                  <option>Monthly</option>
                  <option>Quarterly</option>
                </select>
              </div>

              {#if volume.length > 0}
                <div class="flex items-end justify-between gap-2 h-48 mb-6">
                  {#each volume as bar}
                    {@const maxVolume = Math.max(...volume.map(v => v.value), 1)}
                    {@const heightPercent = (bar.value / maxVolume) * 100}
                    <div class="flex flex-col items-center gap-2 flex-1">
                      <div class="w-full relative h-32 rounded-t-lg overflow-hidden bg-base-200/30 border border-base-content/5 border-b-0">
                        <div
                          class="absolute bottom-0 inset-x-0 bg-linear-to-t from-primary/80 to-primary/40 transition-all duration-300"
                          style="height: {heightPercent}%"
                        ></div>
                      </div>
                      <div class="flex flex-col items-center gap-1">
                        <span class="text-xs font-bold text-base-content">{bar.value}</span>
                        <span class="text-xs text-base-content/40 font-medium">{bar.day}</span>
                      </div>
                    </div>
                  {/each}
                </div>

                <div class="flex items-center justify-between pt-4 border-t border-base-content/5">
                  <span class="text-xs text-base-content/50 font-medium">
                    Peak: {Math.max(...volume.map(v => v.value))} tickets
                  </span>
                  <span class="text-xs text-base-content/50 font-medium">
                    Avg: {Math.round(volume.reduce((a, b) => a + b.value, 0) / volume.length)} tickets/day
                  </span>
                </div>
              {:else}
                <div class="flex items-center justify-center h-40 text-base-content/30">
                  <p class="text-sm font-medium">No volume data available</p>
                </div>
              {/if}
            </div>
          </div>

          <div class="bg-base-100/50 border border-base-content/5 rounded-2xl shadow-md hover:shadow-lg transition-all duration-200">
            <ActivityFeed />
          </div>
        </section>

        <section class="mt-2 px-4 pt-6">
          <TicketBoard />
        </section>
      {/if}
    </div>
  </div>
</AdminLayout>

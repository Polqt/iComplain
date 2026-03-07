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
import {
	getDashboardStats,
	exportDashboardCsv,
} from "../../../lib/api/ticket.ts";

let stats: DashboardStats | null = null;
let isLoading = true;
let error: string | null = null;
let actionError: string | null = null;
let isExportingCsv = false;
let isExportModalOpen = false;
const today = new Date();
const defaultStart = new Date();
defaultStart.setDate(today.getDate() - 29);
const formatDateInput = (value: Date) => value.toISOString().slice(0, 10);
const isoToUsDate = (isoDate: string) => {
	const [year, month, day] = isoDate.split("-");
	return `${month}/${day}/${year}`;
};
const usDateToIso = (usDate: string): string | null => {
	const match = usDate.trim().match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/);
	if (!match) return null;

	const month = Number(match[1]);
	const day = Number(match[2]);
	const year = Number(match[3]);

	if (month < 1 || month > 12 || day < 1 || year < 1000) return null;
	const parsed = new Date(year, month - 1, day);
	if (
		parsed.getFullYear() !== year ||
		parsed.getMonth() !== month - 1 ||
		parsed.getDate() !== day
	) {
		return null;
	}

	return `${year.toString().padStart(4, "0")}-${month.toString().padStart(2, "0")}-${day.toString().padStart(2, "0")}`;
};
let exportStartDate = formatDateInput(defaultStart);
let exportEndDate = formatDateInput(today);
let exportStartDisplay = isoToUsDate(exportStartDate);
let exportEndDisplay = isoToUsDate(exportEndDate);

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

function openExportModal() {
	actionError = null;
	exportStartDisplay = isoToUsDate(exportStartDate);
	exportEndDisplay = isoToUsDate(exportEndDate);
	isExportModalOpen = true;
}

function closeExportModal() {
	if (isExportingCsv) return;
	isExportModalOpen = false;
}

async function handleExportCsv() {
	if (isExportingCsv) return;
	const parsedStart = usDateToIso(exportStartDisplay);
	const parsedEnd = usDateToIso(exportEndDisplay);

	if (!parsedStart || !parsedEnd) {
		actionError = "Use MM/DD/YYYY format (example: 03/07/2026).";
		return;
	}

	if (parsedStart > parsedEnd) {
		actionError = "Start date cannot be later than end date.";
		return;
	}

	exportStartDate = parsedStart;
	exportEndDate = parsedEnd;
	exportStartDisplay = isoToUsDate(parsedStart);
	exportEndDisplay = isoToUsDate(parsedEnd);

	actionError = null;
	isExportingCsv = true;
	try {
		await exportDashboardCsv({
			startDate: parsedStart,
			endDate: parsedEnd,
		});
		isExportModalOpen = false;
	} catch (err) {
		actionError = err instanceof Error ? err.message : "Failed to export CSV";
		console.error("Export CSV error:", err);
	} finally {
		isExportingCsv = false;
	}
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
        <button
          class="btn btn-sm btn-outline gap-2"
          onclick={openExportModal}
        >
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

  {#if isExportModalOpen}
    <div class="modal modal-open">
      <div class="modal-box p-0 max-w-lg border border-base-content/10 shadow-2xl">
        <div class="flex items-center justify-between px-6 py-4 bg-primary text-primary-content">
          <h3 class="text-xl font-bold">Download Data</h3>
          <button
            type="button"
            class="btn btn-sm btn-circle btn-ghost text-primary-content"
            onclick={closeExportModal}
            disabled={isExportingCsv}
            aria-label="Close export modal"
          >
            <Icon icon="mdi:close" width="20" height="20" />
          </button>
        </div>

        <div class="px-6 py-5 space-y-4 bg-base-100">
          <div>
            <p class="text-base font-semibold text-base-content mb-3">Date Range</p>
            <div class="flex flex-wrap items-center gap-3">
              <label class="input input-bordered flex items-center gap-2">
                <span class="text-sm text-base-content/60">From</span>
                <input
                  type="text"
                  inputmode="numeric"
                  placeholder="MM/DD/YYYY"
                  bind:value={exportStartDisplay}
                />
              </label>
              <span class="text-base-content/50 font-medium">to</span>
              <label class="input input-bordered flex items-center gap-2">
                <span class="text-sm text-base-content/60">To</span>
                <input
                  type="text"
                  inputmode="numeric"
                  placeholder="MM/DD/YYYY"
                  bind:value={exportEndDisplay}
                />
              </label>
            </div>
            <p class="text-xs text-base-content/50 mt-2">Format: MM/DD/YYYY</p>
          </div>

          {#if actionError}
            <div class="alert alert-warning shadow-sm">
              <Icon icon="mdi:alert" width="18" height="18" />
              <span class="text-sm">{actionError}</span>
            </div>
          {/if}
        </div>

        <div class="px-6 py-4 border-t border-base-content/10 bg-base-100 flex justify-end gap-2">
          <button
            type="button"
            class="btn btn-ghost"
            onclick={closeExportModal}
            disabled={isExportingCsv}
          >
            Cancel
          </button>
          <button
            type="button"
            class="btn btn-primary gap-2"
            onclick={handleExportCsv}
            disabled={isExportingCsv}
          >
            <Icon icon="mdi:download" width="18" height="18" />
            {isExportingCsv ? "Exporting..." : "Download CSV"}
          </button>
        </div>
      </div>
      <button
        class="modal-backdrop"
        aria-label="Close export modal backdrop"
        onclick={closeExportModal}
      ></button>
    </div>
  {/if}
</AdminLayout>

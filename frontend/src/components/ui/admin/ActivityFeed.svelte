<script lang="ts">
import Icon from "@iconify/svelte";
import { onMount } from "svelte";
import { goto } from "$app/navigation";
import { getActivityLogs } from "../../../lib/api/ticket.ts";
import type { ActivityLog } from "../../../lib/api/ticket.ts";

let activities: ActivityLog[] = [];
let isLoading = true;
let error: string | null = null;

onMount(async () => {
	try {
		const response = await getActivityLogs(10); // Load last 10 activities
		activities = response.items;
		error = null;
	} catch (err) {
		error = err instanceof Error ? err.message : "Failed to load activities";
		console.error("Activity feed error:", err);
	} finally {
		isLoading = false;
	}
});

function getActionIcon(action: ActivityLog["action"]): string {
	switch (action) {
		case "commented":
			return "mdi:comment-multiple";
		case "status_changed":
			return "mdi:swap-horizontal";
		case "priority_changed":
			return "mdi:alert-octagon";
		case "resolved":
			return "mdi:check-circle";
		case "reopened":
			return "mdi:sync";
		case "created":
			return "mdi:plus-circle";
		case "assigned":
			return "mdi:account-check";
		default:
			return "mdi:information";
	}
}

function getActionColor(action: ActivityLog["action"]): string {
	switch (action) {
		case "resolved":
			return "text-success";
		case "reopened":
			return "text-error";
		case "priority_changed":
			return "text-warning";
		case "created":
			return "text-info";
		default:
			return "text-primary";
	}
}

function getInitials(name: string | null | undefined): string {
	if (!name) return "?";
	return name
		.split(" ")
		.map((n) => n[0])
		.join("")
		.toUpperCase()
		.slice(0, 2);
}

function formatTime(dateString: string): string {
	const date = new Date(dateString);
	const now = new Date();
	const diffMs = now.getTime() - date.getTime();
	const diffMins = Math.floor(diffMs / 60000);
	const diffHours = Math.floor(diffMins / 60);
	const diffDays = Math.floor(diffHours / 24);

	if (diffMins < 1) return "now";
	if (diffMins < 60) return `${diffMins}m ago`;
	if (diffHours < 24) return `${diffHours}h ago`;
	if (diffDays < 7) return `${diffDays}d ago`;

	return date.toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

function isRecentAction(created_at: string): boolean {
	const date = new Date(created_at);
	const now = new Date();
	const diffHours = (now.getTime() - date.getTime()) / (1000 * 60 * 60);
	return diffHours < 24; // Emphasis if within 24 hours
}

function navigateToHistory() {
	goto("/history");
}
</script>

<div class="flex flex-col h-full">
  <!-- Header -->
  <div class="px-6 py-4 border-b border-base-content/5">
    <div class="flex items-center justify-between mb-1">
      <h3 class="text-lg font-bold text-base-content">Activity Feed</h3>
      <a href="/history" class="text-xs font-semibold text-primary hover:text-primary/80">
        View all
      </a>
    </div>
    <p class="text-xs text-base-content/50 font-medium">
      Latest support team updates
    </p>
  </div>

  <!-- Activity List -->
  <div class="flex-1 overflow-y-auto min-h-0">
    {#if isLoading}
      <div class="flex items-center justify-center h-40">
        <span class="loading loading-spinner loading-sm text-primary"></span>
      </div>
    {:else if error}
      <div class="flex flex-col items-center justify-center h-40 px-4 gap-2">
        <Icon icon="mdi:alert-circle" width="32" height="32" class="text-error/50" />
        <p class="text-xs text-center text-error/70">{error}</p>
        <button 
          onclick={() => window.location.reload()}
          class="text-xs text-primary hover:underline"
        >
          Retry
        </button>
      </div>
    {:else if activities.length === 0}
      <div class="flex flex-col items-center justify-center h-40 text-center px-4">
        <Icon icon="mdi:history" width="32" height="32" class="text-base-content/20 mb-2" />
        <p class="text-xs text-base-content/40 font-medium">No recent activity</p>
      </div>
    {:else}
      <div class="space-y-3 p-6">
        {#each activities as activity (activity.id)}
          <button
            type="button"
            onclick={navigateToHistory}
            class="w-full text-left flex gap-3 pb-3 border-b border-base-content/5 last:border-b-0 last:pb-0 rounded-lg transition-colors hover:bg-base-200/50 {isRecentAction(activity.created_at)
              ? 'bg-error/5 p-3 rounded-lg'
              : ''}"
          >
            <!-- Avatar -->
            <div class="w-8 h-8 rounded-full bg-gradient-to-br from-primary/60 to-primary/40 flex items-center justify-center text-white text-xs font-bold flex-shrink-0">
              {getInitials(activity.performed_by?.name)}
            </div>

            <!-- Content -->
            <div class="flex-1 min-w-0">
              <div class="flex items-start gap-2 mb-0.5">
                <div class="flex-1 min-w-0">
                  <p class="text-xs font-semibold text-base-content">
                    {activity.performed_by?.name || activity.performed_by?.email || "System"}
                  </p>
                  <p class="text-xs text-base-content/60">
                    <span class="font-medium text-base-content/70">{activity.ticket_number}</span>
                    <span class="text-base-content/60"> – </span>
                    <span>{activity.ticket_title}</span>
                  </p>
                </div>
                <Icon
                  icon={getActionIcon(activity.action)}
                  width="14"
                  height="14"
                  class="flex-shrink-0 mt-0.5 {getActionColor(activity.action)}"
                />
              </div>
              <p class="text-xs text-base-content/50">
                {activity.description}
              </p>
              <p class="text-xs text-base-content/30 mt-1">
                {formatTime(activity.created_at)}
              </p>
            </div>
          </button>
        {/each}
      </div>
    {/if}
  </div>
</div>

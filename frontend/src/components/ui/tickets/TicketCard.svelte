<script lang="ts">
  import Icon from "@iconify/svelte";
  import type { Ticket } from "../../../types/tickets.ts";
  import {
    getPriorityKey,
    priorityAccent,
    priorityConfig,
    priorityIcons,
    statusConfig,
  } from "../../../utils/ticketConfig.ts";
  import { goto } from "$app/navigation";

  export let report: Ticket;
  export let onEdit: (report: Ticket) => void = () => {};
  export let onDelete: (report: Ticket) => void = () => {};

  $: pKey = getPriorityKey(report.priority);
  $: pIcon = priorityIcons[pKey] ?? "mdi:minus";
  $: pAccent = priorityAccent[pKey] ?? "border-l-info";

  function navigate() {
    goto(`/student/tickets/${report.id}`);
  }
</script>

<div
  class="group relative w-full bg-base-100 rounded-xl
         border border-base-content/8 border-l-[3px] {pAccent}
         hover:border-base-content/20 hover:shadow-md
         transition-all duration-200 cursor-pointer"
  role="button"
  tabindex="0"
  aria-label={`Open ticket ${report.title}`}
  onclick={navigate}
  onkeydown={(e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      navigate();
    }
  }}
>
  <div class="p-4">
    <div class="flex items-center justify-between mb-3">
      <div class="flex items-center gap-2">
        <span
          class="badge badge-xs {statusConfig[report.status]
            .color} font-semibold"
        >
          {statusConfig[report.status].label}
        </span>
        <span class="text-[10px] font-mono text-base-content/25 tracking-wider">
          {report.ticket_number}
        </span>
      </div>

      <div
        class="opacity-0 group-hover:opacity-100 transition-opacity duration-150 shrink-0"
        onclick={(e) => e.stopPropagation()}
        role="none"
      >
        <div class="dropdown dropdown-end">
          <button
            type="button"
            tabindex="0"
            class="btn btn-ghost btn-xs btn-circle text-base-content/40 hover:text-base-content"
            aria-label="Card actions"
          >
            <Icon icon="mdi:dots-horizontal" width="15" height="15" />
          </button>
          <ul
            tabindex="-1"
            role="menu"
            class="dropdown-content menu bg-base-100 border border-base-content/10
                   rounded-xl shadow-xl z-50 w-40 p-1.5 text-sm"
          >
            {#if report.status === "pending"}
              <li>
                <button
                  type="button"
                  role="menuitem"
                  class="flex items-center gap-2 rounded-lg px-3 py-2 hover:bg-base-200"
                  onclick={(e) => {
                    e.stopPropagation();
                    onEdit(report);
                  }}
                >
                  <Icon icon="mdi:pencil-outline" width="14" height="14" /> Edit
                </button>
              </li>
              <li>
                <button
                  type="button"
                  role="menuitem"
                  class="flex items-center gap-2 rounded-lg px-3 py-2 text-error hover:bg-error/10"
                  onclick={(e) => {
                    e.stopPropagation();
                    onDelete(report);
                  }}
                >
                  <Icon icon="mdi:delete-outline" width="14" height="14" /> Delete
                </button>
              </li>
            {:else}
              <li>
                <button
                  type="button"
                  role="menuitem"
                  class="flex items-center gap-2 rounded-lg px-3 py-2 hover:bg-base-200 btn-disabled cursor-not-allowed"
                  onclick={(e) => {
                    e.stopPropagation();
                    onEdit(report);
                  }}
                >
                  <Icon icon="mdi:pencil-outline" width="14" height="14" /> Edit
                </button>
              </li>
              <li>
                <button
                  type="button"
                  role="menuitem"
                  class="flex items-center gap-2 rounded-lg px-3 py-2 text-error hover:bg-error/10 btn-disabled cursor-not-allowed"
                  onclick={(e) => {
                    e.stopPropagation();
                    onDelete(report);
                  }}
                >
                  <Icon icon="mdi:delete-outline" width="14" height="14" /> Delete
                </button>
              </li>
            {/if}
          </ul>
        </div>
      </div>
    </div>

    <h3
      class="font-semibold text-sm text-base-content leading-snug line-clamp-2 mb-1.5"
    >
      {report.title}
    </h3>

    <p class="text-xs text-base-content/45 line-clamp-2 leading-relaxed mb-3">
      {report.description}
    </p>

    <div class="flex items-center gap-1.5 mb-3.5">
      <Icon
        icon="mdi:map-marker-outline"
        width="11"
        height="11"
        class="text-base-content/30 shrink-0"
      />
      <span class="text-[11px] text-base-content/40 truncate">
        {report.building} · {report.room_name}
      </span>
    </div>

    <div class="border-t border-base-content/6 mb-3"></div>

    <div class="flex items-center justify-between gap-2">
      <span
        class="inline-flex items-center gap-1 text-[11px]
                   bg-base-200 text-base-content/50 rounded-full px-2.5 py-0.5
                   max-w-[60%] truncate font-medium"
      >
        {report.category.name}
      </span>

      <span
        class="inline-flex items-center gap-1 badge badge-sm
                   {priorityConfig[pKey].color} font-semibold shrink-0"
      >
        <Icon icon={pIcon} width="11" height="11" />
        {priorityConfig[pKey].label}
      </span>
    </div>

    <div class="flex items-center gap-1 mt-2.5">
      <Icon
        icon="mdi:calendar-blank-outline"
        width="11"
        height="11"
        class="text-base-content/25"
      />
      <span class="text-[10px] text-base-content/30">
        {new Date(report.created_at).toLocaleDateString("en-US", {
          month: "short",
          day: "numeric",
          year: "numeric",
        })}
      </span>
    </div>
  </div>
</div>

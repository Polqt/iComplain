<script lang="ts">
  import Icon from "@iconify/svelte";
  import type { Ticket } from "../../../types/tickets.ts";
  import { statusConfig } from "../../../utils/ticketConfig.ts";

  export let ticket: Ticket;
  export let variant: "grid" | "list" = "grid";

  function handleUpdate() {}
</script>

{#if variant === "grid"}
  <div
    class="card bg-base-200 dark:bg-base-300 shadow-sm hover:shadow-md transition-all border border-base-content/5 shrink-0 cursor-pointer"
  >
    <div class="card-body p-4">
      <div class="flex items-center justify-between mb-3">
        <div
          class="badge badge-sm {statusConfig[
            ticket.status as keyof typeof statusConfig
          ].color}"
        >
          {statusConfig[ticket.status as keyof typeof statusConfig].label}
        </div>
        <div class="dropdown dropdown-end">
          <label class="btn btn-ghost btn-xs btn-circle cursor-pointer">
            <Icon icon="mdi:dots-vertical" width="14" height="14" />
          </label>
          <ul
            class="dropdown-content menu bg-base-100 rounded-box z-1 w-40 p-2 shadow-lg border border-base-content/5"
          >
            <li>
              <button type="button" class="gap-2" onclick={handleUpdate}
                >Update</button
              >
            </li>
          </ul>
        </div>
      </div>

      <h3 class="font-semibold text-base text-base-content mb-2 line-clamp-2">
        {ticket.title}
      </h3>
      <p class="text-sm text-base-content/60 mb-3 line-clamp-2">
        {ticket.description}
      </p>
    </div>
  </div>
{:else}
  <div
    class="card bg-base-100 shadow-sm hover:shadow-md transition-all duration-200 border border-base-content/50"
  ></div>
{/if}

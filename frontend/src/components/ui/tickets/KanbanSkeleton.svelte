<script lang="ts">
  import { columns } from "../../../utils/ticketConfig.ts";
</script>

<div class="flex gap-6 flex-1">
  <div class="flex-1 flex flex-col gap-3">
    {#each Array(6) as _}
      <div class="skeleton h-24 w-full rounded-xl"></div>
    {/each}
  </div>

  <div class="w-64 shrink-0 flex flex-col gap-2">
    {#each columns as _}
      <div class="skeleton h-24 w-full rounded-xl"></div>
    {/each}
  </div>
</div>

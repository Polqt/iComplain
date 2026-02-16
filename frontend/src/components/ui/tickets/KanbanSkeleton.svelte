<script lang="ts">
  import { columns } from "../../../utils/ticketConfig.ts";
</script>

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

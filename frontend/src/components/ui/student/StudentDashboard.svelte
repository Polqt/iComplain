<script lang="ts">
  import { onMount } from "svelte";
  import StudentLayout from "../../../components/layout/StudentLayout.svelte";
  import TicketBoard from "../../../components/ui/tickets/TicketBoard.svelte";
  import { ticketsStore } from "../../../stores/tickets.store.ts";

  onMount(async () => {
    await ticketsStore.loadTickets();
  });
</script>

<StudentLayout>
  <div class="flex flex-col h-[calc(100vh-8rem)]">
    <div class="flex-1 overflow-y-auto pr-2 space-y-8 min-h-0">
      <section class="mt-2">
        <TicketBoard />
      </section>
    </div>
  </div>
</StudentLayout>
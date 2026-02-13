<script lang="ts">
  import StudentLayout from "../../../components/layout/StudentLayout.svelte";
  import TicketHistoryView from "../../../components/ui/history/TicketHistoryView.svelte";
  import { fetchTicketHistory } from "../../../lib/api/history.ts";
</script>

<StudentLayout>
  <TicketHistoryView
    fetchItems={fetchTicketHistory}
    title="Ticket History"
    description="View all your ticket activities and status changes."
    ticketUrlPrefix="/tickets"
  />
</StudentLayout>

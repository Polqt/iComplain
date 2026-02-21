<script lang="ts">
  import AdminLayout from "../../../components/layout/AdminLayout.svelte";
  import TicketHistoryView from "../history/TicketHistoryView.svelte";
  import { fetchTicketHistory } from "../../../lib/api/history.ts";
</script>

<AdminLayout>
  <TicketHistoryView fetchItems={fetchTicketHistory} />
</AdminLayout>

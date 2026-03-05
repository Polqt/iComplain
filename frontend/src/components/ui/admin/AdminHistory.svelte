<script lang="ts">
  import { fetchTicketHistory } from "../../../lib/api/history.ts";
import AdminLayout from "../../../components/layout/AdminLayout.svelte";
import TicketHistoryView from "../history/TicketHistoryView.svelte";
</script>

<AdminLayout>
  <TicketHistoryView fetchItems={fetchTicketHistory} />
</AdminLayout>

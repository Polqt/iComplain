<script lang="ts">
  import AdminLayout from "../../../components/layout/AdminLayout.svelte";
  import TicketHistoryView from "../history/TicketHistoryView.svelte";
  import { fetchAdminTicketHistory } from "../../../lib/api/history.ts";
</script>

<AdminLayout>
  <TicketHistoryView fetchItems={fetchAdminTicketHistory} />
</AdminLayout>

<script lang="ts">
  import StudentLayout from "../../../components/layout/StudentLayout.svelte";
  import TicketBoard from "../tickets/TicketBoard.svelte";
</script>

<StudentLayout>
  <div class="flex flex-col h-[calc(100vh-8rem)]">
    <!-- Announcements Section -->
    <TicketBoard />
  </div>
</StudentLayout>

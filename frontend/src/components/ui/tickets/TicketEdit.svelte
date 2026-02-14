<script lang="ts">
  import TicketCreateModal from "./TicketCreateModal.svelte";
  import { ticketsStore } from "../../../stores/tickets.store.ts";
  import type { Ticket, TicketUpdatePayload } from "../../../types/tickets.ts";

  export let open = false;
  export let ticket: Ticket | null = null;
  export let isLoading = false;
  export let onclose: () => void = () => {};

  $: formData = ticket ? { ...ticket } : {};

  async function handleSubmit(data: Partial<Ticket>, file?: File | null) {
    if (!ticket) return;
    const categoryId =
      typeof data.category === "number" ? data.category : data.category?.id;
    const payload: TicketUpdatePayload = {
      title: data.title,
      description: data.description,
      building: data.building,
      room_name: data.room_name,
      category: categoryId,
    };
    const updated = await ticketsStore.updateTicket(ticket.id, payload, file);
    if (updated) {
      await ticketsStore.loadTicketById(ticket.id);
      onclose();
    }
  }
</script>

<TicketCreateModal
  {open}
  mode="edit"
  {formData}
  {isLoading}
  onclose={() => {
    ticketsStore.setError(null);
    onclose();
  }}
  onsubmit={handleSubmit}
/>

<script lang="ts">
  import { authStore } from "../../stores/auth.store.ts";
  import AdminTicket from "../../components/ui/admin/AdminTicket.svelte";
  import StudentTicket from "../../components/ui/student/StudentTicket.svelte";

  let isLoading: boolean = true;
  let role: string | null = null;

  $: ({ isLoading, isAuthenticated, role } = $authStore);
</script>

{#if isLoading}
  <div class="flex justify-center items-center min-h-[40vh]">
    <span class="loading loading-spinner loading-lg"></span>
  </div>
{:else if role === "admin"}
  <AdminTicket />
{:else if role === "student"}
  <StudentTicket />
{/if}

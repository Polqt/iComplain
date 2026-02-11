<script lang="ts">
  import { authStore } from "../../stores/auth.store.ts";
  import StudentHistory from "../../components/ui/student/StudentHistory.svelte";
  import AdminHistory from "../../components/ui/admin/AdminHistory.svelte";

  let isLoading: boolean = true;
  let role: string | null = null;

  $: ({ isLoading, isAuthenticated, role } = $authStore);
</script>

{#if isLoading}
  <div class="flex justify-center items-center min-h-[40vh]">
    <span class="loading loading-spinner loading-lg"></span>
  </div>
{:else if role === "admin"}
  <AdminHistory />
{:else if role === "student"}
  <StudentHistory />
{/if}

<script lang="ts">
  import { onMount } from "svelte";
  import AdminDashboard from "../../components/ui/admin/AdminDashboard.svelte";
  import StudentDashboard from "../../components/ui/student/StudentDashboard.svelte";
  import { authStore } from "../../stores/auth.store.ts";

  let isLoading: boolean = true;
  let role: string | null = null;

  $: ({ isLoading, isAuthenticated, role } = $authStore);

  onMount(() => {
    authStore.checkAuth();
  });
  
</script>

{#if isLoading}
  <div class="flex justify-center items-center min-h-[40vh]">
    <span class="loading loading-spinner loading-lg"></span>
  </div>
{:else if role === "admin"}
  <AdminDashboard />
{:else if role === "student"}
  <StudentDashboard />
{/if}

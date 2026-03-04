<script lang="ts">
  import AdminDashboard from "../../components/ui/admin/AdminDashboard.svelte";
  import StudentDashboard from "../../components/ui/student/StudentDashboard.svelte";
  import { authStore } from "../../stores/auth.store.ts";
  import { goto } from "$app/navigation";
  import Icon from "@iconify/svelte";

  let isLoading: boolean = true;
  let role: string | null = null;
  let isAuthenticated: boolean = false;

  $: ({ isLoading, isAuthenticated, role } = $authStore);

  // Redirect if not authenticated after loading
  $: if (!isLoading && !isAuthenticated) {
    goto('/not-signed-in', { replaceState: true });
  }
</script>

{#if isLoading}
  <div class="flex justify-center items-center min-h-[40vh]">
    <span class="loading loading-spinner loading-lg"></span>
  </div>
{:else if isAuthenticated && role === "admin"}
  <AdminDashboard />
{:else if isAuthenticated && role === "student"}
  <StudentDashboard />
{:else}
  <div class="flex flex-col items-center justify-center min-h-[50vh] gap-4">
    <div class="text-center">
      <Icon icon="mdi:alert-circle" width="48" height="48" class="text-error mx-auto mb-4" />
      <h1 class="text-2xl font-bold mb-2">Access Denied</h1>
      <p class="text-base-content/60 mb-6">Unable to determine user role. Please contact support.</p>
      <button class="btn btn-primary" on:click={() => goto('/not-signed-in')}>
        Return to Sign In
      </button>
    </div>
  </div>
{/if}

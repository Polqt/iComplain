<script lang="ts">
  import AdminSettings from "../../components/ui/admin/AdminSettings.svelte";
  import StudentSettings from "../../components/ui/student/StudentSettings.svelte";
  import { authStore } from "../../stores/auth.store.ts";

  let isLoading: boolean = true;
  let role: string | null = null;

  $: ({ isLoading, isAuthenticated, role } = $authStore);
</script>

<svelte:head>
  <title>Settings - iComplain</title>
</svelte:head>

{#if isLoading}
  <div class="flex justify-center items-center min-h-[40vh]">
    <span class="loading loading-spinner loading-lg"></span>
  </div>
{:else if role === "admin"}
  <AdminSettings />
{:else if role === "student"}
  <StudentSettings />
{:else}
  <div class="flex flex-col items-center justify-center min-h-[40vh] gap-3">
    <p class="text-base-content/70">
      You need to be signed in to view settings.
    </p>
    <a href="/signin" class="btn btn-primary btn-sm">Go to Sign In</a>
  </div>
{/if}

<script lang="ts">
  import { onMount } from "svelte";
  import { authStore } from "../../stores/auth.store.ts";
  import AdminHelp from "../../components/ui/admin/AdminHelp.svelte";
  import StudentHelp from "../../components/ui/student/StudentHelp.svelte";

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
  <AdminHelp />
{:else if role === "student"}
  <StudentHelp />
{:else}
  <div class="flex flex-col items-center justify-center min-h-[40vh] gap-3">
    <p class="text-base-content/70">
      You need to be signed in to view the help center.
    </p>
    <a href="/signin" class="btn btn-primary btn-sm">Go to Sign In</a>
  </div>
{/if}

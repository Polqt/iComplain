<script lang="ts">
  import { goto } from "$app/navigation";
  import { authStore } from "../../stores/auth.store.ts";
  import StudentNotification from "../../components/ui/student/StudentNotification.svelte";
  import AdminNotification from "../../components/ui/admin/AdminNotification.svelte";

  let isLoading: boolean = true;
  let role: string | null = null;
  let isAuthenticated: boolean = false;

  $: ({ isLoading, isAuthenticated, role } = $authStore);

  $: if (!isLoading && !isAuthenticated) {
    goto("/not-signed-in", { replaceState: true });
  }
</script>

{#if isLoading}
  <div class="flex justify-center items-center min-h-[40vh]">
    <span class="loading loading-spinner loading-lg"></span>
  </div>
{:else if role === "admin"}
  <AdminNotification />
{:else if role === "student"}
  <StudentNotification />
{/if}

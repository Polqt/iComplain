<script lang="ts">
  import AdminProfile from "../../components/ui/admin/AdminProfile.svelte";
  import { authStore } from "../../stores/auth.store.ts";
  import StudentProfile from "../../components/ui/student/StudentProfile.svelte";

  let isLoading: boolean = true;
  let role: string | null = null;

  $: ({ isLoading, isAuthenticated, role } = $authStore);
</script>

{#if isLoading}
  <div class="flex justify-center items-center min-h-[40vh]">
    <span class="loading loading-spinner loading-lg"></span>
  </div>
{:else if role === "admin"}
  <AdminProfile />
{:else if role === "student"}
  <StudentProfile />
{/if}

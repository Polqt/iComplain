<script lang="ts">
  import { onMount } from "svelte";
  import AdminDashboard from "../../../components/ui/admin/AdminDashboard.svelte";
  import { authStore } from "../../../stores/auth.store.ts";

  let isLoading = true;
  let role: string | null = null;

  $: ({ isLoading, role } = $authStore);

  onMount(() => {
    authStore.checkAuth();
  });
</script>

<AdminDashboard />

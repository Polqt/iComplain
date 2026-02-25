<script lang="ts">
  import "./layout.css";
  import { onDestroy, onMount } from "svelte";
  import { authStore } from "../stores/auth.store.ts";
  import { wsStore } from "../stores/websocket.store.ts";

  let unsubscribeAuth: (() => void) | null = null;

  const { children } = $props();

  // Initialize auth once for the whole app (prevents repeated /api/user/profile calls)
  onMount(() => {
    authStore.checkAuth();

    // Websocket connection
    unsubscribeAuth = authStore.subscribe(($auth) => {
      if ($auth.isAuthenticated) {
        wsStore.connect();
      } else {
        wsStore.disconnect();
      }
    });
  });

  onDestroy(() => {
    if (unsubscribeAuth) {
      unsubscribeAuth();
    }
    wsStore.disconnect();
  });
</script>

{@render children()}

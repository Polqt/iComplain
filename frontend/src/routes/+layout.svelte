<script lang="ts">
import "./layout.css";
import { onDestroy, onMount } from "svelte";
import { goto } from "$app/navigation";
import { page } from "$app/state";
import { authStore } from "../stores/auth.store.ts";
import { wsStore } from "../stores/websocket.store.ts";

let unsubscribeAuth: (() => void) | null = null;

const { children } = $props();

const ADMIN_ONLY_PATHS = ["/admin"];

onMount(() => {
	authStore.checkAuth();

	// Skip while auth check is still in flight.
	// Enforce role-based route protection once auth resolves.
	let firstConnect = true;
	unsubscribeAuth = authStore.subscribe(($auth) => {
		if ($auth.isLoading) return;
		if ($auth.isAuthenticated) {
			const path = page.url.pathname;

			// Redirect non-admins away from admin-only routes
			if (ADMIN_ONLY_PATHS.some((p) => path.startsWith(p)) && $auth.role !== "admin") {
				goto("/dashboard");
				return;
			}

			const delay = firstConnect ? 1500 : 0;
			firstConnect = false;
			wsStore.connect(delay);
		} else {
			firstConnect = true;
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

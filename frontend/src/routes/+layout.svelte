<script lang="ts">
	import './layout.css';
	import { onMount } from 'svelte';
	import { authStore } from '../stores/auth.store.ts';

	const { children } = $props();

	// Initialize auth once for the whole app (prevents repeated /api/user/profile calls)
	onMount(() => {
		authStore.checkAuth();
	});
</script>

{@render children()}

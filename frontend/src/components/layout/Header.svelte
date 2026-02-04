<script lang="ts">
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import Icon from "@iconify/svelte";

  let menuOpen = false;

  $: currentPath = $page.url.pathname;

  function isActivePath(path: string): boolean {
    return currentPath === path;
  }

  function toggleMenu() {
    menuOpen = !menuOpen;
  }

  function closeMenu() {
    menuOpen = false;
  }
</script>

<header class="w-full py-4 md:py-6">
  <div class="flex items-center justify-between">
    <button
      type="button"
      aria-label="iComplain Logo"
      on:click={() => goto("/")}
      class="text-lg font-semibold text-base-content hover:text-base-content/70"
    >
      iComplain
    </button>

    <nav class="hidden md:flex items-center gap-1">
      <a
        href="/about"
        class="px-3 py-2 text-sm font-medium transition-colors rounded-lg
            {isActivePath('/about')
          ? 'bg-base-200 text-base-content'
          : 'text-base-content/60 hover:text-base-content hover:bg-base-200/50'}"
        >About</a
      >
      <a
        href="/signin"
        class="px-3 py-2 text-sm font-medium transition-colors rounded-lg
            {isActivePath('/signin') && currentPath !== '/signup' 
          ? 'bg-base-200 text-base-content'
          : 'text-base-content/60 hover:text-base-content hover:bg-base-200/50'}"
        >Sign In</a
      >
    </nav>

    <button
      type="button"
      aria-label="Toggle menu"
      on:click={toggleMenu}
      class="md:hidden p-2 text-base-content hover:bg-base-200 rounded-lg transition-colors"
    >
      <Icon icon={menuOpen ? "mdi:close" : "mdi:menu"} width="24" height="24" />
    </button>
  </div>

  {#if menuOpen}
    <div class="md:hidden mt-4 pb-4 border-t border-base-300 pt-4">
      <nav class="flex flex-col gap-2">
        <a
          href="/about"
          on:click={closeMenu}
          class="px-3 py-2 text-sm font-medium transition-colors rounded-lg
              {isActivePath('/about')
            ? 'bg-base-200 text-base-content'
            : 'text-base-content/60 hover:text-base-content hover:bg-base-200/50'}"
          >About</a
        >
        <a
          href="/signin"
          on:click={closeMenu}
          class="px-3 py-2 text-sm font-medium transition-colors rounded-lg
              {isActivePath('/signin')
            ? 'bg-base-200 text-base-content'
            : 'text-base-content/60 hover:text-base-content hover:bg-base-200/50'}"
          >Sign In</a
        >
      </nav>
    </div>
  {/if}
</header>

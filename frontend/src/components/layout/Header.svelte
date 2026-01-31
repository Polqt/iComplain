<script lang="ts">
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";

  $: currentPath = $page.url.pathname;

  function isActivePath(path: string): boolean {
    return currentPath === path;
  }
</script>

<header class="w-full py-6">
  <div class="flex items-center justify-between">
    <button
      type="button"
      aria-label="iComplain Logo"
      on:click={() => goto("/")}
      class="text-lg font-semibold text-base-content hover:text-base-content/70"
    >
      iComplain
    </button>

    <nav class="flex items-center gap-1">
      <a
        href="/about"
        class="px-3 py-2 text-sm font-medium transition-colors rounded-lg
            {isActivePath('/about')
          ? 'bg-base-200 text-base-content'
          : 'text-base-content/60 hover:text-base-content hover:bg-base-200/50'}"
        >About</a
      >
      <a
        href="/login"
        class="px-3 py-2 text-sm font-medium transition-colors rounded-lg
            {isActivePath('/login')
          ? 'bg-base-200 text-base-content'
          : 'text-base-content/60 hover:text-base-content hover:bg-base-200/50'}"
        >Sign In</a
      >
    </nav>
  </div>
</header>

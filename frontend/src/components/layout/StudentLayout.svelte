<script lang="ts">
  import Icon from "@iconify/svelte";
  import { onMount } from "svelte";

  let showModal: boolean = false;

  function handleKeyDown(event: KeyboardEvent) {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
      event.preventDefault();
      showModal = true;
    }
  }

  function closeModal() {
    showModal = false;
  }

  onMount(() => {
    window.addEventListener("keydown", handleKeyDown);
  });
</script>

<div class="min-h-screen flex flex-col w-full">
  <aside>
    <div class="drawer lg:drawer-open">
      <input id="my-drawer-4" type="checkbox" class="drawer-toggle" />
      <div class="drawer-content">
        <nav class="navbar w-full border-b">
          <label
            for="my-drawer-4"
            aria-label="open sidebar"   
            class="btn btn-square btn-ghost"
          >
            <Icon icon="lucide:sidebar-open"  width="24" height="24" />
          </label>
          {#if showModal}
            <div
              class="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
            >
              <div
                class="bg-base-100 rounded-lg shadow-lg p-8 max-w-md w-full relative"
              >
                <button
                  class="absolute top-2 right-2 btn btn-sm btn-ghost"
                  on:click={closeModal}
                  aria-label="Close"
                >
                  ✕
                </button>
                <h2 class="text-xl font-bold mb-4">Search</h2>
                <input
                  type="search"
                  class="input input-bordered w-full"
                  placeholder="Type to search..."
                />
              </div>
            </div>
          {/if}
          <div class="px-4">
            <div class="flex flex-row justify-between items-center w-full">
              <label class="input rounded-lg">
                <svg
                  class="h-[1em] opacity-50"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                >
                  <g
                    stroke-linejoin="round"
                    stroke-linecap="round"
                    stroke-width="2.5"
                    fill="none"
                    stroke="currentColor"
                  >
                    <circle cx="11" cy="11" r="8"></circle>
                    <path d="m21 21-4.3-4.3"></path>
                  </g>
                </svg>
                <input
                  type="search"
                  required
                  placeholder="Start searching here..."
                />
                <kbd class="kbd">⌘ K</kbd>
              </label>
            </div>
          </div>
        </nav>
        <div class="p-4">Page Content</div>
      </div>

      <div
        class="drawer-side is-drawer-close:overflow-visible border-r"
      >
        <label
          for="my-drawer-4"
          aria-label="close sidebar"
          class="drawer-overlay"
        ></label>
        <div
          class="flex min-h-full flex-col items-start bg-base-200 is-drawer-close:w-14 is-drawer-open:w-64"
        >
          <ul class="menu w-full grow"></ul>
        </div>
      </div>
    </div>
  </aside>
</div>

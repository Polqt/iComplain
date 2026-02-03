<script lang="ts">
  import Icon from "@iconify/svelte";
  import { onMount } from "svelte";
  import { formattedDate } from "../../utils/date.ts";

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

  const items = [
    {
      name: "Home",
      icon: "lucide:home",
      href: "/student/dashboard",
    },
    { name: "Tickets", icon: "lucide:ticket", href: "/tickets" },
    { name: "Notifications", icon: "lucide:bell", href: "/notifications" },
    { name: "History", icon: "lucide:clock", href: "/history" },
  ];

  const profileItem = {
    name: "Profile",
    icon: "lucide:user-circle",
    href: "/profile",
  };
</script>

<div class="min-h-screen flex flex-col w-full bg-gray-50">
  <aside class="h-screen">
    <div class="drawer lg:drawer-open h-screen">
      <input id="my-drawer-3" type="checkbox" class="drawer-toggle" />
      <div class="drawer-content">
        <nav class="navbar w-full">
          <label for="my-drawer-3" class="btn btn-square btn-ghost lg:hidden">
            <Icon icon="lucide:sidebar-open" width="24" height="24" />
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
                  <Icon icon="lucide:x" width="16" height="16" />
                </button>
                <h2 class="text-xl font-bold mb-4">Search</h2>
                <input
                  type="search"
                  class="input w-full"
                  placeholder="Type to search..."
                />
              </div>
            </div>
          {/if}
          <div class="px-4 flex justify-between w-full">
            <div
              class="flex flex-row justify-between items-center w-full gap-4"
            >
              <div class="flex-1">
                <label
                  class="flex items-center gap-2 bg-white rounded-lg shadow px-4 py-2 w-full"
                >
                  <Icon
                    icon="lucide:search"
                    width="24"
                    height="24"
                    class="text-base-content/50"
                  />
                  <input
                    type="search"
                    required
                    placeholder="Start searching here..."
                    class="flex-1 bg-transparent outline-none border-none focus:ring-0"
                  />
                  <kbd class="kbd sm:kbd-xs lg:kbd-lg md:kbd-md">⌘ K</kbd>
                </label>
              </div>

              <div
                class="flex items-center gap-2 bg-white rounded-lg shadow px-3 py-2"
              >
                <button
                  aria-label="moon"
                  type="button"
                  class="btn btn-ghost btn-sm rounded-full"
                >
                  <Icon icon="lucide:moon" width="20" height="20" />
                </button>
                <span class="text-gray-300">|</span>
                <button
                  aria-label="sun"
                  type="button"
                  class="btn btn-ghost btn-sm rounded-full"
                >
                  <Icon icon="lucide:sun" width="20" height="20" />
                </button>
              </div>

              <div
                class="flex items-center gap-3 bg-white rounded-lg shadow px-4 py-2 min-w-fit"
              >
                <Icon
                  icon="solar:calendar-line-duotone"
                  width="20"
                  height="20"
                />
                <span class="text-base font-medium">{formattedDate}</span>
                <span class="mx-1 text-gray-300">|</span>
                <Icon icon="lucide:bell" width="20" height="20" />
                <div class="avatar">
                  <div class="w-8 h-8 ml-2 rounded-full overflow-hidden">
                    <img
                      src="https://img.daisyui.com/images/profile/demo/yellingcat@192.webp"
                      alt="User"
                      width="32"
                      height="32"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </nav>
        <div class="p-4">Page Content</div>
      </div>

      <div class="drawer-side p-2 mx-2 lg:overflow-visible lg:relative">
        <label
          for="my-drawer-3"
          aria-label="close sidebar"
          class="drawer-overlay"
        ></label>
        <ul
          class="menu h-full bg-white shadow rounded-lg w-16 flex flex-col items-center gap-2"
        >
          {#each items as item}
            <li>
              <a
                href={item.href}
                class="tooltip tooltip-right flex items-center justify-center w-12 h-12 rounded-lg hover:bg-gray-100 transition"
                data-tip={item.name}
              >
                <Icon icon={item.icon} width="28" height="28" />
              </a>
            </li>
          {/each}
          <li class="mt-auto">
            <a
              href={profileItem.href}
              class="tooltip tooltip-right flex items-center justify-center w-12 h-12 rounded-lg hover:bg-gray-100 transition"
              data-tip={profileItem.name}
            >
              <Icon icon={profileItem.icon} width="28" height="28" />
            </a>
          </li>
        </ul>
      </div>
    </div>
  </aside>
</div>

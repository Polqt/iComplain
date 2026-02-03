<script lang="ts">
  import Icon from "@iconify/svelte";
  import { onMount } from "svelte";
  import { formattedDate, mobileFormattedDate } from "../../utils/date.ts";

  let showModal: boolean = false;
  let theme: string = "lofi";
  let isMobile: boolean = false;

  function handleKeyDown(event: KeyboardEvent) {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
      event.preventDefault();
      showModal = true;
    }
  }

  function closeModal() {
    showModal = false;
  }

  function setTheme(newTheme: string) {
    theme = newTheme;
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", newTheme);
  }

  function checkMobile() {
    isMobile = window.innerWidth < 768;
  }

  onMount(() => {
    window.addEventListener("keydown", handleKeyDown);
    const savedTheme = localStorage.getItem("theme") || "lofi";
    setTheme(savedTheme);
    window.addEventListener("resize", checkMobile);
    checkMobile();

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      window.removeEventListener("resize", checkMobile);
    };
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

<div class="min-h-screen w-full bg-gray-50">
  <div class="drawer lg:drawer-open">
    <input id="my-drawer-3" type="checkbox" class="drawer-toggle" />
    <div class="drawer-content flex flex-col w-full">
      <nav class="navbar w-full px-2 sm:px-4 py-2">
        <label
          for="my-drawer-3"
          class="btn btn-square btn-ghost lg:hidden shrink-0"
        >
          <Icon icon="lucide:menu" width="24" height="24" />
        </label>

        {#if showModal}
          <div
            class="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
          >
            <div
              class="bg-base-100 rounded-lg shadow-lg p-4 sm:p-8 max-w-md w-[90%] sm:w-full relative mx-4"
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

        <div
          class="flex-1 flex items-center justify-between gap-2 sm:gap-4 overflow-hidden"
        >
          <div class="flex-1 min-w-0">
            <label
              class="flex items-center gap-2 bg-white rounded-lg shadow px-2 sm:px-4 py-2 w-full"
            >
              <Icon
                icon="lucide:search"
                width="20"
                height="20"
                class="text-base-content/50 shrink-0"
              />
              <input
                type="search"
                required
                placeholder={isMobile ? "Search..." : "Start searching here..."}
                class="flex-1 min-w-0 bg-transparent outline-none border-none focus:ring-0 text-sm sm:text-base"
              />
              <kbd class="kbd kbd-sm hidden sm:inline-flex">⌘ K</kbd>
            </label>
          </div>

          <div
            class="flex items-center gap-1 sm:gap-2 bg-white rounded-lg shadow px-2 sm:px-3 py-2 shrink-0"
          >
            <button
              aria-label="Toggle theme"
              type="button"
              class="btn btn-ghost btn-xs sm:btn-sm rounded-full"
            >
              <Icon
                icon="lucide:moon"
                width="18"
                height="18"
                class="sm:w-5 sm:h-5"
              />
            </button>
            <!-- Hide separator and sun icon on mobile -->
            <span class="text-gray-300 hidden sm:inline">|</span>
            <button
              aria-label="Light mode"
              type="button"
              class="btn btn-ghost btn-xs sm:btn-sm rounded-full hidden sm:flex"
            >
              <Icon icon="lucide:sun" width="20" height="20" />
            </button>
          </div>

          <!--Profile-->
          <div
            class="flex items-center gap-1 sm:gap-3 bg-white rounded-lg shadow px-2 sm:px-4 py-2 shrink-0"
          >
            <!--Calender icon (hidden if mobile view)-->
            <Icon
              icon="solar:calendar-line-duotone"
              width="18"
              height="18"
              class="hidden xs:block sm:w-5 sm:h-5"
            />
            <!--Date -->
            <span class="text-xs sm:text-base font-medium whitespace-nowrap">
              {#if isMobile}
                {mobileFormattedDate}
              {:else}
                {formattedDate}
              {/if}
            </span>
            <span class="mx-1 text-gray-300 hidden sm:inline">|</span>
            <Icon
              icon="lucide:bell"
              width="18"
              height="18"
              class="sm:w-5 sm:h-5"
            />
            <div class="avatar">
              <div class="w-6 h-6 sm:w-8 sm:h-8 rounded-full overflow-hidden">
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
      </nav>
      <main class="flex-1 p-2 sm:p-4 w-full">
        <slot />
      </main>
    </div>

    <div class="drawer-side z-40 overflow-visible">
      <label for="my-drawer-3" aria-label="close sidebar" class="drawer-overlay"
      ></label>
      <ul
        class="menu min-h-full bg-white shadow-lg w-20 flex flex-col items-center gap-2 py-4 overflow-visible"
      >
        {#each items as item}
          <li>
            <a
              href={item.href}
              class="flex items-center justify-center w-12 h-12 rounded-lg hover:bg-gray-100 transition tooltip tooltip-right"
              data-tip={item.name}
            >
              <Icon icon={item.icon} width="24" height="24" />
            </a>
          </li>
        {/each}
        <li class="mt-auto">
          <a
            href={profileItem.href}
            class="flex items-center justify-center w-12 h-12 rounded-lg hover:bg-gray-100 transition tooltip tooltip-right"
            data-tip={profileItem.name}
          >
            <Icon icon={profileItem.icon} width="24" height="24" />
          </a>
        </li>
      </ul>
    </div>
  </div>
</div>

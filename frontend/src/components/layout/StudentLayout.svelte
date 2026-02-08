<script lang="ts">
  import Icon from "@iconify/svelte";
  import { onMount } from "svelte";
  import { formattedDate, mobileFormattedDate } from "../../utils/date.ts";
  import SearchModal from "../ui/SearchModal.svelte";
  import SearchBar from "../ui/SearchBar.svelte";

  let showModal: boolean = false;
  let theme: string = "lofi";
  let isMobile: boolean = false;

  function openModal() {
    showModal = true;
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
    const savedTheme = localStorage.getItem("theme") || "lofi";
    setTheme(savedTheme);
    window.addEventListener("resize", checkMobile);
    checkMobile();

    return () => {
      window.removeEventListener("resize", checkMobile);
    };
  });

  const items = [
    {
      name: "Home",
      icon: "lucide:home",
      href: "/student/dashboard",
    },
    { name: "Tickets", icon: "lucide:ticket", href: "/student/tickets" },
    {
      name: "Notifications",
      icon: "lucide:bell",
      href: "/student/notifications",
    },
    { name: "History", icon: "lucide:clock", href: "/history" },
  ];

  const profileItem = {
    name: "Profile",
    icon: "lucide:user-circle",
    href: "/profile",
  };
</script>

<div class="min-h-screen w-full bg-base-300 dark:bg-base-300">
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

        <SearchModal isOpen={showModal} on:close={closeModal} />

        <div
          class="flex-1 flex items-center justify-between gap-2 sm:gap-4 overflow-hidden"
        >
          <SearchBar {isMobile} on:openModal={openModal} />

          <div
            class="flex items-center gap-1 sm:gap-2 bg-base-100 dark:bg-base-100 rounded-lg shadow px-2 sm:px-3 py-2 shrink-0"
          >
            <button
              aria-label="Light Theme"
              type="button"
              class="btn btn-ghost btn-xs sm:btn-sm rounded-full"
              on:click={() => setTheme("lofi")}
              disabled={theme === "lofi"}
            >
              <Icon icon="lucide:sun" width="20" height="20" />
            </button>
            <span class="text-gray-300 hidden sm:inline">|</span>
            <button
              aria-label="Dark Theme"
              type="button"
              class="btn btn-ghost btn-xs sm:btn-sm rounded-full hidden sm:flex"
              on:click={() => setTheme("night")}
              disabled={theme === "night"}
            >
              <Icon
                icon="lucide:moon"
                width="18"
                height="18"
                class="sm:w-5 sm:h-5"
              />
            </button>
          </div>

          <div
            class="flex items-center gap-1 sm:gap-3 bg-base-100 dark:bg-base-100 rounded-lg shadow px-2 sm:px-4 py-2 shrink-0"
          >
            <Icon
              icon="solar:calendar-line-duotone"
              width="18"
              height="18"
              class="hidden xs:block sm:w-5 sm:h-5"
            />
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
              <div
                class="w-6 h-6 sm:w-8 sm:h-8 rounded-full overflow-hidden dropdown dropdown-center"
              >
                <img
                  src="https://img.daisyui.com/images/profile/demo/yellingcat@192.webp"
                  alt="User"
                  width="32"
                  height="32"
                />
                <ul
                  tabindex="-1"
                  class="dropdown-content menu bg-base-100 rounded-box z-1 w-52 p-2 shadow-sm"
                ></ul>
              </div>
            </div>
          </div>
        </div>
      </nav>
      <main class="flex-1 p-2 sm:p-4 w-full">
        <slot />
      </main>
    </div>

    <div
      class="drawer-side z-40 overflow-visible lg:p-2 lg:mx-2 lg:overflow-visible lg:sticky lg:top-0 lg:h-screen sm:p-0 sm:mx-0"
    >
      <label for="my-drawer-3" aria-label="close sidebar" class="drawer-overlay"
      ></label>
      <ul
        class="menu min-h-full bg-base-100 dark:bg-base-100 shadow-lg w-16 lg:rounded-lg sm:rounded-md flex flex-col items-center gap-2 py-4 overflow-visible"
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

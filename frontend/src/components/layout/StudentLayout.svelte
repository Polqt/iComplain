<script lang="ts">
  import Icon from "@iconify/svelte";
  import { onMount } from "svelte";
  import SearchModal from "../ui/SearchModal.svelte";
  import SearchBar from "../ui/SearchBar.svelte";
  import NotificationBell from "../ui/NotificationBell.svelte";
  import Profile from "../ui/Profile.svelte";
  import { goto } from "$app/navigation";
  import type { Notification } from "../../types/notifications.js";
  import { formattedDate, mobileFormattedDate } from "../../utils/date.ts";
  import type { ProfileUser } from "../../types/user.ts";

  let showModal: boolean = false;
  let theme: string = "lofi";
  let isMobile: boolean = false;

  let user: ProfileUser | null = {
    name: "Juan Dela Cruz",
    email: "juan.delacruz@usls.edu.ph",
    avatar: "https://img.daisyui.com/images/profile/demo/yellingcat@192.webp",
    role: "student",
  };

  let notifications: Notification[] = [];
  let unreadCount: number = 0;

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

  function handleLogout() {
    localStorage.removeItem("authToken");
    sessionStorage.clear();

    goto("/signin");
  }

  function handleMarkAsRead(event: CustomEvent<{ id: string }>) {
    const { id } = event.detail;

    // Update local state
    notifications = notifications.map((n) =>
      n.id === id ? { ...n, read: true } : n,
    );

    // Recalculate unread count
    unreadCount = notifications.filter((n) => !n.read).length;

    // TODO: Call API to mark as read
    // await api.markNotificationAsRead(id);
  }

  function handleNotificationClick(
    event: CustomEvent<{ notification: Notification }>,
  ) {
    const { notification } = event.detail;

    // Navigate to notification URL if available
    if (notification.actionUrl) {
      goto(notification.actionUrl);
    }
  }

  function handleViewAllNotifications() {
    goto("/notifications");
  }

  onMount(() => {
    const savedTheme = localStorage.getItem("theme") || "lofi";
    setTheme(savedTheme);
    window.addEventListener("resize", checkMobile);
    checkMobile();

    // TODO: Fetch user data from API
    // user = await api.getCurrentUser();

    // TODO: Fetch latest notifications from API
    // const data = await api.getNotifications({ limit: 5 });
    // notifications = data.notifications;
    // unreadCount = data.unreadCount;

    notifications = [
      {
        id: "1",
        type: "success",
        title: "Report Resolved",
        message: "Your report about the broken AC unit has been resolved.",
        timestamp: "5 minutes ago",
        read: false,
        actionUrl: "/student/reports/1",
      },
      {
        id: "2",
        type: "info",
        title: "Report Update",
        message: "Your leaking faucet report is being reviewed.",
        timestamp: "2 hours ago",
        read: false,
        actionUrl: "/student/reports/2",
      },
      {
        id: "3",
        type: "warning",
        title: "Action Required",
        message: "Your report needs additional information.",
        timestamp: "1 day ago",
        read: true,
        actionUrl: "/student/reports/3",
      },
    ];

    unreadCount = notifications.filter((n) => !n.read).length;

    return () => {
      window.removeEventListener("resize", checkMobile);
    };
  });

  const items = [
    {
      name: "Home",
      icon: "lucide:home",
      href: "/dashboard",
    },
    { name: "Tickets", icon: "lucide:ticket", href: "/tickets" },
    {
      name: "Notifications",
      icon: "lucide:bell",
      href: "/notifications",
    },
    { name: "History", icon: "lucide:clock", href: "/history" },
    { name: "Help", icon: "lucide:help-circle", href: "/help" },
  ];

  const profileItem = {
    name: "Profile",
    icon: "lucide:user-circle",
    href: "/profile",
  };

  const settingItem = {
    name: "Settings",
    icon: "lucide:settings",
    href: "/settings",
  };

  const notificationsConfig = {
    success: {
      icon: "lucide:check-circle",
      bgColor: "bg-success",
      iconColor: "text-success",
    },
    info: {
      icon: "lucide:info",
      bgColor: "bg-info",
      iconColor: "text-info",
    },
    warning: {
      icon: "lucide:alert-circle",
      bgColor: "bg-warning",
      iconColor: "text-warning",
    },
    error: {
      icon: "lucide:x-circle",
      bgColor: "bg-error",
      iconColor: "text-error",
    },
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
          class="flex-1 flex items-center justify-between gap-2 sm:gap-4 overflow-visible"
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
            <NotificationBell
              {notifications}
              {unreadCount}
              {notificationsConfig}
              on:markAsRead={handleMarkAsRead}
              on:notificationClick={handleNotificationClick}
              on:viewAll={handleViewAllNotifications}
            />

            <Profile {user} helpHref="/help" on:logout={handleLogout} />
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
            href={settingItem.href}
            class="flex items-center justify-center w-12 h-12 rounded-lg hover:bg-gray-100 transition tooltip tooltip-right"
            data-tip={settingItem.name}
          >
            <Icon icon={settingItem.icon} width="24" height="24" />
          </a>
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

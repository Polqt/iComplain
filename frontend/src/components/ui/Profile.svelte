<script lang="ts">
  import Icon from "@iconify/svelte";
  import { createEventDispatcher } from "svelte";

  export let user: {
    name: string;
    email: string;
    avatar: string;
    role?: string;
  } = {
    name: "Student User",
    email: "student@usls.edu.ph",
    avatar: "https://img.daisyui.com/images/profile/demo/yellingcat@192.webp",
    role: "Student",
  };
  export let profileHref: string = "/student/profile";
  export let settingsHref: string = "/student/settings";
  export let helpHref: string = "/student/help";

  // Events
  const dispatch = createEventDispatcher<{
    logout: void;
    profileClick: void;
    settingsClick: void;
  }>();

  function handleLogout() {
    // Clear session/auth data
    localStorage.removeItem("authToken");
    sessionStorage.clear();

    dispatch("logout");
  }

  function handleProfileClick() {
    dispatch("profileClick");
  }

  function handleSettingsClick() {
    dispatch("settingsClick");
  }

  // Get user initials for fallback
  function getInitials(name: string): string {
    return name
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase()
      .slice(0, 2);
  }
</script>

<div class="dropdown dropdown-end">
  <button
    tabindex="0"
    class="btn btn-ghost btn-circle avatar hover:scale-105 transition-transform"
    aria-label="Profile menu"
  >
    <div
      class="w-8 h-8 rounded-full overflow-hidden ring-2 ring-base-300 ring-offset-2 ring-offset-base-100"
    >
      {#if user.avatar}
        <img src={user.avatar} alt={user.name} width="32" height="32" />
      {:else}
        <div
          class="w-full h-full bg-primary text-primary-content flex items-center justify-center text-sm font-semibold"
        >
          {getInitials(user.name)}
        </div>
      {/if}
    </div>
  </button>

  <ul
    class="dropdown-content menu bg-base-100 rounded-box z-100 w-64 p-2 shadow-xl border border-base-content/10 mt-3"
  >
    <li class="menu-title px-4 py-3 border-b border-base-content/10">
      <div class="flex items-center gap-3">
        <div class="avatar">
          <div class="w-10 h-10 rounded-full">
            {#if user.avatar}
              <img src={user.avatar} alt={user.name} />
            {:else}
              <div
                class="w-full h-full bg-primary text-primary-content flex items-center justify-center text-sm font-semibold"
              >
                {getInitials(user.name)}
              </div>
            {/if}
          </div>
        </div>
        <div class="flex-1 min-w-0">
          <p class="font-semibold text-sm text-base-content truncate">
            {user.name}
          </p>
          <p class="text-xs text-base-content/60 truncate">
            {user.email}
          </p>
          {#if user.role}
            <span class="badge badge-primary badge-xs mt-1">{user.role}</span>
          {/if}
        </div>
      </div>
    </li>

    <li>
      <a
        href={profileHref}
        class="flex items-center gap-3 py-2.5"
        onclick={handleProfileClick}
      >
        <Icon icon="mdi:account-outline" width="18" height="18" />
        <span>Profile</span>
      </a>
    </li>
    <li>
      <a
        href={settingsHref}
        class="flex items-center gap-3 py-2.5"
        onclick={handleSettingsClick}
      >
        <Icon icon="mdi:cog-outline" width="18" height="18" />
        <span>Settings</span>
      </a>
    </li>
    <li>
      <a href={helpHref} class="flex items-center gap-3 py-2.5">
        <Icon icon="mdi:help-circle-outline" width="18" height="18" />
        <span>Help Center</span>
      </a>
    </li>

    <div class="divider my-1"></div>

    <li>
      <button
        type="button"
        class="flex items-center gap-3 py-2.5 text-error hover:bg-error/10"
        onclick={handleLogout}
      >
        <Icon icon="mdi:logout" width="18" height="18" />
        <span>Logout</span>
      </button>
    </li>
  </ul>
</div>

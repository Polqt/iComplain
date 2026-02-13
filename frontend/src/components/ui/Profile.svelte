<script lang="ts">
  import Icon from "@iconify/svelte";
  import { createEventDispatcher } from "svelte";
  import type { User } from "../../types/user.ts";
  import { deriveNameFromEmail, getInitials } from "../../utils/userConfig.ts";
  import { authStore } from "../../stores/auth.store.ts";

  let user: User | null = null;

  export let profileHref: string = "/profile";
  export let settingsHref: string = "/settings";
  export let helpHref: string = "/help";

  $: ({ user } = $authStore);

  // Events
  const dispatch = createEventDispatcher<{
    logout: void;
    profileClick: void;
    settingsClick: void;
  }>();

  function handleLogout() {
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
      {#if user}
        {@const displayName =
          user.name || deriveNameFromEmail(user.email) || "Student"}
        {#if user.avatar}
          <img src={user.avatar} alt={displayName} />
        {:else}
          <div
            class="w-full h-full bg-primary text-primary-content flex items-center justify-center font-bold text-lg"
          >
            {getInitials(displayName)}
          </div>
        {/if}
      {/if}
    </div>
  </button>

  <ul
    class="dropdown-content menu bg-base-100 rounded-box z-100 w-72 sm:w-80 max-w-[calc(100vw-1rem)] p-2 shadow-xl border border-base-content/10 mt-3"
  >
    {#if user}
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
                  {getInitials(
                    user.name || deriveNameFromEmail(user.email) || "Student",
                  )}
                </div>
              {/if}
            </div>
          </div>
          <div class="flex-1 min-w-0">
            <p
              class="font-semibold text-sm text-base-content leading-snug wrap-break-word whitespace-normal"
            >
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
    {/if}
  </ul>
</div>

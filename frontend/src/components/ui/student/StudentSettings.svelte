<script lang="ts">
  import Icon from "@iconify/svelte";
  import StudentLayout from "../../layout/StudentLayout.svelte";
  import { onMount } from "svelte";
  import {
    loadRecentSearches,
    clearRecentSearchesStorage,
  } from "../../../utils/useSearch.ts";

  let theme: string = "lofi";
  let emailNotifications: boolean = true;
  let inAppNotifications: boolean = true;
  let recentSearchesCount: number = 0;
  let clearSuccess: boolean = false;

  function setTheme(newTheme: string) {
    theme = newTheme;
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", newTheme);
  }

  function toggleEmailNotifications() {
    emailNotifications = !emailNotifications;
    localStorage.setItem("settings.emailNotifications", String(emailNotifications));
  }

  function toggleInAppNotifications() {
    inAppNotifications = !inAppNotifications;
    localStorage.setItem("settings.inAppNotifications", String(inAppNotifications));
  }

  function clearRecentSearches() {
    clearRecentSearchesStorage();
    recentSearchesCount = 0;
    clearSuccess = true;
    setTimeout(() => (clearSuccess = false), 2500);
  }

  function refreshRecentSearchesCount() {
    recentSearchesCount = loadRecentSearches().length;
  }

  onMount(() => {
    theme = localStorage.getItem("theme") || "lofi";
    emailNotifications =
      localStorage.getItem("settings.emailNotifications") !== "false";
    inAppNotifications =
      localStorage.getItem("settings.inAppNotifications") !== "false";
    refreshRecentSearchesCount();
  });
</script>

<svelte:head>
  <title>Settings - iComplain</title>
</svelte:head>

<StudentLayout>
  <div class="flex flex-col h-[calc(100vh-8rem)]">
    <div class="shrink-0 mb-6">
      <h1 class="text-3xl font-black text-base-content mb-2">Settings</h1>
      <p class="text-sm text-base-content/60">
        Manage your preferences and account settings
      </p>
    </div>

    <div class="flex-1 overflow-y-auto pr-2">
      <div class="max-w-3xl space-y-6">
        <!-- Appearance -->
        <div class="card bg-base-100 shadow-sm border border-base-content/5">
          <div class="card-body p-6">
            <h2
              class="text-lg font-bold text-base-content mb-4 flex items-center gap-2"
            >
              <Icon icon="lucide:palette" width="22" height="22" />
              Appearance
            </h2>
            <div class="space-y-3">
              <p class="text-sm text-base-content/70">Theme</p>
              <div
                class="flex items-center gap-2 flex-wrap bg-base-200 rounded-lg p-1.5 w-fit"
              >
                <button
                  type="button"
                  class="btn btn-ghost btn-sm rounded-lg gap-2"
                  class:btn-active={theme === "lofi"}
                  onclick={() => setTheme("lofi")}
                >
                  <Icon icon="lucide:sun" width="18" height="18" />
                  Light
                </button>
                <button
                  type="button"
                  class="btn btn-ghost btn-sm rounded-lg gap-2"
                  class:btn-active={theme === "night"}
                  onclick={() => setTheme("night")}
                >
                  <Icon icon="lucide:moon" width="18" height="18" />
                  Dark
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Notifications -->
        <div class="card bg-base-100 shadow-sm border border-base-content/5">
          <div class="card-body p-6">
            <h2
              class="text-lg font-bold text-base-content mb-4 flex items-center gap-2"
            >
              <Icon icon="lucide:bell" width="22" height="22" />
              Notifications
            </h2>
            <div class="space-y-4">
              <div class="flex items-center justify-between gap-4">
                <div>
                  <p class="font-medium text-base-content">In-app notifications</p>
                  <p class="text-sm text-base-content/60">
                    Show ticket updates in the notification bell
                  </p>
                </div>
                <input
                  type="checkbox"
                  class="toggle toggle-primary"
                  checked={inAppNotifications}
                  onchange={toggleInAppNotifications}
                />
              </div>
              <div class="divider my-1"></div>
              <div class="flex items-center justify-between gap-4">
                <div>
                  <p class="font-medium text-base-content">Email notifications</p>
                  <p class="text-sm text-base-content/60">
                    Receive emails for ticket status changes
                  </p>
                </div>
                <input
                  type="checkbox"
                  class="toggle toggle-primary"
                  checked={emailNotifications}
                  onchange={toggleEmailNotifications}
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Data & Privacy -->
        <div class="card bg-base-100 shadow-sm border border-base-content/5">
          <div class="card-body p-6">
            <h2
              class="text-lg font-bold text-base-content mb-4 flex items-center gap-2"
            >
              <Icon icon="lucide:shield" width="22" height="22" />
              Data &amp; Privacy
            </h2>
            <div class="space-y-3">
              <div class="flex items-center justify-between gap-4 flex-wrap">
                <div>
                  <p class="font-medium text-base-content">Recent searches</p>
                  <p class="text-sm text-base-content/60">
                    {recentSearchesCount} saved
                    {recentSearchesCount === 1 ? "search" : "searches"}
                  </p>
                </div>
                <button
                  type="button"
                  class="btn btn-outline btn-sm gap-2"
                  disabled={recentSearchesCount === 0}
                  onclick={clearRecentSearches}
                >
                  <Icon icon="lucide:trash-2" width="16" height="16" />
                  Clear
                </button>
              </div>
              {#if clearSuccess}
                <div class="alert alert-success py-2 text-sm">
                  <Icon icon="lucide:check-circle" width="18" height="18" />
                  <span>Recent searches cleared</span>
                </div>
              {/if}
            </div>
          </div>
        </div>

        <!-- Account -->
        <div class="card bg-base-100 shadow-sm border border-base-content/5">
          <div class="card-body p-6">
            <h2
              class="text-lg font-bold text-base-content mb-4 flex items-center gap-2"
            >
              <Icon icon="lucide:user" width="22" height="22" />
              Account
            </h2>
            <div class="space-y-2">
              <a
                href="/profile"
                class="flex items-center justify-between p-3 rounded-lg hover:bg-base-200 transition-colors"
              >
                <span class="font-medium text-base-content">Profile</span>
                <Icon icon="lucide:chevron-right" width="20" height="20" />
              </a>
              <a
                href="/help"
                class="flex items-center justify-between p-3 rounded-lg hover:bg-base-200 transition-colors"
              >
                <span class="font-medium text-base-content">Help Center</span>
                <Icon icon="lucide:chevron-right" width="20" height="20" />
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</StudentLayout>

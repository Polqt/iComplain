<script lang="ts">
  import Icon from "@iconify/svelte";
  import StudentLayout from "../../layout/StudentLayout.svelte";
  import { authStore } from "../../../stores/auth.store.ts";
  import type { User } from "../../../types/user.ts";
  import { deriveNameFromEmail, getInitials } from "../../../utils/userConfig.ts";

  let user: User | null = null;
  let isLoading: boolean = true;

  $: ({ user, isLoading } = $authStore);
</script>

<svelte:head>
  <title>Student Profile - iComplain</title>
</svelte:head>

<StudentLayout>
  {#if isLoading}
    <div class="flex justify-center items-center min-h-[40vh]">
      <span class="loading loading-spinner loading-lg"></span>
    </div>
  {:else if user}
    {@const displayName = user.name || deriveNameFromEmail(user.email) || "Student"}
    <div class="max-w-3xl mx-auto space-y-6">
      <div class="card bg-base-100 shadow-sm border border-base-content/5">
        <div class="card-body p-6">
          <div class="flex items-start gap-4">
            <div class="avatar">
              <div class="w-16 h-16 rounded-full ring-2 ring-base-300 ring-offset-2 ring-offset-base-100 overflow-hidden">
                {#if user.avatar}
                  <img src={user.avatar} alt={displayName} />
                {:else}
                  <div class="w-full h-full bg-primary text-primary-content flex items-center justify-center font-bold text-lg">
                    {getInitials(displayName)}
                  </div>
                {/if}
              </div>
            </div>

            <div class="flex-1 min-w-0">
              <h1 class="text-2xl font-black text-base-content truncate">
                {displayName}
              </h1>
              <p class="text-sm text-base-content/60 truncate">{user.email}</p>
              <div class="mt-2 flex items-center gap-2">
                <span class="badge badge-primary badge-sm">{user.role}</span>
              </div>
            </div>
          </div>

          <div class="divider my-5"></div>

          <div class="text-sm text-base-content/70 flex items-start gap-2">
            <Icon icon="mdi:information-outline" width="18" height="18" class="mt-0.5" />
            <p>
              Profile customization (avatar upload, name editing) is coming soon.
              For now, your name and avatar come from Google sign-in when available.
            </p>
          </div>
        </div>
      </div>
    </div>
  {:else}
    <div class="max-w-xl mx-auto">
      <div class="alert alert-warning">
        <Icon icon="mdi:alert" width="20" height="20" />
        <span>You’re not signed in.</span>
      </div>
    </div>
  {/if}
</StudentLayout>

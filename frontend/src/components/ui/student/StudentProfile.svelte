<script lang="ts">
  import Icon from "@iconify/svelte";
  import StudentLayout from "../../layout/StudentLayout.svelte";
  import AvatarUploadModal from "../../common/AvatarUploadModal.svelte";
  import { authStore } from "../../../stores/auth.store.ts";
  import type { User } from "../../../types/user.ts";
  import { deriveNameFromEmail, getInitials } from "../../../utils/userConfig.ts";
  import { updateProfile, uploadAvatar, deleteAvatar } from "../../../lib/api/user.ts";

  let user: User | null = null;
  let isLoading: boolean = true;

  let isEditing = false;
  let editName = "";
  let isSaving = false;
  let errorMessage = "";
  let successMessage = "";
  let showAvatarModal = false;

  $: ({ user, isLoading } = $authStore);
  $: displayName = user?.name || deriveNameFromEmail(user?.email || "") || "Student";

  function startEditing() {
    editName = user?.name || "";
    isEditing = true;
    errorMessage = "";
    successMessage = "";
  }

  function cancelEditing() {
    isEditing = false;
    editName = "";
    errorMessage = "";
  }

  async function handleAvatarSave(file: File) {
    isSaving = true;
    try {
      const updatedUser = await uploadAvatar(file);
      authStore.updateUser(updatedUser);
      successMessage = "Avatar updated!";
      setTimeout(() => (successMessage = ""), 3000);
    } finally {
      isSaving = false;
    }
  }

  async function handleAvatarRemove() {
    isSaving = true;
    try {
      const updatedUser = await deleteAvatar();
      authStore.updateUser(updatedUser);
      successMessage = "Avatar removed!";
      setTimeout(() => (successMessage = ""), 3000);
    } finally {
      isSaving = false;
    }
  }

  async function saveProfile() {
    if (!editName.trim()) {
      errorMessage = "Name cannot be empty.";
      return;
    }

    if (editName.trim().length > 150) {
      errorMessage = "Name must be 150 characters or fewer.";
      return;
    }

    isSaving = true;
    errorMessage = "";

    try {
      const updatedUser = await updateProfile({ name: editName.trim() });
      authStore.updateUser(updatedUser);
      isEditing = false;
      successMessage = "Profile updated successfully!";
      setTimeout(() => (successMessage = ""), 3000);
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : "Failed to update profile.";
    } finally {
      isSaving = false;
    }
  }
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
    <div class="max-w-3xl mx-auto space-y-6">
      {#if successMessage}
        <div class="alert alert-success shadow-sm">
          <Icon icon="mdi:check-circle" width="20" height="20" />
          <span>{successMessage}</span>
        </div>
      {/if}

      <div class="card bg-base-100 shadow-sm border border-base-content/5">
        <div class="card-body p-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-bold text-base-content">Profile Information</h2>
            {#if !isEditing}
              <button
                type="button"
                class="btn btn-ghost btn-sm gap-2"
                onclick={startEditing}
              >
                <Icon icon="mdi:pencil" width="16" height="16" />
                Edit
              </button>
            {/if}
          </div>

          <div class="flex items-start gap-5">
            <div class="relative group">
              <div class="avatar">
                <div class="w-24 h-24 rounded-full ring-2 ring-base-300 ring-offset-2 ring-offset-base-100 overflow-hidden">
                  {#if user.avatar}
                    <img src={user.avatar} alt={displayName} />
                  {:else}
                    <div class="w-full h-full bg-primary text-primary-content flex items-center justify-center font-bold text-2xl">
                      {getInitials(displayName)}
                    </div>
                  {/if}
                </div>
              </div>
              <button
                type="button"
                class="absolute inset-0 flex items-center justify-center bg-black/50 rounded-full opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer"
                onclick={() => (showAvatarModal = true)}
                aria-label="Change avatar"
              >
                <Icon icon="mdi:camera" width="24" height="24" class="text-white" />
              </button>
            </div>

            <div class="flex-1 min-w-0">
              {#if isEditing}
                <div class="space-y-4">
                  {#if errorMessage}
                    <div class="alert alert-error text-sm py-2">
                      <Icon icon="mdi:alert-circle" width="18" height="18" />
                      <span>{errorMessage}</span>
                    </div>
                  {/if}

                  <div class="form-control">
                    <label for="edit-name" class="label">
                      <span class="label-text font-medium">Display Name</span>
                    </label>
                    <input
                      id="edit-name"
                      type="text"
                      class="input input-bordered w-full max-w-md"
                      placeholder="Enter your name"
                      bind:value={editName}
                      disabled={isSaving}
                      maxlength="150"
                    />
                    <label for="edit-name" class="label">
                      <span class="label-text-alt text-base-content/50">
                        {editName.length}/150 characters
                      </span>
                    </label>
                  </div>

                  <div class="flex gap-2">
                    <button
                      type="button"
                      class="btn btn-primary btn-sm"
                      onclick={saveProfile}
                      disabled={isSaving}
                    >
                      {#if isSaving}
                        <span class="loading loading-spinner loading-xs"></span>
                        Saving...
                      {:else}
                        <Icon icon="mdi:check" width="16" height="16" />
                        Save
                      {/if}
                    </button>
                    <button
                      type="button"
                      class="btn btn-ghost btn-sm"
                      onclick={cancelEditing}
                      disabled={isSaving}
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              {:else}
                <h1 class="text-2xl font-black text-base-content truncate">
                  {displayName}
                </h1>
                <div class="mt-3 flex items-center gap-2">
                  <span class="badge badge-primary badge-sm capitalize">{user.role}</span>
                  {#if user.is_active}
                    <span class="badge badge-success badge-sm badge-outline">Active</span>
                  {/if}
                </div>
              {/if}
            </div>
          </div>

          {#if !isEditing}
            <div class="divider my-5"></div>

            <div class="grid gap-4 sm:grid-cols-2">
              <div class="bg-base-200/50 rounded-lg p-4">
                <div class="flex items-center gap-2 text-base-content/60 mb-1">
                  <Icon icon="mdi:email-outline" width="16" height="16" />
                  <span class="text-xs font-medium uppercase tracking-wider">Email</span>
                </div>
                <p class="text-sm font-medium text-base-content truncate">{user.email}</p>
              </div>

              <div class="bg-base-200/50 rounded-lg p-4">
                <div class="flex items-center gap-2 text-base-content/60 mb-1">
                  <Icon icon="mdi:account-outline" width="16" height="16" />
                  <span class="text-xs font-medium uppercase tracking-wider">Role</span>
                </div>
                <p class="text-sm font-medium text-base-content capitalize">{user.role}</p>
              </div>
            </div>
          {/if}
        </div>
      </div>
    </div>

    <AvatarUploadModal
      show={showAvatarModal}
      currentAvatar={user.avatar}
      {displayName}
      {isSaving}
      onSave={handleAvatarSave}
      onRemove={handleAvatarRemove}
      onClose={() => (showAvatarModal = false)}
    />
  {:else}
    <div class="max-w-xl mx-auto">
      <div class="alert alert-warning">
        <Icon icon="mdi:alert" width="20" height="20" />
        <span>You're not signed in.</span>
      </div>
    </div>
  {/if}
</StudentLayout>

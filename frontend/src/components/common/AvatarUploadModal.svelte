<script lang="ts">
  import Icon from "@iconify/svelte";
  import { getInitials } from "../../utils/userConfig.ts";
  import { AVATAR_UPLOAD, validateImageFile } from "../../utils/uploadConfig.ts";

  export let show: boolean = false;
  export let currentAvatar: string | null = null;
  export let displayName: string = "";
  export let isSaving: boolean = false;
  export let onSave: (file: File) => Promise<void>;
  export let onRemove: () => Promise<void>;
  export let onClose: () => void;

  let selectedFile: File | null = null;
  let previewUrl: string | null = null;
  let errorMessage: string = "";
  let fileInputRef: HTMLInputElement;

  function handleClose() {
    selectedFile = null;
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
      previewUrl = null;
    }
    errorMessage = "";
    onClose();
  }

  function handleFileSelect(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    
    if (!file) return;

    const validation = validateImageFile(file);
    if (!validation.valid) {
      errorMessage = validation.error!;
      return;
    }

    errorMessage = "";
    selectedFile = file;
    
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    previewUrl = URL.createObjectURL(file);
  }

  function triggerFileInput() {
    fileInputRef?.click();
  }

  async function handleSave() {
    if (!selectedFile) return;
    errorMessage = "";
    try {
      await onSave(selectedFile);
      handleClose();
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : "Failed to upload avatar.";
    }
  }

  async function handleRemove() {
    errorMessage = "";
    try {
      await onRemove();
      handleClose();
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : "Failed to remove avatar.";
    }
  }

  $: if (!show) {
    selectedFile = null;
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
      previewUrl = null;
    }
    errorMessage = "";
  }
</script>

{#if show}
  <div class="modal modal-open">
    <div class="modal-box">
      <h3 class="font-bold text-lg mb-4">Change Profile Picture</h3>
      
      <div class="flex justify-center mb-6">
        <div class="avatar">
          <div class="w-32 h-32 rounded-full ring-2 ring-base-300 overflow-hidden">
            {#if previewUrl}
              <img src={previewUrl} alt="Preview" />
            {:else if currentAvatar}
              <img src={currentAvatar} alt={displayName} />
            {:else}
              <div class="w-full h-full bg-primary text-primary-content flex items-center justify-center font-bold text-3xl">
                {getInitials(displayName)}
              </div>
            {/if}
          </div>
        </div>
      </div>

      {#if errorMessage}
        <div class="alert alert-error text-sm mb-4">
          <Icon icon="mdi:alert-circle" width="18" height="18" />
          <span>{errorMessage}</span>
        </div>
      {/if}

      <input
        type="file"
        accept={AVATAR_UPLOAD.allowedTypes.join(',')}
        class="hidden"
        bind:this={fileInputRef}
        onchange={handleFileSelect}
      />

      <div class="space-y-3">
        <button
          type="button"
          class="btn btn-outline btn-block gap-2"
          onclick={triggerFileInput}
          disabled={isSaving}
        >
          <Icon icon="mdi:upload" width="20" height="20" />
          {selectedFile ? 'Choose Different Photo' : 'Upload Photo'}
        </button>

        {#if selectedFile}
          <div class="text-sm text-base-content/60 text-center">
            Selected: {selectedFile.name} ({(selectedFile.size / 1024 / 1024).toFixed(2)} MB)
          </div>
        {/if}

        <p class="text-xs text-base-content/50 text-center">
          {AVATAR_UPLOAD.allowedTypesDisplay}. Max {AVATAR_UPLOAD.maxFileSize / 1024 / 1024}MB.
        </p>
      </div>

      {#if currentAvatar && !selectedFile}
        <div class="divider text-xs text-base-content/40">OR</div>
        <button
          type="button"
          class="btn btn-error btn-outline btn-block btn-sm gap-2"
          onclick={handleRemove}
          disabled={isSaving}
        >
          {#if isSaving}
            <span class="loading loading-spinner loading-xs"></span>
          {:else}
            <Icon icon="mdi:delete" width="18" height="18" />
          {/if}
          Remove Current Photo
        </button>
      {/if}

      <div class="modal-action">
        <button 
          type="button" 
          class="btn btn-ghost" 
          onclick={handleClose}
          disabled={isSaving}
        >
          Cancel
        </button>
        {#if selectedFile}
          <button
            type="button"
            class="btn btn-primary"
            onclick={handleSave}
            disabled={isSaving}
          >
            {#if isSaving}
              <span class="loading loading-spinner loading-xs"></span>
              Uploading...
            {:else}
              Save
            {/if}
          </button>
        {/if}
      </div>
    </div>
    <button type="button" class="modal-backdrop" onclick={handleClose} aria-label="Close modal"></button>
  </div>
{/if}

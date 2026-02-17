<script lang="ts">
  import Icon from "@iconify/svelte";

  export let error: string | null;
  export let onRetry: () => void;
  export let retryLabel: string = "Retry";
</script>

<div class="flex flex-col items-center justify-center flex-1 gap-3">
  <div
    class="w-12 h-12 rounded-2xl bg-error/8 flex items-center justify-center"
  >
    <Icon
      icon="mdi:alert-circle-outline"
      width="22"
      height="22"
      class="text-error/50"
    />
  </div>
  <div class="text-sm text-base-content/50">{error}</div>
  <button
    class="btn btn-ghost btn-xs rounded-lg gap-1.5"
    onclick={onRetry}
  >
    <Icon icon="mdi:refresh" width="13" height="13" />
    {retryLabel}
  </button>
</div>

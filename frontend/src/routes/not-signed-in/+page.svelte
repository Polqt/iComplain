<script lang="ts">
  import { goto } from "$app/navigation";
  import Icon from "@iconify/svelte";

  function handleSignIn(): void {
    goto("/signin");
  }

  function handleGoHome(): void {
    goto("/");
  }
</script>

<div
  class="min-h-screen flex flex-col items-center justify-center bg-base-100 px-6"
>
  <div class="w-full max-w-md">
    <div class="flex justify-center mb-10">
      <div class="badge badge-outline gap-2 py-3 px-4">
        <div class="w-1.5 h-1.5 rounded-full bg-warning animate-pulse"></div>
        <span
          class="text-xs font-semibold tracking-widest uppercase text-base-content/50"
          >401 · Not Authenticated</span
        >
      </div>
    </div>

    <div
      class="card bg-base-100 border border-base-content/8 shadow-sm hover:shadow-md transition-shadow duration-500"
    >
      <div class="card-body p-10 text-center">
        <div class="flex justify-center mb-8">
          <div class="relative">
            <div
              class="w-16 h-16 rounded-full border border-warning/30 flex items-center justify-center"
            >
              <Icon
                icon="mdi:lock-open-variant-outline"
                width="24"
                height="24"
                class="text-warning"
              />
            </div>
            <div
              class="absolute inset-0 rounded-full border border-warning/10 animate-ping"
            ></div>
          </div>
        </div>

        <h1 class="text-2xl font-black text-base-content tracking-tight mb-3">
          Not Signed In
        </h1>

        <div
          class="w-10 h-0.5 bg-linear-to-r from-amber-500 via-sky-500 to-teal-500 mx-auto mb-4 rounded-full"
        ></div>

        <p
          class="text-sm text-base-content/45 leading-relaxed max-w-sm mx-auto mb-7"
        >
          Sign in to access this page. Your data and privacy are protected
          behind authentication.
        </p>

        <div
          class="border border-base-content/10 rounded-lg p-4 mb-7 bg-base-200/40"
        >
          <div class="flex items-start gap-3">
            <Icon
              icon="mdi:information-outline"
              width="16"
              height="16"
              class="text-base-content/40 mt-0.5 shrink-0"
            />
            <p class="text-xs text-base-content/45 text-left leading-relaxed">
              This page requires authentication. Sign in to continue.
            </p>
          </div>
        </div>

        <button
          class="btn btn-primary w-full group hover:scale-105 active:scale-95 hover:shadow-xl transition-all duration-200"
          onclick={handleSignIn}
        >
          <span class="flex items-center gap-2">
            Sign In
            <Icon
              icon="mdi:arrow-right"
              width="18"
              height="18"
              class="transition-transform group-hover:translate-x-1 duration-300"
            />
          </span>
        </button>

        <div class="mt-7">
          <button
            class="text-xs text-base-content/35 hover:text-base-content/55 transition-colors duration-200"
            onclick={handleGoHome}
          >
            Back to homepage
          </button>
        </div>
      </div>
    </div>
  </div>
</div>

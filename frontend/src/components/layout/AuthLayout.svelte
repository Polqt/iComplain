<script lang="ts">
  import { page } from "$app/stores";

  $: isSignIn = $page.url.pathname.includes("/signin");
</script>

<div class="min-h-screen flex flex-col lg:flex-row">
  <div
    class="relative lg:w-1/2 p-8 lg:p-12 flex flex-col justify-between overflow-hidden"
  >
    <div class="absolute inset-0 opacity-[0.03]"></div>

    <div class="relative z-10">
      <div class="flex items-center gap-3 mb-12">
        <div
          class="w-10 h-10 rounded-lg flex items-center justify-center"
        ></div>
      </div>

      <div class="max-w md">
        <h1 class="text-4xl lg:text-5xl text-base-content leading-tight mb-4">
          {isSignIn ? "The Campus Awaits" : "Start Making a Difference"}
        </h1>
        <p class="text-lg text-base-content/70 leading-relaxed mb-2">
          {isSignIn
            ? "Continue managing campus facilities with transparency and efficiency."
            : "Join the movement to create a better campus environment for every Lasallian."}
        </p>
      </div>
    </div>
  </div>
  <div
    class="lg:w-1/2 bg-base-100 flex items-center justify-center p-8 lg:p-12"
  >
    <div class="w-full max-w-md">
      <slot />
    </div>
  </div>
</div>

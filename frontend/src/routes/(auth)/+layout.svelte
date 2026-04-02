<script lang="ts">
  import { page } from "$app/state";
  import { onMount, type Snippet } from "svelte";

  let { children }: { children: Snippet } = $props();

  let isSignIn = $derived(page.url.pathname.includes("/signin"));

  onMount(() => {
    const saved = localStorage.getItem("lofi") || "lofi";
    document.documentElement.setAttribute("data-theme", saved);
  });
</script>

<div class="min-h-screen flex flex-col lg:flex-row">
  <!-- Left Side - Image Hero Section -->
  <div
    class="relative lg:w-1/2 bg-linear-to-br from-green-600 via-green-700 to-green-900 flex items-center justify-center overflow-hidden min-h-[40vh] lg:min-h-screen"
  >
    <!-- Background Image with Overlay -->
    <div class="absolute inset-0">
      <img
        src="/images/lasalle.jpg"
        alt="La Salle Campus"
        class="w-full h-full object-cover opacity-30"
      />
      <div
        class="absolute inset-0 bg-linear-to-br from-green-800/80 via-green-900/70 to-green-950/90"
      ></div>
    </div>

    <!-- Content -->
    <div class="relative z-10 px-8 py-12 lg:px-16 lg:py-20 w-full">
      <!-- Logo -->
      <div class="mb-16 lg:mb-20">
        <img
          src="/images/usls.png"
          alt="USLS Logo"
          class="h-16 lg:h-20 w-auto drop-shadow-2xl"
        />
      </div>

      <!-- Heading -->
      <div class="max-w-xl">
        <h1
          class="text-4xl lg:text-5xl xl:text-6xl font-bold text-white leading-[1.1] mb-6 lg:mb-8"
        >
          {isSignIn ? "Welcome Back, Lasallian" : "Join the Movement"}
        </h1>
        <p
          class="text-lg lg:text-xl text-green-50/90 leading-relaxed font-light"
        >
          {isSignIn
            ? "Continue your journey in making our campus a better place for everyone."
            : "Start making a difference in our campus community today."}
        </p>
      </div>
    </div>
  </div>

  <!-- Right Side - Form Section -->
  <div
    class="lg:w-1/2 bg-base-100 flex items-center justify-center p-6 sm:p-8 lg:p-12 xl:p-16 min-h-[60vh] lg:min-h-screen"
  >
    <div class="w-full max-w-md">
      {@render children()}
    </div>
  </div>
</div>

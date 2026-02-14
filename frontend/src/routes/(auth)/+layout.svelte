<script lang="ts">
  import { page } from "$app/stores";
  import Header from "../../components/layout/Header.svelte";

  $: isSignIn = $page.url.pathname.includes("/signin");
</script>

<div class="min-h-screen flex flex-col bg-base-100">
  <div class="w-full border-b border-base-300 px-4">
    <div class="max-w-7xl mx-auto px-6 lg:px-8">
      <Header />
    </div>
  </div>

  <div class="flex-1 flex flex-col lg:flex-row">
    <div
      class="lg:w-1/2 relative flex flex-col justify-center p-8 lg:p-16 bg-linear-to-br from-base-200/30 to-base-100"
    >
      <div class="absolute inset-0 overflow-hidden">
        <img
          src="/images/lasalle.jpg"
          alt="La Salle Campus"
          class="w-full h-full object-cover opacity-[0.08]"
        />
      </div>
      <div class="space-y-6">
        <h1
          class="text-4xl lg:text-5xl font-bold text-base-content tracking-tight"
        >
          {isSignIn ? "Welcome Back" : "Join iComplain"}
        </h1>

        <p class="text-lg text-base-content/70 leading-relaxed">
          {isSignIn
            ? "Access your dashboard to manage campus facilities with transparency and efficiency."
            : "Empower campus improvement through streamlined facility reporting and community collaboration."}
        </p>
      </div>
    </div>

    <div
      class="lg:w-1/2 flex items-center justify-center p-8 lg:p-16 bg-base-100"
    >
      <div class="w-full max-w-md">
        <slot />
      </div>
    </div>
  </div>
</div>

<script>
  import { goto } from "$app/navigation";
  import Icon from "@iconify/svelte";
  import Footer from "../components/layout/Footer.svelte";
  import Header from "../components/layout/Header.svelte";

  function handleGetStarted() {
    goto("/login");
  }

  function handleLearnMore() {
    goto("/learn-more");
  }
</script>

<div class="w-full flex flex-col items-center bg-base-100 min-h-screen">
  <div class="w-full max-w-7xl px-4 sm:px-6 lg:px-8">
    <Header />
  </div>

  <section class="w-full max-w-4xl px-4 sm:px-6 lg:px-8 pt-16 sm:pt-20 md:pt-24 pb-12 sm:pb-16 md:pb-20">
    <div class="flex flex-col gap-2 sm:gap-3 mb-8 sm:mb-10">
      <h1
        class="text-3xl sm:text-4xl md:text-5xl font-black text-base-content leading-none tracking-tight"
      >
        <span
          class="tooltip tooltip-right font-light"
          data-tip="Submit facility issues instantly"
        >
          <span
            class="inline-block hover:scale-110 hover:-rotate-2 active:scale-95 transition-all duration-300 cursor-default hover:text-amber-500 drop-shadow-sm font-black"
          >
            REPORT
          </span>
        </span>
        <span class="text-amber-500/30 animate-pulse">.</span>
      </h1>
      <h1
        class="text-3xl sm:text-4xl md:text-5xl font-black text-base-content leading-none tracking-tight"
      >
        <span
          class="tooltip tooltip-right font-light"
          data-tip="Monitor progress in real-time"
        >
          <span
            class="inline-block hover:scale-110 hover:rotate-2 active:scale-95 transition-all duration-300 cursor-default hover:text-sky-500 drop-shadow-sm font-black"
          >
            TRACK
          </span>
        </span>
        <span class="text-sky-500/30 animate-pulse [animation-delay:0.3s]"
          >.</span
        >
      </h1>
      <h1
        class="text-3xl sm:text-4xl md:text-5xl font-black text-base-content leading-none tracking-tight"
      >
        <span
          class="tooltip tooltip-right font-light"
          data-tip="Get issues fixed efficiently"
        >
          <span
            class="inline-block hover:scale-110 hover:-rotate-1 active:scale-95 transition-all duration-300 cursor-default hover:text-teal-500 drop-shadow-sm font-black"
          >
            RESOLVE
          </span>
        </span>
        <span class="text-teal-500/30 animate-pulse [animation-delay:0.6s]"
          >.</span
        >
      </h1>
    </div>

    <div class="relative mb-6 sm:mb-8">
      <div
        class="w-24 sm:w-32 h-1 bg-linear-to-r from-amber-200 via-sky-200 border-t border-base-content/10"
      ></div>
    </div>

    <div class="space-y-3">
      <p
        class="text-base sm:text-lg text-base-content/80 leading-relaxed max-w-2xl font-medium"
      >
        Transform campus facility management with
        <span class="relative inline-block group cursor-default">
          <span
            class="font-black text-sky-600 group-hover:text-sky-500 transition-colors"
          >
            iComplain
          </span>
          <span
            class="absolute -bottom-1 left-0 w-full h-1 bg-sky-500/30 scale-x-0 group-hover:scale-x-100 transition-transform origin-left duration-500 rounded-full"
          ></span>
        </span>.
      </p>
      <p class="text-sm sm:text-base text-base-content/60 leading-relaxed max-w-2xl">
        Report issues instantly, track progress in real-time, and ensure every
        concern gets the attention it deserves.
      </p>
    </div>

    <div class="mt-8 sm:mt-10 flex flex-col sm:flex-row gap-3 sm:gap-4">
      <button
        class="btn btn-primary btn-md sm:btn-lg group hover:scale-105 active:scale-95 hover:shadow-xl transition-all duration-200 w-full sm:w-auto"
        onclick={handleGetStarted}
      >
        <span class="flex items-center justify-center gap-2">
          Start Reporting
          <Icon
            icon="lucide:arrow-right"
            width="20"
            height="20"
            class="transition-transform group-hover:translate-x-1 duration-300"
          />
        </span></button
      >
      <button
        class="btn btn-outline btn-md sm:btn-lg group hover:scale-105 active:scale-95 hover:shadow-lg transition-all duration-200 w-full sm:w-auto"
        onclick={handleLearnMore}
      >
        <span class="flex items-center justify-center gap-2">
          Learn More
          <Icon
            icon="lucide:external-link"
            width="20"
            height="20"
            class="transition-transform group-hover:rotate-45 duration-300"
          />
        </span>
      </button>
    </div>
  </section>

  <div class="w-full max-w-7xl px-4 sm:px-6 lg:px-8 mt-auto">
    <div class="border-t border-base-content/10"></div>
    <Footer />
  </div>
</div>

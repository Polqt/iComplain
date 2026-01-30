<script>
  import { goto } from "$app/navigation";
  import Footer from "../components/layout/Footer.svelte";
  import Header from "../components/layout/Header.svelte";

  function handleGetStarted() {
    goto("/login");
  }

  function handleLearMore() {
    goto("/learn-more");
  }
</script>

<div class="w-full flex flex-col items-center">
  <div class="w-full max-w-7xl px-4">
    <Header />
  </div>
  <main class="flex-1 w-full max-w-7xl px-4">
    <div class="hero min-h-screen">
      <div class="hero-content text-center">
        <div class="max-w-md mx-auto px-4">
          <h1 class="text-5xl font-bold underline decoration-4 decoration-amber-500 hover:decoration-6 transition-all">REPORT.</h1>
          <h1 class="text-5xl font-bold underline decoration-4 decoration-sky-500 hover:decoration-6 transition-all">TRACK.</h1>
          <h1 class="text-5xl font-bold underline decoration-4 decoration-teal-500 hover:decoration-6 transition-all">RESOLVE.</h1>
          <p class="py-6">
            Transform campus facility management with <span class="underline decoration-sky-500 hover:decoration-2 transition-all ">iComplain</span>. Report issues
            instantly, track progress in real-time, and ensure every concern
            gets the attention it deserves.
          </p>
          <div>
            <button class="btn btn-primary" on:click={handleGetStarted}
              >Start Reporting</button
            >
            <button class="btn btn-primary" on:click={handleLearMore}
              >Learn More</button
            >
          </div>
        </div>
      </div>
    </div>
    <div class="divider items-center-safe max-w-7xl mx-auto"></div>
  </main>
  <div class="w-full max-w-7xl mx-auto px-4">
    <Footer />
  </div>
</div>

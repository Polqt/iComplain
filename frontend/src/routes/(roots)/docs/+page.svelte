<script>
  import Footer from "../../../components/layout/Footer.svelte";
  import Header from "../../../components/layout/Header.svelte";
</script>

<svelte:head>
  <title>Documents | iComplain</title>
</svelte:head>

<div class="w-full flex flex-col items-center bg-base-100 min-h-screen">
  <div class="w-full max-w-7xl px-4 sm:px-6 lg:px-8">
    <Header />
  </div>
  <div class="w-full max-w-7xl px-4 sm:px-6 lg:px-8 mt-auto">
    <div class="border-t border-base-content/10"></div>
    <Footer />
  </div>
</div>

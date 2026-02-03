<script>
  import Icon from "@iconify/svelte";
</script>

<footer class="footer footer-horizontal text-base-content items-center p-4 sm:p-6">
  <aside class="grid-flow-col items-center">
    <p class="text-sm sm:text-base">© {new Date().getFullYear()}. All rights reserved.</p>
  </aside>
  <nav class="grid-flow-col gap-3 sm:gap-4 md:place-self-center md:justify-self-end">
    <a
      aria-label="Github"
      href="https://github.com/Polqt/iComplain"
      target="_blank"
    >
      <Icon icon="mdi:github" width="24" height="24" />
    </a>
    <a aria-label="School" href="https://www.usls.edu.ph/" target="_blank">
      <Icon icon="mdi:school" width="24" height="24" />
    </a>
    <a
      aria-label="Facebook"
      href="https://www.facebook.com/lasallebcd"
      target="_blank"
    >
      <Icon icon="mdi:facebook" width="24" height="24" />
    </a>
  </nav>
</footer>

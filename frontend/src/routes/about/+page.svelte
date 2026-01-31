<script>
  import Header from "../../components/layout/Header.svelte";
</script>

<div class="w-full flex flex-col items-center bg-base-100 min-h-screen">
  <div class="w-full max-w-7xl px-4">
    <Header />
  </div>

  <section class="w-full max-w-3xl px-6 pt-24 pb-20">
    <p
      class="badge badge-ghost text-xs font-semibold tracking-widest uppercase mb-6"
    >
      About
    </p>
    <h1 class="text-5xl font-semibold text-base-content leading-tight">
      A better way to care for our campus.
    </h1>
    <div class="mt-6 w-12 h-px bg-base-content/20"></div>
    <p class="mt-6 text-base text-base-content/60 leading-relaxed max-w-2xl">
      iComplain was built to give every Lasallian a simple, transparent, and
      reliable way to report facility-related issues and to help the institution
      respond faster than ever.
    </p>
    <p class="mt-4 text-base text-base-content/60 leading-relaxed max-w-2xl">
      The platform connects students, administrators, and maintenance teams in
      one unified system that ensures issues are seen, tracked, and resolved
      efficiently. No more guessing. No more missing reports. Just a clear,
      campus-wide flow of responsible communication.
    </p>
  </section>

  <div class="w-full max-w-3xl px-6">
    <div class="border-t border-base-content/10"></div>
  </div>

  <section class="w-full max-w-3xl px-6 py-16">
    <p
      class="text-xs font-semibold tracking-widest uppercase text-base-content/35 mb-3"
    >
      Purpose
    </p>
    <h2 class="text-2xl font-semibold text-base-content">
      Why iComplain exists?
    </h2>
    <p class="mt-6 text-base text-base-content/60 leading-relaxed">
      A university thrives when its students feel supported by the environment
      around them. From classrooms and labs to restrooms and hallways,
      well-maintained facilities play an enormous role in shaping everyday
      learning.
    </p>
    <p class="mt-4 text-base text-base-content/60 leading-relaxed">
      iComplain was developed to solve a recurring problem at the University of
      St. La Salle — the lack of a centralized, visible, and accountable system
      for facility issue management. Students struggled to report problems, and
      administrators had no unified channel to track them.
    </p>
    <p class="mt-6 text-sm text-base-content/45 italic">
      iComplain bridges that gap with a platform that's easy for students and
      powerful for administrators.
    </p>
  </section>

  <div class="w-full max-w-3xl px-6">
    <div class="border-t border-base-content/10"></div>
  </div>

  <section class="w-full max-w-3xl px-6 py-16">
    <p
      class="text-xs font-semibold tracking-widest uppercase text-base-content/35 mb-3"
    >
      Solutions
    </p>
    <h2 class="text-2xl font-semibold text-base-content">
      What iComplain Solves
    </h2>

    <div
      class="mt-8 flex flex-col gap-px bg-base-content/8 rounded-lg overflow-hidden border border-base-content/10"
    >
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-px bg-base-content/8">
        <div class="bg-base-100 p-6 hover:bg-base-200 transition-colors">
          <p
            class="text-xs font-semibold text-base-content/35 uppercase tracking-wider mb-2"
          >
            01
          </p>
          <h3 class="text-sm font-semibold text-base-content">
            Centralized Reporting
          </h3>
          <p class="mt-2 text-sm text-base-content/50 leading-relaxed">
            All facility concerns, from AC failures to classroom lighting
            issues, are submitted through one system.
          </p>
        </div>
        <div class="bg-base-100 p-6 hover:bg-base-200 transition-colors">
          <p
            class="text-xs font-semibold text-base-content/35 uppercase tracking-wider mb-2"
          >
            02
          </p>
          <h3 class="text-sm font-semibold text-base-content">
            Faster Response Times
          </h3>
          <p class="mt-2 text-sm text-base-content/50 leading-relaxed">
            Maintenance teams get the information they need immediately:
            location, photos, timestamps, and severity.
          </p>
        </div>
        <div class="bg-base-100 p-6 hover:bg-base-200 transition-colors">
          <p
            class="text-xs font-semibold text-base-content/35 uppercase tracking-wider mb-2"
          >
            03
          </p>
          <h3 class="text-sm font-semibold text-base-content">
            Transparency & Accountability
          </h3>
          <p class="mt-2 text-sm text-base-content/50 leading-relaxed">
            Everyone sees progress. Every ticket has a status. Nothing
            disappears without a trace.
          </p>
        </div>
      </div>
    </div>
  </section>

  <div class="w-full max-w-3xl px-6">
    <div class="border-t border-base-content/10"></div>
  </div>

  <section class="w-full max-w-3xl px-6 py-16">
    <p
      class="text-xs font-semibold tracking-widest uppercase text-base-content/35 mb-3"
    >
      Process
    </p>
    <h2 class="text-2xl font-semibold text-base-content">How It Works</h2>

    <div class="mt-10 flex flex-col gap-0">
      <div class="flex gap-6">
        <div class="flex flex-col items-center">
          <div
            class="w-8 h-8 rounded-full border border-base-content/20 bg-base-100 flex items-center justify-center shrink-0"
          >
            <span class="text-xs font-semibold text-base-content/50">1</span>
          </div>
          <div class="w-px h-full bg-base-content/10 mt-1 mb-1 min-h-15"></div>
        </div>
        <div class="pb-8 pt-0.5">
          <h3 class="text-sm font-semibold text-base-content">
            Students Submit Issues
          </h3>
          <p class="mt-1 text-sm text-base-content/50 leading-relaxed">
            Attach photos, add details, and send with one click.
          </p>
        </div>
      </div>
      <div class="flex gap-6">
        <div class="flex flex-col items-center">
          <div
            class="w-8 h-8 rounded-full border border-base-content/20 bg-base-100 flex items-center justify-center shrink-0"
          >
            <span class="text-xs font-semibold text-base-content/50">2</span>
          </div>
          <div class="w-px h-full bg-base-content/10 mt-1 mb-1 min-h-15"></div>
        </div>
        <div class="pb-8 pt-0.5">
          <h3 class="text-sm font-semibold text-base-content">
            Admins Review Issues
          </h3>
          <p class="mt-1 text-sm text-base-content/50 leading-relaxed">
            Tickets are prioritized and assigned.
          </p>
        </div>
      </div>
      <div class="flex gap-6">
        <div class="flex flex-col items-center">
          <div
            class="w-8 h-8 rounded-full border border-base-content/20 bg-base-100 flex items-center justify-center shrink-0"
          >
            <span class="text-xs font-semibold text-base-content/50">3</span>
          </div>
        </div>
        <div class="pt-0.5">
          <h3 class="text-sm font-semibold text-base-content">
            Maintenance Teams Resolve Issues
          </h3>
          <p class="mt-1 text-sm text-base-content/50 leading-relaxed">
            Updates are logged, and students receive notifications instantly.
          </p>
        </div>
      </div>
    </div>
  </section>

  <div class="w-full max-w-3xl px-6">
    <div class="border-t border-base-content/10"></div>
  </div>

  <section class="w-full max-w-3xl px-6 py-16">
    <p
      class="text-xs font-semibold tracking-widest uppercase text-base-content/35 mb-3"
    >
      Team
    </p>
    <h2 class="text-2xl font-semibold text-base-content">Meet the Team</h2>

    <div class="mt-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div
        class="border border-base-content/10 rounded-lg p-5 bg-base-100 hover:bg-base-200 transition-colors"
      >
        <p
          class="text-xs font-semibold text-base-content/35 uppercase tracking-wider mb-3"
        >
          Developer & Administrator
        </p>
        <h3 class="text-sm font-semibold text-base-content">Maulvi Limpao</h3>
        <p class="mt-2 text-sm text-base-content/50 leading-relaxed">
          Full-Stack Developer & Database Administrator
        </p>
      </div>
      <div
        class="border border-base-content/10 rounded-lg p-5 bg-base-100 hover:bg-base-200 transition-colors"
      >
        <p
          class="text-xs font-semibold text-base-content/35 uppercase tracking-wider mb-3"
        >
          Developer & Designer
        </p>
        <h3 class="text-sm font-semibold text-base-content">Franz Fortaleza</h3>
        <p class="mt-2 text-sm text-base-content/50 leading-relaxed">
          Full-Stack Developer & UI/UX Designer
        </p>
      </div>
      <div
        class="border border-base-content/10 rounded-lg p-5 bg-base-100 hover:bg-base-200 transition-colors"
      >
        <p
          class="text-xs font-semibold text-base-content/35 uppercase tracking-wider mb-3"
        >
          Developer & Lead
        </p>
        <h3 class="text-sm font-semibold text-base-content">Janpol Hidalgo</h3>
        <p class="mt-2 text-sm text-base-content/50 leading-relaxed">
          Full-Stack Developer & Project Manager
        </p>
      </div>
      <div
        class="border border-base-content/10 rounded-lg p-5 bg-base-100 hover:bg-base-200 transition-colors"
      >
        <p
          class="text-xs font-semibold text-base-content/35 uppercase tracking-wider mb-3"
        >
          Developer & QA Engineer
        </p>
        <h3 class="text-sm font-semibold text-base-content">Owen Espanola</h3>
        <p class="mt-2 text-sm text-base-content/50 leading-relaxed">
          Full-Stack Developer & QA Tester
        </p>
      </div>
    </div>
  </section>

  <div class="w-full max-w-3xl px-6">
    <div class="border-t border-base-content/10"></div>
  </div>

  <section class="w-full max-w-3xl px-6 py-16 pb-28">
    <p
      class="text-xs font-semibold tracking-widest uppercase text-base-content/35 mb-3"
    >
      Our Commitment
    </p>
    <h2 class="text-2xl font-semibold text-base-content">Commitment to USLS</h2>
    <p class="mt-6 text-base text-base-content/60 leading-relaxed">
      iComplain was created specifically for the University of St. La Salle -
      Bacolod, tailored to the unique needs of its students and administrators.
      This isn't a generic solution; it's built with community, context, and
      campus culture in mind.
    </p>
  </section>
</div>

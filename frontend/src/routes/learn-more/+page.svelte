<script>
  import Footer from "../../components/layout/Footer.svelte";
  import Header from "../../components/layout/Header.svelte";
</script>

<div class="w-full flex flex-col items-center bg-base-100 min-h-screen">
  <div class="w-full max-w-7xl px-4 sm:px-6 lg:px-8">
    <Header />
  </div>

  <section class="w-full max-w-4xl px-4 sm:px-6 lg:px-8 pt-16 sm:pt-20 md:pt-24 pb-12 sm:pb-16 md:pb-20">
    <p
      class="badge badge-ghost text-xs font-semibold tracking-widest uppercase mb-4 sm:mb-6"
    >
      Learn More
    </p>
    <h1 class="text-3xl sm:text-4xl md:text-5xl font-semibold text-base-content leading-tight">
      Making campus maintenance simpler, smarter, and more transparent
    </h1>
    <div class="mt-4 sm:mt-6 w-8 sm:w-12 h-px bg-base-content/20"></div>
    <p class="mt-4 sm:mt-6 text-sm sm:text-base text-base-content/60 leading-relaxed max-w-2xl">
      Learn how iComplain transforms facility reporting into a structured system
      that empowers students and streamlines administrative work across the USLS
      campus.
    </p>
  </section>

  <div class="w-full max-w-4xl px-4 sm:px-6 lg:px-8">
    <div class="border-t border-base-content/10"></div>
  </div>

  <section class="w-full max-w-4xl px-4 sm:px-6 lg:px-8 py-12 sm:py-16">
    <p
      class="text-xs font-semibold tracking-widest uppercase text-base-content/35 mb-3"
    >
      Overview
    </p>
    <h2 class="text-xl sm:text-2xl font-semibold text-base-content">What is iComplain?</h2>
    <p class="text-xs sm:text-sm text-base-content/45 mt-1">
      A centralized system for reporting and resolving facility issues
    </p>
    <p class="mt-4 sm:mt-6 text-sm sm:text-base text-base-content/60 leading-relaxed">
      iComplain acts as the reporting hub for all facility-related concerns
      within the University of St. La Salle. Instead of scattered messages,
      unclear requests, or lost reports, the system gathers every complaint into
      one organized space.
    </p>
    <div class="mt-6 sm:mt-8 flex flex-col gap-3">
      <div class="flex items-start gap-3 group">
        <div
          class="mt-1.5 w-1.5 h-1.5 rounded-full bg-base-content/25 group-hover:bg-base-content/50 transition-colors shrink-0"
        ></div>
        <p class="text-sm sm:text-base text-base-content/60">
          Built for <span class="text-base-content/80 font-medium">clarity</span
          > — every report has a place and a path.
        </p>
      </div>
      <div class="flex items-start gap-3 group">
        <div
          class="mt-1.5 w-1.5 h-1.5 rounded-full bg-base-content/25 group-hover:bg-base-content/50 transition-colors shrink-0"
        ></div>
        <p class="text-sm sm:text-base text-base-content/60">
          Built for <span class="text-base-content/80 font-medium"
            >accountability</span
          > — actions are tracked, not forgotten.
        </p>
      </div>
      <div class="flex items-start gap-3 group">
        <div
          class="mt-1.5 w-1.5 h-1.5 rounded-full bg-base-content/25 group-hover:bg-base-content/50 transition-colors shrink-0"
        ></div>
        <p class="text-sm sm:text-base text-base-content/60">
          Built for <span class="text-base-content/80 font-medium"
            >students</span
          > — the people who depend on reliable facilities every day.
        </p>
      </div>
    </div>
  </section>

  <div class="w-full max-w-4xl px-4 sm:px-6 lg:px-8">
    <div class="border-t border-base-content/10"></div>
  </div>

  <section class="w-full max-w-4xl px-4 sm:px-6 lg:px-8 py-12 sm:py-16">
    <p
      class="text-xs font-semibold tracking-widest uppercase text-base-content/35 mb-3"
    >
      Capabilities
    </p>
    <h2 class="text-xl sm:text-2xl font-semibold text-base-content">Key Capabilities</h2>

    <div
      class="mt-6 sm:mt-8 flex flex-col gap-px bg-base-content/8 rounded-lg overflow-hidden border border-base-content/10"
    >
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-px bg-base-content/8">
        <div class="bg-base-100 p-4 sm:p-6 hover:bg-base-200 transition-colors">
          <p
            class="text-xs font-semibold text-base-content/35 uppercase tracking-wider mb-2"
          >
            01
          </p>
          <h3 class="text-sm font-semibold text-base-content">
            Streamlined Ticket Submission
          </h3>
          <p class="mt-2 text-xs sm:text-sm text-base-content/50 leading-relaxed">
            Submit issues in seconds with photos, location tags, and severity
            levels.
          </p>
        </div>
        <div class="bg-base-100 p-4 sm:p-6 hover:bg-base-200 transition-colors">
          <p
            class="text-xs font-semibold text-base-content/35 uppercase tracking-wider mb-2"
          >
            02
          </p>
          <h3 class="text-sm font-semibold text-base-content">
            Role-Based Access
          </h3>
          <p class="mt-2 text-xs sm:text-sm text-base-content/50 leading-relaxed">
            Students report. Administrators manage. Maintenance teams resolve,
            each with the right level of access.
          </p>
        </div>
        <div class="bg-base-100 p-4 sm:p-6 hover:bg-base-200 transition-colors">
          <p
            class="text-xs font-semibold text-base-content/35 uppercase tracking-wider mb-2"
          >
            03
          </p>
          <h3 class="text-sm font-semibold text-base-content">
            Notifications & Updates
          </h3>
          <p class="mt-2 text-xs sm:text-sm text-base-content/50 leading-relaxed">
            Real-time notifications keep you informed on every status change.
          </p>
        </div>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-px bg-base-content/8">
        <div class="bg-base-100 p-4 sm:p-6 hover:bg-base-200 transition-colors">
          <p
            class="text-xs font-semibold text-base-content/35 uppercase tracking-wider mb-2"
          >
            04
          </p>
          <h3 class="text-sm font-semibold text-base-content">
            Comment System
          </h3>
          <p class="mt-2 text-xs sm:text-sm text-base-content/50 leading-relaxed">
            Students, admins, and maintenance staff can communicate directly
            within each ticket for clarity.
          </p>
        </div>
        <div class="bg-base-100 p-4 sm:p-6 hover:bg-base-200 transition-colors">
          <p
            class="text-xs font-semibold text-base-content/35 uppercase tracking-wider mb-2"
          >
            05
          </p>
          <h3 class="text-sm font-semibold text-base-content">
            Full Audit Trail
          </h3>
          <p class="mt-2 text-xs sm:text-sm text-base-content/50 leading-relaxed">
            Every action is logged, ensuring transparency and accountability
            throughout the entire resolution process.
          </p>
        </div>
      </div>
    </div>
  </section>

  <div class="w-full max-w-4xl px-4 sm:px-6 lg:px-8">
    <div class="border-t border-base-content/10"></div>
  </div>

  <section class="w-full max-w-4xl px-4 sm:px-6 lg:px-8 py-12 sm:py-16">
    <p
      class="text-xs font-semibold tracking-widest uppercase text-base-content/35 mb-3"
    >
      Motivation
    </p>
    <h2 class="text-xl sm:text-2xl font-semibold text-base-content">
      Why a Dedicated System Matters?
    </h2>
    <p class="mt-3 sm:mt-4 text-sm sm:text-base text-base-content/60 leading-relaxed">
      Most universities rely on scattered communication; email, messenger,
      handwritten logs, or verbal reports. These methods are easy to forget,
      hard to track, and impossible to measure. iComplain solves this by
      digitizing the entire process.
    </p>

    <div
      class="mt-6 sm:mt-8 border border-base-content/10 rounded-lg p-4 sm:p-6 bg-base-200/40"
    >
      <p
        class="text-xs font-semibold text-base-content/40 uppercase tracking-wider mb-3 sm:mb-4"
      >
        What the institution gains
      </p>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-y-3 gap-x-6 sm:gap-x-8">
        <div class="flex items-center gap-3">
          <div
            class="w-1.5 h-1.5 rounded-full bg-base-content/30 shrink-0"
          ></div>
          <p class="text-xs sm:text-sm text-base-content/65">Traceable case history</p>
        </div>
        <div class="flex items-center gap-3">
          <div
            class="w-1.5 h-1.5 rounded-full bg-base-content/30 shrink-0"
          ></div>
          <p class="text-xs sm:text-sm text-base-content/65">
            Accountability across departments
          </p>
        </div>
        <div class="flex items-center gap-3">
          <div
            class="w-1.5 h-1.5 rounded-full bg-base-content/30 shrink-0"
          ></div>
          <p class="text-xs sm:text-sm text-base-content/65">Faster turnaround times</p>
        </div>
        <div class="flex items-center gap-3">
          <div
            class="w-1.5 h-1.5 rounded-full bg-base-content/30 shrink-0"
          ></div>
          <p class="text-xs sm:text-sm text-base-content/65">
            Better decision-making through data
          </p>
        </div>
        <div class="flex items-center gap-3 sm:col-span-2">
          <div
            class="w-1.5 h-1.5 rounded-full bg-base-content/30 shrink-0"
          ></div>
          <p class="text-xs sm:text-sm text-base-content/65">
            Increased student satisfaction
          </p>
        </div>
      </div>
    </div>

    <p class="mt-4 sm:mt-6 text-xs sm:text-sm text-base-content/45 italic">
      A centralized system isn't just convenient, it's foundational to a
      well-run campus.
    </p>
  </section>

  <div class="w-full max-w-4xl px-4 sm:px-6 lg:px-8">
    <div class="border-t border-base-content/10"></div>
  </div>

  <section class="w-full max-w-4xl px-4 sm:px-6 lg:px-8 py-12 sm:py-16">
    <p
      class="text-xs font-semibold tracking-widest uppercase text-base-content/35 mb-3"
    >
      Process
    </p>
    <h2 class="text-xl sm:text-2xl font-semibold text-base-content">The Workflow</h2>

    <div class="mt-8 sm:mt-10 flex flex-col gap-0">
      <div class="flex gap-4 sm:gap-6">
        <div class="flex flex-col items-center">
          <div
            class="w-6 sm:w-8 h-6 sm:h-8 rounded-full border border-base-content/20 bg-base-100 flex items-center justify-center shrink-0"
          >
            <span class="text-xs font-semibold text-base-content/50">1</span>
          </div>
          <div class="w-px h-full bg-base-content/10 mt-1 mb-1 min-h-12 sm:min-h-15"></div>
        </div>
        <div class="pb-6 sm:pb-8 pt-0.5">
          <h3 class="text-sm font-semibold text-base-content">Report</h3>
          <p class="mt-1 text-xs sm:text-sm text-base-content/50 leading-relaxed">
            Students report a facility issue through the online form.
          </p>
        </div>
      </div>
      <div class="flex gap-4 sm:gap-6">
        <div class="flex flex-col items-center">
          <div
            class="w-6 sm:w-8 h-6 sm:h-8 rounded-full border border-base-content/20 bg-base-100 flex items-center justify-center shrink-0"
          >
            <span class="text-xs font-semibold text-base-content/50">2</span>
          </div>
          <div class="w-px h-full bg-base-content/10 mt-1 mb-1 min-h-12 sm:min-h-15"></div>
        </div>
        <div class="pb-6 sm:pb-8 pt-0.5">
          <h3 class="text-sm font-semibold text-base-content">Review</h3>
          <p class="mt-1 text-xs sm:text-sm text-base-content/50 leading-relaxed">
            Admins verify information, classify the issue, and assign it to the
            right team.
          </p>
        </div>
      </div>
      <div class="flex gap-4 sm:gap-6">
        <div class="flex flex-col items-center">
          <div
            class="w-6 sm:w-8 h-6 sm:h-8 rounded-full border border-base-content/20 bg-base-100 flex items-center justify-center shrink-0"
          >
            <span class="text-xs font-semibold text-base-content/50">3</span>
          </div>
          <div class="w-px h-full bg-base-content/10 mt-1 mb-1 min-h-12 sm:min-h-15"></div>
        </div>
        <div class="pb-6 sm:pb-8 pt-0.5">
          <h3 class="text-sm font-semibold text-base-content">Resolve</h3>
          <p class="mt-1 text-xs sm:text-sm text-base-content/50 leading-relaxed">
            Maintenance staff perform repairs or inspections and update the
            system.
          </p>
        </div>
      </div>
      <div class="flex gap-4 sm:gap-6">
        <div class="flex flex-col items-center">
          <div
            class="w-6 sm:w-8 h-6 sm:h-8 rounded-full border border-base-content/20 bg-base-100 flex items-center justify-center shrink-0"
          >
            <span class="text-xs font-semibold text-base-content/50">4</span>
          </div>
        </div>
        <div class="pt-0.5">
          <h3 class="text-sm font-semibold text-base-content">
            Confirm & Close
          </h3>
          <p class="mt-1 text-xs sm:text-sm text-base-content/50 leading-relaxed">
            Students receive status updates and admins close the ticket once
            resolved.
          </p>
        </div>
      </div>
    </div>
  </section>

  <div class="w-full max-w-4xl px-4 sm:px-6 lg:px-8">
    <div class="border-t border-base-content/10"></div>
  </div>

  <section class="w-full max-w-4xl px-4 sm:px-6 lg:px-8 py-12 sm:py-16 pb-20 sm:pb-28">
    <p
      class="text-xs font-semibold tracking-widest uppercase text-base-content/35 mb-3"
    >
      Stakeholders
    </p>
    <h2 class="text-xl sm:text-2xl font-semibold text-base-content">Who Benefits?</h2>

    <div class="mt-6 sm:mt-8 grid grid-cols-1 sm:grid-cols-3 gap-3 sm:gap-4">
      <div
        class="border border-base-content/10 rounded-lg p-4 sm:p-5 bg-base-100 hover:bg-base-200 transition-colors"
      >
        <p
          class="text-xs font-semibold text-base-content/35 uppercase tracking-wider mb-2 sm:mb-3"
        >
          Students
        </p>
        <h3 class="text-sm font-semibold text-base-content">
          Report with confidence
        </h3>
        <p class="mt-2 text-xs sm:text-sm text-base-content/50 leading-relaxed">
          Submit complaints quickly, track their status in real time, and know
          that every issue is being addressed.
        </p>
      </div>
      <div
        class="border border-base-content/10 rounded-lg p-4 sm:p-5 bg-base-100 hover:bg-base-200 transition-colors"
      >
        <p
          class="text-xs font-semibold text-base-content/35 uppercase tracking-wider mb-2 sm:mb-3"
        >
          Administrators
        </p>
        <h3 class="text-sm font-semibold text-base-content">
          Manage with clarity
        </h3>
        <p class="mt-2 text-xs sm:text-sm text-base-content/50 leading-relaxed">
          Oversee all reports from a single dashboard, assign tasks, and
          maintain a complete log of every action taken.
        </p>
      </div>
      <div
        class="border border-base-content/10 rounded-lg p-4 sm:p-5 bg-base-100 hover:bg-base-200 transition-colors"
      >
        <p
          class="text-xs font-semibold text-base-content/35 uppercase tracking-wider mb-2 sm:mb-3"
        >
          Maintenance
        </p>
        <h3 class="text-sm font-semibold text-base-content">
          Resolve with direction
        </h3>
        <p class="mt-2 text-xs sm:text-sm text-base-content/50 leading-relaxed">
          Receive clearly assigned tickets with full context such as location,
          severity, and photos, to act fast.
        </p>
      </div>
    </div>
  </section>
  <div class="w-full max-w-7xl px-4 sm:px-6 lg:px-8 mt-auto">
    <div class="border-t border-base-content/10"></div>
      <Footer />
  </div>
</div>

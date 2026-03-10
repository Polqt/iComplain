<script>
import Icon from "@iconify/svelte";
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

  <section
    class="w-full max-w-6xl px-4 sm:px-6 lg:px-8 pt-16 sm:pt-20 md:pt-24 pb-12 sm:pb-16 md:pb-20"
  >
    <p
      class="badge badge-ghost text-xs font-semibold tracking-widest uppercase mb-4 sm:mb-6"
    >
      Getting started
    </p>
    <h1
      class="text-3xl sm:text-4xl md:text-5xl font-semibold text-base-content leading-tight"
    >
      Learn how to use iComplain.
    </h1>
    <div class="mt-4 sm:mt-6 w-8 sm:w-12 h-px bg-base-content/20"></div>
    <p
      class="mt-4 sm:mt-6 text-sm sm:text-base text-base-content/60 leading-relaxed max-w-2xl"
    >
      This page walks you through the full flow of the app – from submitting
      your first complaint to tracking status and seeing it resolved.
    </p>

    <div class="mt-6 space-y-4">
      <div class="flex gap-3">
        <div
          class="mt-1 h-6 w-6 rounded-full border border-base-content/20 bg-base-100 flex items-center justify-center text-[11px] font-semibold text-base-content/60"
        >
          1
        </div>
        <div>
          <p class="text-sm font-semibold text-base-content">
            Sign in with your USLS account
          </p>
          <p class="text-xs sm:text-sm text-base-content/60 leading-relaxed">
            Go to <span class="font-medium">Sign in</span> and use your
            university email to access the app as a student, admin, or maintenance
            staff.
          </p>
        </div>
      </div>
      <div class="flex gap-3">
        <div
          class="mt-1 h-6 w-6 rounded-full border border-base-content/20 bg-base-100 flex items-center justify-center text-[11px] font-semibold text-base-content/60"
        >
          2
        </div>
        <div>
          <p class="text-sm font-semibold text-base-content">
            Report an issue
          </p>
          <p class="text-xs sm:text-sm text-base-content/60 leading-relaxed">
            From your dashboard, open the complaint form, describe the issue, add a
            location and optional photos, then submit.
          </p>
        </div>
      </div>
      <div class="flex gap-3">
        <div
          class="mt-1 h-6 w-6 rounded-full border border-base-content/20 bg-base-100 flex items-center justify-center text-[11px] font-semibold text-base-content/60"
        >
          3
        </div>
        <div>
          <p class="text-sm font-semibold text-base-content">
            Track and follow up
          </p>
          <p class="text-xs sm:text-sm text-base-content/60 leading-relaxed">
            Use your <span class="font-medium">Tickets</span> view to see status,
            read updates, and add comments while the issue is being resolved.
          </p>
        </div>
      </div>
    </div>
  </section>

  <!-- Visual feature & flow showcase + video -->
  <section
    class="w-full max-w-6xl px-4 sm:px-6 lg:px-8 pb-12 sm:pb-16 md:pb-20"
  >
    <div class="grid gap-10 lg:grid-cols-[minmax(0,3fr)_minmax(0,2.5fr)] items-start">
      <div class="space-y-4">
        <p
          class="text-xs font-semibold tracking-widest uppercase text-base-content/40"
        >
          How it works at a glance
        </p>
        <h2 class="text-xl sm:text-2xl font-semibold text-base-content">
          Report, track, and resolve in one place.
        </h2>
        <p class="text-sm sm:text-base text-base-content/65 max-w-2xl">
          The cards on the right shuffle to highlight the main steps of the
          experience – reporting issues, monitoring progress, and seeing them
          resolved.
        </p>

        <div class="mt-4 grid gap-3 text-sm text-base-content/70">
          <div class="flex gap-2">
            <span class="mt-1 h-1.5 w-1.5 rounded-full bg-emerald-400"></span>
            <p>
              <span class="font-medium">Students</span> create tickets with
              location, photos, and details.
            </p>
          </div>
          <div class="flex gap-2">
            <span class="mt-1 h-1.5 w-1.5 rounded-full bg-sky-400"></span>
            <p>
              <span class="font-medium">Admins</span> review, prioritize, and
              assign complaints to the right teams.
            </p>
          </div>
          <div class="flex gap-2">
            <span class="mt-1 h-1.5 w-1.5 rounded-full bg-amber-400"></span>
            <p>
              <span class="font-medium">Maintenance</span> updates progress
              until the issue is fully resolved.
            </p>
          </div>
        </div>
      </div>

      <div class="mt-4 lg:mt-0 space-y-4">
        <div class="relative mx-auto max-w-md">
          <div
            class="pointer-events-none absolute inset-0 -translate-y-4 scale-110 rounded-[2rem] bg-gradient-to-br from-sky-500/10 via-emerald-400/5 to-amber-400/10 blur-3xl"
          ></div>

          <div class="relative h-64 sm:h-72 hero-card-shuffle">
            <div
              class="absolute inset-x-6 top-6 rounded-2xl border border-base-content/10 bg-base-200/80 shadow-xl shadow-base-content/10 transform rotate-[-6deg] -translate-y-2"
            ></div>

            <div
              class="absolute inset-x-3 top-8 rounded-2xl border border-base-content/10 bg-base-100/90 shadow-xl shadow-base-content/10 transform rotate-[4deg] translate-y-1"
            ></div>

            <div
              class="absolute inset-0 rounded-2xl border border-base-content/15 bg-base-100 shadow-2xl shadow-base-content/20 transform translate-y-4 translate-x-2 rotate-[-2deg] overflow-hidden"
            >
              <div class="flex items-center justify-between px-4 pt-4">
                <div class="flex items-center gap-2">
                  <span class="h-2 w-2 rounded-full bg-emerald-400"></span>
                  <p class="text-xs font-semibold text-base-content/60 uppercase tracking-wider">
                    App flow
                  </p>
                </div>
                <span class="badge badge-sm badge-outline text-[10px]">
                  Overview
                </span>
              </div>

              <div class="mt-3 space-y-2 px-4 pb-4">
                <div
                  class="flex items-center justify-between rounded-xl border border-emerald-400/20 bg-emerald-400/5 px-3 py-2"
                >
                  <div>
                    <p class="text-[11px] font-medium text-base-content/70">
                      Report
                    </p>
                    <p class="text-[10px] text-base-content/45">
                      Students submit facility complaints with details &amp;
                      photos.
                    </p>
                  </div>
                  <span class="badge badge-xs badge-info gap-1 text-[10px]">
                    Step 1
                  </span>
                </div>

                <div
                  class="flex items-center justify-between rounded-xl border border-amber-400/25 bg-amber-400/5 px-3 py-2"
                >
                  <div>
                    <p class="text-[11px] font-medium text-base-content/70">
                      Track
                    </p>
                    <p class="text-[10px] text-base-content/45">
                      Status, comments, and history are visible in one
                      place.
                    </p>
                  </div>
                  <span class="badge badge-xs badge-warning gap-1 text-[10px]">
                    Step 2
                  </span>
                </div>

                <div
                  class="flex items-center justify-between rounded-xl border border-base-content/10 bg-base-200/60 px-3 py-2"
                >
                  <div>
                    <p class="text-[11px] font-medium text-base-content/70">
                      Resolve
                    </p>
                    <p class="text-[10px] text-base-content/45">
                      Maintenance updates the ticket and closes it when
                      done.
                    </p>
                  </div>
                  <span class="badge badge-xs badge-success gap-1 text-[10px]">
                    Step 3
                  </span>
                </div>
              </div>

              <div class="border-t border-base-content/10 bg-base-100/90 px-4 py-3">
                <div class="flex items-center justify-between text-[11px] text-base-content/55">
                  <div class="flex items-center gap-2">
                    <span class="h-1.5 w-1.5 rounded-full bg-sky-400"></span>
                    <span>Notifications keep everyone in sync</span>
                  </div>
                  <span class="text-[10px] text-base-content/40">
                    REPORT · TRACK · RESOLVE
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Video placeholder -->
        <div
          class="relative mx-auto max-w-md rounded-2xl border border-base-content/10 bg-base-200/40 p-4 sm:p-5"
        >
          <div
            class="aspect-video w-full rounded-xl bg-base-300/60 flex items-center justify-center relative overflow-hidden"
          >
            <div
              class="absolute inset-0 bg-gradient-to-tr from-base-300 via-base-200/70 to-base-100/40"
            ></div>
            <button
              type="button"
              class="relative z-10 flex items-center justify-center h-14 w-14 rounded-full bg-base-100/90 shadow-lg shadow-base-content/20 border border-base-content/10"
              aria-label="Tutorial video placeholder"
            >
              <Icon icon="mdi:play" width="26" height="26" class="text-base-content" />
            </button>
          </div>
          <div class="mt-3 space-y-1">
            <p class="text-sm font-semibold text-base-content">
              Video tutorial (coming soon)
            </p>
            <p class="text-xs text-base-content/60">
              A step-by-step walkthrough of iComplain will be available here soon via
              YouTube. You&apos;ll be able to follow along from sign-in to resolution.
            </p>
            <p class="text-[11px] text-base-content/45">
              Placeholder for: <span class="font-mono">YouTube link</span>
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="w-full max-w-6xl px-4 sm:px-6 lg:px-8 pb-16 sm:pb-20 md:pb-24">
    <div class="grid gap-10 lg:grid-cols-2">
      <div class="space-y-4">
        <p
          class="text-xs font-semibold tracking-widest uppercase text-base-content/40"
        >
          For students
        </p>
        <h2 class="text-xl sm:text-2xl font-semibold text-base-content">
          Submitting and following your complaints
        </h2>
        <ul class="mt-2 space-y-2 text-sm sm:text-base text-base-content/65">
          <li>
            <span class="font-medium">Create a ticket:</span> Go to your dashboard and
            choose the option to file a new complaint.
          </li>
          <li>
            <span class="font-medium">Describe the issue:</span> Add a short but clear
            description, select the correct location, and attach photos if needed.
          </li>
          <li>
            <span class="font-medium">Watch the status:</span> Use the
            <span class="font-medium">Tickets</span> page to see whether your complaint
            is pending, in progress, resolved, or closed.
          </li>
          <li>
            <span class="font-medium">Stay informed:</span> Check your notification bell
            for real-time updates whenever admins or maintenance teams act on your case.
          </li>
        </ul>
      </div>

      <div class="space-y-4">
        <p
          class="text-xs font-semibold tracking-widest uppercase text-base-content/40"
        >
          For staff &amp; admins
        </p>
        <h2 class="text-xl sm:text-2xl font-semibold text-base-content">
          Managing and resolving tickets
        </h2>
        <ul class="mt-2 space-y-2 text-sm sm:text-base text-base-content/65">
          <li>
            <span class="font-medium">Review new tickets:</span> Use the admin dashboard
            to filter and prioritize incoming complaints.
          </li>
          <li>
            <span class="font-medium">Assign &amp; update:</span> Change status (e.g.
            pending, in progress, resolved), add internal notes, and assign to the right
            maintenance team.
          </li>
          <li>
            <span class="font-medium">Communicate in context:</span> Use comments inside
            each ticket instead of separate email threads.
          </li>
          <li>
            <span class="font-medium">Close with a clear history:</span> Every action is
            logged so future reviews and audits are simple.
          </li>
        </ul>
      </div>
    </div>
  </section>

  <div class="w-full max-w-7xl px-4 sm:px-6 lg:px-8 mt-auto">
    <div class="border-t border-base-content/10"></div>
    <Footer />
  </div>
</div>

<style>
  .hero-card-shuffle {
    animation: heroCardShuffle 14s infinite ease-in-out;
    transform-style: preserve-3d;
  }

  @keyframes heroCardShuffle {
    0% {
      transform: translateY(0) rotateX(0deg) rotateY(0deg);
    }
    20% {
      transform: translateY(-6px) rotateX(8deg) rotateY(-6deg);
    }
    40% {
      transform: translateY(4px) rotateX(-6deg) rotateY(4deg);
    }
    60% {
      transform: translateY(-4px) rotateX(5deg) rotateY(6deg);
    }
    80% {
      transform: translateY(2px) rotateX(-4deg) rotateY(-4deg);
    }
    100% {
      transform: translateY(0) rotateX(0deg) rotateY(0deg);
    }
  }
</style>

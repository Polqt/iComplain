<script>
import { goto } from "$app/navigation";
import Icon from "@iconify/svelte";
import Footer from "../components/layout/Footer.svelte";
import Header from "../components/layout/Header.svelte";
function handleGetStarted() {
	goto("/signin");
}

function handleLearnMore() {
	goto("/learn-more");
}
</script>

<svelte:head>
  <title>iComplain</title>
</svelte:head>

<div class="flex flex-col items-center bg-base-100 min-h-screen overflow-x-hidden">
  <div class="w-full max-w-7xl px-4 sm:px-6 lg:px-8">
    <Header />
  </div>

  <section
    class="w-full max-w-6xl px-4 sm:px-6 lg:px-8 pt-16 sm:pt-20 md:pt-24 pb-12 sm:pb-16 md:pb-20"
  >
    <div class="grid gap-10 lg:grid-cols-[minmax(0,3fr)_minmax(0,2.5fr)] items-center">
      <!-- Left: existing hero copy -->
      <div>
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
          <p
            class="text-sm sm:text-base text-base-content/60 leading-relaxed max-w-2xl"
          >
            Report issues instantly, track progress in real-time, and ensure every
            concern gets the attention it deserves.
          </p>
        </div>

        <div class="mt-6 sm:mt-10 flex flex-col sm:flex-row gap-3 sm:gap-4">
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
      </div>

      <!-- Right: 3D-inspired ticket stack -->
      <div class="mt-8 lg:mt-0">
        <div class="relative mx-auto max-w-md">
          <!-- soft glow background -->
          <div
            class="pointer-events-none absolute inset-0 -translate-y-4 scale-110 rounded-[2rem] bg-gradient-to-br from-sky-500/10 via-emerald-400/5 to-amber-400/10 blur-3xl"
          ></div>

          <div class="relative h-64 sm:h-72 hero-card-shuffle">
            <!-- back card -->
            <div
              class="absolute inset-x-6 top-6 rounded-2xl border border-base-content/10 bg-base-200/80 shadow-xl shadow-base-content/10 transform rotate-[-6deg] -translate-y-2"
            ></div>

            <!-- middle card -->
            <div
              class="absolute inset-x-3 top-8 rounded-2xl border border-base-content/10 bg-base-100/90 shadow-xl shadow-base-content/10 transform rotate-[4deg] translate-y-1"
            ></div>

            <!-- front card: mini dashboard -->
            <div
              class="absolute inset-0 rounded-2xl border border-base-content/15 bg-base-100 shadow-2xl shadow-base-content/20 transform translate-y-4 translate-x-2 rotate-[-2deg] overflow-hidden"
            >
              <div class="flex items-center justify-between px-4 pt-4">
                <div class="flex items-center gap-2">
                  <span class="h-2 w-2 rounded-full bg-emerald-400"></span>
                  <p class="text-xs font-semibold text-base-content/60 uppercase tracking-wider">
                    Live tickets
                  </p>
                </div>
                <span class="badge badge-sm badge-outline text-[10px]">
                  Campus view
                </span>
              </div>

              <div class="mt-3 space-y-2 px-4 pb-4">
                <div
                  class="flex items-center justify-between rounded-xl border border-emerald-400/20 bg-emerald-400/5 px-3 py-2"
                >
                  <div>
                    <p class="text-[11px] font-medium text-base-content/70">
                      Broken PC – CSL 2
                    </p>
                    <p class="text-[10px] text-base-content/45">
                      Submitted · 2 min ago
                    </p>
                  </div>
                  <span class="badge badge-xs badge-info gap-1 text-[10px]">
                    <span class="h-1.5 w-1.5 rounded-full bg-sky-400"></span>
                    In progress
                  </span>
                </div>

                <div
                  class="flex items-center justify-between rounded-xl border border-amber-400/25 bg-amber-400/5 px-3 py-2"
                >
                  <div>
                    <p class="text-[11px] font-medium text-base-content/70">
                      AC not working – PS 22
                    </p>
                    <p class="text-[10px] text-base-content/45">
                      Waiting for maintenance
                    </p>
                  </div>
                  <span class="badge badge-xs badge-warning gap-1 text-[10px]">
                    <span class="h-1.5 w-1.5 rounded-full bg-amber-400"></span>
                    Pending
                  </span>
                </div>

                <div
                  class="flex items-center justify-between rounded-xl border border-base-content/10 bg-base-200/60 px-3 py-2"
                >
                  <div>
                    <p class="text-[11px] font-medium text-base-content/70">
                      Water leak – MM 2F
                    </p>
                    <p class="text-[10px] text-base-content/45">
                      Resolved · Logged in history
                    </p>
                  </div>
                  <span class="badge badge-xs badge-success gap-1 text-[10px]">
                    <span class="h-1.5 w-1.5 rounded-full bg-emerald-400"></span>
                    Resolved
                  </span>
                </div>
              </div>

              <div class="border-t border-base-content/10 bg-base-100/90 px-4 py-3">
                <div class="flex items-center justify-between text-[11px] text-base-content/55">
                  <div class="flex items-center gap-2">
                    <span class="h-1.5 w-1.5 rounded-full bg-sky-400"></span>
                    <span>Real-time notifications enabled</span>
                  </div>
                  <span class="text-[10px] text-base-content/40">
                    REPORT · TRACK · RESOLVE
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

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

  <!-- Expanded landing content, refined from docs/about but keeping core hero design -->
  <section
    class="w-full max-w-6xl px-4 sm:px-6 lg:px-8 pb-12 sm:pb-16 md:pb-20"
  >
    <div
      class="relative rounded-2xl border border-base-content/10 bg-gradient-to-br from-base-100 via-base-200/40 to-base-100 shadow-sm overflow-hidden"
    >
      <div
        class="pointer-events-none absolute -right-20 -top-20 h-64 w-64 rounded-full bg-sky-500/5 blur-3xl"
      ></div>
      <div
        class="pointer-events-none absolute -left-16 bottom-0 h-48 w-48 rounded-full bg-amber-500/5 blur-3xl"
      ></div>

      <div class="relative grid gap-8 p-6 sm:p-8 lg:grid-cols-[minmax(0,3fr)_minmax(0,2fr)]">
        <div class="space-y-4">
          <p
            class="badge badge-ghost text-[10px] sm:text-xs font-semibold tracking-widest uppercase"
          >
            Designed for USLS
          </p>
          <h2
            class="text-xl sm:text-2xl md:text-3xl font-semibold text-base-content leading-tight"
          >
            A centralized way to care for every corner of campus.
          </h2>
          <p class="text-sm sm:text-base text-base-content/70 leading-relaxed max-w-xl">
            iComplain brings students, administrators, and maintenance teams into
            one shared space. Every report has a clear path: from submission, to
            review, to resolution — with full visibility at every step.
          </p>

          <div class="mt-4 grid gap-3 sm:grid-cols-3">
            <div
              class="rounded-xl border border-base-content/10 bg-base-100/80 p-3 sm:p-4 backdrop-blur-sm"
            >
              <p class="text-[11px] font-semibold tracking-widest uppercase text-base-content/40">
                Students
              </p>
              <p class="mt-1 text-xs sm:text-sm text-base-content/70">
                Report facility issues quickly and track them in real time.
              </p>
            </div>
            <div
              class="rounded-xl border border-base-content/10 bg-base-100/80 p-3 sm:p-4 backdrop-blur-sm"
            >
              <p class="text-[11px] font-semibold tracking-widest uppercase text-base-content/40">
                Administrators
              </p>
              <p class="mt-1 text-xs sm:text-sm text-base-content/70">
                See the full picture, prioritize work, and keep everything
                accountable.
              </p>
            </div>
            <div
              class="rounded-xl border border-base-content/10 bg-base-100/80 p-3 sm:p-4 backdrop-blur-sm"
            >
              <p class="text-[11px] font-semibold tracking-widest uppercase text-base-content/40">
                Maintenance
              </p>
              <p class="mt-1 text-xs sm:text-sm text-base-content/70">
                Receive clear, actionable tickets with photos, locations, and
                history.
              </p>
            </div>
          </div>
        </div>

        <div class="space-y-4">
          <p
            class="text-[11px] sm:text-xs font-semibold tracking-widest uppercase text-base-content/40"
          >
            How it feels to use
          </p>
          <div
            class="relative rounded-2xl border border-base-content/10 bg-base-100/90 p-4 sm:p-5 shadow-lg shadow-base-content/5"
          >
            <div class="flex items-center justify-between gap-3">
              <div>
                <p class="text-xs font-medium text-base-content/60">
                  Live ticket snapshot
                </p>
                <p class="mt-1 text-sm font-semibold text-base-content">
                  “Aircon not working – CL 204”
                </p>
              </div>
              <span class="badge badge-info badge-outline text-[10px]">
                In progress
              </span>
            </div>
            <div class="mt-3 space-y-2 text-[11px] sm:text-xs text-base-content/60">
              <div class="flex items-center gap-2">
                <span class="h-1.5 w-1.5 rounded-full bg-emerald-400"></span>
                <span>Submitted by a student in seconds — with photo and room details.</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="h-1.5 w-1.5 rounded-full bg-sky-400"></span>
                <span>Assigned to the right team, visible on the admin dashboard.</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="h-1.5 w-1.5 rounded-full bg-amber-400"></span>
                <span>Updates sent instantly through in‑app notifications.</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section
    class="w-full max-w-6xl px-4 sm:px-6 lg:px-8 pb-12 sm:pb-16 md:pb-20"
  >
    <div class="flex flex-col gap-2 mb-6 sm:mb-8">
      <p
        class="text-[11px] sm:text-xs font-semibold tracking-widest uppercase text-base-content/40"
      >
        End‑to‑end workflow
      </p>
      <h2 class="text-xl sm:text-2xl md:text-3xl font-semibold text-base-content">
        From report to resolution, always in view.
      </h2>
      <p class="text-sm sm:text-base text-base-content/65 max-w-2xl">
        iComplain turns scattered complaints into a single, traceable flow so no
        issue falls through the cracks.
      </p>
    </div>

    <div
      class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4"
    >
      <div
        class="relative rounded-2xl border border-base-content/10 bg-base-100 p-4 sm:p-5 shadow-sm hover:-translate-y-1 hover:shadow-lg transition-all duration-200"
      >
        <p class="text-xs font-semibold text-base-content/35 uppercase tracking-wider">
          01 · Report
        </p>
        <h3 class="mt-1 text-sm font-semibold text-base-content">
          Submit issues in seconds
        </h3>
        <p class="mt-2 text-xs sm:text-sm text-base-content/60 leading-relaxed">
          Students file complaints with details, photos, and precise locations
          — right from their browser.
        </p>
      </div>
      <div
        class="relative rounded-2xl border border-base-content/10 bg-base-100 p-4 sm:p-5 shadow-sm hover:-translate-y-1 hover:shadow-lg transition-all duration-200"
      >
        <p class="text-xs font-semibold text-base-content/35 uppercase tracking-wider">
          02 · Track
        </p>
        <h3 class="mt-1 text-sm font-semibold text-base-content">
          Follow every update
        </h3>
        <p class="mt-2 text-xs sm:text-sm text-base-content/60 leading-relaxed">
          Real-time notifications and a clear status view show exactly what’s
          happening to each ticket.
        </p>
      </div>
      <div
        class="relative rounded-2xl border border-base-content/10 bg-base-100 p-4 sm:p-5 shadow-sm hover:-translate-y-1 hover:shadow-lg transition-all duration-200"
      >
        <p class="text-xs font-semibold text-base-content/35 uppercase tracking-wider">
          03 · Collaborate
        </p>
        <h3 class="mt-1 text-sm font-semibold text-base-content">
          Comment and clarify
        </h3>
        <p class="mt-2 text-xs sm:text-sm text-base-content/60 leading-relaxed">
          Students, admins, and maintenance teams discuss details directly in
          the ticket thread.
        </p>
      </div>
      <div
        class="relative rounded-2xl border border-base-content/10 bg-base-100 p-4 sm:p-5 shadow-sm hover:-translate-y-1 hover:shadow-lg transition-all duration-200"
      >
        <p class="text-xs font-semibold text-base-content/35 uppercase tracking-wider">
          04 · Resolve
        </p>
        <h3 class="mt-1 text-sm font-semibold text-base-content">
          Close with confidence
        </h3>
        <p class="mt-2 text-xs sm:text-sm text-base-content/60 leading-relaxed">
          Actions are logged, tickets are closed with a full history, and
          students see when issues are resolved.
        </p>
      </div>
    </div>
  </section>

  <section
    class="w-full max-w-6xl px-4 sm:px-6 lg:px-8 pb-16 sm:pb-20 md:pb-24"
  >
    <div
      class="rounded-2xl border border-base-content/10 bg-base-200/40 p-6 sm:p-8 flex flex-col gap-6 lg:flex-row lg:items-center"
    >
      <div class="flex-1 space-y-3">
        <p
          class="text-[11px] sm:text-xs font-semibold tracking-widest uppercase text-base-content/40"
        >
          Why it matters
        </p>
        <h2 class="text-xl sm:text-2xl font-semibold text-base-content">
          Built for clarity, accountability, and a better campus experience.
        </h2>
        <p class="text-sm sm:text-base text-base-content/65 max-w-xl">
          iComplain is more than a form — it’s a full complaint lifecycle,
          designed specifically for the University of St. La Salle to keep
          facilities responsive and students heard.
        </p>

        <div class="mt-4 grid gap-3 sm:grid-cols-2">
          <div class="flex items-start gap-2">
            <span class="mt-1 h-1.5 w-1.5 rounded-full bg-base-content/40"></span>
            <p class="text-xs sm:text-sm text-base-content/70">
              Traceable history of every facility issue for better decisions.
            </p>
          </div>
          <div class="flex items-start gap-2">
            <span class="mt-1 h-1.5 w-1.5 rounded-full bg-base-content/40"></span>
            <p class="text-xs sm:text-sm text-base-content/70">
              Clear responsibilities across departments and maintenance teams.
            </p>
          </div>
          <div class="flex items-start gap-2">
            <span class="mt-1 h-1.5 w-1.5 rounded-full bg-base-content/40"></span>
            <p class="text-xs sm:text-sm text-base-content/70">
              Faster turnaround times powered by structured workflows and
              real‑time updates.
            </p>
          </div>
          <div class="flex items-start gap-2">
            <span class="mt-1 h-1.5 w-1.5 rounded-full bg-base-content/40"></span>
            <p class="text-xs sm:text-sm text-base-content/70">
              A tangible boost in student trust and satisfaction with campus
              facilities.
            </p>
          </div>
        </div>
      </div>

      <div class="flex-1">
        <div
          class="relative mx-auto mt-2 max-w-md rounded-2xl border border-base-content/10 bg-base-100 p-4 sm:p-5 shadow-xl shadow-base-content/10"
        >
          <div class="flex items-center justify-between gap-3">
            <div>
              <p class="text-xs font-semibold text-base-content/60 uppercase tracking-wider">
                Live system feel
              </p>
              <p class="mt-1 text-sm font-semibold text-base-content">
                “Your ticket was updated”
              </p>
            </div>
            <span class="badge badge-success badge-outline text-[10px]">
              Notification
            </span>
          </div>
          <p class="mt-3 text-xs sm:text-sm text-base-content/65 leading-relaxed">
            A student reports a broken light. Minutes later, they get a status
            update — the request is assigned, progress is visible, and closure
            is confirmed.
          </p>
          <div class="mt-4 flex flex-wrap gap-2 text-[11px] sm:text-xs">
            <span class="badge badge-outline border-emerald-400/60 text-emerald-500">
              Real-time notifications
            </span>
            <span class="badge badge-outline border-sky-400/60 text-sky-500">
              Comment threads
            </span>
            <span class="badge badge-outline border-amber-400/60 text-amber-500">
              Status history
            </span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <div class="w-full max-w-7xl px-4 sm:px-6 lg:px-8 mt-auto">
    <div class="border-t border-base-content/10"></div>
    <Footer />
  </div>
</div>

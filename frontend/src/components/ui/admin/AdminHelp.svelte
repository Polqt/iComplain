<script lang="ts">
  import Icon from "@iconify/svelte";
  import AdminLayout from "../../../components/layout/AdminLayout.svelte";
  import type { HelpSection } from "../../../types/help.ts";
  import { loadHelpContent } from "../../../utils/helpConfig.ts";

  const helpData = loadHelpContent({ role: "admin", name: "", avatar: "", email: "" });

  let activeTab: string = helpData.sections[0]?.id || "getting-started";
  let searchQuery: string = "";
  let openAccordions: Set<string> = new Set();

  // Computed
  $: filteredSections = helpData.sections.filter((section: HelpSection) => {
    if (!searchQuery.trim()) return true;
    const query = searchQuery.toLowerCase();
    return (
      section.title.toLowerCase().includes(query) ||
      section.content.toLowerCase().includes(query) ||
      section.faqs?.some(
        (faq) =>
          faq.question.toLowerCase().includes(query) ||
          faq.answer.toLowerCase().includes(query)
      )
    );
  });

  $: activeSection = helpData.sections.find((s: HelpSection) => s.id === activeTab);

  // Functions
  function toggleAccordion(id: string) {
    if (openAccordions.has(id)) {
      openAccordions.delete(id);
    } else {
      openAccordions.add(id);
    }
    openAccordions = openAccordions;
  }

  function setActiveTab(tabId: string) {
    activeTab = tabId;
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
</script>

<svelte:head>
  <title>Admin Help - iComplain</title>
</svelte:head>

<AdminLayout>
  <div class="flex flex-col h-[calc(100vh-8rem)]">
    <div class="shrink-0 mb-6">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h1 class="text-3xl font-black text-base-content mb-2">
            Admin Help Center
          </h1>
          <p class="text-sm text-base-content/60">
            Learn how to manage tickets, generate reports, and use admin features
          </p>
        </div>
        <!-- Logo -->
        <div class="hidden sm:flex items-center gap-2 text-primary">
          <Icon icon="mdi:shield-account-outline" width="32" height="32" />
        </div>
      </div>
      <div class="relative">
        <Icon
          icon="mdi:magnify"
          width="20"
          height="20"
          class="absolute left-4 top-1/2 -translate-y-1/2 text-base-content/40"
        />
        <input
          type="search"
          placeholder="Search admin documentation..."
          class="input input-bordered w-full pl-12 pr-4 bg-base-100 focus:outline-primary transition-all duration-200"
          bind:value={searchQuery}
        />
      </div>
    </div>

    <div class="tabs tabs-boxed bg-base-200 p-1 mb-6 shrink-0 overflow-x-auto">
      {#each filteredSections as section}
        <button
          class="tab {activeTab === section.id
            ? 'tab-active scale-105'
            : ''} whitespace-nowrap transition-all duration-200"
          onclick={() => setActiveTab(section.id)}
        >
          <Icon icon={section.icon} width="18" height="18" class="mr-2" />
          {section.title}
        </button>
      {/each}
    </div>

    <div class="flex-1 overflow-y-auto pr-2">
      {#if activeSection}
        <div class="transition-opacity duration-300">
          <div class="card bg-linear-to-br from-primary/10 to-secondary/10 border border-base-content/10 mb-6">
            <div class="card-body">
              <div class="flex items-start gap-4">
                <div class="p-3 bg-primary/20 rounded-lg">
                  <Icon
                    icon={activeSection.icon}
                    width="32"
                    height="32"
                    class="text-primary"
                  />
                </div>
                <div class="flex-1">
                  <h2 class="text-2xl font-bold text-base-content mb-2">
                    {activeSection.title}
                  </h2>
                  <p class="text-base-content/70">
                    {activeSection.content}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- FAQs -->
          {#if activeSection.faqs && activeSection.faqs.length > 0}
            <div class="space-y-3">
              <h3 class="text-lg font-bold text-base-content mb-4 flex items-center gap-2">
                <Icon icon="mdi:frequently-asked-questions" width="24" height="24" />
                Frequently Asked Questions
              </h3>

              {#each activeSection.faqs as faq, index}
                {@const accordionId = `${activeSection.id}-${index}`}
                <div
                  class="collapse collapse-arrow bg-base-100 border border-base-content/10 hover:border-primary/50 transition-all duration-200"
                  class:collapse-open={openAccordions.has(accordionId)}
                >
                  <input
                    type="checkbox"
                    checked={openAccordions.has(accordionId)}
                    onchange={() => toggleAccordion(accordionId)}
                    class="peer"
                  />
                  <div
                    class="collapse-title text-base font-semibold text-base-content peer-checked:text-primary transition-colors duration-200"
                  >
                    {faq.question}
                  </div>
                  <div class="collapse-content">
                    <p class="text-sm text-base-content/70 leading-relaxed pt-2">
                      {faq.answer}
                    </p>
                  </div>
                </div>
              {/each}
            </div>
          {/if}
        </div>
      {:else}
        <div class="flex flex-col items-center justify-center py-12 text-center">
          <Icon
            icon="mdi:magnify"
            width="64"
            height="64"
            class="text-base-content/20 mb-4"
          />
          <h3 class="text-lg font-semibold text-base-content/80 mb-2">
            No results found
          </h3>
          <p class="text-sm text-base-content/60 mb-4">
            Try adjusting your search terms
          </p>
          <button
            class="btn btn-primary btn-sm"
            onclick={() => (searchQuery = "")}
          >
            Clear search
          </button>
        </div>
      {/if}

      <!-- Contact Support Section -->
      <div class="mt-8 mb-4">
        <div class="divider">Need Additional Support?</div>
        <div class="card bg-base-200 border border-base-content/10">
          <div class="card-body text-center">
            <h3 class="font-bold text-lg mb-2">Contact IT Support</h3>
            <p class="text-sm text-base-content/70 mb-4">
              For technical issues with the admin system or questions not covered here,
              contact the IT department.
            </p>
            <div class="flex flex-col sm:flex-row gap-2 justify-center">
              <a href="mailto:{helpData.contact.email}" class="btn btn-primary btn-sm">
                <Icon icon="mdi:email-outline" width="18" height="18" />
                Email IT Support
              </a>
              <a href="tel:{helpData.contact.phone}" class="btn btn-outline btn-sm">
                <Icon icon="mdi:phone-outline" width="18" height="18" />
                Call {helpData.contact.phoneDisplay}
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</AdminLayout>
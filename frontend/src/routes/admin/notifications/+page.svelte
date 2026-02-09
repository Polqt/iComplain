<script lang="ts">
  import Icon from "@iconify/svelte";
  import AdminLayout from "../../../components/layout/AdminLayout.svelte";

  type Notice = {
    id: string;
    type: "success" | "info" | "warning" | "error";
    title: string;
    message: string;
    time: string;
    read: boolean;
    ticketId?: string;
  };

  const typeConfig = {
    success: { icon: "lucide:check-circle", color: "text-success" },
    info: { icon: "lucide:info", color: "text-info" },
    warning: { icon: "lucide:alert-circle", color: "text-warning" },
    error: { icon: "lucide:x-circle", color: "text-error" },
  };

  let filter: "all" | "unread" = "all";
  let searchQuery = "";

  let notifications: Notice[] = [
    {
      id: "N-1001",
      type: "success",
      title: "Ticket Resolved",
      message: "Ticket #4021 was marked as resolved.",
      time: "10 mins ago",
      read: false,
      ticketId: "TC-0004",
    },
    {
      id: "N-1002",
      type: "warning",
      title: "SLA Risk",
      message: "Ticket #3987 is nearing SLA deadline.",
      time: "2 hours ago",
      read: false,
      ticketId: "TC-0001",
    },
    {
      id: "N-1003",
      type: "info",
      title: "New Assignment",
      message: "Ticket #3964 assigned to Maintenance Team.",
      time: "Yesterday",
      read: true,
      ticketId: "TC-0003",
    },
    {
      id: "N-1004",
      type: "error",
      title: "System Alert",
      message: "Email service latency detected.",
      time: "2 days ago",
      read: true,
    },
  ];

  function markAllRead() {
    notifications = notifications.map((n) => ({ ...n, read: true }));
  }

  function markRead(id: string) {
    notifications = notifications.map((n) =>
      n.id === id ? { ...n, read: true } : n,
    );
  }

  $: filtered = notifications.filter((n) => {
    if (filter === "unread" && n.read) return false;
    const q = searchQuery.trim().toLowerCase();
    if (!q) return true;
    return (
      n.title.toLowerCase().includes(q) ||
      n.message.toLowerCase().includes(q) ||
      (n.ticketId ?? "").toLowerCase().includes(q)
    );
  });

  $: unreadCount = notifications.filter((n) => !n.read).length;
</script>

<AdminLayout>
  <div class="flex flex-col h-[calc(100vh-8rem)]">
    <div class="flex flex-wrap items-center justify-between gap-4 mb-6 shrink-0">
      <div>
        <h1 class="text-2xl font-black text-base-content">Notifications</h1>
        <p class="text-sm text-base-content/60">
          Stay on top of ticket updates and system alerts.
        </p>
      </div>
      <div class="flex items-center gap-2">
        <button class="btn btn-sm btn-outline" onclick={markAllRead}>
          Mark all as read
        </button>
      </div>
    </div>

    <div class="flex-1 overflow-y-auto pr-2 space-y-4">
      <section class="card bg-base-100 dark:bg-base-100 shadow-sm border border-base-content/5 rounded-lg">
        <div class="card-body p-4">
          <div class="flex flex-wrap items-center gap-3">
            <label class="input input-bordered flex items-center gap-2 flex-1 min-w-[220px]">
              <Icon icon="mdi:magnify" width="16" height="16" />
              <input
                type="search"
                placeholder="Search notifications..."
                class="grow"
                bind:value={searchQuery}
              />
            </label>
            <div class="tabs tabs-boxed bg-base-200 p-1">
              <button
                class="tab {filter === 'all' ? 'tab-active' : ''}"
                onclick={() => (filter = "all")}
              >
                All
              </button>
              <button
                class="tab {filter === 'unread' ? 'tab-active' : ''}"
                onclick={() => (filter = "unread")}
              >
                Unread {#if unreadCount > 0}<span class="ml-1">{unreadCount}</span>{/if}
              </button>
            </div>
          </div>
        </div>
      </section>

      <section class="space-y-3">
        {#each filtered as notice}
          <div
            class="card bg-base-100 dark:bg-base-100 shadow-sm border border-base-content/5 rounded-lg"
          >
            <div class="card-body p-4">
              <div class="flex items-start justify-between gap-3">
                <div class="flex items-start gap-3">
                  <div class="w-10 h-10 rounded-full bg-base-200 flex items-center justify-center">
                    <Icon
                      icon={typeConfig[notice.type].icon}
                      width="20"
                      height="20"
                      class={typeConfig[notice.type].color}
                    />
                  </div>
                  <div class="space-y-1">
                    <div class="flex items-center gap-2">
                      <h3 class="font-semibold text-sm text-base-content">
                        {notice.title}
                      </h3>
                      {#if !notice.read}
                        <span class="badge badge-primary badge-xs">New</span>
                      {/if}
                    </div>
                    <p class="text-sm text-base-content/70">{notice.message}</p>
                    <div class="flex items-center gap-2 text-xs text-base-content/50">
                      <span>{notice.time}</span>
                      {#if notice.ticketId}
                        <span class="badge badge-ghost badge-xs">
                          {notice.ticketId}
                        </span>
                      {/if}
                    </div>
                  </div>
                </div>
                <button
                  class="btn btn-xs btn-ghost"
                  onclick={() => markRead(notice.id)}
                >
                  Mark read
                </button>
              </div>
            </div>
          </div>
        {/each}

        {#if filtered.length === 0}
          <div class="text-sm text-base-content/60 text-center py-10">
            No notifications found.
          </div>
        {/if}
      </section>
    </div>
  </div>
</AdminLayout>

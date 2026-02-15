import { formatRelativeTime } from "./historyConfig.ts";

export function formatNotificationTimestamp(iso: string): string {
  if (!iso) return "";
  const d = new Date(iso);
  const fallback = Number.isNaN(d.getTime()) ? "" : d.toLocaleDateString();
  return formatRelativeTime(iso, fallback);
}

export const notificationConfig = {
    info: {
      icon: "mdi:information-outline",
      iconColor: "text-info",
      bgColor: "bg-info/10",
      borderColor: "border-info/20",
    },
    success: {
      icon: "mdi:check-circle-outline",
      iconColor: "text-success",
      bgColor: "bg-success/10",
      borderColor: "border-success/20",
    },
    warning: {
      icon: "mdi:alert-outline",
      iconColor: "text-warning",
      bgColor: "bg-warning/10",
      borderColor: "border-warning/20",
    },
    error: {
      icon: "mdi:close-circle-outline",
      iconColor: "text-error",
      bgColor: "bg-error/10",
      borderColor: "border-error/20",
    },
    default: {
    icon: "lucide:bell",
    bgColor: "bg-base-300",
    iconColor: "text-base-content",
  },
};
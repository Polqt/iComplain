function formatDateToCustomString(date: Date): string {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

    const day = date.getDate().toString().padStart(2, '0');

    const month = months[date.getMonth()];

    const year = date.getFullYear();

    return `${day} ${month} ${year}`;
}

function formatMobileDate(date: Date): string {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

    const day = date.getDate();

    const month = months[date.getMonth()];

    return `${month} ${day}`;
}

const currentDate = new Date();
export const formattedDate = formatDateToCustomString(currentDate);
export const mobileFormattedDate = formatMobileDate(currentDate);

export function formatDate(iso: string) {
    return new Date(iso).toLocaleString("en-US", {
        month: "long", day: "numeric", year: "numeric"
    })
}

export function formatDateTime(iso: string) {
    return new Date(iso).toLocaleString("en-US", {
        month: "short", day: "numeric", year: "numeric",
        hour: "numeric", minute: "2-digit"
    })
}

export function formatTime(iso: string): string {
    const d = new Date(iso);
    const now = new Date();
    const diffMs = now.getTime() - d.getTime();
    const diffMin = Math.floor(diffMs / 60_000);
    if (diffMin < 1) return "Just now";
    if (diffMin < 60) return `${diffMin} min ago`;
    const diffHr = Math.floor(diffMin / 60);
    if (diffHr < 24) return `${diffHr} hr ago`;
    const diffDay = Math.floor(diffHr / 24);
    if (diffDay < 7) return `${diffDay} day${diffDay > 1 ? "s" : ""} ago`;
    return d.toLocaleDateString("en-US", {
        year: "numeric", month: "short", day: "numeric", hour: "2-digit",minute: "2-digit"
    })
}
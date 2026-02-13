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
function formatDateToCustomString(date: Date): string {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

    const day = date.getDate().toString().padStart(2, '0');

    const month = months[date.getMonth()];

    const year = date.getFullYear();

    return `${day} ${month} ${year}`;
}


const currentDate = new Date();
export const formattedDate = formatDateToCustomString(currentDate);

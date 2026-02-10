import { PUBLIC_API_URL } from "$env/static/public";

const BASE = `${PUBLIC_API_URL}/notifications`;

async function handleRes(res: Response) {
    if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.message || res.statusText);
    }

    return res.json();
}

import { PUBLIC_API_URL } from '$env/static/public';
import type { RawAuthResponse, RawUser, User } from '../../types/user.ts';

const BASE = `${PUBLIC_API_URL}/user`;

async function handleRes<T>(res: Response): Promise<T> {
    if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error((body as { message?: string }).message || res.statusText);
    }
    return res.json() as Promise<T>;
}

function mapUser(raw: RawUser): User {
    const role = raw.role ?? 'student';

    return {
        id: raw.id,
        email: raw.email,
        is_active: raw.is_active ?? true,
        role,
    };
}

export async function register(email: string, password: string): Promise<User> {
    const res = await fetch(`${BASE}/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
        credentials: 'include',
    });

    const data = await handleRes<RawAuthResponse>(res);
    if (!data.success || !data.user) {
        throw new Error(data.message || 'Registration failed.');
    }

    return mapUser(data.user);
}

export async function login(email: string, password: string): Promise<User> {
    const res = await fetch(`${BASE}/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ email, password }),
    });

    const data = await handleRes<RawAuthResponse>(res);
    if (!data.success || !data.user) {
        throw new Error(data.message || 'Login failed.');
    }

    return mapUser(data.user);
}

export async function googleLogin(idToken: string): Promise<User> {
    const res = await fetch(`${BASE}/google-login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ id_token: idToken }),
    });

    const data = await handleRes<RawAuthResponse>(res);
    if (!data.success || !data.user) {
        throw new Error(data.message || 'Google login failed.');
    }

    return mapUser(data.user);
}

export async function getCurrentUser(): Promise<User | null> {
    const res = await fetch(`${BASE}/profile`, {
        method: 'GET',
        credentials: 'include',
    });

    if (!res.ok && (res.status === 401 || res.status === 403)) {
        return null;
    }

    const data = await handleRes<RawAuthResponse>(res);

    if (!data.success || !data.user) {
        return null;
    }

    return mapUser(data.user);
}

export async function logout(): Promise<void> {
    const res = await fetch(`${BASE}/logout`, {
        method: 'POST',
        credentials: 'include',
    });

    if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error((body as { message?: string }).message || res.statusText);
    }
}
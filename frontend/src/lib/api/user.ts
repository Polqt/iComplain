import { apiFetch, invalidateCsrfToken } from "../../utils/api.ts";
import type { RawAuthResponse, RawUser, User } from "../../types/user.ts";

const BASE = "/user";

async function handleRes<T>(res: Response): Promise<T> {
	if (!res.ok) {
		const body = await res.json().catch(() => ({}));
		throw new Error((body as { message?: string }).message || res.statusText);
	}
	return res.json() as Promise<T>;
}

function mapUser(raw: RawUser): User {
	const role = raw.role ?? "student";

	return {
		id: raw.id,
		email: raw.email,
		is_active: raw.is_active ?? true,
		role,
		name: raw.name ?? null,
		avatar: raw.avatar ?? null,
	};
}

export async function register(email: string, password: string): Promise<User> {
	const res = await apiFetch(`${BASE}/register`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ email, password }),
	});

	const data = await handleRes<RawAuthResponse>(res);
	if (!data.success || !data.user) {
		throw new Error(data.message || "Registration failed.");
	}

	invalidateCsrfToken();
	return mapUser(data.user);
}

export async function login(email: string, password: string): Promise<User> {
	const res = await apiFetch(`${BASE}/login`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ email, password }),
	});

	const data = await handleRes<RawAuthResponse>(res);
	if (!data.success || !data.user) {
		throw new Error(data.message || "Login failed.");
	}

	invalidateCsrfToken();
	return mapUser(data.user);
}

export async function googleLogin(idToken: string): Promise<User> {
	const res = await apiFetch(`${BASE}/google-login`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ id_token: idToken }),
	});

	const data = await handleRes<RawAuthResponse>(res);
	if (!data.success || !data.user) {
		throw new Error(data.message || "Google login failed.");
	}

	invalidateCsrfToken();
	return mapUser(data.user);
}

export async function getCurrentUser(): Promise<User | null> {
	const res = await apiFetch(`${BASE}/profile`, {
		method: "GET",
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
	const res = await apiFetch(`${BASE}/logout`, {
		method: "POST",
	});

	if (!res.ok) {
		const body = await res.json().catch(() => ({}));
		throw new Error((body as { message?: string }).message || res.statusText);
	}

	invalidateCsrfToken();
}

export interface ProfileUpdate {
	name?: string;
}

export async function updateProfile(profileData: ProfileUpdate): Promise<User> {
	const res = await apiFetch(`${BASE}/profile`, {
		method: "PATCH",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify(profileData),
	});

	const data = await handleRes<RawAuthResponse>(res);
	if (!data.success || !data.user) {
		throw new Error(data.message || "Failed to update profile.");
	}

	return mapUser(data.user);
}

export async function uploadAvatar(file: File): Promise<User> {
	const formData = new FormData();
	formData.append("file", file);

	const res = await apiFetch(`${BASE}/profile/avatar`, {
		method: "POST",
		body: formData,
	});

	const data = await handleRes<RawAuthResponse>(res);
	if (!data.success || !data.user) {
		throw new Error(data.message || "Failed to upload avatar.");
	}

	return mapUser(data.user);
}

export async function deleteAvatar(): Promise<User> {
	const res = await apiFetch(`${BASE}/profile/avatar`, {
		method: "DELETE",
	});

	const data = await handleRes<RawAuthResponse>(res);
	if (!data.success || !data.user) {
		throw new Error(data.message || "Failed to remove avatar.");
	}

	return mapUser(data.user);
}

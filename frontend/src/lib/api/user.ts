import { apiFetch, invalidateCsrfToken, resolveApiAssetUrl } from "../../utils/api.ts";
import { parseApiResponse, requestJson } from "./core.ts";
import type { RawAuthResponse, RawUser, User } from "../../types/user.ts";

const BASE = "/user";

function mapUser(raw: RawUser): User {
	const role = raw.role ?? "student";

	return {
		id: raw.id,
		email: raw.email,
		is_active: raw.is_active ?? true,
		role,
		name: raw.name ?? null,
		avatar: resolveApiAssetUrl(raw.avatar),
	};
}

export async function login(email: string, password: string): Promise<User> {
	const data = await requestJson<RawAuthResponse>(`${BASE}/login`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ email, password }),
	});

	if (!data.success || !data.user) {
		throw new Error(data.message || "Login failed.");
	}

	invalidateCsrfToken();
	return mapUser(data.user);
}

export async function googleLogin(idToken: string): Promise<User> {
	const data = await requestJson<RawAuthResponse>(`${BASE}/google-login`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ id_token: idToken }),
	});

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

	const data = await parseApiResponse<RawAuthResponse>(res);

	if (!data.success || !data.user) {
		return null;
	}

	return mapUser(data.user);
}

export async function logout(): Promise<void> {
	await requestJson<RawAuthResponse>(`${BASE}/logout`, {
		method: "POST",
	});

	invalidateCsrfToken();
}

export interface ProfileUpdate {
	name?: string;
}

export async function updateProfile(profileData: ProfileUpdate): Promise<User> {
	const data = await requestJson<RawAuthResponse>(`${BASE}/profile`, {
		method: "PATCH",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify(profileData),
	});

	if (!data.success || !data.user) {
		throw new Error(data.message || "Failed to update profile.");
	}

	return mapUser(data.user);
}

export async function uploadAvatar(file: File): Promise<User> {
	const formData = new FormData();
	formData.append("file", file);

	const data = await requestJson<RawAuthResponse>(`${BASE}/profile/avatar`, {
		method: "POST",
		body: formData,
	});

	if (!data.success || !data.user) {
		throw new Error(data.message || "Failed to upload avatar.");
	}

	return mapUser(data.user);
}

export async function deleteAvatar(): Promise<User> {
	const data = await requestJson<RawAuthResponse>(`${BASE}/profile/avatar`, {
		method: "DELETE",
	});

	if (!data.success || !data.user) {
		throw new Error(data.message || "Failed to remove avatar.");
	}

	return mapUser(data.user);
}

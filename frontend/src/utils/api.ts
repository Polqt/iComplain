import { PUBLIC_API_URL, PUBLIC_GOOGLE_CLIENT_ID } from "$env/static/public";

const DEFAULT_API_BASE = "http://localhost:8000/api";
const SAFE_METHODS = new Set(["GET", "HEAD", "OPTIONS", "TRACE"]);

function isAbsoluteUrl(value: string): boolean {
	return /^https?:\/\//i.test(value);
}

function hasNonHttpScheme(value: string): boolean {
	return /^[a-z][a-z0-9+.-]*:/i.test(value);
}

function isLocalHost(value: string): boolean {
	return /^(localhost|127(?:\.\d{1,3}){3})(:\d+)?(\/|$)/i.test(value);
}

function normalizeApiBase(rawValue: string | undefined): string {
	const trimmed = rawValue?.trim().replace(/\/+$/, "") ?? "";

	if (!trimmed) {
		return DEFAULT_API_BASE;
	}

	if (trimmed.startsWith("/")) {
		return trimmed === "/" ? "/api" : trimmed;
	}

	const candidate = isAbsoluteUrl(trimmed)
		? trimmed
		: `${isLocalHost(trimmed) ? "http" : "https"}://${trimmed}`;
	const url = new URL(candidate);

	if (!url.pathname || url.pathname === "/") {
		url.pathname = "/api";
	}

	return url.toString().replace(/\/+$/, "");
}

function joinApiPath(path: string): string {
	const suffix = path.startsWith("/") ? path : `/${path}`;
	return `${API_BASE}${suffix}`;
}

function describeApiTarget(path: string): string {
	const requestUrl = joinApiPath(path);

	if (isAbsoluteUrl(requestUrl)) {
		return requestUrl;
	}

	const browserOrigin =
		typeof window !== "undefined" ? window.location.origin : undefined;

	return browserOrigin ? new URL(requestUrl, browserOrigin).toString() : requestUrl;
}

function createApiConnectivityError(path: string, cause: unknown): Error {
	const apiOrigin = getApiOrigin() ?? API_BASE;
	const error = new Error(
		`Unable to reach the API at ${apiOrigin}. Check PUBLIC_API_URL and the backend CORS_ALLOWED_ORIGINS/CSRF_TRUSTED_ORIGINS configuration.`,
	);

	Object.assign(error, {
		cause,
		target: describeApiTarget(path),
	});

	return error;
}

async function requestApi(path: string, init: RequestInit): Promise<Response> {
	try {
		return await fetch(joinApiPath(path), init);
	} catch (error) {
		throw createApiConnectivityError(path, error);
	}
}

export function getApiOrigin(fallbackOrigin?: string): string | null {
	if (isAbsoluteUrl(API_BASE)) {
		return new URL(API_BASE).origin;
	}

	if (API_BASE.startsWith("/")) {
		const baseOrigin =
			fallbackOrigin ??
			(typeof window !== "undefined" ? window.location.origin : undefined);

		return baseOrigin ? new URL(API_BASE, baseOrigin).origin : null;
	}

	return null;
}

export function resolveApiAssetUrl(
	value: string | null | undefined,
	fallbackOrigin?: string,
): string | null {
	if (!value) {
		return null;
	}

	const trimmed = value.trim();
	if (!trimmed) {
		return null;
	}

	if (isAbsoluteUrl(trimmed) || trimmed.startsWith("//") || hasNonHttpScheme(trimmed)) {
		return trimmed;
	}

	const apiOrigin = getApiOrigin(fallbackOrigin);
	if (!apiOrigin) {
		return trimmed;
	}

	return new URL(trimmed, apiOrigin).toString();
}

let csrfToken: string | null = null;
let csrfTokenPromise: Promise<string> | null = null;

export async function getCsrfToken(forceRefresh = false): Promise<string> {
	if (!forceRefresh && csrfToken) {
		return csrfToken;
	}

	if (!forceRefresh && csrfTokenPromise) {
		return csrfTokenPromise;
	}

	csrfTokenPromise = requestApi("/user/csrf", {
		method: "GET",
		credentials: "include",
		headers: {
			Accept: "application/json",
		},
	})
		.then(async (res) => {
			if (!res.ok) {
				throw new Error("Failed to initialize CSRF protection.");
			}

			const data = (await res.json()) as { csrfToken?: string };
			if (!data.csrfToken) {
				throw new Error("CSRF token was not returned by the server.");
			}

			csrfToken = data.csrfToken;
			return data.csrfToken;
		})
		.finally(() => {
			csrfTokenPromise = null;
		});

	return csrfTokenPromise;
}

export function invalidateCsrfToken(): void {
	csrfToken = null;
}

export async function apiFetch(
	path: string,
	init: RequestInit = {},
): Promise<Response> {
	const method = (init.method ?? "GET").toUpperCase();
	const headers = new Headers(init.headers ?? {});

	if (!headers.has("Accept")) {
		headers.set("Accept", "application/json");
	}

	if (!SAFE_METHODS.has(method)) {
		headers.set("X-CSRFToken", await getCsrfToken());
	}

	return requestApi(path, {
		credentials: "include",
		...init,
		headers,
	});
}

/**
 * API base URL for the Django backend.
 * Accepts either a full `/api` URL or a bare backend origin and normalizes it.
 */
export const API_BASE = normalizeApiBase(PUBLIC_API_URL);

/**
 * Google OAuth 2.0 Web client ID (public).
 * Set PUBLIC_GOOGLE_CLIENT_ID in .env or .env.local to enable "Sign in with Google".
 */
export const GOOGLE_CLIENT_ID =
	typeof PUBLIC_GOOGLE_CLIENT_ID === "string" ? PUBLIC_GOOGLE_CLIENT_ID : "";

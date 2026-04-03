import type { Handle, HandleServerError } from "@sveltejs/kit";
import { redirect } from "@sveltejs/kit";
import { getApiOrigin } from "../utils/api.ts";

function isSameOriginApi(requestOrigin: string): boolean {
	return getApiOrigin(requestOrigin) === requestOrigin;
}

export const handle: Handle = async ({ event, resolve }) => {
	// When the API is hosted on another origin (e.g. Vercel frontend + Railway backend),
	// the Django session cookie is scoped to the API domain and is not visible here.
	// In that setup, rely on the client-side auth bootstrap instead of SSR cookie redirects.
	if (!isSameOriginApi(event.url.origin)) {
		return resolve(event);
	}

	const sessionCookie = event.cookies.get("sessionid");
	const authHeader = event.request.headers.get("authorization");
	const hasAuthCookie = !!sessionCookie || !!authHeader;

	// Define protected routes
	const protectedRoutes = [
		"/dashboard",
		"/profile",
		"/settings",
		"/tickets",
		"/history",
		"/notifications",
		"/community-board",
		"/help",
	];

	// Auth Routes
	const authRoutes = ["/signin", "/not-signed-in"];

	// Check if current route is protected
	const isProtectedRoute = protectedRoutes.some((path) =>
		event.url.pathname.startsWith(path),
	);
	const isAuthRoute = authRoutes.some((path) =>
		event.url.pathname.startsWith(path),
	);

	// Redirect unauthenticated users from protected routes
	if (isProtectedRoute && !hasAuthCookie) {
		return redirect(303, "/not-signed-in");
	}

	// Redirect authenticated users away from auth pages
	if (isAuthRoute && hasAuthCookie) {
		return redirect(303, "/dashboard");
	}

	const response = await resolve(event);
	return response;
};

export const handleError: HandleServerError = async ({ error, event }) => {
	return {
		message: "An internal server error occurred.",
		code: (error as any)?.code ?? "INTERNAL_SERVER_ERROR",
	};
};

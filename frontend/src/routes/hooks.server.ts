import type { Handle, HandleServerError } from "@sveltejs/kit"
import { redirect } from "@sveltejs/kit";

export const handle: Handle = async ({ event, resolve }) => {
    // Get authentication cookie from request headers
    const cookieHeader = event.request.headers.get('cookie') || '';
    const hasAuthCookie = cookieHeader.includes('sessionid') || cookieHeader.includes('Authorization');

    // Define protected routes
    const protectedRoutes = ['/dashboard', '/profile', '/settings', '/tickets', '/history', '/notifications'];

    // Auth Routes
    const authRoutes = ['/signin', '/signup', '/not-signed-in'];

    // Check if current route is protected
    const isProtectedRoute = protectedRoutes.some(path => event.url.pathname.startsWith(path));
    const isAuthRoute = authRoutes.some(path => event.url.pathname.startsWith(path));

    // Redirect unauthenticated users from protected routes
    if (isProtectedRoute && !hasAuthCookie) {
        return redirect(303, '/not-signed-in');
    }

    // Redirect authenticated users away from auth pages
    if (isAuthRoute && hasAuthCookie) {
        return redirect(303, '/dashboard');
    }

    const response = await resolve(event);
    return response;
}

export const handleError: HandleServerError = async ({ error, event }) => {
    return {
        message: 'An internal server error occurred.',
        code:  (error as any)?.code ?? 'INTERNAL_SERVER_ERROR'
    }
}
import type { Handle, HandleServerError } from "@sveltejs/kit"

export const handle: Handle = async ({ event, resolve }) => {
    // TODO: Get user session from cookies or headers

    // TODO: Define protected routes
    const protectedRoutes = ['/dashboard', '/profile'];

    // Auth Routes
    const authRoutes = ['/signin', '/signup'];

    // TODO: Redirect unauthenticated users from protected routes
    // if (protectedRoutes.some(path => event.url.pathname.startsWith(path)) && !user) {
    //     return Response.redirect('/not-signed-in', 303);
    // }

    // TODO: Determine user role and redirect accordingly

    const response = await resolve(event);
    return response;
}

export const handleError: HandleServerError = async ({ error, event }) => {
    return {
        message: 'An internal server error occurred.',
        code:  (error as any)?.code ?? 'INTERNAL_SERVER_ERROR'
    }
}
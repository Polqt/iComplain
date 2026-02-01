import type { Handle, HandleServerError } from "@sveltejs/kit"

export const handle: Handle = async ({ event, resolve }) => {
    const url = event.url

    // TODO: Get user session from cookies or headers

    // TODO: Define protected routes
    const authRoutes = ['/signin', '/signup'];

    // TODO: Redirect unauthenticated users from protected routes

    // TODO: Redirect authenticated users away from auth routes to dashboard

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
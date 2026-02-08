import { PUBLIC_API_URL, PUBLIC_GOOGLE_CLIENT_ID } from '$env/static/public';

/**
 * API base URL for the Django backend.
 * Set PUBLIC_API_URL in .env or .env.local (e.g. http://localhost:8000/api) to override.
 */
export const API_BASE =
	typeof PUBLIC_API_URL === 'string' && PUBLIC_API_URL
		? PUBLIC_API_URL.replace(/\/$/, '')
		: 'http://localhost:8000/api';

/**
 * Google OAuth 2.0 Web client ID (public).
 * Set PUBLIC_GOOGLE_CLIENT_ID in .env or .env.local to enable "Sign in with Google".
 */
export const GOOGLE_CLIENT_ID = typeof PUBLIC_GOOGLE_CLIENT_ID === 'string' ? PUBLIC_GOOGLE_CLIENT_ID : '';

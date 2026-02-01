// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
declare global {
	namespace App {
		interface Error {
			message: string;
			code?: string;
		}
		interface Locals {
			user: {
				id: string;
				email: string;
				role: 'student' | 'admin';
			} | null;
		}
		interface PageData {
			user?: {
				id: string;
				email: string;
				role: 'student' | 'admin';
			};
		}
		// interface PageState {}
		// interface Platform {}
	}
}

export {};

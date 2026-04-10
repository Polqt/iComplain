import type { HandleClientError } from "@sveltejs/kit";

export const handleError: HandleClientError = async ({
	error,
	event,
	status,
	message,
}) => {
	const errorId = crypto.randomUUID();

	const userMessage =
		status === 404
			? "Page not found."
			: status === 403
				? "You don't have permission to view this page."
				: status === 401
					? "You need to sign in to continue."
					: message || "Something went wrong. Please try again.";

	return {
		message: userMessage,
		errorId,
	};
};

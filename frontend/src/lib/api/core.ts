import { apiFetch } from "../../utils/api.ts";

type ErrorLike = {
	message?: string;
	detail?: string | Array<{ msg?: string }>;
};

function stringifyDetail(detail: ErrorLike["detail"]): string | undefined {
	if (Array.isArray(detail)) {
		return detail.map((item) => item?.msg).filter(Boolean).join(", ");
	}
	return typeof detail === "string" ? detail : undefined;
}

export async function parseJsonOrEmpty<T>(response: Response): Promise<T | null> {
	if (response.status === 204) {
		return null;
	}
	return (await response.json().catch(() => null)) as T | null;
}

export async function parseApiResponse<T>(response: Response): Promise<T> {
	if (!response.ok) {
		const body = (await parseJsonOrEmpty<ErrorLike>(response)) ?? {};
		const detail = stringifyDetail(body.detail);
		throw new Error(body.message || detail || response.statusText);
	}

	const data = await parseJsonOrEmpty<T>(response);
	if (data === null) {
		throw new Error("Expected response body but none was returned.");
	}

	return data;
}

export async function requestJson<T>(path: string, init: RequestInit = {}): Promise<T> {
	const response = await apiFetch(path, init);
	return parseApiResponse<T>(response);
}

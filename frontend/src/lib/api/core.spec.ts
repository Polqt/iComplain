import { describe, expect, it } from "vitest";
import { vi } from "vitest";

vi.mock("../../utils/api.ts", () => ({
	apiFetch: vi.fn(),
}));

import { parseApiResponse } from "./core.ts";

describe("api core", () => {
	it("parses successful JSON responses", async () => {
		const res = new Response(JSON.stringify({ ok: true }), {
			status: 200,
			headers: { "Content-Type": "application/json" },
		});

		const data = await parseApiResponse<{ ok: boolean }>(res);
		expect(data.ok).toBe(true);
	});

	it("normalizes API errors", async () => {
		const res = new Response(JSON.stringify({ detail: "Unauthorized" }), {
			status: 401,
			headers: { "Content-Type": "application/json" },
		});

		await expect(parseApiResponse(res)).rejects.toThrow("Unauthorized");
	});
});

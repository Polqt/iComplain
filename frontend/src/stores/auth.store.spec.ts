import { get } from "svelte/store";
import { beforeEach, describe, expect, it, vi } from "vitest";

const {
	gotoMock,
	loginMock,
	googleLoginMock,
	getCurrentUserMock,
	logoutMock,
} = vi.hoisted(() => ({
	gotoMock: vi.fn(),
	loginMock: vi.fn(),
	googleLoginMock: vi.fn(),
	getCurrentUserMock: vi.fn(),
	logoutMock: vi.fn(),
}));

vi.mock("$app/navigation", () => ({
	goto: gotoMock,
}));

vi.mock("../lib/api/user.ts", () => ({
	login: loginMock,
	googleLogin: googleLoginMock,
	getCurrentUser: getCurrentUserMock,
	logout: logoutMock,
}));

import { authStore } from "./auth.store.ts";

const student = {
	id: 1,
	email: "student@usls.edu.ph",
	is_active: true,
	role: "student" as const,
	name: "Student",
	avatar: null,
};

describe("authStore", () => {
	beforeEach(() => {
		loginMock.mockReset();
		googleLoginMock.mockReset();
		getCurrentUserMock.mockReset();
		logoutMock.mockReset();
		gotoMock.mockReset();
	});

	it("checkAuth sets authenticated state when API returns user", async () => {
		getCurrentUserMock.mockResolvedValue(student);

		const ok = await authStore.checkAuth();
		const state = get(authStore);

		expect(ok).toBe(true);
		expect(state.isAuthenticated).toBe(true);
		expect(state.user?.email).toBe("student@usls.edu.ph");
	});

	it("checkAuth preserves state on transient API failure", async () => {
		getCurrentUserMock.mockResolvedValueOnce(student);
		await authStore.checkAuth();

		getCurrentUserMock.mockRejectedValueOnce(new Error("network"));
		const ok = await authStore.checkAuth();
		const state = get(authStore);

		expect(ok).toBe(false);
		expect(state.isAuthenticated).toBe(true);
		expect(state.user?.email).toBe("student@usls.edu.ph");
	});

	it("logout clears auth state and redirects to signin", async () => {
		getCurrentUserMock.mockResolvedValue(student);
		await authStore.checkAuth();

		logoutMock.mockResolvedValue(undefined);
		await authStore.logout();

		const state = get(authStore);
		expect(state.isAuthenticated).toBe(false);
		expect(state.user).toBeNull();
		expect(gotoMock).toHaveBeenCalledWith("/signin");
	});
});

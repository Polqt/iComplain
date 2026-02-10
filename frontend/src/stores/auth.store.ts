import { goto } from "$app/navigation";
import { writable, type Readable } from "svelte/store";
import type { AuthState, User, UserRole } from "../types/user.ts";

import {
    login as apiLogin,
    googleLogin as apiGoogleLogin,
    getCurrentUser as apiGetCurrentUser,
    logout as apiLogout,
} from "../lib/api/user.ts";

interface AuthStore extends Readable<AuthState> {

    loginWithEmailPassword: (email: string, password: string) => Promise<void>;

    loginWithGoogle: (idToken: string) => Promise<void>;

    logout: () => Promise<void>;

    checkAuth: () => Promise<boolean>;

    updateUser: (updates: Partial<User>) => void;
}

function createAuthStore(): AuthStore {
    const { subscribe, set, update } = writable<AuthState>({
        user: null,
        isAuthenticated: false,
        isLoading: true,
        role: null,
    });

    const setAuthenticatedUser = (user: User) => {
        set({
            user,
            isAuthenticated: true,
            isLoading: false,
            role: user.role ?? null,
        });
    };

    const clearAuthState = () => {
        set({
            user: null,
            isAuthenticated: false,
            isLoading: false,
            role: null,
        });
    };

    return {
        subscribe,

        async loginWithEmailPassword(email: string, password: string): Promise<void> {
            try {
                const user = await apiLogin(email, password);
                setAuthenticatedUser(user);
            } catch (error) {
                clearAuthState();
                throw error;
            }
        },

        async loginWithGoogle(idToken: string): Promise<void> {
            try {
                const user = await apiGoogleLogin(idToken);
                setAuthenticatedUser(user);
            } catch (error) {
                clearAuthState();
                throw error;
            }
        },

        async logout(): Promise<void> {
            try {
                await apiLogout();
            } catch {
            }

            clearAuthState();

            if (typeof window !== "undefined") {
                sessionStorage.clear();
                localStorage.removeItem("rememberMe");
            }

            goto("/signin");
        },

        async checkAuth(): Promise<boolean> {
            try {
                const user = await apiGetCurrentUser();
                if (user) {
                    setAuthenticatedUser(user);
                    return true;
                }

                clearAuthState();
                return false;
            } catch {
                clearAuthState();
                return false;
            }
        },

        updateUser: (updates: Partial<User>) => {
            update((state) => ({
                ...state,
                user: state.user ? { ...state.user, ...updates } : null,
            }));
        },
    };
}

export const authStore = createAuthStore();

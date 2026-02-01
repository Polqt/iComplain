import { goto } from "$app/navigation";
import { writable, type Readable } from "svelte/store";

type UserRole = 'student' | 'admin';

type User = {
    id: string;
    email: string;
    role: UserRole;
    [key: string]: any;
}

type AuthState = {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    role: UserRole | null;
}

interface AuthStore extends Readable<AuthState> {
    login: (userData: User) => void;
    logout: () => void;
    checkAuth: () => Promise<boolean>;
    updateUser: (updates: Partial<User>) => void;
}

function createAuthStore(): AuthStore {
    const { subscribe, set, update } = writable<AuthState>({
        user: null,
        isAuthenticated: false,
        isLoading: true,
        role: null,
    })
    
    return {
        subscribe,

        /**
         * Set user data upon login.
         */
        login: (userData: User) => {
            set({
                user: userData,
                isAuthenticated: true,
                isLoading: false,
                role: userData.role,
            })
        },

        /**
         * Clear user data upon logout.
         */
        logout: async () => {
            set({
                user: null,
                isAuthenticated: false,
                isLoading: false,
                role: null,
            })

            // Clear user session from local storage
            if (typeof window !== 'undefined') {
                sessionStorage.clear();
                localStorage.removeItem('rememberMe');
            }

            goto('/signin');
        },

        /**
         * Check if user is authenticated (e.g., on app load).
         */
        checkAuth: async (): Promise<boolean> => {
            try {
                // TODO: Implement actual auth check logic (e.g., API call)
                const response = await fetch('', {
                    credentials: 'include',
                })

                if (response.ok) {
                    const userData: User = await response.json();
                    set({
                        user: userData,
                        isAuthenticated: true,
                        isLoading: false,
                        role: userData.role,
                    });
                    return true;
                } else {
                    set({
                        user: null,
                        isAuthenticated: false,
                        isLoading: false,
                        role: null,
                    })
                    return false;
                }
            } catch (error) {
                set({
                    user: null,
                    isAuthenticated: false,
                    isLoading: false,
                    role: null,
                })
                return false;
            }
        },

        /**
         * Update user data in the store.
         */
        updateUser: (updates: Partial<User>) => {
            update(state => ({
                ...state,
                usesr: state.user ? { ...state.user, ...updates } : null
            }));
        }
    }
}

export const authStore = createAuthStore();


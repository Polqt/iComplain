export type UserRole = 'student' | 'admin';

export type User = {
    id: number;
    email: string;
    is_active: boolean;
    role: UserRole;
    name?: string | null;
    avatar?: string | null;
}

export type ProfileUser = {
    name: string;
    email: string;
    avatar: string;
    role: UserRole;
}

export type RawUser = {
    id: number;
    email: string;
    is_active?: boolean;
    role?: UserRole;
    name?: string | null;
    avatar?: string | null;
};

export type RawAuthResponse = {
    success: boolean;
    message: string;
    user: RawUser | null;
};

export type AuthState = {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    role: UserRole | null;
};
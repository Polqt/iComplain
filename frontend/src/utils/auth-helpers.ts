type FormErrors = {
    email: string;
    password: string;
    confirmPassword: string;
    general: string;
}

type UserData = {
    id: string;
    email: string;
    role: 'student' | 'admin';
    [key: string]: any;
}

export function createFormErrors(): FormErrors {
    return {
        email: '',
        password: '',
        confirmPassword: '',
        general: '',
    }
}

export function handleAuthError(error: any): string {
    const errorMessages: Record<string, string> = {
        'auth/invalid-email': 'The email address is not valid.',
        'auth/user-disabled': 'The user account has been disabled.',
        'auth/user-not-found': 'No user found with the provided email.',
        'auth/wrong-password': 'The password is incorrect.',
        'auth/email-already-in-use': 'The email address is already in use by another account.',
        'auth/weak-password': 'The password is too weak. Please choose a stronger password.',
        'auth/too-many-requests': 'Too many unsuccessful login attempts. Please try again later.',
        'auth/network-request-failed': 'A network error has occurred. Please check your connection and try again.',
    }

    if (error?.code && errorMessages[error.code]) {
        return errorMessages[error.code];
    }

    if (error?.message) {
        return error.message;
    }

    return 'An unknown error has occurred. Please try again.';
}

/**
 * Store user session data in local storage.
 */
export function setUserSession(token: string, userId: string): void {

}


/**
 * Get stored user session data from local storage.
 */
export function getUserSession(): UserData | null {
    if (typeof window === 'undefined') {
        const data = localStorage.getItem('user');
        return data ? JSON.parse(data) : null;
    }
    return null;
}

/**
 * Clear user session data from local storage.
 */
export function clearUserSession(userData: UserData | null): void {
    if (typeof window === 'undefined') return;

    if (userData) {
        localStorage.setItem('user', JSON.stringify(userData));
        localStorage.setItem('userId', userData.id);
    } else {
        localStorage.removeItem('user');
        localStorage.removeItem('userId');
    }
}

/**
 * Handle `remember me` functionality by storing or clearing session data based on user preference.
 */
export function handleRememberMe(remember: boolean, email: string): void {
    if (typeof window !== 'undefined') {
        if (remember) {
            localStorage.setItem('rememberMe', email);
        } else {
            localStorage.removeItem('rememberMe');
        }
    }
}

/**
 * Get stored `remember me` email from local storage.
 */
export function getRememberEmail(): string | null {
    if (typeof window !== 'undefined') {
        return localStorage.getItem('rememberMe');
    }

    return null;
}

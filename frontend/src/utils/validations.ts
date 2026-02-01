export interface ValidationResult {
    valid: boolean;
    message: string;
    warning?: boolean;
}

export interface PasswordValidationResult extends ValidationResult {
    strength?: 'weak' | 'medium' | 'strong';
}

export function isValidEmail(email: string): ValidationResult {
    if (!email) {
        return {
            valid: false,
            message: 'Email is required.',
        };
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        return {
            valid: false,
            message: 'Invalid email format.',
        }
    }

    if (!email.toLowerCase().endsWith('@usls.edu.ph')) {
        return {
            valid: false,
            message: 'Email must be a valid @usls.edu.ph address.',
            warning: true,
        }
    }

    return {
        valid: true,
        message: '',
    }
}

export function validatePassword(password: string): PasswordValidationResult {
    if (!password) {
        return {
            valid: false,
            message: 'Password is required.',
            strength: 'weak',
        }
    }

    if (password.length < 8) {
        return {
            valid: false,
            message: 'Password must be at least 8 characters long.',
            strength: 'weak',
        }
    }

    let strength: 'weak' | 'medium' | 'strong' = 'weak';
    let score = 0;

    if (/[a-z]/.test(password)) score++; 
    if (/[A-Z]/.test(password)) score++; 
    if (/[0-9]/.test(password)) score++;
    if (/[^A-Za-z0-9]/.test(password)) score++; 

    if (password.length >= 8 && score >= 2) strength = 'medium';
    if (password.length >= 12 && score >= 3) strength = 'strong';

    const messages: Record<'weak' | 'medium' | 'strong', string> = {
        weak: 'Weak! Consider adding uppercase letters, numbers, and special characters.',
        medium: 'Good! Adding more variety can make it stronger.',
        strong: 'Strong password!',
    }

    return {
        valid: strength !== 'weak',
        message: messages[strength],
        strength,
    };
}

export function validatePasswordMatch(password: string, confirmPassword: string): ValidationResult {
    if (!confirmPassword) {
        return {
            valid: false,
            message: 'Please confirm your password.',
        }
    }

    if (password !== confirmPassword) {
        return {
            valid: false,
            message: 'Passwords do not match.',
        }
    }

    return {
        valid: true,
        message: 'Passwords match',
    }
}

export function sanitizeInput(input: string): string {
    if (typeof input !== 'string') return '';
    return input.trim();
}

export function validateField(
    fieldName: string,
    value: string,
    option: { password?: string } = {}
): ValidationResult | PasswordValidationResult {4
    const sanitized = sanitizeInput(value);
    
    switch (fieldName) {
        case 'email':
            return isValidEmail(sanitized);
        case 'password':
            return validatePassword(sanitized);
        case 'confirmPassowrd':
            return validatePasswordMatch(option.password || '', sanitized);
        default:
            if (!sanitized) {
                return {
                    valid: false,
                    message: `{fieldName} is required.`,
                }
            }
            return {
                valid: true,
                message: '',
            }
    }
}
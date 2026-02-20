export const AVATAR_UPLOAD = {
  maxFileSize: 5 * 1024 * 1024, // 5MB
  allowedTypes: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'] as const,
  allowedTypesDisplay: 'JPEG, PNG, GIF, or WebP',
};

export type ValidationResult = {
  valid: boolean;
  error: string | null;
};

export function validateImageFile(file: File): ValidationResult {
  if (!AVATAR_UPLOAD.allowedTypes.includes(file.type as typeof AVATAR_UPLOAD.allowedTypes[number])) {
    return { valid: false, error: `Please select a ${AVATAR_UPLOAD.allowedTypesDisplay} image.` };
  }

  if (file.size > AVATAR_UPLOAD.maxFileSize) {
    return { valid: false, error: `File too large. Maximum size is ${AVATAR_UPLOAD.maxFileSize / 1024 / 1024}MB.` };
  }

  return { valid: true, error: null };
}

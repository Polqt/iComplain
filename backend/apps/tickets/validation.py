ALLOWED_TYPES = ['image/jpeg', 'image/png', 'application/pdf']
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

def validate_file(file):
    if file.content_type not in ALLOWED_TYPES:
        raise ValueError("Unsupported file type.")
    if file.size > MAX_FILE_SIZE:
        raise ValueError("File size exceeds the maximum limit.")
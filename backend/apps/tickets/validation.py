ALLOWED_TYPES = ['image/jpeg', 'image/png', 'application/pdf', 'image/webp']
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

MAGIC_BYTES = {
    'image/jpeg': [
        b'\xFF\xD8\xFF',  # JPEG
    ],
    'image/png': [
        b'\x89PNG\r\n\x1a\n',  # PNG
    ],
    'image/webp': [
        b'RIFF',  # WebP (first 4 bytes, followed by 'WEBP' at offset 8)
    ],
    'application/pdf': [
        b'%PDF-',  # PDF
    ],
}

def matches_magic_bytes(header: bytes, content_type: str) -> bool:
    if content_type == 'image/webp':
        # WebP: "RIFF" at start and "WEBP" at offset 8
        return header.startswith(b'RIFF') and header[8:12] == b'WEBP'

    magic_bytes_list = MAGIC_BYTES.get(content_type, ())
    return any(header.startswith(magic) for magic in magic_bytes_list)

def validate_file(file):
    if file.content_type not in ALLOWED_TYPES:
        raise ValueError("Unsupported file type.")
    if file.size > MAX_FILE_SIZE:
        raise ValueError("File size exceeds the maximum limit.")
    
    # Validate magic bytes (prevent extension spoofing)
    file.seek(0) 
    header = file.read(12) # Read first 12 bytes for magic byte validation
    file.seek(0) # Reset file pointer after reading
    
    if file.content_type in MAGIC_BYTES and not matches_magic_bytes(header, file.content_type):
        raise ValueError("File content does not match its declared type.")

    return True
    
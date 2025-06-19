import hashlib
import os

SCANNER_HASHES = {
    "gitleaks": "sha256:...",
    "semgrep": "sha256:...",
    # дополни актуальными хэшами бинарников/CLI-скриптов
}

def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def check_integrity(scanner_bin, expected_sha256):
    actual_sha256 = file_sha256(scanner_bin)
    return actual_sha256 == expected_sha256
import subprocess
import shutil
import hashlib
import os

SCANNERS = [
    "gitleaks",
    "semgrep",
    "bandit",
    "brakeman",
    "eslint",
    "trufflehog",
    "checkov",
    "tfsec",
    "kubesec",
    "trivy",
    "dockle",
    "syft",
    "osv-scanner"
]

def which(bin_name):
    return shutil.which(bin_name)

def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def main():
    hashes = {}
    for scanner in SCANNERS:
        path = which(scanner)
        if not path:
            print(f"[!] {scanner} not found in PATH")
            continue
        sha = file_sha256(path)
        hashes[scanner] = f"sha256:{sha}"
        print(f"{scanner:12}: {path}\n  -> sha256:{sha}")
    print("\n--- SCANNER_HASHES for paste ---\n")
    print("SCANNER_HASHES = {")
    for k, v in hashes.items():
        print(f'    "{k}": "{v}",')
    print("}")

if __name__ == "__main__":
    main()
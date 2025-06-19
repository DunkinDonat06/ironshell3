import subprocess

def get_licenses(target_dir):
    cmd = ["syft", target_dir, "-o", "json"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    # Простая выборка лицензий из результата syft
    import json
    data = json.loads(result.stdout)
    licenses = set()
    for pkg in data.get("artifacts", []):
        lic = pkg.get("licenses") or []
        for l in lic:
            licenses.add(l)
    return list(licenses)
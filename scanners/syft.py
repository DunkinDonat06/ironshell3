import subprocess
import json

class Scanner:
    def __init__(self, profile=None, logger=None):
        self.profile = profile or {}
        self.logger = logger

    def run(self):
        cmd = ["syft", ".", "-o", "json"]
        for k, v in self.profile.get("syft", {}).items():
            cmd.extend([f"--{k}", str(v)])
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if result.returncode != 0:
                if self.logger:
                    self.logger.error(f"Syft failed: {result.stderr}")
                return []
            syft_json = json.loads(result.stdout)
            findings = []
            for pkg in syft_json.get("artifacts", []):
                findings.append({
                    "severity": "info",
                    "title": pkg.get("name", ""),
                    "description": f"SBOM: {pkg.get('version', '')} ({pkg.get('type', '')})"
                })
            return findings
        except Exception as e:
            if self.logger:
                self.logger.error(f"Syft error: {e}")
            return []
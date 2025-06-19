import subprocess
import json

class Scanner:
    def __init__(self, profile=None, logger=None):
        self.profile = profile or {}
        self.logger = logger

    def run(self):
        cmd = ["dockle", "-f", "json", "."]
        for k, v in self.profile.get("dockle", {}).items():
            cmd.extend([f"--{k}", str(v)])
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if result.returncode != 0:
                if self.logger:
                    self.logger.error(f"Dockle failed: {result.stderr}")
                return []
            dockle_json = json.loads(result.stdout)
            findings = []
            for detail in dockle_json.get("details", []):
                findings.append({
                    "severity": detail.get("level", "N/A"),
                    "title": detail.get("code", ""),
                    "description": detail.get("title", "")
                })
            return findings
        except Exception as e:
            if self.logger:
                self.logger.error(f"Dockle error: {e}")
            return []
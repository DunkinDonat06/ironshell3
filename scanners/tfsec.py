import subprocess
import json

class Scanner:
    def __init__(self, profile=None, logger=None):
        self.profile = profile or {}
        self.logger = logger

    def run(self):
        cmd = ["tfsec", ".", "--format", "json"]
        for k, v in self.profile.get("tfsec", {}).items():
            cmd.extend([f"--{k}", str(v)])
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if result.returncode != 0:
                if self.logger:
                    self.logger.error(f"Tfsec failed: {result.stderr}")
                return []
            tfsec_json = json.loads(result.stdout)
            findings = []
            for r in tfsec_json.get("results", []):
                findings.append({
                    "severity": r.get("severity", "N/A"),
                    "title": r.get("rule_id", ""),
                    "description": r.get("description", "")
                })
            return findings
        except Exception as e:
            if self.logger:
                self.logger.error(f"Tfsec error: {e}")
            return []
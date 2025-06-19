import subprocess
import json

class Scanner:
    def __init__(self, profile=None, logger=None):
        self.profile = profile or {}
        self.logger = logger

    def run(self):
        cmd = ["kubesec", "scan", "."]
        for k, v in self.profile.get("kubesec", {}).items():
            cmd.extend([f"--{k}", str(v)])
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if result.returncode != 0:
                if self.logger:
                    self.logger.error(f"Kubesec failed: {result.stderr}")
                return []
            kubesec_json = json.loads(result.stdout)
            findings = []
            for file_result in kubesec_json:
                for advice in file_result.get("scoring", {}).get("advise", []):
                    findings.append({
                        "severity": advice.get("severity", "N/A"),
                        "title": advice.get("reason", ""),
                        "description": advice.get("selector", "")
                    })
            return findings
        except Exception as e:
            if self.logger:
                self.logger.error(f"Kubesec error: {e}")
            return []
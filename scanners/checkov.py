import subprocess
import json

class Scanner:
    def __init__(self, profile=None, logger=None):
        self.profile = profile or {}
        self.logger = logger

    def run(self):
        cmd = ["checkov", "-d", ".", "-o", "json"]
        for k, v in self.profile.get("checkov", {}).items():
            cmd.extend([f"--{k}", str(v)])
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if result.returncode != 0:
                if self.logger:
                    self.logger.error(f"Checkov failed: {result.stderr}")
                return []
            checkov_json = json.loads(result.stdout)
            findings = []
            for result_block in checkov_json.get("results", {}).values():
                for finding in result_block:
                    findings.append({
                        "severity": finding.get("severity", "N/A"),
                        "title": finding.get("check_name", ""),
                        "description": finding.get("check_message", "")
                    })
            return findings
        except Exception as e:
            if self.logger:
                self.logger.error(f"Checkov error: {e}")
            return []
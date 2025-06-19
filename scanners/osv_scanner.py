import subprocess
import json

class Scanner:
    def __init__(self, profile=None, logger=None):
        self.profile = profile or {}
        self.logger = logger

    def run(self):
        cmd = ["osv-scanner", "--json", "."]
        for k, v in self.profile.get("osv_scanner", {}).items():
            cmd.extend([f"--{k}", str(v)])
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if result.returncode != 0:
                if self.logger:
                    self.logger.error(f"OSV-Scanner failed: {result.stderr}")
                return []
            osv_json = json.loads(result.stdout)
            findings = []
            for r in osv_json.get("results", []):
                for vuln in r.get("vulnerabilities", []):
                    findings.append({
                        "severity": vuln.get("severity", "N/A"),
                        "title": vuln.get("id", ""),
                        "description": vuln.get("summary", "")
                    })
            return findings
        except Exception as e:
            if self.logger:
                self.logger.error(f"OSV-Scanner error: {e}")
            return []
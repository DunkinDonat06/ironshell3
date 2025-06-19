import subprocess
import json

class Scanner:
    def __init__(self, profile=None, logger=None):
        self.profile = profile or {}
        self.logger = logger

    def run(self):
        cmd = ["trufflehog", "filesystem", "--json", "."]
        for k, v in self.profile.get("trufflehog", {}).items():
            cmd.extend([f"--{k}", str(v)])
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if result.returncode != 0:
                if self.logger:
                    self.logger.error(f"Trufflehog failed: {result.stderr}")
                return []
            # trufflehog печатает JSON-объекты в каждой строке
            findings = []
            for line in result.stdout.strip().split("\n"):
                if line.strip():
                    try:
                        obj = json.loads(line)
                        findings.append({
                            "severity": obj.get("reason", "N/A"),
                            "title": obj.get("DetectorName", "Secret"),
                            "description": obj.get("Raw", obj.get("SourceMetadata", ""))
                        })
                    except Exception:
                        continue
            return findings
        except Exception as e:
            if self.logger:
                self.logger.error(f"Trufflehog error: {e}")
            return []
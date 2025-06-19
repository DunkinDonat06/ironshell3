import subprocess
import json

class Scanner:
    def __init__(self, profile=None, logger=None):
        self.profile = profile or {}
        self.logger = logger

    def run(self):
        cmd = ["gitleaks", "detect", "--report-format", "json"]
        for k, v in self.profile.get("gitleaks", {}).items():
            cmd.extend([f"--{k}", str(v)])
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if result.returncode != 0:
                if self.logger:
                    self.logger.error(f"Gitleaks failed: {result.stderr}")
                return []
            return json.loads(result.stdout)
        except Exception as e:
            if self.logger:
                self.logger.error(f"Gitleaks error: {e}")
            return []
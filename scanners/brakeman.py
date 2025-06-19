import subprocess
import json

class Scanner:
    def __init__(self, profile=None, logger=None):
        self.profile = profile or {}
        self.logger = logger

    def run(self):
        cmd = ["brakeman", "-f", "json"]
        for k, v in self.profile.get("brakeman", {}).items():
            cmd.extend([f"--{k}", str(v)])
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if result.returncode != 0:
                if self.logger:
                    self.logger.error(f"Brakeman failed: {result.stderr}")
                return []
            brakeman_json = json.loads(result.stdout)
            return [
                {
                    "severity": warning["confidence"],
                    "title": warning["warning_type"],
                    "description": warning["message"]
                }
                for warning in brakeman_json.get("warnings", [])
            ]
        except Exception as e:
            if self.logger:
                self.logger.error(f"Brakeman error: {e}")
            return []
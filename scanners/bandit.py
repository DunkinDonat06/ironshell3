import subprocess
import json

class Scanner:
    def __init__(self, profile=None, logger=None):
        self.profile = profile or {}
        self.logger = logger

    def run(self):
        cmd = ["bandit", "-r", ".", "-f", "json"]
        for k, v in self.profile.get("bandit", {}).items():
            cmd.extend([f"--{k}", str(v)])
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if result.returncode != 0:
                if self.logger:
                    self.logger.error(f"Bandit failed: {result.stderr}")
                return []
            bandit_json = json.loads(result.stdout)
            # Привести к общему формату
            return [
                {
                    "severity": issue["issue_severity"],
                    "title": issue["test_name"],
                    "description": issue["issue_text"]
                }
                for issue in bandit_json.get("results", [])
            ]
        except Exception as e:
            if self.logger:
                self.logger.error(f"Bandit error: {e}")
            return []
import subprocess
class Scanner:
    def __init__(self, target_url, profile=None, logger=None):
        self.target_url = target_url
        self.profile = profile or {}
        self.logger = logger

    def run(self):
        cmd = ["zap-cli", "quick-scan", "--self-contained", self.target_url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return [{"severity": "medium", "title": "ZAP finding", "description": line}
                for line in result.stdout.splitlines() if line.strip()]
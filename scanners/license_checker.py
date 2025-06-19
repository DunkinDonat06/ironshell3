import subprocess
class Scanner:
    def run(self):
        cmd = ["reuse", "lint"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return [{"severity": "info", "title": "License", "description": line}
                for line in result.stdout.splitlines() if line.strip()]
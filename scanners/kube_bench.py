import subprocess
class Scanner:
    def run(self):
        cmd = ["kube-bench"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return [{"severity": "warning", "title": "Kube-bench", "description": line}
                for line in result.stdout.splitlines() if line.strip()]
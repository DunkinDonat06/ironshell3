import subprocess
import json

class Scanner:
    def __init__(self, profile=None, logger=None):
        self.profile = profile or {}
        self.logger = logger

    def run(self):
        cmd = ["eslint", ".", "-f", "json"]
        for k, v in self.profile.get("eslint", {}).items():
            cmd.extend([f"--{k}", str(v)])
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if result.returncode != 0:
                if self.logger:
                    self.logger.error(f"ESLint failed: {result.stderr}")
                return []
            eslint_json = json.loads(result.stdout)
            # eslint возвращает список файлов с ошибками, агрегируем
            findings = []
            for file_entry in eslint_json:
                for m in file_entry.get("messages", []):
                    findings.append({
                        "severity": m.get("severity", "N/A"),
                        "title": m.get("ruleId", ""),
                        "description": m.get("message", ""),
                        "file": file_entry.get("filePath", "")
                    })
            return findings
        except Exception as e:
            if self.logger:
                self.logger.error(f"ESLint error: {e}")
            return []
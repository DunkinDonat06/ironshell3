import subprocess
import sys
import os

def test_gitleaks_dryrun():
    result = subprocess.run(
        [sys.executable, "main.py", "--only", "gitleaks", "--dry-run"],
        capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(__file__))
    )
    assert result.returncode == 0
    assert "gitleaks" in result.stdout
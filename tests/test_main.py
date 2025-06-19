import subprocess
import sys
import os

def test_cli_list_scanners():
    result = subprocess.run(
        [sys.executable, "main.py", "--list-scanners"],
        capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(__file__))
    )
    assert result.returncode == 0
    assert "gitleaks" in result.stdout
    assert "semgrep" in result.stdout

def test_cli_dry_run():
    result = subprocess.run(
        [sys.executable, "main.py", "--only", "gitleaks", "--dry-run"],
        capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(__file__))
    )
    assert result.returncode == 0
    assert "gitleaks" in result.stdout